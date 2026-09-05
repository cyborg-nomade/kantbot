"""Generated invariants for the formal model's accepted boundaries."""

from collections.abc import Sequence

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from kantbot.interfaces import RoleContext
from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    CognitiveGround,
    ConditionResult,
    ConditionStatus,
    ConfigurationIdentity,
    ContentField,
    Derivation,
    EvaluatorReference,
    GroundKind,
    JudgmentWithheld,
    LimitReport,
    Observation,
    ObservationQuality,
    OutcomeContext,
    OutcomeKind,
    PresentedElement,
    RuleAuthority,
    Scope,
    dump_terminal_outcome,
    validate_terminal_outcome_json,
)
from kantbot.provenance import InvalidProvenance, ProvenanceGraph, ProvenanceTrace
from kantbot.transitions import dump_cycle_state, open_cycle, validate_cycle_state_json

_IDENTIFIER_ALPHABET = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-"
)
_IDENTIFIER_INITIALS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
_IDENTIFIERS = st.tuples(
    st.sampled_from(tuple(_IDENTIFIER_INITIALS)),
    st.text(alphabet=_IDENTIFIER_ALPHABET, max_size=19),
).map("".join)
_SCALARS = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(max_size=30),
)
_CONTENTS = st.dictionaries(_IDENTIFIERS, _SCALARS, min_size=1, max_size=5)
_CONDITION_STATUSES = st.sampled_from(tuple(ConditionStatus))


def _scope(episode_id: str = "episode") -> Scope:
    return Scope(
        scope_id=f"scope-{episode_id}",
        episode_id=episode_id,
        description="generated bounded episode",
        presentation_conditions=("a total order",),
    )


def _configuration() -> ConfigurationIdentity:
    return ConfigurationIdentity(
        configuration_id="configuration-generated",
        variant_id="kant-ab-default",
    )


def _content(values: dict[str, object]) -> tuple[ContentField, ...]:
    return tuple(ContentField(name=name, value=value) for name, value in values.items())


def _unused_content_name(content: tuple[ContentField, ...]) -> str:
    names = {item.name for item in content}
    candidate = "changed"
    while candidate in names:
        candidate += "x"
    return candidate


def _observation(
    observation_id: str,
    position: int,
    content: tuple[ContentField, ...],
    episode_id: str = "episode",
) -> Observation:
    return Observation(
        observation_id=observation_id,
        episode_id=episode_id,
        position=position,
        source="generated-source",
        content=content,
        quality=ObservationQuality.COMPLETE,
    )


def _derivation(
    grounds: tuple[CognitiveGround, ...], scope: Scope, operation: str = "generated"
) -> Derivation:
    return Derivation(
        operation=operation,
        grounds=grounds,
        scope=scope,
        configuration=_configuration(),
    )


def _presented(observation: Observation, scope: Scope) -> PresentedElement:
    return PresentedElement(
        presented_element_id=f"presented-{observation.observation_id}",
        observation_id=observation.observation_id,
        episode_id=observation.episode_id,
        position=observation.position,
        source=observation.source,
        content=observation.content,
        derivation=_derivation(
            (
                CognitiveGround(
                    ground_id=observation.observation_id,
                    kind=GroundKind.OBSERVATION,
                ),
            ),
            scope,
            "shared reception",
        ),
    )


@given(position=st.integers(), values=_CONTENTS)
def test_shared_reception_preserves_arbitrary_supplied_content(
    position: int, values: dict[str, object]
) -> None:
    scope = _scope()
    observation = _observation("observation", position, _content(values))
    presented = _presented(observation, scope)
    trace = ProvenanceTrace(
        cycle_id="cycle",
        scope=scope,
        configuration=_configuration(),
        observations=(observation,),
        presented_elements=(presented,),
    )

    graph = ProvenanceGraph(trace)
    assert graph.trace.presented_elements[0].content == observation.content
    changed_name = _unused_content_name(presented.content)
    changed = PresentedElement.model_validate(
        {
            **presented.model_dump(mode="python"),
            "content": (
                *presented.content,
                ContentField(name=changed_name, value=None),
            ),
        }
    )
    with pytest.raises(InvalidProvenance, match="shared reception changed"):
        ProvenanceGraph(
            ProvenanceTrace.model_validate(
                {**trace.model_dump(mode="python"), "presented_elements": (changed,)}
            )
        )


def _expected_application_status(
    statuses: Sequence[ConditionStatus],
) -> ApplicationStatus:
    if ConditionStatus.FAILED in statuses:
        return ApplicationStatus.NOT_APPLICABLE
    if ConditionStatus.UNDECIDED in statuses:
        return ApplicationStatus.UNDERDETERMINED
    return ApplicationStatus.APPLICABLE


@given(
    statuses=st.lists(_CONDITION_STATUSES, min_size=1, max_size=8),
    reported_status=st.sampled_from(tuple(ApplicationStatus)),
)
def test_application_status_is_determined_by_all_required_conditions(
    statuses: list[ConditionStatus], reported_status: ApplicationStatus
) -> None:
    scope = _scope()
    conditions = tuple(
        ConditionResult(
            condition_id=f"condition-{index}",
            required=True,
            status=status,
            explanation="generated application result",
        )
        for index, status in enumerate(statuses)
    )
    expected = _expected_application_status(statuses)
    data = {
        "application_result_id": "application",
        "object_candidate_id": "object",
        "concept_id": "concept",
        "schema_id": "schema",
        "status": reported_status,
        "condition_results": conditions,
        "derivation": _derivation(
            (
                CognitiveGround(ground_id="object", kind=GroundKind.OBJECT_CANDIDATE),
                CognitiveGround(ground_id="concept", kind=GroundKind.CONCEPT),
                CognitiveGround(ground_id="schema", kind=GroundKind.SCHEMA),
            ),
            scope,
            "schema-mediated application",
        ),
    }

    if reported_status is expected:
        assert ApplicationResult.model_validate(data).status is expected
    else:
        with pytest.raises(ValidationError, match="does not match"):
            ApplicationResult.model_validate(data)


@given(
    kind=st.sampled_from(tuple(GroundKind)),
    authority=st.one_of(st.none(), st.sampled_from(tuple(RuleAuthority))),
)
def test_rule_authority_is_admitted_only_on_rule_grounds(
    kind: GroundKind, authority: RuleAuthority | None
) -> None:
    data = {"ground_id": "ground", "kind": kind, "authority": authority}
    allowed = (kind is GroundKind.RULE) == (authority is not None)
    if allowed:
        assert CognitiveGround.model_validate(data).authority is authority
    else:
        with pytest.raises(ValidationError):
            CognitiveGround.model_validate(data)


@given(kind=st.sampled_from(tuple(GroundKind)))
def test_evaluator_identity_never_resolves_as_a_cognitive_kind(
    kind: GroundKind,
) -> None:
    scope = _scope()
    graph = ProvenanceGraph(
        ProvenanceTrace(
            cycle_id="cycle",
            scope=scope,
            configuration=_configuration(),
            evaluator_references=(
                EvaluatorReference(
                    evaluator_reference_id="evaluator",
                    description="hidden comparison state",
                ),
            ),
        )
    )
    authority = RuleAuthority.CONSTITUTIVE if kind is GroundKind.RULE else None
    ground = CognitiveGround(ground_id="evaluator", kind=kind, authority=authority)

    assert not graph.resolves(ground)


@given(count=st.integers(min_value=2, max_value=8))
def test_circular_evidence_is_rejected_for_every_generated_cycle_length(
    count: int,
) -> None:
    scope = _scope()
    content = (ContentField(name="value", value=1),)
    observations = tuple(
        _observation(f"observation-{index}", index, content) for index in range(count)
    )
    presented = tuple(
        PresentedElement(
            presented_element_id=f"presented-{index}",
            observation_id=observation.observation_id,
            episode_id=observation.episode_id,
            position=observation.position,
            source=observation.source,
            content=observation.content,
            derivation=_derivation(
                (
                    CognitiveGround(
                        ground_id=observation.observation_id,
                        kind=GroundKind.OBSERVATION,
                    ),
                    CognitiveGround(
                        ground_id=f"presented-{(index + 1) % count}",
                        kind=GroundKind.PRESENTED_ELEMENT,
                    ),
                ),
                scope,
                "circular presentation",
            ),
        )
        for index, observation in enumerate(observations)
    )
    trace = ProvenanceTrace(
        cycle_id="cycle",
        scope=scope,
        configuration=_configuration(),
        observations=observations,
        presented_elements=presented,
    )

    with pytest.raises(InvalidProvenance, match="circular evidence"):
        ProvenanceGraph(trace)


@given(identifiers=st.lists(_IDENTIFIERS, min_size=1, max_size=8, unique=True))
def test_registration_order_does_not_change_cognitive_lookup(
    identifiers: list[str],
) -> None:
    scope = _scope()
    content = (ContentField(name="value", value=1),)
    observations = tuple(
        _observation(f"observation-{identifier}", index, content)
        for index, identifier in enumerate(identifiers)
    )
    common = {
        "cycle_id": "cycle",
        "scope": scope,
        "configuration": _configuration(),
    }
    forward = ProvenanceGraph(ProvenanceTrace(**common, observations=observations))
    reverse = ProvenanceGraph(
        ProvenanceTrace(**common, observations=tuple(reversed(observations)))
    )

    for observation in observations:
        ground = CognitiveGround(
            ground_id=observation.observation_id, kind=GroundKind.OBSERVATION
        )
        assert forward.resolves(ground) == reverse.resolves(ground)
        assert forward.immediate_grounds(ground.ground_id) == ()
        assert reverse.immediate_grounds(ground.ground_id) == ()


@given(
    representation_ids=st.lists(_IDENTIFIERS, min_size=1, max_size=5, unique=True),
    unmet_ids=st.lists(_IDENTIFIERS, min_size=1, max_size=5, unique=True),
)
def test_withholding_round_trip_preserves_every_reported_limit(
    representation_ids: list[str], unmet_ids: list[str]
) -> None:
    scope = _scope()
    configuration = _configuration()
    missing = tuple(f"missing-{identifier}" for identifier in unmet_ids)
    report = LimitReport(
        limit_report_id="limit",
        strongest_licensed=OutcomeKind.JUDGMENT_WITHHELD,
        scope=scope,
        boundary="generated limit boundary",
        missing_condition_ids=missing,
    )
    context = OutcomeContext(
        configuration=configuration,
        derivation=Derivation(
            operation="withhold judgment",
            grounds=(
                CognitiveGround(ground_id="external", kind=GroundKind.EXTERNAL_INPUT),
            ),
            unmet_conditions=missing,
            scope=scope,
            configuration=configuration,
        ),
        limit_report=report,
    )
    outcome = JudgmentWithheld(
        outcome_id="withheld",
        context=context,
        strongest_representation_ids=tuple(
            f"representation-{identifier}" for identifier in representation_ids
        ),
        unmet_condition_ids=missing,
    )

    assert validate_terminal_outcome_json(dump_terminal_outcome(outcome)) == outcome
    incomplete = {
        **context.model_dump(mode="python"),
        "limit_report": {
            **report.model_dump(mode="python"),
            "missing_condition_ids": (),
        },
    }
    with pytest.raises(ValidationError, match="withheld conditions"):
        JudgmentWithheld.model_validate(
            {**outcome.model_dump(mode="python"), "context": incomplete}
        )


@given(
    positions=st.lists(st.integers(), min_size=1, max_size=8, unique=True),
    values=_CONTENTS,
)
def test_open_cycle_preserves_arbitrary_episode_order_and_round_trips(
    positions: list[int], values: dict[str, object]
) -> None:
    scope = _scope()
    observations = tuple(
        _observation(f"observation-{index}", position, _content(values))
        for index, position in enumerate(positions)
    )
    opened = open_cycle(
        "cycle", observations, RoleContext(scope=scope, configuration=_configuration())
    )

    assert opened.observations == observations
    assert validate_cycle_state_json(dump_cycle_state(opened)) == opened
    foreign = _observation(
        "foreign-observation", positions[0], _content(values), "foreign-episode"
    )
    with pytest.raises(ValidationError, match="scoped episode"):
        open_cycle(
            "cycle",
            (*observations, foreign),
            RoleContext(scope=scope, configuration=_configuration()),
        )
