"""Closed graph identities, evidence, alternatives, and wire boundaries."""

from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from kantbot.interfaces import ProvenanceView
from kantbot.model import (
    ApplicationStatus,
    ApplicationUnderdetermined,
    AuthorityViolation,
    CognitiveGround,
    ConceptNotApplicable,
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
    RetainedIntuition,
    RetentionStatus,
    Rule,
    RuleAuthority,
    SemanticModel,
    SynthesisAmbiguous,
    SynthesisFailed,
    UnityConflict,
)
from kantbot.provenance import (
    ExternalInputReference,
    InvalidProvenance,
    ProvenanceGraph,
    ProvenanceTrace,
    dump_provenance,
    validate_provenance,
    validate_provenance_json,
)


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    """Construct locally validated adversarial values, without validation bypass."""

    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def _ground(entity_id: str, kind: GroundKind) -> CognitiveGround:
    return CognitiveGround(ground_id=entity_id, kind=kind)


@pytest.fixture
def complete_trace(successful_trace: SimpleNamespace) -> ProvenanceTrace:
    """Register every referenced resource and every canonical transformation."""

    t = successful_trace
    rules = tuple(
        Rule(
            rule_id=rule_id,
            name=rule_id,
            description="declared experiment rule",
            authority=RuleAuthority.CONSTITUTIVE,
            scope=t.scope,
        )
        for rule_id in ("I-1", "U-1")
    )
    return ProvenanceTrace(
        cycle_id="cycle-1",
        scope=t.scope,
        configuration=t.configuration,
        observations=(t.observation,),
        forms=t.projection.required_forms,
        projections=(t.projection,),
        rules=rules,
        concepts=(t.concept,),
        schemas=(t.schema,),
        presented_elements=(t.presented,),
        intuitions=(t.intuition,),
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


def _prefix(trace: ProvenanceTrace) -> ProvenanceTrace:
    return _change(
        trace,
        proposals=(),
        unity_checks=(),
        judgments=(),
        outcomes=(),
        limit_reports=(),
    )


def test_complete_trace_round_trips_and_supplies_read_only_view(
    complete_trace: ProvenanceTrace,
) -> None:
    graph = ProvenanceGraph(complete_trace)
    view: ProvenanceView = graph
    assert view.resolves(_ground("obs-1", GroundKind.OBSERVATION))
    assert not view.resolves(_ground("obs-1", GroundKind.INTUITION))
    assert not view.resolves(_ground("absent", GroundKind.OBSERVATION))
    assert view.scope_for("application-1") == complete_trace.scope
    assert view.configuration_for("obs-1") == complete_trace.configuration
    assert _ground("object-1", GroundKind.OBJECT_CANDIDATE) in view.immediate_grounds(
        "application-1"
    )
    assert view.immediate_grounds("obs-1") == ()
    assert validate_provenance(complete_trace.model_dump(mode="python")) == graph
    encoded = dump_provenance(graph)
    assert dump_provenance(validate_provenance_json(encoded)) == encoded
    with pytest.raises(FrozenInstanceError):
        graph.trace = complete_trace
    with pytest.raises(ValidationError, match="frozen"):
        graph.trace.observations = ()


def test_closed_prefix_does_not_require_an_outcome(
    complete_trace: ProvenanceTrace,
) -> None:
    graph = ProvenanceGraph(_prefix(complete_trace))
    assert graph.trace.outcomes == ()
    assert graph.resolves(_ground("application-1", GroundKind.APPLICATION_RESULT))


def test_removing_a_referenced_observation_is_rejected(
    complete_trace: ProvenanceTrace,
) -> None:
    broken = _change(complete_trace, observations=())
    with pytest.raises(InvalidProvenance, match="obs-1"):
        ProvenanceGraph(broken)


def test_duplicate_registration_and_evaluator_id_collision_are_rejected(
    complete_trace: ProvenanceTrace,
) -> None:
    duplicate = _change(complete_trace, observations=complete_trace.observations * 2)
    with pytest.raises(InvalidProvenance, match="duplicate identity"):
        ProvenanceGraph(duplicate)
    hidden = EvaluatorReference(
        evaluator_reference_id="obs-1", description="hidden identity"
    )
    with pytest.raises(InvalidProvenance, match="duplicate identity"):
        ProvenanceGraph(_change(complete_trace, evaluator_references=(hidden,)))


def test_evaluator_reference_cannot_resolve_or_hide_in_condition_evidence(
    complete_trace: ProvenanceTrace,
) -> None:
    hidden = EvaluatorReference(
        evaluator_reference_id="hidden-1", description="hidden identity"
    )
    trace = _change(complete_trace, evaluator_references=(hidden,))
    graph = ProvenanceGraph(trace)
    assert not graph.resolves(_ground("hidden-1", GroundKind.OBSERVATION))
    for lookup in (graph.immediate_grounds, graph.scope_for, graph.configuration_for):
        with pytest.raises(KeyError, match="no cognitive entity"):
            lookup("hidden-1")
    application = trace.applications[0]
    condition = _change(
        application.condition_results[0],
        evidence=(_ground("hidden-1", GroundKind.OBSERVATION),),
    )
    poisoned = _change(application, condition_results=(condition,))
    with pytest.raises(InvalidProvenance, match="hidden-1"):
        ProvenanceGraph(_change(trace, applications=(poisoned,)))


def test_rule_authority_must_match_the_registered_rule(
    complete_trace: ProvenanceTrace,
) -> None:
    rule = _change(complete_trace.rules[0], authority=RuleAuthority.REGULATIVE)
    with pytest.raises(InvalidProvenance, match="unauthorized ground"):
        ProvenanceGraph(_change(complete_trace, rules=(rule, complete_trace.rules[1])))


def test_embedded_unity_copy_cannot_redefine_registered_identity(
    complete_trace: ProvenanceTrace,
) -> None:
    unity = complete_trace.unity_checks[0]
    condition = _change(unity.condition_results[0], explanation="different definition")
    replacement = _change(unity, condition_results=(condition,))
    with pytest.raises(InvalidProvenance, match="incompatible embedded entity"):
        ProvenanceGraph(_change(complete_trace, unity_checks=(replacement,)))


def test_direct_retained_ids_are_evidence_edges(
    complete_trace: ProvenanceTrace,
) -> None:
    retained = complete_trace.retained_sequences[0]
    foreign = RetainedIntuition(
        intuition_id="missing-intuition", status=RetentionStatus.CURRENT
    )
    with pytest.raises(InvalidProvenance, match="missing-intuition"):
        ProvenanceGraph(
            _change(
                complete_trace,
                retained_sequences=(_change(retained, items=(foreign,)),),
            )
        )


def test_circular_evidence_is_rejected_even_when_nodes_validate(
    complete_trace: ProvenanceTrace,
) -> None:
    intuition = complete_trace.intuitions[0]
    circular = _change(
        intuition.derivation,
        grounds=(
            *intuition.derivation.grounds,
            _ground("application-1", GroundKind.APPLICATION_RESULT),
        ),
    )
    with pytest.raises(InvalidProvenance, match="circular evidence"):
        ProvenanceGraph(
            _change(
                complete_trace, intuitions=(_change(intuition, derivation=circular),)
            )
        )


def _rivals(trace: ProvenanceTrace) -> ProvenanceTrace:
    candidate = trace.candidates[0]
    first = _change(candidate, alternative_candidate_ids=("candidate-rival",))
    second = _change(
        candidate,
        candidate_representation_id="candidate-rival",
        alternative_candidate_ids=(candidate.candidate_representation_id,),
    )
    return _change(trace, candidates=(first, second))


def test_reciprocal_alternatives_are_not_circular_evidence(
    complete_trace: ProvenanceTrace,
) -> None:
    graph = ProvenanceGraph(_rivals(_prefix(complete_trace)))
    assert not any(
        g.ground_id == "candidate-rival" for g in graph.immediate_grounds("candidate-1")
    )
    assert validate_provenance_json(dump_provenance(graph)) == graph


def test_missing_alternatives_are_not_silently_dropped(
    complete_trace: ProvenanceTrace,
) -> None:
    candidate = _change(
        complete_trace.candidates[0], alternative_candidate_ids=("absent-alternative",)
    )
    with pytest.raises(InvalidProvenance, match="missing or non-cognitive alternative"):
        ProvenanceGraph(_change(complete_trace, candidates=(candidate,)))


def test_committed_ancestry_cannot_merge_rivals(
    complete_trace: ProvenanceTrace,
) -> None:
    trace = _rivals(complete_trace)
    application = trace.applications[0]
    derivation = _change(
        application.derivation,
        grounds=(
            *application.derivation.grounds,
            _ground("candidate-rival", GroundKind.CANDIDATE_REPRESENTATION),
        ),
    )
    trace = _change(trace, applications=(_change(application, derivation=derivation),))
    # A defective proposal can be inspected by a future CheckUnity policy.
    ProvenanceGraph(_change(trace, judgments=(), outcomes=()))
    with pytest.raises(InvalidProvenance, match="merges rival"):
        ProvenanceGraph(trace)


def test_nonconstitutive_rule_cannot_enter_committed_ancestry(
    complete_trace: ProvenanceTrace,
) -> None:
    rule = Rule(
        rule_id="Q-1",
        name="inquiry preference",
        description="does not license objects",
        authority=RuleAuthority.REGULATIVE,
        scope=complete_trace.scope,
    )
    application = complete_trace.applications[0]
    reference = CognitiveGround(
        ground_id="Q-1", kind=GroundKind.RULE, authority=RuleAuthority.REGULATIVE
    )
    derivation = _change(
        application.derivation, grounds=(*application.derivation.grounds, reference)
    )
    trace = _change(
        complete_trace,
        rules=(*complete_trace.rules, rule),
        applications=(_change(application, derivation=derivation),),
    )
    with pytest.raises(InvalidProvenance, match="non-constitutive authority"):
        ProvenanceGraph(trace)


def test_foreign_context_and_projection_are_rejected(
    complete_trace: ProvenanceTrace,
) -> None:
    projection = _change(complete_trace.projections[0], variant_id="foreign-variant")
    with pytest.raises(InvalidProvenance, match="another variant"):
        ProvenanceGraph(_change(complete_trace, projections=(projection,)))
    scope = _change(complete_trace.scope, scope_id="foreign-scope")
    with pytest.raises(InvalidProvenance, match="mixed scopes"):
        ProvenanceGraph(
            _change(
                complete_trace,
                rules=(
                    _change(complete_trace.rules[0], scope=scope),
                    complete_trace.rules[1],
                ),
            )
        )


def test_commitment_cannot_change_proposition(complete_trace: ProvenanceTrace) -> None:
    judgment = complete_trace.judgments[0]
    changed = _change(
        judgment, proposition=_change(judgment.proposition, text="A different claim")
    )
    with pytest.raises(InvalidProvenance, match="commitment changed"):
        ProvenanceGraph(_change(complete_trace, judgments=(changed,), outcomes=()))


def test_committed_warrant_must_cover_application_ancestry(
    complete_trace: ProvenanceTrace,
) -> None:
    proposal = complete_trace.proposals[0]
    warrant = _change(
        proposal.warrant,
        synthesis_grounds=(_ground("object-1", GroundKind.OBJECT_CANDIDATE),),
    )
    judgment = complete_trace.judgments[0]
    changed = _change(judgment, warrant=_change(judgment.warrant, assembled=warrant))
    trace = _change(
        complete_trace,
        proposals=(_change(proposal, warrant=warrant),),
        judgments=(changed,),
        outcomes=(),
    )
    with pytest.raises(InvalidProvenance, match="omits required application ancestry"):
        ProvenanceGraph(trace)


def _context(trace: ProvenanceTrace, kind: OutcomeKind) -> OutcomeContext:
    report = LimitReport(
        limit_report_id="limit-test",
        strongest_licensed=kind,
        scope=trace.scope,
        boundary="the declared episode",
        missing_condition_ids=("amber-content",),
        conflict_ids=("branch-conflict",),
        alternative_ids=("candidate-1", "candidate-rival"),
    )
    return OutcomeContext(
        configuration=trace.configuration,
        limit_report=report,
        derivation=Derivation(
            operation="report test outcome",
            grounds=(_ground("retained-1", GroundKind.RETAINED_SEQUENCE),),
            scope=trace.scope,
            configuration=trace.configuration,
        ),
    )


@pytest.mark.parametrize("kind", list(OutcomeKind))
def test_every_terminal_kind_can_be_stored_with_closed_references(
    complete_trace: ProvenanceTrace, kind: OutcomeKind
) -> None:
    if kind is OutcomeKind.JUDGMENT_COMMITTED:
        graph = ProvenanceGraph(complete_trace)
        assert validate_provenance_json(dump_provenance(graph)) == graph
        return
    trace = _rivals(
        _change(complete_trace, judgments=(), outcomes=(), limit_reports=())
    )
    context = _context(trace, kind)
    common = {"outcome_id": "outcome-test", "context": context}
    outcomes = {
        OutcomeKind.INPUT_ERROR: lambda: InputError(
            **common, invalid_input_ids=("invalid-input",), errors=("invalid position",)
        ),
        OutcomeKind.NOT_PRESENTABLE: lambda: NotPresentable(
            **common,
            presented_element_ids=("pe-1",),
            failed_condition_ids=("amber-content",),
        ),
        OutcomeKind.SYNTHESIS_FAILED: lambda: SynthesisFailed(
            **common, manifold_id="manifold-1", failed_rule_ids=("I-1",)
        ),
        OutcomeKind.SYNTHESIS_AMBIGUOUS: lambda: SynthesisAmbiguous(
            **common, candidate_representation_ids=("candidate-1", "candidate-rival")
        ),
        OutcomeKind.CONCEPT_NOT_APPLICABLE: lambda: ConceptNotApplicable(
            **common,
            object_candidate_id="object-1",
            application_result_id="application-1",
            failed_condition_ids=("amber-content",),
        ),
        OutcomeKind.APPLICATION_UNDERDETERMINED: lambda: ApplicationUnderdetermined(
            **common,
            object_candidate_id="object-1",
            application_result_id="application-1",
            undecided_condition_ids=("amber-content",),
        ),
        OutcomeKind.UNITY_CONFLICT: lambda: UnityConflict(
            **common,
            proposed_judgment_id="proposal-1",
            conflict_ids=("branch-conflict",),
        ),
        OutcomeKind.JUDGMENT_WITHHELD: lambda: JudgmentWithheld(
            **common,
            strongest_representation_ids=("application-1",),
            unmet_condition_ids=("amber-content",),
        ),
    }
    if kind in (
        OutcomeKind.CONCEPT_NOT_APPLICABLE,
        OutcomeKind.APPLICATION_UNDERDETERMINED,
    ):
        application = trace.applications[0]
        condition_status = ConditionStatus.FAILED
        status = ApplicationStatus.NOT_APPLICABLE
        if kind is OutcomeKind.APPLICATION_UNDERDETERMINED:
            condition_status = ConditionStatus.UNDECIDED
            status = ApplicationStatus.UNDERDETERMINED
        condition = _change(application.condition_results[0], status=condition_status)
        application = _change(
            application, status=status, condition_results=(condition,)
        )
        trace = _change(
            trace, applications=(application,), proposals=(), unity_checks=()
        )
    if kind is OutcomeKind.OVERREACH:
        hidden = EvaluatorReference(
            evaluator_reference_id="hidden-1", description="evaluator-only label"
        )
        violation = AuthorityViolation(
            source_id="hidden-1",
            attempted_use="object identity",
            explanation="not presented",
            evaluator_reference=hidden,
        )
        report = _change(context.limit_report, authority_violations=(violation,))
        context = _change(context, limit_report=report)
        outcome = Overreach(
            outcome_id="outcome-test",
            context=context,
            rejected_claim="the hidden identity is known",
            violations=(violation,),
        )
        trace = _change(trace, evaluator_references=(hidden,))
    else:
        outcome = outcomes[kind]()
    trace = _change(
        trace,
        external_inputs=(
            ExternalInputReference(
                input_id="invalid-input", description="rejected record"
            ),
        ),
        limit_reports=(context.limit_report,),
        outcomes=(outcome,),
    )
    graph = ProvenanceGraph(trace)
    assert validate_provenance_json(dump_provenance(graph)) == graph


def test_unity_must_identify_the_proposal_it_checked(
    complete_trace: ProvenanceTrace,
) -> None:
    unity = complete_trace.unity_checks[0]
    conditions = tuple(
        _change(
            item, evidence=(_ground("application-1", GroundKind.APPLICATION_RESULT),)
        )
        for item in unity.condition_results
    )
    trace = _change(
        complete_trace,
        unity_checks=(_change(unity, condition_results=conditions),),
        judgments=(),
        outcomes=(),
    )
    with pytest.raises(InvalidProvenance, match="one checked proposal"):
        ProvenanceGraph(trace)


def test_application_cannot_relax_a_required_concept_condition(
    complete_trace: ProvenanceTrace,
) -> None:
    application = complete_trace.applications[0]
    condition = _change(application.condition_results[0], required=False)
    replacement = _change(application.condition_results[0], condition_id="replacement")
    trace = _change(
        _prefix(complete_trace),
        applications=(
            _change(application, condition_results=(condition, replacement)),
        ),
    )
    with pytest.raises(InvalidProvenance, match="declared concept conditions"):
        ProvenanceGraph(trace)


def test_application_alternatives_resolve_as_applications(
    complete_trace: ProvenanceTrace,
) -> None:
    application = complete_trace.applications[0]
    rival = _change(
        application,
        application_result_id="application-rival",
        alternative_application_ids=("application-1",),
    )
    application = _change(
        application, alternative_application_ids=("application-rival",)
    )
    trace = _change(_prefix(complete_trace), applications=(application, rival))
    ProvenanceGraph(trace)
    mistyped = _change(application, alternative_application_ids=("candidate-1",))
    with pytest.raises(InvalidProvenance, match="must resolve as ApplicationResult"):
        ProvenanceGraph(_change(trace, applications=(mistyped, rival)))


def test_rejected_rule_authority_is_reported_without_becoming_evidence(
    complete_trace: ProvenanceTrace,
) -> None:
    trace = _rivals(_prefix(complete_trace))
    rule = Rule(
        rule_id="Q-1",
        name="inquiry preference",
        description="does not license objects",
        authority=RuleAuthority.REGULATIVE,
        scope=trace.scope,
    )
    violation = AuthorityViolation(
        source_id="Q-1",
        declared_authority=RuleAuthority.REGULATIVE,
        attempted_use="object identity",
        explanation="a heuristic is not constitutive evidence",
    )
    context = _context(trace, OutcomeKind.OVERREACH)
    report = _change(context.limit_report, authority_violations=(violation,))
    outcome = Overreach(
        outcome_id="outcome-test",
        context=_change(context, limit_report=report),
        rejected_claim="the heuristic proves identity",
        violations=(violation,),
    )
    trace = _change(
        trace, rules=(*trace.rules, rule), limit_reports=(report,), outcomes=(outcome,)
    )
    ProvenanceGraph(trace)
    misreported = _change(rule, authority=RuleAuthority.ENGINEERING)
    with pytest.raises(InvalidProvenance, match="misstates rule authority"):
        ProvenanceGraph(_change(trace, rules=(*complete_trace.rules, misreported)))


def test_wire_validation_rejects_unknown_versions_and_fields(
    complete_trace: ProvenanceTrace,
) -> None:
    data = complete_trace.model_dump(mode="python")
    with pytest.raises(ValidationError):
        validate_provenance({**data, "format_version": 2})
    with pytest.raises(ValidationError, match="extra_forbidden"):
        validate_provenance({**data, "hidden_world": {}})
