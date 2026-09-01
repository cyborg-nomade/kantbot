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
    Condition,
    ConditionResult,
    ConditionStatus,
    ConfigurationIdentity,
    ContentField,
    Derivation,
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
    RuleAuthority,
    Schema,
    Scope,
    SynthesisPolicy,
    UnityCheck,
    VariantProjection,
)


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


@pytest.fixture
def successful_trace() -> SimpleNamespace:
    """One compact committed trace, used as values rather than an execution."""

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
    observation = Observation(
        observation_id="obs-1",
        episode_id="episode-1",
        position=0,
        source="strip-camera",
        content=(
            ContentField(name="color", value="amber"),
            ContentField(name="x", value=0),
        ),
        quality=ObservationQuality.COMPLETE,
    )
    presented = PresentedElement(
        presented_element_id="pe-1",
        observation_id=observation.observation_id,
        episode_id=observation.episode_id,
        position=observation.position,
        source=observation.source,
        content=observation.content,
        derivation=derivation(
            "shared reception",
            (ground("obs-1", GroundKind.OBSERVATION),),
            scope,
            configuration,
        ),
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
        conditions=("singular", "preconceptual"),
    )
    intuition = Intuition(
        intuition_id="intuition-1",
        presented_element_id=presented.presented_element_id,
        projection_id=projection.projection_id,
        episode_id=presented.episode_id,
        position=presented.position,
        content=presented.content,
        form_ids=(temporal_form.form_id,),
        derivation=derivation(
            "Kantian variant projection",
            (
                ground("pe-1", GroundKind.PRESENTED_ELEMENT),
                ground("projection-kant-ab", GroundKind.VARIANT_PROJECTION),
            ),
            scope,
            configuration,
        ),
    )
    manifold = ManifoldOfIntuition(
        manifold_id="manifold-1",
        episode_id="episode-1",
        intuition_ids=(intuition.intuition_id,),
        form_ids=(temporal_form.form_id,),
        derivation=derivation(
            "manifold formation",
            (ground("intuition-1", GroundKind.INTUITION),),
            scope,
            configuration,
        ),
    )
    retained = RetainedSequence(
        retained_sequence_id="retained-1",
        manifold_id=manifold.manifold_id,
        items=(
            RetainedIntuition(
                intuition_id=intuition.intuition_id,
                status=RetentionStatus.CURRENT,
            ),
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
        intuition_ids=(intuition.intuition_id,),
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
        evidence=(ground("intuition-1", GroundKind.INTUITION),),
    )
    constitutive_result = ConditionResult(
        condition_id="local-unity-passes",
        required=True,
        status=ConditionStatus.SATISFIED,
        explanation="the candidate uses one compatible branch",
        evidence=(ground("candidate-1", GroundKind.CANDIDATE_REPRESENTATION),),
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
        applicability_conditions=(color_condition,),
        inferential_consequences=("the represented color is amber",),
        scope=scope,
        authority=RuleAuthority.CONSTITUTIVE,
    )
    schema = Schema(
        schema_id="S-amber",
        concept_id=concept.concept_id,
        name="amber-content schema",
        procedure="inspect the color carried by the formed particular",
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
        evidence=(ground("object-1", GroundKind.OBJECT_CANDIDATE),),
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
        observation_grounds=(ground("obs-1", GroundKind.OBSERVATION),),
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

    return SimpleNamespace(
        scope=scope,
        configuration=configuration,
        observation=observation,
        presented=presented,
        projection=projection,
        intuition=intuition,
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
