"""Distinct object, applicability, proposal, and commitment operations."""

from kantbot.cycle._support import derive, ground, outcome_context
from kantbot.cycle.synthesis import evaluate_rules
from kantbot.interfaces import (
    ApplicationRequest,
    CommitmentRequest,
    CommitmentResult,
    ObjectFormationRequest,
    ObjectFormationResult,
    ProposalRequest,
    ProposalResult,
    ProvenanceView,
)
from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    CandidateRepresentation,
    CommittedJudgment,
    CompleteWarrant,
    ConditionResult,
    ConditionStatus,
    GroundKind,
    JudgmentWithheld,
    ObjectCandidate,
    OutcomeKind,
    ProposedJudgment,
    SynthesisFailed,
    TerminalOutcome,
    dump_terminal_outcome,
)
from kantbot.procedures import evaluate_procedure


def object_conditions(
    candidate: CandidateRepresentation, provenance: ProvenanceView
) -> tuple[tuple[ConditionResult, ...], tuple[ConditionResult, ...]]:
    """Recompute both licenses on the canonical selected intuitions."""

    if provenance.candidate_for(candidate.candidate_representation_id) != candidate:
        raise ValueError("object request differs from registered candidate")
    intuitions = tuple(
        provenance.intuition_for(item) for item in candidate.intuition_ids
    )
    identity = tuple(provenance.rule_for(item) for item in candidate.identity_rule_ids)
    constitutive = tuple(
        provenance.rule_for(item) for item in candidate.constitutive_rule_ids
    )
    return evaluate_rules(identity, intuitions, provenance), evaluate_rules(
        constitutive, intuitions, provenance
    )


def constitute_object(
    request: ObjectFormationRequest, provenance: ProvenanceView, /
) -> ObjectFormationResult:
    """License objecthood only from replayed identity and constitutive results."""

    candidate = request.candidate
    identity, constitutive = object_conditions(candidate, provenance)
    supplied = request.identity_results + request.constitutive_results

    def claims(results: tuple[ConditionResult, ...]) -> tuple[tuple[object, ...], ...]:
        return tuple(
            (item.condition_id, item.required, item.status, item.evidence)
            for item in results
        )

    if claims(supplied) != claims(identity + constitutive):
        raise ValueError("object request disagrees with replayed results")
    if (
        not all(item.passed for item in identity + constitutive)
        or candidate.conflict_ids
        or candidate.derivation.unmet_conditions
    ):
        manifold_ids = tuple(
            item.ground_id
            for item in provenance.immediate_grounds(candidate.retained_sequence_id)
            if item.kind is GroundKind.MANIFOLD
        )
        if len(manifold_ids) != 1:
            raise ValueError("candidate retention must identify one manifold")
        label = f"object-failed:{candidate.candidate_representation_id}"
        failed_conditions = {
            item.condition_id for item in identity + constitutive if not item.passed
        }
        failed_rules = tuple(
            rule_id
            for rule_id in candidate.identity_rule_ids + candidate.constitutive_rule_ids
            if failed_conditions.intersection(
                condition.condition_id
                for condition in provenance.rule_for(rule_id).conditions
            )
        )
        if candidate.conflict_ids or candidate.derivation.unmet_conditions:
            failed_rules = tuple(
                dict.fromkeys((*failed_rules, *candidate.constitutive_rule_ids))
            )
        return SynthesisFailed(
            outcome_id=f"outcome:{label}",
            manifold_id=manifold_ids[0],
            failed_rule_ids=failed_rules,
            context=outcome_context(
                request.context,
                OutcomeKind.SYNTHESIS_FAILED,
                label,
                (
                    ground(
                        candidate.candidate_representation_id,
                        GroundKind.CANDIDATE_REPRESENTATION,
                    ),
                ),
                missing=tuple(
                    item.condition_id
                    for item in identity + constitutive
                    if not item.passed
                )
                or ("compatible-candidate-unity",),
            ),
        )
    return ObjectCandidate(
        object_candidate_id=f"object:{candidate.candidate_representation_id}",
        candidate_representation_id=candidate.candidate_representation_id,
        identity_results=identity,
        constitutive_results=constitutive,
        derivation=derive(
            request.context,
            "license object identity and unity",
            (
                ground(
                    candidate.candidate_representation_id,
                    GroundKind.CANDIDATE_REPRESENTATION,
                ),
            ),
        ),
    )


def apply_concept(
    request: ApplicationRequest, provenance: ProvenanceView, /
) -> ApplicationResult:
    """Run the schema; an applicable concept is still no judgment."""

    request.concept_schema.validate_concept(request.concept)
    candidate = provenance.candidate_for(
        request.object_candidate.candidate_representation_id
    )
    intuitions = tuple(
        provenance.intuition_for(item) for item in candidate.intuition_ids
    )
    forms = tuple(
        dict.fromkeys(
            form
            for item in intuitions
            for form in provenance.forms_for(item.intuition_id)
        )
    )
    results = evaluate_procedure(
        request.concept_schema.procedure,
        request.concept.applicability_conditions,
        intuitions,
        forms,
    )
    required = tuple(item for item in results if item.required)
    if any(item.status is ConditionStatus.FAILED for item in required):
        status = ApplicationStatus.NOT_APPLICABLE
    elif any(item.status is ConditionStatus.UNDECIDED for item in required):
        status = ApplicationStatus.UNDERDETERMINED
    else:
        status = ApplicationStatus.APPLICABLE
    obj_id = request.object_candidate.object_candidate_id
    return ApplicationResult(
        application_result_id=f"application:{obj_id}:{request.concept.concept_id}",
        object_candidate_id=obj_id,
        concept_id=request.concept.concept_id,
        schema_id=request.concept_schema.schema_id,
        status=status,
        condition_results=results,
        derivation=derive(
            request.context,
            "schema-mediated applicability",
            (
                ground(obj_id, GroundKind.OBJECT_CANDIDATE),
                ground(request.concept.concept_id, GroundKind.CONCEPT),
                ground(request.concept_schema.schema_id, GroundKind.SCHEMA),
            ),
        ),
    )


def propose_judgment(request: ProposalRequest, /) -> ProposalResult:
    """Assemble a proposition only when applicability and warrant roles permit it."""

    required_synthesis = {
        GroundKind.MANIFOLD,
        GroundKind.RETAINED_SEQUENCE,
        GroundKind.CANDIDATE_REPRESENTATION,
        GroundKind.OBJECT_CANDIDATE,
    }
    has_synthesis = required_synthesis <= {
        item.kind for item in request.warrant.synthesis_grounds
    }
    if not request.application.applicable or not has_synthesis:
        label = f"proposal-withheld:{request.application.application_result_id}"
        missing = ("complete-applicable-warrant",)
        return JudgmentWithheld(
            outcome_id=f"outcome:{label}",
            strongest_representation_ids=(request.application.application_result_id,),
            unmet_condition_ids=missing,
            context=outcome_context(
                request.context,
                OutcomeKind.JUDGMENT_WITHHELD,
                label,
                (
                    ground(
                        request.application.application_result_id,
                        GroundKind.APPLICATION_RESULT,
                    ),
                ),
                missing=missing,
            ),
        )
    return ProposedJudgment(
        proposed_judgment_id=f"proposal:{request.application.application_result_id}",
        proposition=request.proposition,
        warrant=request.warrant,
        derivation=derive(
            request.context,
            "assemble scoped proposition",
            (
                ground(
                    request.object_candidate.object_candidate_id,
                    GroundKind.OBJECT_CANDIDATE,
                ),
                ground(
                    request.application.application_result_id,
                    GroundKind.APPLICATION_RESULT,
                ),
            ),
        ),
    )


def commit_judgment(request: CommitmentRequest, /) -> CommitmentResult:
    """Construct a commitment; the runner must still certify its complete graph."""

    report = request.limit_report
    if (
        not request.unity_check.passed
        or report.missing_condition_ids
        or report.conflict_ids
        or report.authority_violations
    ):
        missing = report.missing_condition_ids or ("successful-unity-and-limits",)
        label = f"commitment-withheld:{request.proposal.proposed_judgment_id}"
        return JudgmentWithheld(
            outcome_id=f"outcome:{label}",
            strongest_representation_ids=(request.proposal.proposed_judgment_id,),
            unmet_condition_ids=missing,
            context=outcome_context(
                request.context,
                OutcomeKind.JUDGMENT_WITHHELD,
                label,
                (ground(request.proposal.proposed_judgment_id, GroundKind.JUDGMENT),),
                missing=missing,
            ),
        )
    return CommittedJudgment(
        judgment_id=f"judgment:{request.proposal.proposed_judgment_id}",
        proposed_judgment_id=request.proposal.proposed_judgment_id,
        proposition=request.proposal.proposition,
        warrant=CompleteWarrant(
            assembled=request.proposal.warrant,
            unity_check=request.unity_check,
            limit_report_id=report.limit_report_id,
        ),
        derivation=request.derivation,
    )


def critique_and_report(outcome: TerminalOutcome, /) -> str:
    """Expose the typed result and its limits through the existing canonical codec."""

    return dump_terminal_outcome(outcome)
