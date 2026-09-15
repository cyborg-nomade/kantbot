"""Replay, sensor limits, and invariance under evaluator-only changes."""

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from kantbot.model import Observation, ObservationQuality, SemanticModel
from kantbot.worlds import (
    SCENARIO_NAMES,
    STRIP_SENSOR,
    MarkerState,
    ObservationSequence,
    StripFrame,
    StripWorld,
    load_scenario,
    observe_world,
)


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


@pytest.mark.parametrize("name", SCENARIO_NAMES)
def test_scripts_and_sensor_sequences_round_trip_and_replay(name: str) -> None:
    world = load_scenario(name)
    original_world = world.model_dump_json()
    sequence = observe_world(world)
    assert StripWorld.model_validate_json(original_world) == world
    assert (
        ObservationSequence.model_validate_json(sequence.model_dump_json()) == sequence
    )
    assert observe_world(StripWorld.model_validate_json(original_world)) == sequence
    assert (
        observe_world(load_scenario(name)).model_dump_json()
        == sequence.model_dump_json()
    )
    assert world.model_dump_json() == original_world
    assert all(type(item) is Observation for item in sequence.observations)
    assert all(item.source == STRIP_SENSOR for item in sequence.observations)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("rightward", ((0, "amber", 0), (1, "amber", 1), (2, "amber", 2))),
        ("stationary", ((0, "amber", 2), (1, "amber", 2), (2, "amber", 2))),
        ("reordered-motion", ((0, "amber", 0), (1, "amber", 2), (2, "amber", 1))),
        (
            "ambiguous-middle",
            ((0, "amber", 0), (1, "amber", 1), (1, "amber", 2), (2, "amber", 3)),
        ),
        ("short-interval", ((0, "amber", 0), (1, "amber", 1))),
        ("broken-color", ((0, "amber", 0), (1, "blue", 1), (2, "amber", 2))),
    ],
)
def test_named_scenarios_have_explicit_observation_oracles(
    name: str, expected: tuple[tuple[int, str, int], ...]
) -> None:
    observations = observe_world(load_scenario(name)).observations
    actual = tuple(
        (item.position, item.content[0].value, item.content[1].value)
        for item in observations
    )
    assert actual == expected
    assert all(item.quality is ObservationQuality.COMPLETE for item in observations)


def test_sensor_export_has_only_public_fields_and_frame_local_identities() -> None:
    sequence = observe_world(load_scenario("rightward"))
    assert sequence.model_dump(mode="json") == {
        "format_version": 1,
        "episode_id": "strip-demo",
        "source": STRIP_SENSOR,
        "observations": [
            {
                "observation_id": f"strip-observation:strip-demo:{position}:0",
                "episode_id": "strip-demo",
                "position": position,
                "source": STRIP_SENSOR,
                "content": [
                    {"name": "color", "value": "amber"},
                    {"name": "x", "value": position},
                ],
                "quality": "complete",
                "quality_notes": None,
            }
            for position in range(3)
        ],
    }


@given(
    st.lists(
        st.tuples(st.integers(-100, 100), st.sampled_from(("amber", "blue"))),
        min_size=1,
        max_size=8,
    )
)
def test_sensor_ignores_marker_names_storage_order_and_hidden_multiplicity(
    patches: list[tuple[int, str]],
) -> None:
    markers = tuple(
        MarkerState(marker_id=f"hidden-{index}", x=x, color=color)
        for index, (x, color) in enumerate(patches)
    )
    world = StripWorld(
        episode_id="generated", frames=(StripFrame(position=0, markers=markers),)
    )
    renamed = tuple(
        _change(marker, marker_id=f"changed-{index}")
        for index, marker in enumerate(reversed(markers))
    )
    alternative = _change(world, frames=(StripFrame(position=0, markers=renamed),))
    actual = observe_world(world)
    assert actual.model_dump_json() == observe_world(alternative).model_dump_json()
    assert world.evaluator_references() != alternative.evaluator_references()
    expected_patches = sorted(set(patches))
    assert tuple(
        (item.content[1].value, item.content[0].value) for item in actual.observations
    ) == tuple(expected_patches)
    duplicated = (*markers, _change(markers[0], marker_id="extra-hidden-marker"))
    assert (
        observe_world(
            _change(world, frames=(StripFrame(position=0, markers=duplicated),))
        )
        == actual
    )


def test_swapping_hidden_identity_across_time_leaves_rival_paths_unselected() -> None:
    world = load_scenario("ambiguous-middle")
    middle = world.frames[1]
    swapped = (
        _change(middle.markers[0], marker_id="rival"),
        _change(middle.markers[1], marker_id="target-17"),
    )
    alternative = _change(
        world,
        frames=(world.frames[0], _change(middle, markers=swapped), world.frames[2]),
    )
    assert world != alternative
    assert observe_world(world) == observe_world(alternative)
    observations = observe_world(world).observations
    assert observations[1].position == observations[2].position
    assert observations[1].observation_id != observations[2].observation_id


def test_empty_and_unreadable_frames_are_distinct_and_not_silently_dropped() -> None:
    empty = observe_world(load_scenario("empty-middle")).observations[1]
    world = load_scenario("unreadable-middle")
    unreadable = observe_world(world).observations[1]
    assert empty.position == unreadable.position == 1
    assert empty.content[0].name == "patch-present"
    assert empty.content[0].value is False
    assert empty.quality is ObservationQuality.COMPLETE
    assert unreadable.content[0].name == "frame-readable"
    assert unreadable.content[0].value is False
    assert unreadable.quality is ObservationQuality.IMPAIRED
    assert unreadable.quality_notes
    assert all(item.name not in {"color", "x"} for item in unreadable.content)
    hidden_empty = _change(world.frames[1], markers=())
    alternative = _change(
        world, frames=(world.frames[0], hidden_empty, world.frames[2])
    )
    assert observe_world(world) == observe_world(alternative)


def test_appending_a_future_frame_cannot_rewrite_an_earlier_sample() -> None:
    world = load_scenario("short-interval")
    future = StripFrame(
        position=100,
        markers=(MarkerState(marker_id="future-secret", color="blue", x=-100),),
    )
    longer = _change(world, frames=(*world.frames, future))
    previous = observe_world(world).observations
    assert observe_world(longer).observations[: len(previous)] == previous


@pytest.mark.parametrize("positions", [(1, 0), (0, 0), (-1, 0)])
def test_world_rejects_invalid_frame_order_instead_of_sorting(
    positions: tuple[int, ...],
) -> None:
    with pytest.raises(ValidationError):
        StripWorld(
            episode_id="invalid",
            frames=tuple(StripFrame(position=p) for p in positions),
        )


def test_world_rejects_duplicated_identity_within_one_frame() -> None:
    marker = MarkerState(marker_id="same", color="amber", x=0)
    with pytest.raises(ValidationError, match="marker IDs"):
        StripFrame(position=0, markers=(marker, _change(marker, x=1)))


@pytest.mark.parametrize("mutation", ["episode", "source", "duplicate", "order"])
def test_sequence_rejects_corrupted_observation_boundaries(mutation: str) -> None:
    sequence = observe_world(load_scenario("rightward"))
    observations = sequence.observations
    match mutation:
        case "episode":
            observations = (_change(observations[0], episode_id="foreign"),)
        case "source":
            observations = (_change(observations[0], source="foreign"),)
        case "duplicate":
            observations = (observations[0], observations[0])
        case "order":
            observations = tuple(reversed(observations))
    with pytest.raises(ValidationError):
        _change(sequence, observations=observations)


def test_world_and_sequence_reject_unknown_versions_and_empty_episodes() -> None:
    world = load_scenario("rightward")
    sequence = observe_world(world)
    for value in (world, sequence):
        with pytest.raises(ValidationError):
            _change(value, format_version=2)
    with pytest.raises(ValidationError):
        _change(world, frames=())
    with pytest.raises(ValidationError):
        _change(sequence, observations=())


def test_world_values_are_strict_and_recursively_immutable() -> None:
    world = load_scenario("rightward")
    with pytest.raises(ValidationError, match="frozen"):
        world.frames[0].markers[0].x = 99
    with pytest.raises(ValidationError):
        _change(world, frames=list(world.frames))
    with pytest.raises(ValidationError):
        _change(world.frames[0].markers[0], x=True)


def test_unknown_scenario_is_an_input_error_not_a_cognitive_outcome() -> None:
    with pytest.raises(ValueError, match="unknown strip scenario"):
        load_scenario("not-a-world")
