"""A cycle-wide unity policy over the cognitive read port."""

from kantbot.cycle._support import ground, outcome_context, replace_value
from kantbot.interfaces import ProvenanceView, UnityRequest, UnityResult
from kantbot.model import (
    AuthorityViolation,
    CognitiveGround,
    ConditionResult,
    ConditionStatus,
    GroundKind,
    Modality,
    OutcomeKind,
    Overreach,
    RuleAuthority,
    UnityCheck,
    UnityConflict,
)


def ancestry(
    root: CognitiveGround, provenance: ProvenanceView
) -> tuple[CognitiveGround, ...]:
    """Traverse actual evidence, excluding comparison alternatives."""

    pending = [root]
    found: dict[str, CognitiveGround] = {}
    while pending:
        item = pending.pop()
        if item.ground_id in found:
            continue
        if not provenance.resolves(item):
            raise ValueError("unity requires a closed, correctly typed cognitive view")
        found[item.ground_id] = item
        pending.extend(reversed(provenance.immediate_grounds(item.ground_id)))
    return tuple(found.values())


def check_unity(request: UnityRequest, provenance: ProvenanceView, /) -> UnityResult:
    """Check compatibility of the whole proposal, not merely application status."""

    proposal = request.proposal
    root = ground(proposal.proposed_judgment_id, GroundKind.JUDGMENT)
    lineage = ancestry(root, provenance)
    violations = tuple(
        AuthorityViolation(
            source_id=item.ground_id,
            attempted_use=proposal.proposition.text,
            explanation="Non-constitutive guidance was promoted into object warrant",
            declared_authority=item.authority,
        )
        for item in lineage
        if item.kind is GroundKind.RULE
        and item.authority is not RuleAuthority.CONSTITUTIVE
    )
    label = f"unity:{proposal.proposed_judgment_id}"
    if violations:
        context = outcome_context(
            request.context, OutcomeKind.OVERREACH, label, (root,)
        )
        context = replace_value(
            context,
            limit_report=replace_value(
                context.limit_report, authority_violations=violations
            ),
        )
        return Overreach(
            outcome_id=f"outcome:{label}",
            rejected_claim=proposal.proposition.text,
            violations=violations,
            context=context,
        )
    conflicts = _unity_conflicts(request, provenance, lineage)
    if conflicts:
        context = outcome_context(
            request.context, OutcomeKind.UNITY_CONFLICT, label, (root,)
        )
        context = replace_value(
            context,
            limit_report=replace_value(context.limit_report, conflict_ids=conflicts),
        )
        return UnityConflict(
            outcome_id=f"outcome:{label}",
            proposed_judgment_id=proposal.proposed_judgment_id,
            conflict_ids=conflicts,
            context=context,
        )
    return UnityCheck(
        unity_check_id=f"check:{proposal.proposed_judgment_id}",
        status=ConditionStatus.SATISFIED,
        condition_results=(
            ConditionResult(
                condition_id="cycle-wide-unity",
                required=True,
                status=ConditionStatus.SATISFIED,
                explanation=(
                    "Compatible ancestry, constitutive authority, "
                    "complete warrant, and bounded modality"
                ),
                evidence=(root,),
            ),
        ),
        scope=request.context.scope,
        configuration=request.context.configuration,
    )


def _unity_conflicts(
    request: UnityRequest,
    provenance: ProvenanceView,
    lineage: tuple[CognitiveGround, ...],
) -> tuple[str, ...]:
    conflicts: list[str] = []
    for item in lineage:
        if (
            provenance.scope_for(item.ground_id) != request.context.scope
            or provenance.configuration_for(item.ground_id)
            != request.context.configuration
        ):
            conflicts.append("one-frozen-context")
    candidates = tuple(
        provenance.candidate_for(item.ground_id)
        for item in lineage
        if item.kind is GroundKind.CANDIDATE_REPRESENTATION
    )
    candidate_ids = {item.candidate_representation_id for item in candidates}
    for candidate in candidates:
        if (
            candidate.conflict_ids
            or candidate.derivation.unmet_conditions
            or candidate_ids.intersection(candidate.alternative_candidate_ids)
        ):
            conflicts.append("incompatible-identity-branches")
    if request.proposal.proposition.modality is Modality.APODICTIC:
        conflicts.append("modality-exceeds-empirical-ground")
    warrant = request.proposal.warrant
    application_lineage = ancestry(warrant.application_ground, provenance)
    for kinds, supplied in (
        ({GroundKind.OBSERVATION}, warrant.observation_grounds),
        ({GroundKind.VARIANT_PROJECTION}, warrant.projection_grounds),
        (
            {
                GroundKind.MANIFOLD,
                GroundKind.RETAINED_SEQUENCE,
                GroundKind.CANDIDATE_REPRESENTATION,
                GroundKind.OBJECT_CANDIDATE,
            },
            warrant.synthesis_grounds,
        ),
    ):
        required = {
            item.ground_id for item in application_lineage if item.kind in kinds
        }
        if not required <= {item.ground_id for item in supplied}:
            conflicts.append("incomplete-warrant-ancestry")
    identity_ids = {
        item for candidate in candidates for item in candidate.identity_rule_ids
    }
    constitutive_ids = {
        item for candidate in candidates for item in candidate.constitutive_rule_ids
    }
    if not identity_ids <= {
        item.ground_id for item in warrant.identity_rule_grounds
    } or not constitutive_ids <= {
        item.ground_id for item in warrant.constitutive_rule_grounds
    }:
        conflicts.append("incomplete-rule-warrant")
    forms = {
        form.form_id
        for item in application_lineage
        if item.kind is GroundKind.INTUITION
        for form in provenance.forms_for(item.ground_id)
    }
    if forms != set(warrant.presentation_form_ids):
        conflicts.append("incompatible-presentation-forms")
    return tuple(dict.fromkeys(conflicts))
