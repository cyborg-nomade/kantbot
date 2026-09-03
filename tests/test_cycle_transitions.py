"""Executable legal and terminal paths through one cognitive cycle."""

from types import SimpleNamespace
from typing import NamedTuple

import pytest
from pydantic import ValidationError

from kantbot.interfaces import RoleContext
from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    ApplicationUnderdetermined,
    AuthorityViolation,
    CognitiveGround,
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
    OutcomeContext,
    OutcomeKind,
    Overreach,
    SynthesisAmbiguous,
    SynthesisFailed,
    UnityCheck,
    UnityConflict,
)
from kantbot.transitions import (
    CandidateRecognized,
    ConceptApplied,
    CycleBoundary,
    CycleStage,
    CycleTerminated,
    InvalidTransition,
    JudgmentProposed,
    dump_cycle_state,
    open_cycle,
    record_application,
    record_commitment,
    record_critique,
    record_manifold,
    record_object_formation,
    record_projection,
    record_reception,
    record_recognition,
    record_retention,
    record_unity,
    reject_input,
    resolve_application,
    validate_cycle_state,
    validate_cycle_state_json,
    withhold_rival_applications,
)


def _role_context(trace: SimpleNamespace) -> RoleContext:
    return RoleContext(scope=trace.scope, configuration=trace.configuration)


class _OutcomeDetails(NamedTuple):
    ground_id: str = "external-episode-1"
    ground_kind: GroundKind = GroundKind.EXTERNAL_INPUT
    missing: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    violations: tuple[AuthorityViolation, ...] = ()


_EMPTY_OUTCOME_DETAILS = _OutcomeDetails()


def _outcome_context(
    trace: SimpleNamespace,
    kind: OutcomeKind,
    details: _OutcomeDetails = _EMPTY_OUTCOME_DETAILS,
) -> OutcomeContext:
    return OutcomeContext(
        configuration=trace.configuration,
        derivation=Derivation(
            operation=f"report {kind.value}",
            grounds=(
                CognitiveGround(
                    ground_id=details.ground_id,
                    kind=details.ground_kind,
                ),
            ),
            alternatives=details.alternatives,
            unmet_conditions=details.missing,
            scope=trace.scope,
            configuration=trace.configuration,
        ),
        limit_report=LimitReport(
            limit_report_id=f"limit-{kind.value}",
            strongest_licensed=kind,
            scope=trace.scope,
            boundary=f"boundary for {kind.value}",
            missing_condition_ids=details.missing,
            conflict_ids=details.conflicts,
            alternative_ids=details.alternatives,
            authority_violations=details.violations,
        ),
    )


def _reach_application(trace: SimpleNamespace) -> ConceptApplied:
    context = _role_context(trace)
    opened = open_cycle("cycle-1", (trace.observation,), context)
    presented = record_reception(opened, (trace.presented,))
    projected = record_projection(presented, (trace.intuition,))
    assert not isinstance(projected, CycleTerminated)
    manifold = record_manifold(projected, trace.manifold)
    retained = record_retention(manifold, trace.retained)
    assert not isinstance(retained, CycleTerminated)
    recognized = record_recognition(retained, (trace.candidate,))
    assert isinstance(recognized, tuple)
    constituted = record_object_formation(recognized[0], trace.object_candidate)
    assert not isinstance(constituted, CycleTerminated)
    return record_application(constituted, trace.application)


def _failed_application(
    trace: SimpleNamespace, status: ConditionStatus
) -> ApplicationResult:
    condition = ConditionResult(
        condition_id="amber-content",
        required=True,
        status=status,
        explanation=f"application is {status.value}",
        evidence=(
            CognitiveGround(
                ground_id=trace.object_candidate.object_candidate_id,
                kind=GroundKind.OBJECT_CANDIDATE,
            ),
        ),
    )
    application_status = ApplicationStatus.NOT_APPLICABLE
    if status is ConditionStatus.UNDECIDED:
        application_status = ApplicationStatus.UNDERDETERMINED
    return ApplicationResult(
        application_result_id=f"application-{status.value}",
        object_candidate_id=trace.object_candidate.object_candidate_id,
        concept_id=trace.concept.concept_id,
        schema_id=trace.schema.schema_id,
        status=application_status,
        condition_results=(condition,),
        derivation=trace.application.derivation,
    )


def test_success_path_crosses_every_gate_and_round_trips(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    applied = _reach_application(trace)
    proposed = resolve_application(applied, trace.proposal)
    assert isinstance(proposed, JudgmentProposed)
    united = record_unity(proposed, trace.unity_check)
    assert not isinstance(united, CycleTerminated)
    committed = record_commitment(united, trace.judgment)
    assert not isinstance(committed, CycleTerminated)
    terminal = record_critique(committed, trace.committed_outcome)

    assert terminal.stage is CycleStage.TERMINAL
    assert terminal.boundary is CycleBoundary.CRITIQUE
    assert terminal.outcome.kind is OutcomeKind.JUDGMENT_COMMITTED
    encoded = dump_cycle_state(terminal)
    assert validate_cycle_state_json(encoded) == terminal
    assert validate_cycle_state(terminal.model_dump(mode="python")) == terminal


def test_every_nonterminal_snapshot_round_trips_through_the_state_union(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    opened = open_cycle("cycle-round-trip", (trace.observation,), _role_context(trace))
    presented = record_reception(opened, (trace.presented,))
    projected = record_projection(presented, (trace.intuition,))
    assert not isinstance(projected, CycleTerminated)
    manifold = record_manifold(projected, trace.manifold)
    retained = record_retention(manifold, trace.retained)
    assert not isinstance(retained, CycleTerminated)
    recognized = record_recognition(retained, (trace.candidate,))
    assert isinstance(recognized, tuple)
    constituted = record_object_formation(recognized[0], trace.object_candidate)
    assert not isinstance(constituted, CycleTerminated)
    applied = record_application(constituted, trace.application)
    proposed = resolve_application(applied, trace.proposal)
    assert isinstance(proposed, JudgmentProposed)
    united = record_unity(proposed, trace.unity_check)
    assert not isinstance(united, CycleTerminated)
    committed = record_commitment(united, trace.judgment)
    assert not isinstance(committed, CycleTerminated)

    snapshots = (
        opened,
        presented,
        projected,
        manifold,
        retained,
        recognized[0],
        constituted,
        applied,
        proposed,
        united,
        committed,
    )
    for snapshot in snapshots:
        assert validate_cycle_state_json(dump_cycle_state(snapshot)) == snapshot


def test_input_error_stops_before_cognitive_reception(
    successful_trace: SimpleNamespace,
) -> None:
    outcome = InputError(
        outcome_id="outcome-input",
        context=_outcome_context(successful_trace, OutcomeKind.INPUT_ERROR),
        invalid_input_ids=("record-without-position",),
        errors=("episode position is absent",),
    )

    terminal = reject_input("cycle-input", _role_context(successful_trace), outcome)

    assert terminal.boundary is CycleBoundary.INPUT_VALIDATION
    assert terminal.outcome == outcome


def test_projection_refusal_preserves_the_presented_element(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    opened = open_cycle("cycle-projection", (trace.observation,), _role_context(trace))
    presented = record_reception(opened, (trace.presented,))
    refusal = NotPresentable(
        outcome_id="outcome-not-presentable",
        context=_outcome_context(
            trace,
            OutcomeKind.NOT_PRESENTABLE,
            _OutcomeDetails(missing=("temporal-form",)),
        ),
        presented_element_ids=(trace.presented.presented_element_id,),
        failed_condition_ids=("temporal-form",),
    )

    terminal = record_projection(presented, refusal)

    assert isinstance(terminal, CycleTerminated)
    assert terminal.boundary is CycleBoundary.VARIANT_PROJECTION


@pytest.mark.parametrize(
    ("operation", "boundary"),
    [
        ("retention", CycleBoundary.RETENTION),
        ("recognition", CycleBoundary.RECOGNITION),
        ("object", CycleBoundary.OBJECT_FORMATION),
    ],
)
def test_synthesis_failure_stops_at_its_actual_boundary(
    successful_trace: SimpleNamespace,
    operation: str,
    boundary: CycleBoundary,
) -> None:
    trace = successful_trace
    context = _role_context(trace)
    opened = open_cycle("cycle-synthesis", (trace.observation,), context)
    presented = record_reception(opened, (trace.presented,))
    projected = record_projection(presented, (trace.intuition,))
    assert not isinstance(projected, CycleTerminated)
    manifold = record_manifold(projected, trace.manifold)
    failure = SynthesisFailed(
        outcome_id=f"outcome-{operation}-failure",
        context=_outcome_context(trace, OutcomeKind.SYNTHESIS_FAILED),
        manifold_id=trace.manifold.manifold_id,
        failed_rule_ids=("I-1",),
    )

    if operation == "retention":
        terminal = record_retention(manifold, failure)
    else:
        retained = record_retention(manifold, trace.retained)
        assert not isinstance(retained, CycleTerminated)
        if operation == "recognition":
            terminal = record_recognition(retained, failure)
        else:
            recognized = record_recognition(retained, (trace.candidate,))
            assert isinstance(recognized, tuple)
            terminal = record_object_formation(recognized[0], failure)

    assert isinstance(terminal, CycleTerminated)
    assert terminal.boundary is boundary


def test_recognition_can_stop_at_ambiguity_or_fork_explicit_paths(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    context = _role_context(trace)
    opened = open_cycle("cycle-branches", (trace.observation,), context)
    presented = record_reception(opened, (trace.presented,))
    projected = record_projection(presented, (trace.intuition,))
    assert not isinstance(projected, CycleTerminated)
    manifold = record_manifold(projected, trace.manifold)
    retained = record_retention(manifold, trace.retained)
    assert not isinstance(retained, CycleTerminated)

    ambiguity = SynthesisAmbiguous(
        outcome_id="outcome-ambiguous",
        context=_outcome_context(
            trace,
            OutcomeKind.SYNTHESIS_AMBIGUOUS,
            _OutcomeDetails(alternatives=("candidate-a", "candidate-b")),
        ),
        candidate_representation_ids=("candidate-a", "candidate-b"),
    )
    terminal = record_recognition(retained, ambiguity)
    assert isinstance(terminal, CycleTerminated)

    candidate_type = trace.candidate.__class__
    common = trace.candidate.model_dump(
        mode="python",
        exclude={"candidate_representation_id", "alternative_candidate_ids"},
    )
    candidate_a = candidate_type(
        **common,
        candidate_representation_id="candidate-a",
        alternative_candidate_ids=("candidate-b",),
    )
    candidate_b = candidate_type(
        **common,
        candidate_representation_id="candidate-b",
        alternative_candidate_ids=("candidate-a",),
    )
    branches = record_recognition(retained, (candidate_a, candidate_b))

    assert isinstance(branches, tuple)
    assert [branch.candidate.candidate_representation_id for branch in branches] == [
        "candidate-a",
        "candidate-b",
    ]


@pytest.mark.parametrize(
    "status",
    [ConditionStatus.FAILED, ConditionStatus.UNDECIDED],
)
def test_application_status_requires_its_matching_terminal_outcome(
    successful_trace: SimpleNamespace,
    status: ConditionStatus,
) -> None:
    trace = successful_trace
    successful_stage = _reach_application(trace)
    application = _failed_application(trace, status)
    applied = ConceptApplied(
        cycle_id=successful_stage.cycle_id,
        context=successful_stage.context,
        application=application,
    )

    if status is ConditionStatus.FAILED:
        outcome = ConceptNotApplicable(
            outcome_id="outcome-not-applicable",
            context=_outcome_context(
                trace,
                OutcomeKind.CONCEPT_NOT_APPLICABLE,
                _OutcomeDetails(missing=("amber-content",)),
            ),
            object_candidate_id=application.object_candidate_id,
            application_result_id=application.application_result_id,
            failed_condition_ids=("amber-content",),
        )
    else:
        outcome = ApplicationUnderdetermined(
            outcome_id="outcome-underdetermined",
            context=_outcome_context(
                trace,
                OutcomeKind.APPLICATION_UNDERDETERMINED,
                _OutcomeDetails(missing=("amber-content",)),
            ),
            object_candidate_id=application.object_candidate_id,
            application_result_id=application.application_result_id,
            undecided_condition_ids=("amber-content",),
        )

    terminal = resolve_application(applied, outcome)

    assert isinstance(terminal, CycleTerminated)
    assert terminal.boundary is CycleBoundary.APPLICATION


def test_successful_application_can_end_in_withholding(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    applied = _reach_application(trace)
    withheld = JudgmentWithheld(
        outcome_id="outcome-withheld-at-proposal",
        context=_outcome_context(
            trace,
            OutcomeKind.JUDGMENT_WITHHELD,
            _OutcomeDetails(missing=("licensed-subject",)),
        ),
        strongest_representation_ids=(trace.application.application_result_id,),
        unmet_condition_ids=("licensed-subject",),
    )

    terminal = resolve_application(applied, withheld)

    assert isinstance(terminal, CycleTerminated)
    assert terminal.boundary is CycleBoundary.PROPOSAL


def test_successful_rival_applications_converge_only_as_withheld(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    first = _reach_application(trace)
    rival_application = ApplicationResult(
        **trace.application.model_dump(
            mode="python", exclude={"application_result_id"}
        ),
        application_result_id="application-rival",
    )
    rival = ConceptApplied(
        cycle_id=first.cycle_id,
        context=first.context,
        application=rival_application,
    )
    withheld = JudgmentWithheld(
        outcome_id="outcome-rivals-withheld",
        context=_outcome_context(
            trace,
            OutcomeKind.JUDGMENT_WITHHELD,
            _OutcomeDetails(missing=("singular-subject",)),
        ),
        strongest_representation_ids=(
            first.application.application_result_id,
            rival.application.application_result_id,
        ),
        unmet_condition_ids=("singular-subject",),
    )

    terminal = withhold_rival_applications((first, rival), withheld)

    assert terminal.boundary is CycleBoundary.PROPOSAL
    assert terminal.outcome == withheld


def test_unity_exposes_conflict_and_overreach_without_repair(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    applied = _reach_application(trace)
    proposed = resolve_application(applied, trace.proposal)
    assert isinstance(proposed, JudgmentProposed)
    conflict = UnityConflict(
        outcome_id="outcome-unity-conflict",
        context=_outcome_context(
            trace,
            OutcomeKind.UNITY_CONFLICT,
            _OutcomeDetails(conflicts=("branch-conflict",)),
        ),
        proposed_judgment_id=trace.proposal.proposed_judgment_id,
        conflict_ids=("branch-conflict",),
    )
    conflicted = record_unity(proposed, conflict)
    assert isinstance(conflicted, CycleTerminated)

    violation = AuthorityViolation(
        source_id="hidden-world-id",
        attempted_use="object-level warrant",
        explanation="evaluator state cannot ground cognition",
        evaluator_reference=EvaluatorReference(
            evaluator_reference_id="hidden-world-id",
            description="hidden evaluator identity",
        ),
    )
    overreach = Overreach(
        outcome_id="outcome-overreach",
        context=_outcome_context(
            trace,
            OutcomeKind.OVERREACH,
            _OutcomeDetails(
                ground_id=trace.proposal.proposed_judgment_id,
                ground_kind=GroundKind.JUDGMENT,
                violations=(violation,),
            ),
        ),
        rejected_claim="the presented marker has the hidden identity",
        violations=(violation,),
    )
    rejected = record_unity(proposed, overreach)

    assert isinstance(rejected, CycleTerminated)
    assert rejected.boundary is CycleBoundary.UNITY


def test_commitment_may_still_withhold_after_successful_unity(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    applied = _reach_application(trace)
    proposed = resolve_application(applied, trace.proposal)
    assert isinstance(proposed, JudgmentProposed)
    united = record_unity(proposed, trace.unity_check)
    assert not isinstance(united, CycleTerminated)
    withheld = JudgmentWithheld(
        outcome_id="outcome-withheld-at-commitment",
        context=_outcome_context(
            trace,
            OutcomeKind.JUDGMENT_WITHHELD,
            _OutcomeDetails(missing=("complete-warrant",)),
        ),
        strongest_representation_ids=(trace.proposal.proposed_judgment_id,),
        unmet_condition_ids=("complete-warrant",),
    )

    terminal = record_commitment(united, withheld)

    assert isinstance(terminal, CycleTerminated)
    assert terminal.boundary is CycleBoundary.COMMITMENT


def test_cross_stage_mismatches_are_programming_errors_not_cognitive_failures(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    context = _role_context(trace)
    opened = open_cycle("cycle-invalid", (trace.observation,), context)

    with pytest.raises(InvalidTransition, match="every and only"):
        record_reception(opened, ())

    other_presented = trace.presented.model_copy(
        update={"observation_id": "foreign-observation"}
    )
    with pytest.raises(InvalidTransition, match="every and only"):
        record_reception(opened, (other_presented,))

    presented = record_reception(opened, (trace.presented,))
    foreign_intuition = trace.intuition.model_copy(
        update={"presented_element_id": "foreign-presentation"}
    )
    with pytest.raises(InvalidTransition, match="every and only"):
        record_projection(presented, (foreign_intuition,))


def test_states_reject_mixed_contexts_and_illegal_terminal_boundaries(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    other_scope = trace.scope.model_copy(update={"scope_id": "other-scope"})
    other_context = RoleContext(
        scope=other_scope,
        configuration=trace.configuration,
    )
    with pytest.raises(ValidationError, match="share the cycle context"):
        CandidateRecognized(
            cycle_id="cycle-mixed",
            context=other_context,
            manifold_id=trace.manifold.manifold_id,
            candidate=trace.candidate,
        )

    with pytest.raises(ValidationError, match="cannot terminate"):
        CycleTerminated(
            cycle_id="cycle-invalid-terminal",
            context=_role_context(trace),
            boundary=CycleBoundary.APPLICATION,
            outcome=trace.committed_outcome,
        )


def test_failed_unity_check_cannot_hide_behind_the_success_type(
    successful_trace: SimpleNamespace,
) -> None:
    trace = successful_trace
    applied = _reach_application(trace)
    proposed = resolve_application(applied, trace.proposal)
    assert isinstance(proposed, JudgmentProposed)
    failed_condition = ConditionResult(
        condition_id="cycle-wide-unity",
        required=True,
        status=ConditionStatus.FAILED,
        explanation="branches conflict",
        evidence=(
            CognitiveGround(
                ground_id=trace.proposal.proposed_judgment_id,
                kind=GroundKind.JUDGMENT,
            ),
        ),
    )
    failed_unity = UnityCheck(
        unity_check_id="unity-failed",
        status=ConditionStatus.FAILED,
        condition_results=(failed_condition,),
        conflict_ids=("branch-conflict",),
        scope=trace.scope,
        configuration=trace.configuration,
    )

    with pytest.raises(InvalidTransition, match="unity-conflict"):
        record_unity(proposed, failed_unity)
