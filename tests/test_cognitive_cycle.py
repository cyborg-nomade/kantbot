"""The first production cycle computes its own representations and warrants."""

import pytest
from pydantic import ValidationError

from kantbot.cycle import (
    AmbiguityPolicy,
    CyclePolicies,
    SearchCapacityExceeded,
    retain_current,
    run_cycle,
    strip_plan,
)
from kantbot.cycle.judgment import apply_concept, propose_judgment
from kantbot.cycle.reception import present_observation
from kantbot.interfaces import (
    ApplicationRequest,
    ProposalRequest,
    ProposalResult,
    ProvenanceView,
    ReceptionRequest,
)
from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    ConditionStatus,
    ContentField,
    GroundKind,
    JudgmentCommitted,
    Modality,
    Observation,
    OutcomeKind,
    PresentedElement,
    SemanticModel,
    SynthesisPolicy,
    TemporalOrder,
)
from kantbot.provenance import (
    InvalidProvenance,
    dump_provenance,
    validate_provenance_json,
)
from kantbot.worlds import SCENARIO_NAMES, load_scenario, observe_world


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def _observations(name: str) -> tuple[Observation, ...]:
    return observe_world(load_scenario(name)).observations


EXPECTED = (
    ("rightward", OutcomeKind.JUDGMENT_COMMITTED),
    ("stationary", OutcomeKind.CONCEPT_NOT_APPLICABLE),
    ("reordered-motion", OutcomeKind.CONCEPT_NOT_APPLICABLE),
    ("ambiguous-middle", OutcomeKind.SYNTHESIS_AMBIGUOUS),
    ("short-interval", OutcomeKind.APPLICATION_UNDERDETERMINED),
    ("unreadable-middle", OutcomeKind.NOT_PRESENTABLE),
    ("broken-color", OutcomeKind.SYNTHESIS_FAILED),
    ("empty-middle", OutcomeKind.NOT_PRESENTABLE),
)


@pytest.mark.parametrize(("name", "kind"), EXPECTED)
@pytest.mark.parametrize("policy", tuple(SynthesisPolicy))
def test_world_episodes_are_computed_from_observations(
    name: str, kind: OutcomeKind, policy: SynthesisPolicy
) -> None:
    observations = _observations(name)
    original = tuple(item.model_dump_json() for item in observations)
    plan = strip_plan("strip-demo", synthesis_policy=policy)
    result = run_cycle(observations, plan)
    assert tuple(item.kind for item in result.outcomes) == (kind,)
    assert result.trace.observations == observations
    assert not result.trace.evaluator_references
    assert validate_provenance_json(dump_provenance(result.graph)).trace == result.trace
    assert result.trace == run_cycle(observations, plan).trace
    assert tuple(item.model_dump_json() for item in observations) == original
    assert result.reports


def test_scenario_catalog_and_behavior_table_cover_the_same_inputs() -> None:
    assert tuple(name for name, _ in EXPECTED) == SCENARIO_NAMES


def test_success_has_actual_retention_evidence_and_complete_warrant() -> None:
    result = run_cycle(_observations("rightward"), strip_plan("strip-demo"))
    outcome = result.outcomes[0]
    assert isinstance(outcome, JudgmentCommitted)
    assert result.trace.object_candidates
    assert result.trace.applications[0].status is ApplicationStatus.APPLICABLE
    assert all(
        item.passed for item in result.trace.object_candidates[0].identity_results
    )
    assert tuple(
        item.status.value for item in result.trace.retained_sequences[0].items
    ) == (
        "reproduced",
        "reproduced",
        "current",
    )
    warrant = outcome.judgment.warrant.assembled
    assert {item.ground_id for item in warrant.observation_grounds} == {
        item.observation_id for item in result.trace.observations
    }
    assert {item.kind for item in warrant.synthesis_grounds} == {
        GroundKind.MANIFOLD,
        GroundKind.RETAINED_SEQUENCE,
        GroundKind.CANDIDATE_REPRESENTATION,
        GroundKind.OBJECT_CANDIDATE,
    }
    assert outcome.judgment.warrant.unity_check.passed
    assert all(result.graph.resolves(item) for item in warrant.synthesis_grounds)


@pytest.mark.parametrize("policy", tuple(SynthesisPolicy))
def test_bp002_removing_reproduction_prevents_identity(policy: SynthesisPolicy) -> None:
    plan = strip_plan("strip-demo", synthesis_policy=policy)
    observations = _observations("rightward")
    result = run_cycle(
        observations, plan, policies=CyclePolicies(retain=retain_current)
    )
    assert result.outcomes[0].kind is OutcomeKind.SYNTHESIS_FAILED
    assert not result.trace.candidates
    assert not result.trace.judgments
    assert tuple(
        item.status.value for item in result.trace.retained_sequences[0].items
    ) == ("current",)
    assert result.trace.observations == observations


@pytest.mark.parametrize("policy", tuple(SynthesisPolicy))
def test_bp005_applicable_rival_paths_withhold_a_singular_subject(
    policy: SynthesisPolicy,
) -> None:
    plan = strip_plan(
        "strip-demo", synthesis_policy=policy, ambiguity_policy=AmbiguityPolicy.CONTINUE
    )
    result = run_cycle(_observations("ambiguous-middle"), plan)
    assert result.outcomes[0].kind is OutcomeKind.JUDGMENT_WITHHELD
    assert all(item.applicable for item in result.trace.applications)
    assert tuple(
        tuple(
            result.graph.intuition_for(item).content[1].value
            for item in candidate.intuition_ids
        )
        for candidate in result.trace.candidates
    ) == ((0, 1, 3), (0, 2, 3))
    assert all(
        candidate.alternative_candidate_ids for candidate in result.trace.candidates
    )
    assert len(result.trace.applications) == len(result.trace.candidates)
    assert not result.trace.proposals
    assert not result.trace.judgments


def test_bp001_reordering_changes_application_after_object_formation() -> None:
    plan = strip_plan("strip-demo")
    control = run_cycle(_observations("rightward"), plan)
    contrast = run_cycle(_observations("reordered-motion"), plan)
    assert control.trace.object_candidates == contrast.trace.object_candidates
    assert control.outcomes[0].kind is OutcomeKind.JUDGMENT_COMMITTED
    assert contrast.outcomes[0].kind is OutcomeKind.CONCEPT_NOT_APPLICABLE


def test_full_identity_rule_rejects_a_jump_before_objecthood() -> None:
    observations = _observations("short-interval")
    jumping = (
        observations[0],
        _change(
            observations[1],
            content=(
                ContentField(name="color", value="amber"),
                ContentField(name="x", value=5),
            ),
        ),
    )
    result = run_cycle(jumping, strip_plan("strip-demo"))
    assert result.outcomes[0].kind is OutcomeKind.SYNTHESIS_FAILED
    assert not result.trace.object_candidates
    spaced = (jumping[0], _change(jumping[1], position=3))
    result = run_cycle(spaced, strip_plan("strip-demo"))
    assert result.trace.object_candidates
    assert result.outcomes[0].kind is OutcomeKind.APPLICATION_UNDERDETERMINED


@pytest.mark.parametrize("name", ["empty-middle", "unreadable-middle"])
def test_projection_refusal_preserves_received_content_and_partial_intuitions(
    name: str,
) -> None:
    observations = _observations(name)
    result = run_cycle(observations, strip_plan("strip-demo"))
    assert result.trace.presented_elements[1].content == observations[1].content
    assert tuple(item.position for item in result.trace.intuitions) == (0, 2)
    assert result.outcomes[0].kind is OutcomeKind.NOT_PRESENTABLE
    assert not result.trace.manifolds


def test_bp012_variants_execute_different_synthesis_structure() -> None:
    observations = _observations("rightward")
    default = run_cycle(observations, strip_plan("strip-demo"))
    b_led = run_cycle(
        observations,
        strip_plan("strip-demo", synthesis_policy=SynthesisPolicy.B_LED_FIGURATIVE),
    )
    default_steps = tuple(item.operation for item in default.operations)
    b_steps = tuple(item.operation for item in b_led.operations)
    assert tuple(
        item
        for item in default_steps
        if item in {"apprehension", "reproduction", "recognition"}
    ) == ("apprehension", "reproduction", "recognition")
    assert "figurative-synthesis" in b_steps
    assert not {"apprehension", "reproduction", "recognition"}.intersection(b_steps)
    assert default.trace.observations == b_led.trace.observations
    assert tuple(
        item.retention_rule_id for item in default.trace.retained_sequences[0].items
    ) == tuple(
        item.retention_rule_id for item in b_led.trace.retained_sequences[0].items
    )


@pytest.mark.parametrize("policy", tuple(SynthesisPolicy))
def test_b_led_unity_constrains_candidate_formation_earlier(
    policy: SynthesisPolicy,
) -> None:
    plan = strip_plan("strip-demo", synthesis_policy=policy)
    unity = plan.repertoire.rules[2]
    procedure = _change(
        unity.sensible_procedure,
        checks=(TemporalOrder(condition_id="U-successive", minimum_samples=4),),
    )
    repertoire = _change(
        plan.repertoire,
        rules=(
            *plan.repertoire.rules[:2],
            _change(unity, sensible_procedure=procedure),
        ),
    )
    result = run_cycle(_observations("rightward"), _change(plan, repertoire=repertoire))
    assert result.outcomes[0].kind is OutcomeKind.SYNTHESIS_FAILED
    assert bool(result.trace.candidates) is (
        policy is SynthesisPolicy.A_ANALYSIS_B_CONSTRAINT
    )
    assert not result.trace.object_candidates


def test_bp007_missing_retention_warrant_withholds_instead_of_fabricating_it() -> None:
    def missing_retention(request: ProposalRequest, /) -> ProposalResult:
        warrant = _change(
            request.warrant,
            synthesis_grounds=tuple(
                item
                for item in request.warrant.synthesis_grounds
                if item.kind is not GroundKind.RETAINED_SEQUENCE
            ),
        )
        return propose_judgment(_change(request, warrant=warrant))

    result = run_cycle(
        _observations("rightward"),
        strip_plan("strip-demo"),
        policies=CyclePolicies(propose=missing_retention),
    )
    assert result.outcomes[0].kind is OutcomeKind.JUDGMENT_WITHHELD
    assert result.trace.applications[0].applicable
    assert not result.trace.judgments


def test_unity_blocks_an_empirical_claim_of_necessity() -> None:
    def apodictic(request: ProposalRequest, /) -> ProposalResult:
        proposition = _change(request.proposition, modality=Modality.APODICTIC)
        return propose_judgment(_change(request, proposition=proposition))

    result = run_cycle(
        _observations("rightward"),
        strip_plan("strip-demo"),
        policies=CyclePolicies(propose=apodictic),
    )
    assert result.outcomes[0].kind is OutcomeKind.UNITY_CONFLICT
    assert result.trace.proposals
    assert not result.trace.judgments


def test_a_replacement_reception_cannot_rewrite_supplied_content() -> None:
    def invented(request: ReceptionRequest, /) -> PresentedElement:
        return _change(
            present_observation(request),
            content=(ContentField(name="color", value="blue"),),
        )

    with pytest.raises(InvalidProvenance, match="shared reception changed"):
        run_cycle(
            _observations("rightward"),
            strip_plan("strip-demo"),
            policies=CyclePolicies(present=invented),
        )


def test_a_replacement_application_cannot_forge_failed_motion_as_applicable() -> None:
    def invented(
        request: ApplicationRequest, provenance: ProvenanceView, /
    ) -> ApplicationResult:
        result = apply_concept(request, provenance)
        results = tuple(
            _change(item, status=ConditionStatus.SATISFIED)
            for item in result.condition_results
        )
        return _change(
            result, status=ApplicationStatus.APPLICABLE, condition_results=results
        )

    with pytest.raises(InvalidProvenance, match="procedure replay"):
        run_cycle(
            _observations("stationary"),
            strip_plan("strip-demo"),
            policies=CyclePolicies(apply=invented),
        )


def test_bad_input_never_acquires_cognitive_status() -> None:
    plan = strip_plan("strip-demo")
    for bad in (
        (),
        ("not an observation",),
        list(_observations("rightward")),
        tuple(reversed(_observations("rightward"))),
        (_observations("rightward")[0],) * 2,
    ):
        result = run_cycle(bad, plan)
        assert result.outcomes[0].kind is OutcomeKind.INPUT_ERROR
        assert not result.trace.observations
        assert not result.trace.presented_elements
    result = run_cycle(_observations("rightward"), strip_plan("another-episode"))
    assert result.outcomes[0].kind is OutcomeKind.INPUT_ERROR


def test_capacity_limits_do_not_masquerade_as_failed_synthesis() -> None:
    plan = strip_plan("strip-demo")
    with pytest.raises(SearchCapacityExceeded, match="identity search"):
        run_cycle(_observations("ambiguous-middle"), _change(plan, path_budget=1))
    with pytest.raises(SearchCapacityExceeded, match="observation count"):
        run_cycle(_observations("rightward"), _change(plan, observation_budget=1))
    with pytest.raises(ValidationError):
        _change(plan, path_budget=0)


def test_the_cycle_does_not_receive_world_identity() -> None:
    world = load_scenario("ambiguous-middle")
    alternative = _change(
        world,
        frames=tuple(
            _change(
                frame,
                markers=tuple(
                    _change(marker, marker_id=f"other-{index}")
                    for index, marker in enumerate(frame.markers)
                ),
            )
            for frame in world.frames
        ),
    )
    assert world.evaluator_references() != alternative.evaluator_references()
    plan = strip_plan(world.episode_id)
    assert (
        run_cycle(observe_world(world).observations, plan).trace
        == run_cycle(observe_world(alternative).observations, plan).trace
    )


def test_world_arguments_do_not_cross_the_reception_boundary() -> None:
    result = run_cycle(load_scenario("rightward"), strip_plan("strip-demo"))
    assert result.outcomes[0].kind is OutcomeKind.INPUT_ERROR
    assert not result.trace.evaluator_references


def test_bp011_unavailable_temporal_form_preserves_shared_reception() -> None:
    plan = _change(strip_plan("strip-demo"), available_form_ids=("strip-space",))
    observations = _observations("rightward")
    result = run_cycle(observations, plan)
    assert result.trace.observations == observations
    assert tuple(
        item.observation_id for item in result.trace.presented_elements
    ) == tuple(item.observation_id for item in observations)
    assert not result.trace.intuitions
    assert all(item.kind is OutcomeKind.NOT_PRESENTABLE for item in result.outcomes)
    assert all(
        "projection-form:strip-time" in item.context.limit_report.missing_condition_ids
        for item in result.outcomes
    )
