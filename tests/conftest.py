"""Small valid values shared by canonical-model unit tests."""

from types import SimpleNamespace

import pytest

from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    AssembledWarrant,
    CandidateRepresentation,
    CognitiveGround,
    CommittedJudgment,
    CompleteWarrant,
    Concept,
    ConceptKind,
    Condition,
    ConditionResult,
    ConditionStatus,
    ConfigurationIdentity,
    ContentField,
    Derivation,
    FieldConstant,
    FieldEquals,
    FieldProjection,
    Form,
    FormKind,
    GroundKind,
    Intuition,
    JudgmentCommitted,
    LimitReport,
    ManifoldOfIntuition,
    Modality,
    ObjectCandidate,
    Observation,
    ObservationQuality,
    OutcomeContext,
    OutcomeKind,
    PresentedElement,
    ProposedJudgment,
    Proposition,
    RetainedIntuition,
    RetainedSequence,
    RetentionStatus,
    Rule,
    RuleAuthority,
    RuleKind,
    Schema,
    Scope,
    SensibleProcedure,
    SynthesisPolicy,
    TemporalOrder,
    UnityCheck,
    VariantProjection,
)
from kantbot.provenance import ProvenanceTrace


def ground(
    ground_id: str,
    kind: GroundKind,
    authority: RuleAuthority | None = None,
) -> CognitiveGround:
    return CognitiveGround(ground_id=ground_id, kind=kind, authority=authority)


def derivation(
    operation: str,
    grounds: tuple[CognitiveGround, ...],
    scope: Scope,
    configuration: ConfigurationIdentity,
) -> Derivation:
    return Derivation(
        operation=operation,
        grounds=grounds,
        scope=scope,
        configuration=configuration,
    )


def make_successful_trace() -> SimpleNamespace:
    """Two observed moments license the hand-authored temporal success trace."""

    scope = Scope(
        scope_id="scope-episode-1",
        episode_id="episode-1",
        description="the supplied frames in episode 1",
        presentation_conditions=("total temporal order", "one-dimensional strip"),
        excluded_claims=("hidden numerical identity", "future persistence"),
    )
    configuration = ConfigurationIdentity(
        configuration_id="config-1",
        variant_id="kant-ab-default",
    )
    observations = tuple(
        Observation(
            observation_id=f"obs-{index + 1}",
            episode_id="episode-1",
            position=index,
            source="strip-camera",
            content=(
                ContentField(name="color", value="amber"),
                ContentField(name="x", value=0),
            ),
            quality=ObservationQuality.COMPLETE,
        )
        for index in range(2)
    )
    presented_elements = tuple(
        PresentedElement(
            presented_element_id=f"pe-{index + 1}",
            observation_id=item.observation_id,
            episode_id=item.episode_id,
            position=item.position,
            source=item.source,
            content=item.content,
            derivation=derivation(
                "shared reception",
                (ground(item.observation_id, GroundKind.OBSERVATION),),
                scope,
                configuration,
            ),
        )
        for index, item in enumerate(observations)
    )
    temporal_form = Form(
        form_id="time-total",
        kind=FormKind.TEMPORAL,
        description="total order within the episode",
    )
    projection = VariantProjection(
        projection_id="projection-kant-ab",
        variant_id=configuration.variant_id,
        name="Kantian sensible projection",
        representation_kind="intuition",
        required_forms=(temporal_form,),
        conditions=("singular", "preconceptual", "temporal-order"),
        procedure=FieldProjection(fields=("color", "x")),
    )
    intuitions = tuple(
        Intuition(
            intuition_id=f"intuition-{index + 1}",
            presented_element_id=item.presented_element_id,
            projection_id=projection.projection_id,
            episode_id=item.episode_id,
            position=item.position,
            content=item.content,
            form_ids=(temporal_form.form_id,),
            derivation=derivation(
                "Kantian variant projection",
                (
                    ground(item.presented_element_id, GroundKind.PRESENTED_ELEMENT),
                    ground("projection-kant-ab", GroundKind.VARIANT_PROJECTION),
                ),
                scope,
                configuration,
            ),
        )
        for index, item in enumerate(presented_elements)
    )
    intuition_ids = tuple(item.intuition_id for item in intuitions)
    sensible_evidence = tuple(
        ground(item, GroundKind.INTUITION) for item in intuition_ids
    )
    manifold = ManifoldOfIntuition(
        manifold_id="manifold-1",
        episode_id="episode-1",
        intuition_ids=intuition_ids,
        form_ids=(temporal_form.form_id,),
        derivation=derivation(
            "manifold formation",
            sensible_evidence,
            scope,
            configuration,
        ),
    )
    retained = RetainedSequence(
        retained_sequence_id="retained-1",
        manifold_id=manifold.manifold_id,
        items=tuple(
            RetainedIntuition(
                intuition_id=item,
                status=RetentionStatus.CURRENT,
            )
            for item in intuition_ids
        ),
        derivation=derivation(
            "apprehension",
            (ground("manifold-1", GroundKind.MANIFOLD),),
            scope,
            configuration,
        ),
    )
    identity_ground = ground("I-1", GroundKind.RULE, RuleAuthority.CONSTITUTIVE)
    unity_rule_ground = ground("U-1", GroundKind.RULE, RuleAuthority.CONSTITUTIVE)
    candidate = CandidateRepresentation(
        candidate_representation_id="candidate-1",
        retained_sequence_id=retained.retained_sequence_id,
        intuition_ids=intuition_ids,
        policy=SynthesisPolicy.A_ANALYSIS_B_CONSTRAINT,
        identity_rule_ids=(identity_ground.ground_id,),
        constitutive_rule_ids=(unity_rule_ground.ground_id,),
        derivation=derivation(
            "recognition and synthesis",
            (
                ground("retained-1", GroundKind.RETAINED_SEQUENCE),
                identity_ground,
                unity_rule_ground,
            ),
            scope,
            configuration,
        ),
    )
    identity_result = ConditionResult(
        condition_id="identity-passes",
        required=True,
        status=ConditionStatus.SATISFIED,
        explanation="identity is preserved in the bounded sequence",
        evidence=sensible_evidence,
    )
    constitutive_result = ConditionResult(
        condition_id="local-unity-passes",
        required=True,
        status=ConditionStatus.SATISFIED,
        explanation="the candidate uses one compatible branch",
        evidence=sensible_evidence,
    )
    object_candidate = ObjectCandidate(
        object_candidate_id="object-1",
        candidate_representation_id=candidate.candidate_representation_id,
        identity_results=(identity_result,),
        constitutive_results=(constitutive_result,),
        derivation=derivation(
            "object formation",
            (
                ground(
                    "candidate-1",
                    GroundKind.CANDIDATE_REPRESENTATION,
                ),
            ),
            scope,
            configuration,
        ),
    )
    color_condition = Condition(
        condition_id="amber-content",
        description="the formed content carries the color amber",
        required=True,
        authority=RuleAuthority.CONSTITUTIVE,
    )
    concept = Concept(
        concept_id="amber-colored",
        name="amber colored",
        kind=ConceptKind.EMPIRICAL,
        applicability_conditions=(color_condition,),
        inferential_consequences=("the represented color is amber",),
        scope=scope,
        authority=RuleAuthority.CONSTITUTIVE,
    )
    schema = Schema(
        schema_id="S-amber",
        concept_id=concept.concept_id,
        name="amber-content schema",
        procedure=SensibleProcedure(
            checks=(
                FieldEquals(
                    condition_id="amber-content", field="color", expected="amber"
                ),
            ),
        ),
        condition_ids=(color_condition.condition_id,),
        sensible_form_ids=(temporal_form.form_id,),
        scope=scope,
        authority=RuleAuthority.CONSTITUTIVE,
    )
    application_condition = ConditionResult(
        condition_id=color_condition.condition_id,
        required=True,
        status=ConditionStatus.SATISFIED,
        explanation="the inspected formed content carries amber",
        evidence=sensible_evidence,
    )
    application = ApplicationResult(
        application_result_id="application-1",
        object_candidate_id=object_candidate.object_candidate_id,
        concept_id=concept.concept_id,
        schema_id=schema.schema_id,
        status=ApplicationStatus.APPLICABLE,
        condition_results=(application_condition,),
        derivation=derivation(
            "schema-mediated concept application",
            (
                ground("object-1", GroundKind.OBJECT_CANDIDATE),
                ground("amber-colored", GroundKind.CONCEPT),
                ground("S-amber", GroundKind.SCHEMA),
            ),
            scope,
            configuration,
        ),
    )
    warrant = AssembledWarrant(
        observation_grounds=tuple(
            ground(item.observation_id, GroundKind.OBSERVATION) for item in observations
        ),
        presentation_form_ids=(temporal_form.form_id,),
        projection_grounds=(
            ground("projection-kant-ab", GroundKind.VARIANT_PROJECTION),
        ),
        synthesis_grounds=(
            ground("manifold-1", GroundKind.MANIFOLD),
            ground("retained-1", GroundKind.RETAINED_SEQUENCE),
            ground("candidate-1", GroundKind.CANDIDATE_REPRESENTATION),
            ground("object-1", GroundKind.OBJECT_CANDIDATE),
        ),
        identity_rule_grounds=(identity_ground,),
        concept_ground=ground("amber-colored", GroundKind.CONCEPT),
        schema_ground=ground("S-amber", GroundKind.SCHEMA),
        application_ground=ground("application-1", GroundKind.APPLICATION_RESULT),
        constitutive_rule_grounds=(unity_rule_ground,),
        scope=scope,
        configuration=configuration,
    )
    proposition = Proposition(
        subject_candidate_id=object_candidate.object_candidate_id,
        predicate_concept_id=concept.concept_id,
        text="The presented marker is amber in episode 1.",
        modality=Modality.ASSERTORIC,
    )
    proposal = ProposedJudgment(
        proposed_judgment_id="proposal-1",
        proposition=proposition,
        warrant=warrant,
        derivation=derivation(
            "judgment proposal",
            (
                ground("object-1", GroundKind.OBJECT_CANDIDATE),
                ground("application-1", GroundKind.APPLICATION_RESULT),
            ),
            scope,
            configuration,
        ),
    )
    unity_condition = ConditionResult(
        condition_id="cycle-wide-unity",
        required=True,
        status=ConditionStatus.SATISFIED,
        explanation="all grounds share one branch, scope, and configuration",
        evidence=(ground("proposal-1", GroundKind.JUDGMENT),),
    )
    unity_check = UnityCheck(
        unity_check_id="unity-check-1",
        status=ConditionStatus.SATISFIED,
        condition_results=(unity_condition,),
        scope=scope,
        configuration=configuration,
    )
    limit_report = LimitReport(
        limit_report_id="limit-committed-1",
        strongest_licensed=OutcomeKind.JUDGMENT_COMMITTED,
        scope=scope,
        boundary="no claim beyond the supplied episode",
    )
    complete_warrant = CompleteWarrant(
        assembled=warrant,
        unity_check=unity_check,
        limit_report_id=limit_report.limit_report_id,
    )
    judgment = CommittedJudgment(
        judgment_id="judgment-1",
        proposed_judgment_id=proposal.proposed_judgment_id,
        proposition=proposition,
        warrant=complete_warrant,
        derivation=derivation(
            "judgment commitment",
            (ground("proposal-1", GroundKind.JUDGMENT),),
            scope,
            configuration,
        ),
    )
    committed_outcome = JudgmentCommitted(
        outcome_id="outcome-committed-1",
        context=OutcomeContext(
            configuration=configuration,
            derivation=derivation(
                "critique and report",
                (ground("judgment-1", GroundKind.JUDGMENT),),
                scope,
                configuration,
            ),
            limit_report=limit_report,
        ),
        judgment=judgment,
    )

    rules = (
        Rule(
            rule_id="I-1",
            name="bounded identity",
            description="preserve x across the two observed moments only",
            authority=RuleAuthority.CONSTITUTIVE,
            kind=RuleKind.IDENTITY,
            scope=scope,
            conditions=(
                Condition(
                    condition_id="identity-passes",
                    description="x remains stable",
                    required=True,
                    authority=RuleAuthority.CONSTITUTIVE,
                ),
            ),
            sensible_procedure=SensibleProcedure(
                temporal_form_id="time-total",
                checks=(FieldConstant(condition_id="identity-passes", field="x"),),
            ),
        ),
        Rule(
            rule_id="U-1",
            name="temporal unity",
            description="one temporally ordered bounded candidate",
            authority=RuleAuthority.CONSTITUTIVE,
            kind=RuleKind.CATEGORY_INSPIRED,
            scope=scope,
            conditions=(
                Condition(
                    condition_id="local-unity-passes",
                    description="ordered sensible sequence",
                    required=True,
                    authority=RuleAuthority.CONSTITUTIVE,
                ),
            ),
            sensible_procedure=SensibleProcedure(
                temporal_form_id="time-total",
                checks=(TemporalOrder(condition_id="local-unity-passes"),),
            ),
        ),
    )
    return SimpleNamespace(
        rules=rules,
        scope=scope,
        configuration=configuration,
        observations=observations,
        presented_elements=presented_elements,
        intuitions=intuitions,
        observation=observations[0],
        presented=presented_elements[0],
        projection=projection,
        intuition=intuitions[0],
        manifold=manifold,
        retained=retained,
        candidate=candidate,
        object_candidate=object_candidate,
        concept=concept,
        schema=schema,
        application=application,
        warrant=warrant,
        proposition=proposition,
        proposal=proposal,
        unity_check=unity_check,
        limit_report=limit_report,
        judgment=judgment,
        committed_outcome=committed_outcome,
    )


@pytest.fixture
def successful_trace() -> SimpleNamespace:
    return make_successful_trace()


@pytest.fixture
def complete_trace(successful_trace: SimpleNamespace) -> ProvenanceTrace:
    """Register all resources of the hand-authored, replayable committed trace."""

    t = successful_trace
    return ProvenanceTrace(
        cycle_id="cycle-1",
        scope=t.scope,
        configuration=t.configuration,
        observations=t.observations,
        forms=t.projection.required_forms,
        projections=(t.projection,),
        rules=t.rules,
        concepts=(t.concept,),
        schemas=(t.schema,),
        presented_elements=t.presented_elements,
        intuitions=t.intuitions,
        manifolds=(t.manifold,),
        retained_sequences=(t.retained,),
        candidates=(t.candidate,),
        object_candidates=(t.object_candidate,),
        applications=(t.application,),
        proposals=(t.proposal,),
        unity_checks=(t.unity_check,),
        judgments=(t.judgment,),
        limit_reports=(t.limit_report,),
        outcomes=(t.committed_outcome,),
    )
