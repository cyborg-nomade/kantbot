"""World inputs enter existing contracts; test scaffolding is not a cycle engine."""

import pytest

from kantbot.model import (
    CognitiveGround,
    Condition,
    ConditionStatus,
    Derivation,
    FieldConstant,
    GroundKind,
    Intuition,
    ManifoldOfIntuition,
    PresentedElement,
    RuleAuthority,
    SemanticModel,
    SensibleProcedure,
    StrictIncrease,
)
from kantbot.procedures import evaluate_procedure, project_content
from kantbot.provenance import InvalidProvenance, ProvenanceGraph, ProvenanceTrace
from kantbot.worlds import StripFrame, StripWorld, load_scenario, observe_world


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def _ground(entity_id: str, kind: GroundKind) -> CognitiveGround:
    return CognitiveGround(ground_id=entity_id, kind=kind)


def _reception_prefix(template: ProvenanceTrace, world: StripWorld) -> ProvenanceTrace:
    """Hand-author presentation records around real sensor output."""

    sequence = observe_world(world)
    scope = _change(template.scope, episode_id=sequence.episode_id)
    presented = tuple(
        PresentedElement(
            presented_element_id=f"strip-presentation:{index}",
            observation_id=item.observation_id,
            episode_id=item.episode_id,
            position=item.position,
            source=item.source,
            content=item.content,
            derivation=Derivation(
                operation="hand-authored reception for the world contract test",
                grounds=(_ground(item.observation_id, GroundKind.OBSERVATION),),
                scope=scope,
                configuration=template.configuration,
            ),
        )
        for index, item in enumerate(sequence.observations)
    )
    return ProvenanceTrace(
        cycle_id="strip-cycle",
        scope=scope,
        configuration=template.configuration,
        observations=sequence.observations,
        presented_elements=presented,
        forms=template.forms,
        projections=template.projections,
        evaluator_references=world.evaluator_references(),
    )


def _project_prefix(trace: ProvenanceTrace) -> ProvenanceTrace:
    """Use the existing projection kernel, recording its results explicitly."""

    projection = trace.projections[0]
    form_ids = tuple(form.form_id for form in projection.required_forms)
    intuitions = tuple(
        Intuition(
            intuition_id=f"strip-intuition:{index}",
            presented_element_id=item.presented_element_id,
            projection_id=projection.projection_id,
            episode_id=item.episode_id,
            position=item.position,
            content=project_content(item, projection),
            form_ids=form_ids,
            derivation=Derivation(
                operation="hand-authored projection for the world contract test",
                grounds=(
                    _ground(item.presented_element_id, GroundKind.PRESENTED_ELEMENT),
                    _ground(projection.projection_id, GroundKind.VARIANT_PROJECTION),
                ),
                scope=trace.scope,
                configuration=trace.configuration,
            ),
        )
        for index, item in enumerate(trace.presented_elements)
    )
    manifold = ManifoldOfIntuition(
        manifold_id="strip-manifold",
        episode_id=trace.scope.episode_id,
        intuition_ids=tuple(item.intuition_id for item in intuitions),
        form_ids=form_ids,
        derivation=Derivation(
            operation="hand-authored manifold; no identity synthesis",
            grounds=tuple(
                _ground(item.intuition_id, GroundKind.INTUITION) for item in intuitions
            ),
            scope=trace.scope,
            configuration=trace.configuration,
        ),
    )
    return _change(trace, intuitions=intuitions, manifolds=(manifold,))


@pytest.mark.parametrize(
    ("name", "expected_color", "expected_increase"),
    [
        ("rightward", ConditionStatus.SATISFIED, ConditionStatus.SATISFIED),
        ("stationary", ConditionStatus.SATISFIED, ConditionStatus.FAILED),
        ("reordered-motion", ConditionStatus.SATISFIED, ConditionStatus.FAILED),
        ("short-interval", ConditionStatus.SATISFIED, ConditionStatus.UNDECIDED),
        ("broken-color", ConditionStatus.FAILED, ConditionStatus.SATISFIED),
        ("ambiguous-middle", ConditionStatus.FAILED, ConditionStatus.FAILED),
    ],
)
def test_world_content_drives_existing_procedure_results(
    complete_trace: ProvenanceTrace,
    name: str,
    expected_color: ConditionStatus,
    expected_increase: ConditionStatus,
) -> None:
    trace = _project_prefix(_reception_prefix(complete_trace, load_scenario(name)))
    graph = ProvenanceGraph(trace)
    conditions = (
        Condition(
            condition_id="same-color",
            description="same color across at least two moments",
            required=True,
            authority=RuleAuthority.CONSTITUTIVE,
        ),
        Condition(
            condition_id="rightward",
            description="strictly increasing x across at least three moments",
            required=True,
            authority=RuleAuthority.CONSTITUTIVE,
        ),
    )
    procedure = SensibleProcedure(
        temporal_form_id="time-total",
        checks=(
            FieldConstant(condition_id="same-color", field="color"),
            StrictIncrease(condition_id="rightward", field="x", minimum_samples=3),
        ),
    )
    results = evaluate_procedure(procedure, conditions, trace.intuitions, trace.forms)
    assert tuple(item.status for item in results) == (expected_color, expected_increase)
    for result in results:
        assert tuple(item.ground_id for item in result.evidence) == tuple(
            item.intuition_id for item in trace.intuitions
        )
        assert all(graph.resolves(item) for item in result.evidence)
    # The ambiguous manifold is valid, but its simultaneous alternatives cannot
    # be treated as a single successive path. No selection is done by the sensor.
    assert not trace.candidates
    assert not trace.object_candidates
    assert not trace.judgments


@pytest.mark.parametrize("name", ["empty-middle", "unreadable-middle"])
def test_sensor_status_survives_reception_but_cannot_invent_patch_intuition(
    complete_trace: ProvenanceTrace, name: str
) -> None:
    prefix = _reception_prefix(complete_trace, load_scenario(name))
    ProvenanceGraph(prefix)
    assert prefix.presented_elements[1].content == prefix.observations[1].content
    with pytest.raises(ValueError, match="fields absent"):
        _project_prefix(prefix)


def test_hidden_reference_changes_do_not_change_the_cognitive_prefix(
    complete_trace: ProvenanceTrace,
) -> None:
    world = load_scenario("rightward")
    frames = tuple(
        StripFrame(
            position=frame.position,
            markers=tuple(
                _change(item, marker_id="other-label") for item in frame.markers
            ),
        )
        for frame in world.frames
    )
    alternative = _change(world, frames=frames)
    first = _project_prefix(_reception_prefix(complete_trace, world))
    second = _project_prefix(_reception_prefix(complete_trace, alternative))
    ProvenanceGraph(first)
    ProvenanceGraph(second)
    assert first.evaluator_references != second.evaluator_references
    assert _change(first, evaluator_references=()) == _change(
        second, evaluator_references=()
    )


def test_world_evaluator_reference_cannot_be_promoted_to_an_observation_ground(
    complete_trace: ProvenanceTrace,
) -> None:
    trace = _reception_prefix(complete_trace, load_scenario("rightward"))
    hidden = trace.evaluator_references[0].evaluator_reference_id
    graph = ProvenanceGraph(trace)
    forged_ground = _ground(hidden, GroundKind.OBSERVATION)
    assert not graph.resolves(forged_ground)
    presented = trace.presented_elements[0]
    forged = _change(
        presented,
        observation_id=hidden,
        derivation=_change(presented.derivation, grounds=(forged_ground,)),
    )
    with pytest.raises(
        InvalidProvenance, match="unresolved, mistyped, or unauthorized"
    ):
        ProvenanceGraph(_change(trace, presented_elements=(forged,)))
