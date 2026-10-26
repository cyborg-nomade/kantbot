"""Policy replacement must preserve the accepted cognitive licensing boundaries."""

from dataclasses import replace

import pytest
from pydantic import ValidationError

from kantbot.cycle import AmbiguityPolicy, CyclePolicies, run_cycle, strip_plan
from kantbot.cycle._support import derive, ground, outcome_context
from kantbot.cycle.judgment import propose_judgment
from kantbot.cycle.reception import project_intuition
from kantbot.cycle.synthesis import EnumerateCandidates, retain_episode
from kantbot.cycle.unity import ancestry, check_unity
from kantbot.interfaces import (
    ProjectionRequest,
    ProjectionResult,
    ProposalRequest,
    ProposalResult,
    ProvenanceView,
    RecognitionRequest,
    RecognitionResult,
    RetentionRequest,
    RetentionResult,
    UnityRequest,
    UnityResult,
)
from kantbot.model import (
    AssembledWarrant,
    CognitiveGround,
    Condition,
    ConditionResult,
    ConditionStatus,
    ContentField,
    FieldEquals,
    GroundKind,
    Modality,
    Observation,
    OutcomeKind,
    ProposedJudgment,
    Proposition,
    RetainedIntuition,
    RetainedSequence,
    RetentionStatus,
    Rule,
    RuleAuthority,
    SemanticModel,
    SensibleProcedure,
    SynthesisPolicy,
    UnityCheck,
    UnityConflict,
)
from kantbot.provenance import ProvenanceGraph
from kantbot.transitions import InvalidTransition
from kantbot.worlds import load_scenario, observe_world


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def _observations(name: str = "rightward") -> tuple[Observation, ...]:
    return observe_world(load_scenario(name)).observations


def test_reserved_regulative_guidance_cannot_change_a_present_judgment() -> None:
    plan = strip_plan("strip-demo")
    preference = Rule(
        rule_id="Q-1",
        name="look for persistent patches",
        description="Reserved future inquiry preference",
        authority=RuleAuthority.REGULATIVE,
        scope=plan.context.scope,
    )
    reserved = _change(plan, reserved_rules=(preference,))
    control = run_cycle(_observations(), plan)
    contrast = run_cycle(_observations(), reserved)
    assert control.outcomes == contrast.outcomes
    assert control.trace.judgments == contrast.trace.judgments
    assert control.trace.applications == contrast.trace.applications


def test_illicit_regulative_promotion_produces_overreach() -> None:
    plan = strip_plan("strip-demo")
    preference = Rule(
        rule_id="Q-1",
        name="prefer persistence",
        description="Reserved inquiry guidance",
        authority=RuleAuthority.REGULATIVE,
        scope=plan.context.scope,
    )
    plan = _change(plan, reserved_rules=(preference,))

    def promoted(request: ProposalRequest, /) -> ProposalResult:
        proposal = propose_judgment(request)
        assert isinstance(proposal, ProposedJudgment)
        illicit = CognitiveGround(
            ground_id="Q-1", kind=GroundKind.RULE, authority=RuleAuthority.REGULATIVE
        )
        return _change(
            proposal,
            derivation=_change(
                proposal.derivation, grounds=(*proposal.derivation.grounds, illicit)
            ),
        )

    result = run_cycle(_observations(), plan, policies=CyclePolicies(propose=promoted))
    assert result.outcomes[0].kind is OutcomeKind.OVERREACH
    assert (
        result.outcomes[0].context.limit_report.authority_violations[0].source_id
        == "Q-1"
    )
    assert not result.trace.judgments
    assert result.trace.applications[0].applicable


def test_a_replacement_unity_policy_cannot_bypass_the_common_modality_check() -> None:
    def apodictic(request: ProposalRequest, /) -> ProposalResult:
        return propose_judgment(
            _change(
                request,
                proposition=_change(request.proposition, modality=Modality.APODICTIC),
            )
        )

    def accept_without_checks(
        request: UnityRequest, provenance: ProvenanceView, /
    ) -> UnityResult:
        pytest.fail("A failing mandatory unity check must prevent policy approval")

    result = run_cycle(
        _observations(),
        strip_plan("strip-demo"),
        policies=CyclePolicies(propose=apodictic, unity=accept_without_checks),
    )
    assert result.outcomes[0].kind is OutcomeKind.UNITY_CONFLICT
    assert not result.trace.judgments


def test_a_replacement_unity_policy_can_add_a_named_constraint() -> None:
    def additional(request: UnityRequest, provenance: ProvenanceView, /) -> UnityResult:
        default = check_unity(request, provenance)
        assert isinstance(default, UnityCheck)
        condition = ConditionResult(
            condition_id="additional-policy-check",
            required=True,
            status=ConditionStatus.SATISFIED,
            explanation="Declared experimental policy also permits this commitment",
            evidence=default.condition_results[0].evidence,
        )
        return _change(default, condition_results=(condition,))

    result = run_cycle(
        _observations(),
        strip_plan("strip-demo"),
        policies=CyclePolicies(unity=additional),
    )
    assert result.outcomes[0].kind is OutcomeKind.JUDGMENT_COMMITTED
    assert tuple(
        item.condition_id for item in result.trace.unity_checks[0].condition_results
    ) == ("cycle-wide-unity", "additional-policy-check")


def test_a_replacement_unity_policy_can_withhold_a_normally_admissible_commitment() -> (
    None
):
    def stricter(request: UnityRequest, provenance: ProvenanceView, /) -> UnityResult:
        label = "additional-unity-conflict"
        context = outcome_context(
            request.context,
            OutcomeKind.UNITY_CONFLICT,
            label,
            (ground(request.proposal.proposed_judgment_id, GroundKind.JUDGMENT),),
        )
        context = _change(
            context, limit_report=_change(context.limit_report, conflict_ids=(label,))
        )
        return UnityConflict(
            outcome_id=f"outcome:{label}",
            proposed_judgment_id=request.proposal.proposed_judgment_id,
            conflict_ids=(label,),
            context=context,
        )

    result = run_cycle(
        _observations(),
        strip_plan("strip-demo"),
        policies=CyclePolicies(unity=stricter),
    )
    assert result.outcomes[0].kind is OutcomeKind.UNITY_CONFLICT
    assert result.trace.applications[0].applicable
    assert not result.trace.judgments


def test_earlier_samples_cannot_be_laundered_as_current_data() -> None:
    def unlicensed(request: RetentionRequest, /) -> RetentionResult:
        retained = retain_episode(request)
        assert isinstance(retained, RetainedSequence)
        items = tuple(
            RetainedIntuition(
                intuition_id=item.intuition_id, status=RetentionStatus.CURRENT
            )
            for item in retained.items
        )
        return _change(retained, items=items)

    with pytest.raises(InvalidTransition, match="explicitly reproduced"):
        run_cycle(
            _observations(),
            strip_plan("strip-demo"),
            policies=CyclePolicies(retain=unlicensed),
        )


def test_merging_locally_licensed_rivals_fails_cycle_wide_unity() -> None:
    plan = strip_plan("strip-demo", ambiguity_policy=AmbiguityPolicy.CONTINUE)
    computed = run_cycle(_observations("ambiguous-middle"), plan)
    trace = _change(computed.trace, limit_reports=(), outcomes=())
    graph = ProvenanceGraph(trace)
    application = trace.applications[0]
    lineage = ancestry(
        ground(application.application_result_id, GroundKind.APPLICATION_RESULT), graph
    )

    def of_kind(*kinds: GroundKind) -> tuple[CognitiveGround, ...]:
        return tuple(item for item in lineage if item.kind in kinds)

    # The adversarial proposal, unlike its computed object/application inputs,
    # intentionally adds the rival candidate to one singular subject's warrant.
    rival = ground(
        trace.candidates[1].candidate_representation_id,
        GroundKind.CANDIDATE_REPRESENTATION,
    )
    identity = CognitiveGround(
        ground_id="I-1", kind=GroundKind.RULE, authority=RuleAuthority.CONSTITUTIVE
    )
    unity = CognitiveGround(
        ground_id="U-1", kind=GroundKind.RULE, authority=RuleAuthority.CONSTITUTIVE
    )
    warrant = AssembledWarrant(
        observation_grounds=of_kind(GroundKind.OBSERVATION),
        presentation_form_ids=("strip-time", "strip-space"),
        projection_grounds=of_kind(GroundKind.VARIANT_PROJECTION),
        synthesis_grounds=(
            *of_kind(
                GroundKind.MANIFOLD,
                GroundKind.RETAINED_SEQUENCE,
                GroundKind.CANDIDATE_REPRESENTATION,
                GroundKind.OBJECT_CANDIDATE,
            ),
            rival,
        ),
        identity_rule_grounds=(identity,),
        constitutive_rule_grounds=(unity,),
        concept_ground=ground(application.concept_id, GroundKind.CONCEPT),
        schema_ground=ground(application.schema_id, GroundKind.SCHEMA),
        application_ground=ground(
            application.application_result_id, GroundKind.APPLICATION_RESULT
        ),
        scope=plan.context.scope,
        configuration=plan.context.configuration,
    )
    proposal = ProposedJudgment(
        proposed_judgment_id="adversarial-proposal",
        proposition=Proposition(
            subject_candidate_id=application.object_candidate_id,
            predicate_concept_id=application.concept_id,
            text="Both rival paths belong to one selected subject",
            modality=Modality.ASSERTORIC,
        ),
        warrant=warrant,
        derivation=derive(
            plan.context,
            "adversarial merge",
            (
                ground(application.object_candidate_id, GroundKind.OBJECT_CANDIDATE),
                ground(
                    application.application_result_id, GroundKind.APPLICATION_RESULT
                ),
            ),
        ),
    )
    graph = ProvenanceGraph(_change(trace, proposals=(proposal,)))
    result = check_unity(UnityRequest(proposal=proposal, context=plan.context), graph)
    assert isinstance(result, UnityConflict)
    assert "incompatible-identity-branches" in result.conflict_ids
    assert all(item.applicable for item in trace.applications)


@pytest.mark.parametrize(
    "field",
    [
        "identity_rule_ids",
        "constitutive_rule_ids",
        "retention_rule_id",
        "concept_id",
        "schema_id",
    ],
)
def test_the_plan_rejects_unavailable_selected_resources(field: str) -> None:
    plan = strip_plan("strip-demo")
    value = ("missing",) if field.endswith("_ids") else "missing"
    with pytest.raises(ValidationError):
        _change(plan, **{field: value})


def test_the_plan_does_not_accept_scope_or_variant_aliasing() -> None:
    plan = strip_plan("strip-demo")
    with pytest.raises(ValidationError, match="frozen context"):
        _change(plan, projection=_change(plan.projection, variant_id="another-variant"))
    with pytest.raises(ValidationError, match="registered exactly"):
        _change(
            plan,
            forms=(_change(plan.forms[0], description="another form"), plan.forms[1]),
        )
    with pytest.raises(ValidationError, match="object license"):
        _change(plan, retention_rule_id="I-1")


def test_reserved_rules_cannot_smuggle_a_second_constitutive_repertoire() -> None:
    plan = strip_plan("strip-demo")
    with pytest.raises(ValidationError):
        _change(plan, reserved_rules=(plan.repertoire.rules[0],))
    duplicate = _change(plan.repertoire.rules[0], rule_id="other-retention")
    with pytest.raises(ValidationError, match="non-constitutive"):
        _change(plan, reserved_rules=(duplicate,))


def test_a_recognition_policy_cannot_silently_select_a_preferred_rival() -> None:
    def greedy(
        request: RecognitionRequest, provenance: ProvenanceView, /
    ) -> RecognitionResult:
        result = EnumerateCandidates()(request, provenance)
        assert isinstance(result, tuple)
        return result[:1]

    with pytest.raises(InvalidTransition, match="admissible identity paths"):
        run_cycle(
            _observations("ambiguous-middle"),
            strip_plan("strip-demo"),
            policies=CyclePolicies(recognize=greedy),
        )


def test_a_recognition_policy_cannot_change_its_declared_interpretation() -> None:
    def renamed(
        request: RecognitionRequest, provenance: ProvenanceView, /
    ) -> RecognitionResult:
        result = EnumerateCandidates()(request, provenance)
        assert isinstance(result, tuple)
        return tuple(
            _change(item, policy=SynthesisPolicy.B_LED_FIGURATIVE) for item in result
        )

    with pytest.raises(InvalidTransition, match="selected interpretation"):
        run_cycle(
            _observations(),
            strip_plan("strip-demo"),
            policies=CyclePolicies(recognize=renamed),
        )


def test_a_fused_variant_does_not_silently_ignore_a_separate_recognition_override() -> (
    None
):
    plan = strip_plan("strip-demo", synthesis_policy=SynthesisPolicy.B_LED_FIGURATIVE)
    with pytest.raises(ValueError, match="figurative policy"):
        run_cycle(
            _observations(),
            plan,
            policies=CyclePolicies(recognize=EnumerateCandidates()),
        )


def test_one_applicable_branch_does_not_resolve_a_subject_ambiguity() -> None:
    observations = list(_observations("ambiguous-middle"))
    xs = (0, 0, 1, 2)
    observations = [
        _change(
            item,
            content=(
                ContentField(name="color", value="amber"),
                ContentField(name="x", value=x),
            ),
        )
        for item, x in zip(observations, xs, strict=True)
    ]
    result = run_cycle(
        tuple(observations),
        strip_plan("strip-demo", ambiguity_policy=AmbiguityPolicy.CONTINUE),
    )
    assert tuple(item.kind for item in result.outcomes) == (
        OutcomeKind.CONCEPT_NOT_APPLICABLE,
        OutcomeKind.JUDGMENT_WITHHELD,
    )
    assert all(item.alternative_application_ids for item in result.trace.applications)
    assert not result.trace.judgments


def test_an_absent_presented_predicate_remains_underdetermined() -> None:
    plan = strip_plan("strip-demo")
    condition = Condition(
        condition_id="calibration-present",
        description="A calibration label is presented",
        required=True,
        authority=RuleAuthority.CONSTITUTIVE,
    )
    concept = _change(
        plan.repertoire.concepts[0],
        concept_id="calibration-target",
        name="calibration target",
        applicability_conditions=(condition,),
    )
    schema = _change(
        plan.repertoire.schemas[0],
        schema_id="S-calibration",
        concept_id=concept.concept_id,
        condition_ids=(condition.condition_id,),
        procedure=SensibleProcedure(
            checks=(
                FieldEquals(
                    condition_id=condition.condition_id,
                    field="calibration-label",
                    expected=True,
                ),
            )
        ),
    )
    repertoire = _change(
        plan.repertoire,
        concepts=(*plan.repertoire.concepts, concept),
        schemas=(*plan.repertoire.schemas, schema),
    )
    plan = _change(
        plan,
        repertoire=repertoire,
        concept_id=concept.concept_id,
        schema_id=schema.schema_id,
    )
    result = run_cycle(_observations(), plan)
    assert result.outcomes[0].kind is OutcomeKind.APPLICATION_UNDERDETERMINED
    assert result.trace.object_candidates
    assert not result.trace.judgments


def test_execution_paths_cannot_be_detached_from_the_certified_outcomes() -> None:
    plan = strip_plan("strip-demo")
    first = run_cycle(_observations(), plan)
    second = run_cycle(_observations("stationary"), plan)
    with pytest.raises(ValueError, match="certified outcomes"):
        replace(first, terminal_states=second.terminal_states)


def test_a_replacement_projection_cannot_invent_episode_form_availability() -> None:
    def invented(request: ProjectionRequest, /) -> ProjectionResult:
        return project_intuition(_change(request, available_form_ids=None))

    plan = strip_plan("strip-demo", available_form_ids=("strip-space",))
    with pytest.raises(InvalidTransition, match="unavailable to this episode"):
        run_cycle(_observations(), plan, policies=CyclePolicies(project=invented))


def test_available_form_ids_are_declared_resources() -> None:
    with pytest.raises(ValidationError, match="available forms"):
        strip_plan("strip-demo", available_form_ids=("invented-time",))


def test_retention_cannot_hide_a_current_rival() -> None:
    def preferred_current(request: RetentionRequest, /) -> RetentionResult:
        retained = retain_episode(request)
        assert isinstance(retained, RetainedSequence)
        return _change(retained, items=retained.items[:-1])

    observations = _observations("ambiguous-middle")[:3]
    with pytest.raises(InvalidTransition, match="every current presentation"):
        run_cycle(
            observations,
            strip_plan("strip-demo"),
            policies=CyclePolicies(retain=preferred_current),
        )
