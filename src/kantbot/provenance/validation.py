"""Cross-node validation, kept separate from canonical parsing hooks."""

from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    ApplicationUnderdetermined,
    AuthorityViolation,
    CandidateRepresentation,
    CommittedJudgment,
    Concept,
    ConceptNotApplicable,
    ConditionStatus,
    ConfigurationIdentity,
    Form,
    GroundKind,
    InputError,
    Intuition,
    JudgmentCommitted,
    JudgmentWithheld,
    LimitReport,
    ManifoldOfIntuition,
    NotPresentable,
    ObjectCandidate,
    Observation,
    OutcomeKind,
    PresentedElement,
    ProposedJudgment,
    RetainedSequence,
    Rule,
    RuleAuthority,
    Schema,
    Scope,
    SemanticModel,
    SynthesisAmbiguous,
    SynthesisFailed,
    UnityConflict,
    VariantProjection,
)
from kantbot.provenance.format import ExternalInputReference, ProvenanceTrace
from kantbot.provenance.references import nested_models
from kantbot.provenance.registry import Entry, lookup, require


def validate_context(trace: ProvenanceTrace) -> None:
    """Even nested warrants and evidence must belong to the frozen context."""

    for value in nested_models(trace):
        if isinstance(value, Scope):
            require(value == trace.scope, "mixed scopes in provenance")
        elif isinstance(value, ConfigurationIdentity):
            require(value == trace.configuration, "mixed configurations in provenance")
        elif isinstance(value, Observation):
            require(
                value.episode_id == trace.scope.episode_id,
                "foreign observation episode",
            )
        elif isinstance(value, VariantProjection):
            require(
                value.variant_id == trace.configuration.variant_id,
                "projection belongs to another variant",
            )


def _forms(entries: dict[str, Entry], form_ids: tuple[str, ...]) -> None:
    for form_id in form_ids:
        lookup(entries, form_id, Form)


def validate_reception(trace: ProvenanceTrace, entries: dict[str, Entry]) -> None:
    for presented in trace.presented_elements:
        observation = lookup(entries, presented.observation_id, Observation)
        require(
            (
                presented.episode_id,
                presented.position,
                presented.source,
                presented.content,
            )
            == (
                observation.episode_id,
                observation.position,
                observation.source,
                observation.content,
            ),
            "shared reception changed supplied content, source, or ordering",
        )
    for intuition in trace.intuitions:
        presented = lookup(entries, intuition.presented_element_id, PresentedElement)
        projection = lookup(entries, intuition.projection_id, VariantProjection)
        _forms(entries, intuition.form_ids)
        require(
            {form.form_id for form in projection.required_forms}
            <= set(intuition.form_ids),
            "intuition omits a required projection form",
        )
        require(
            intuition.position == presented.position,
            "intuition changed episode position",
        )
    for manifold in trace.manifolds:
        _forms(entries, manifold.form_ids)
        for intuition_id in manifold.intuition_ids:
            intuition = lookup(entries, intuition_id, Intuition)
            require(
                set(manifold.form_ids) <= set(intuition.form_ids),
                "manifold uses forms unavailable to an intuition",
            )


def validate_synthesis(trace: ProvenanceTrace, entries: dict[str, Entry]) -> None:
    for retained in trace.retained_sequences:
        manifold = lookup(entries, retained.manifold_id, ManifoldOfIntuition)
        require(
            {item.intuition_id for item in retained.items}
            <= set(manifold.intuition_ids),
            "retention introduces an intuition outside its manifold",
        )
    for candidate in trace.candidates:
        retained = lookup(entries, candidate.retained_sequence_id, RetainedSequence)
        require(
            set(candidate.intuition_ids)
            <= {item.intuition_id for item in retained.items},
            "candidate uses an intuition absent from retention",
        )
        for rule_id in candidate.identity_rule_ids + candidate.constitutive_rule_ids:
            rule = lookup(entries, rule_id, Rule)
            require(
                rule.authority is RuleAuthority.CONSTITUTIVE,
                "synthesis rule is not constitutive",
            )
        for alternative in candidate.alternative_candidate_ids:
            lookup(entries, alternative, CandidateRepresentation)
    for obj in trace.object_candidates:
        lookup(entries, obj.candidate_representation_id, CandidateRepresentation)


def validate_applications(trace: ProvenanceTrace, entries: dict[str, Entry]) -> None:
    for schema in trace.schemas:
        concept = lookup(entries, schema.concept_id, Concept)
        _forms(entries, schema.sensible_form_ids)
        require(
            set(schema.condition_ids)
            <= {item.condition_id for item in concept.applicability_conditions},
            "schema refers to a condition outside its concept",
        )
    for application in trace.applications:
        obj = lookup(entries, application.object_candidate_id, ObjectCandidate)
        schema = lookup(entries, application.schema_id, Schema)
        concept = lookup(entries, application.concept_id, Concept)
        require(
            schema.concept_id == concept.concept_id,
            "application uses another concept's schema",
        )
        expected = {
            item.condition_id: item.required
            for item in concept.applicability_conditions
        }
        actual = {
            item.condition_id: item.required for item in application.condition_results
        }
        require(
            actual == expected,
            "application omits or changes declared concept conditions",
        )
        candidate = lookup(
            entries, obj.candidate_representation_id, CandidateRepresentation
        )
        for intuition_id in candidate.intuition_ids:
            intuition = lookup(entries, intuition_id, Intuition)
            require(
                set(schema.sensible_form_ids) <= set(intuition.form_ids),
                "application lacks its schema's sensible forms",
            )
        for alternative in application.alternative_application_ids:
            lookup(entries, alternative, ApplicationResult)


def validate_proposals(trace: ProvenanceTrace, entries: dict[str, Entry]) -> None:
    for proposal in trace.proposals:
        application = lookup(
            entries, proposal.warrant.application_result_id, ApplicationResult
        )
        require(
            application.applicable, "proposal is grounded in an inapplicable result"
        )
        require(
            proposal.proposition.subject_candidate_id == application.object_candidate_id
            and proposal.proposition.predicate_concept_id == application.concept_id
            and proposal.warrant.schema_ground.ground_id == application.schema_id,
            "proposal and application disagree on subject, concept, or schema",
        )
        _forms(entries, proposal.warrant.presentation_form_ids)
    for unity in trace.unity_checks:
        proposal_ids = {
            ground.ground_id
            for condition in unity.condition_results
            for ground in condition.evidence
            if ground.kind is GroundKind.JUDGMENT
        }
        require(len(proposal_ids) == 1, "unity must identify one checked proposal")
        for proposal_id in proposal_ids:
            lookup(entries, proposal_id, ProposedJudgment)


def validate_commitments(trace: ProvenanceTrace, entries: dict[str, Entry]) -> None:
    for judgment in trace.judgments:
        proposal = lookup(entries, judgment.proposed_judgment_id, ProposedJudgment)
        require(
            judgment.proposition == proposal.proposition
            and judgment.warrant.assembled == proposal.warrant,
            "commitment changed the proposal or its assembled warrant",
        )
        unity = judgment.warrant.unity_check
        require(
            any(
                ground.ground_id == proposal.proposed_judgment_id
                and ground.kind is GroundKind.JUDGMENT
                for condition in unity.condition_results
                for ground in condition.evidence
            ),
            "committed unity does not identify its proposal",
        )
        report = lookup(entries, judgment.warrant.limit_report_id, LimitReport)
        require(
            report.strongest_licensed is OutcomeKind.JUDGMENT_COMMITTED
            and not (
                report.missing_condition_ids
                or report.conflict_ids
                or report.authority_violations
            ),
            "commitment has a blocking or non-committed limit report",
        )


def _validate_reception_outcome(
    value: SemanticModel, entries: dict[str, Entry]
) -> None:
    match value:
        case InputError():
            for entity_id in value.invalid_input_ids:
                lookup(entries, entity_id, ExternalInputReference)
        case NotPresentable():
            for entity_id in value.presented_element_ids:
                lookup(entries, entity_id, PresentedElement)
        case SynthesisFailed():
            lookup(entries, value.manifold_id, ManifoldOfIntuition)
            for entity_id in value.failed_rule_ids:
                lookup(entries, entity_id, Rule)
        case SynthesisAmbiguous():
            retained_ids: set[str] = set()
            for entity_id in value.candidate_representation_ids:
                candidate = lookup(entries, entity_id, CandidateRepresentation)
                retained_ids.add(candidate.retained_sequence_id)
                require(
                    value.context.derivation.has_ground(
                        candidate.retained_sequence_id, GroundKind.RETAINED_SEQUENCE
                    ),
                    "ambiguity omits a candidate's retained-sequence ground",
                )
            require(
                len(retained_ids) == 1,
                "ambiguity combines different recognition inputs",
            )


def _validate_later_outcome(value: SemanticModel, entries: dict[str, Entry]) -> None:
    match value:
        case ConceptNotApplicable() | ApplicationUnderdetermined():
            application = lookup(
                entries, value.application_result_id, ApplicationResult
            )
            require(
                application.object_candidate_id == value.object_candidate_id,
                "limit names another application object",
            )
            expected = ApplicationStatus.NOT_APPLICABLE
            condition_status = ConditionStatus.FAILED
            if isinstance(value, ApplicationUnderdetermined):
                expected = ApplicationStatus.UNDERDETERMINED
                condition_status = ConditionStatus.UNDECIDED
                reported_ids = value.undecided_condition_ids
            else:
                reported_ids = value.failed_condition_ids
            require(
                application.status is expected, "limit contradicts application status"
            )
            actual_ids = {
                result.condition_id
                for result in application.condition_results
                if result.status is condition_status
            }
            required_ids = {
                result.condition_id
                for result in application.condition_results
                if result.required and result.status is condition_status
            }
            require(
                required_ids <= set(reported_ids) <= actual_ids,
                "application limit misreports failed or undecided conditions",
            )
        case UnityConflict():
            lookup(entries, value.proposed_judgment_id, ProposedJudgment)
        case JudgmentWithheld():
            for entity_id in value.strongest_representation_ids:
                entry = entries.get(entity_id)
                require(
                    entry is not None and entry.kind is not None,
                    "withholding names a non-cognitive or missing representation",
                )
        case JudgmentCommitted():
            lookup(entries, value.judgment.judgment_id, CommittedJudgment)


def validate_outcomes(trace: ProvenanceTrace, entries: dict[str, Entry]) -> None:
    for outcome in trace.outcomes:
        _validate_reception_outcome(outcome, entries)
        _validate_later_outcome(outcome, entries)
    for value in nested_models(trace):
        if isinstance(value, AuthorityViolation):
            if value.evaluator_reference is not None:
                require(
                    value.source_id == value.evaluator_reference.evaluator_reference_id,
                    "authority violation names another evaluator reference",
                )
            if value.declared_authority is not None:
                rule = lookup(entries, value.source_id, Rule)
                require(
                    rule.authority is value.declared_authority,
                    "violation misstates rule authority",
                )
