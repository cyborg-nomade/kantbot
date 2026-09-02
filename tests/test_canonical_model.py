"""Executable checks for the local invariants of the canonical values."""

from types import SimpleNamespace
from typing import NamedTuple

import pytest
from pydantic import ValidationError

from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    ApplicationUnderdetermined,
    AssembledWarrant,
    AuthorityViolation,
    CognitiveGround,
    CompleteWarrant,
    ConceptNotApplicable,
    ConditionResult,
    ConditionStatus,
    Derivation,
    EvaluatorReference,
    GroundKind,
    InputError,
    JudgmentWithheld,
    LimitReport,
    NotPresentable,
    ObjectCandidate,
    Observation,
    OutcomeContext,
    OutcomeKind,
    Overreach,
    Reason,
    RetainedIntuition,
    RetentionStatus,
    Rule,
    RuleAuthority,
    SynthesisAmbiguous,
    SynthesisFailed,
    UnityConflict,
    dump_terminal_outcome,
    validate_terminal_outcome,
    validate_terminal_outcome_json,
)

EXPECTED_OUTCOME_COUNT = 10


class _LimitDetails(NamedTuple):
    missing: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    violations: tuple[AuthorityViolation, ...] = ()


_EMPTY_LIMIT_DETAILS = _LimitDetails()


def test_successful_trace_preserves_every_semantic_gate(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace

    assert trace.observation.observation_id == "obs-1"
    assert trace.presented.observation_id == trace.observation.observation_id
    assert trace.intuition.presented_element_id == trace.presented.presented_element_id
    assert trace.manifold.intuition_ids == (trace.intuition.intuition_id,)
    assert trace.object_candidate.candidate_representation_id == (
        trace.candidate.candidate_representation_id
    )
    assert trace.concept.concept_id != trace.schema.schema_id
    assert trace.application.applicable
    assert trace.proposal.proposed_judgment_id != trace.judgment.judgment_id
    assert trace.judgment.warrant.unity_check.passed
    assert trace.committed_outcome.kind is OutcomeKind.JUDGMENT_COMMITTED


def test_models_are_strict_closed_and_immutable(
    successful_trace: SimpleNamespace,
) -> None:
    observation = successful_trace.observation

    with pytest.raises(ValidationError, match="frozen"):
        observation.position = 2

    with pytest.raises(ValidationError):
        Observation.model_validate(
            {
                **observation.model_dump(mode="python"),
                "position": "0",
            }
        )

    with pytest.raises(ValidationError, match="extra_forbidden"):
        Observation.model_validate(
            {
                **observation.model_dump(mode="python"),
                "hidden_object_id": "world-object-7",
            }
        )

    assert isinstance(observation.content, tuple)
    assert not hasattr(observation.content, "append")


def test_variant_projection_cannot_be_a_relabel(
    successful_trace: SimpleNamespace,
) -> None:
    intuition = successful_trace.intuition
    incomplete = tuple(
        ground
        for ground in intuition.derivation.grounds
        if ground.kind is not GroundKind.VARIANT_PROJECTION
    )

    with pytest.raises(ValidationError, match="variant projection"):
        intuition.__class__(
            **{
                **intuition.model_dump(mode="python", exclude={"derivation"}),
                "derivation": Derivation(
                    operation="mere relabel",
                    grounds=incomplete,
                    scope=successful_trace.scope,
                    configuration=successful_trace.configuration,
                ),
            }
        )


def test_reproduction_requires_an_explicit_retention_rule() -> None:
    with pytest.raises(ValidationError, match="requires a retention rule"):
        RetainedIntuition(
            intuition_id="intuition-earlier",
            status=RetentionStatus.REPRODUCED,
        )


def test_failed_local_conditions_cannot_form_an_object(
    successful_trace: SimpleNamespace,
) -> None:
    failed = ConditionResult(
        condition_id="identity-passes",
        required=True,
        status=ConditionStatus.FAILED,
        explanation="identity does not persist",
    )
    candidate = successful_trace.object_candidate

    with pytest.raises(ValidationError, match="satisfied identity"):
        ObjectCandidate(
            object_candidate_id=candidate.object_candidate_id,
            candidate_representation_id=candidate.candidate_representation_id,
            identity_results=(failed,),
            constitutive_results=candidate.constitutive_results,
            derivation=candidate.derivation,
        )


def test_application_status_is_derived_from_required_conditions(
    successful_trace: SimpleNamespace,
) -> None:
    application = successful_trace.application

    with pytest.raises(ValidationError, match="does not match"):
        ApplicationResult(
            application_result_id=application.application_result_id,
            object_candidate_id=application.object_candidate_id,
            concept_id=application.concept_id,
            schema_id=application.schema_id,
            status=ApplicationStatus.UNDERDETERMINED,
            condition_results=application.condition_results,
            derivation=application.derivation,
        )


def test_evaluator_state_has_no_shape_accepted_by_a_warrant(
    successful_trace: SimpleNamespace,
) -> None:
    hidden = EvaluatorReference(
        evaluator_reference_id="hidden-world-id",
        description="the evaluator's numerical object identity",
    )
    warrant_data = successful_trace.warrant.model_dump(mode="python")
    warrant_data["observation_grounds"] = (hidden,)

    with pytest.raises(ValidationError):
        AssembledWarrant.model_validate(warrant_data)

    with pytest.raises(ValidationError):
        ConditionResult(
            condition_id="hidden-evidence",
            required=True,
            status=ConditionStatus.SATISFIED,
            explanation="would illicitly use evaluator state",
            evidence=(hidden,),
        )

    regulative = CognitiveGround(
        ground_id="Q-1",
        kind=GroundKind.RULE,
        authority=RuleAuthority.REGULATIVE,
    )
    warrant_data = successful_trace.warrant.model_dump(mode="python")
    warrant_data["constitutive_rule_grounds"] = (regulative,)
    with pytest.raises(ValidationError, match="must be constitutive"):
        AssembledWarrant.model_validate(warrant_data)


def test_failed_unity_cannot_complete_a_warrant(
    successful_trace: SimpleNamespace,
) -> None:
    unity = successful_trace.unity_check
    failed_result = ConditionResult(
        condition_id="cycle-wide-unity",
        required=True,
        status=ConditionStatus.FAILED,
        explanation="branches conflict",
    )
    failed_unity = unity.__class__(
        unity_check_id="unity-failed",
        status=ConditionStatus.FAILED,
        condition_results=(failed_result,),
        conflict_ids=("branch-conflict",),
        scope=unity.scope,
        configuration=unity.configuration,
    )

    with pytest.raises(ValidationError, match="successful unity"):
        CompleteWarrant(
            assembled=successful_trace.warrant,
            unity_check=failed_unity,
            limit_report_id="limit-failed",
        )


def test_reason_is_representable_but_only_reserved_and_regulative(
    successful_trace: SimpleNamespace,
) -> None:
    scope = successful_trace.scope
    configuration = successful_trace.configuration
    regulative_rule = Rule(
        rule_id="Q-1",
        name="prefer likely persistence",
        description="organize a later inquiry without licensing an object",
        authority=RuleAuthority.REGULATIVE,
        scope=scope,
    )
    derivation = Derivation(
        operation="reserve reason metadata",
        grounds=(
            CognitiveGround(
                ground_id="Q-1",
                kind=GroundKind.RULE,
                authority=RuleAuthority.REGULATIVE,
            ),
        ),
        scope=scope,
        configuration=configuration,
    )
    reason = Reason(
        reason_id="reason-1",
        principle=regulative_rule,
        guidance="request a later observation of likely persistent patches",
        derivation=derivation,
    )
    assert reason.status.value == "reserved"

    with pytest.raises(ValidationError, match="regulative authority"):
        Reason(
            reason_id="reason-invalid",
            principle=Rule(
                rule_id="I-1",
                name="identity",
                description="form a candidate identity",
                authority=RuleAuthority.CONSTITUTIVE,
                scope=scope,
            ),
            guidance="form an object",
            derivation=derivation,
        )


def _context(
    successful_trace: SimpleNamespace,
    kind: OutcomeKind,
    details: _LimitDetails = _EMPTY_LIMIT_DETAILS,
) -> OutcomeContext:
    scope = successful_trace.scope
    configuration = successful_trace.configuration
    return OutcomeContext(
        configuration=configuration,
        derivation=Derivation(
            operation=f"report {kind.value}",
            grounds=(
                CognitiveGround(
                    ground_id="external-episode-1",
                    kind=GroundKind.EXTERNAL_INPUT,
                ),
            ),
            alternatives=details.alternatives,
            unmet_conditions=details.missing,
            scope=scope,
            configuration=configuration,
        ),
        limit_report=LimitReport(
            limit_report_id=f"limit-{kind.value}",
            strongest_licensed=kind,
            scope=scope,
            boundary=f"boundary for {kind.value}",
            missing_condition_ids=details.missing,
            conflict_ids=details.conflicts,
            alternative_ids=details.alternatives,
            authority_violations=details.violations,
        ),
    )


def test_all_ten_outcomes_are_distinct_and_round_trip(
    successful_trace: SimpleNamespace,
) -> None:
    evaluator_violation = AuthorityViolation(
        source_id="hidden-world-id",
        attempted_use="object-level predicate ground",
        explanation="evaluator state is not presented cognitive evidence",
        evaluator_reference=EvaluatorReference(
            evaluator_reference_id="hidden-world-id",
            description="hidden evaluator object identity",
        ),
    )
    outcomes = (
        InputError(
            outcome_id="outcome-input",
            context=_context(successful_trace, OutcomeKind.INPUT_ERROR),
            invalid_input_ids=("invalid-record-1",),
            errors=("episode position is missing",),
        ),
        NotPresentable(
            outcome_id="outcome-presentation",
            context=_context(
                successful_trace,
                OutcomeKind.NOT_PRESENTABLE,
                _LimitDetails(missing=("temporal-form",)),
            ),
            presented_element_ids=("pe-1",),
            failed_condition_ids=("temporal-form",),
        ),
        SynthesisFailed(
            outcome_id="outcome-synthesis-failed",
            context=_context(successful_trace, OutcomeKind.SYNTHESIS_FAILED),
            manifold_id="manifold-1",
            failed_rule_ids=("I-1",),
        ),
        SynthesisAmbiguous(
            outcome_id="outcome-synthesis-ambiguous",
            context=_context(
                successful_trace,
                OutcomeKind.SYNTHESIS_AMBIGUOUS,
                _LimitDetails(alternatives=("candidate-a", "candidate-b")),
            ),
            candidate_representation_ids=("candidate-a", "candidate-b"),
        ),
        ConceptNotApplicable(
            outcome_id="outcome-not-applicable",
            context=_context(
                successful_trace,
                OutcomeKind.CONCEPT_NOT_APPLICABLE,
                _LimitDetails(missing=("positive-change",)),
            ),
            object_candidate_id="object-1",
            application_result_id="application-failed",
            failed_condition_ids=("positive-change",),
        ),
        ApplicationUnderdetermined(
            outcome_id="outcome-underdetermined",
            context=_context(
                successful_trace,
                OutcomeKind.APPLICATION_UNDERDETERMINED,
                _LimitDetails(missing=("third-position",)),
            ),
            object_candidate_id="object-1",
            application_result_id="application-underdetermined",
            undecided_condition_ids=("third-position",),
        ),
        UnityConflict(
            outcome_id="outcome-unity-conflict",
            context=_context(
                successful_trace,
                OutcomeKind.UNITY_CONFLICT,
                _LimitDetails(conflicts=("branch-conflict",)),
            ),
            proposed_judgment_id="proposal-conflicted",
            conflict_ids=("branch-conflict",),
        ),
        JudgmentWithheld(
            outcome_id="outcome-withheld",
            context=_context(
                successful_trace,
                OutcomeKind.JUDGMENT_WITHHELD,
                _LimitDetails(missing=("licensed-subject",)),
            ),
            strongest_representation_ids=("application-a", "application-b"),
            unmet_condition_ids=("licensed-subject",),
        ),
        successful_trace.committed_outcome,
        Overreach(
            outcome_id="outcome-overreach",
            context=_context(
                successful_trace,
                OutcomeKind.OVERREACH,
                _LimitDetails(violations=(evaluator_violation,)),
            ),
            rejected_claim="object-1 is the evaluator's hidden object 7",
            violations=(evaluator_violation,),
        ),
    )

    assert len(OutcomeKind) == EXPECTED_OUTCOME_COUNT
    assert {outcome.kind for outcome in outcomes} == set(OutcomeKind)

    for outcome in outcomes:
        python_round_trip = validate_terminal_outcome(outcome.model_dump(mode="python"))
        json_round_trip = validate_terminal_outcome_json(dump_terminal_outcome(outcome))
        assert python_round_trip == outcome
        assert json_round_trip == outcome
