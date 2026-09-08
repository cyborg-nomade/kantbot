"""Regression witnesses for the epistemology audit, through public validation."""

from types import SimpleNamespace

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from conftest import make_successful_trace
from kantbot.interfaces import (
    ApplicationRequest,
    ProvenanceView,
    RoleContext,
    UnderstandingRepertoire,
)
from kantbot.model import (
    ConceptKind,
    Condition,
    ConditionStatus,
    ContentField,
    EvaluatorReference,
    FieldProjection,
    FormKind,
    RuleAuthority,
    RuleKind,
    SemanticModel,
    SensibleProcedure,
    StrictIncrease,
    TemporalOrder,
)
from kantbot.procedures import evaluate_procedure, project_content
from kantbot.provenance import (
    InvalidProvenance,
    ProvenanceGraph,
    ProvenanceTrace,
    validate_provenance,
)
from kantbot.transitions import (
    CommitmentCompleted,
    InvalidTransition,
    UnityAccepted,
    record_commitment,
    record_critique,
)


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def _before_application(trace: ProvenanceTrace) -> ProvenanceTrace:
    return _change(
        trace,
        applications=(),
        proposals=(),
        unity_checks=(),
        judgments=(),
        limit_reports=(),
        outcomes=(),
    )


def _blue_input(trace: ProvenanceTrace) -> ProvenanceTrace:
    content = (
        ContentField(name="color", value="blue"),
        ContentField(name="x", value=0),
    )
    return _change(
        trace,
        observations=(_change(trace.observations[0], content=content),),
        presented_elements=(_change(trace.presented_elements[0], content=content),),
        intuitions=(_change(trace.intuitions[0], content=content),),
    )


def _apply_using_only_the_port(
    request: ApplicationRequest, view: ProvenanceView
) -> ConditionStatus:
    candidate = view.candidate_for(request.object_candidate.candidate_representation_id)
    intuitions = tuple(view.intuition_for(item) for item in candidate.intuition_ids)
    forms = tuple(
        dict.fromkeys(
            form for item in candidate.intuition_ids for form in view.forms_for(item)
        )
    )
    results = evaluate_procedure(
        request.concept_schema.procedure,
        request.concept.applicability_conditions,
        intuitions,
        forms,
    )
    return results[0].status


def test_identical_application_requests_can_now_distinguish_amber_and_blue(
    complete_trace: ProvenanceTrace,
) -> None:
    prefix = _before_application(complete_trace)
    amber: ProvenanceView = ProvenanceGraph(prefix)
    blue: ProvenanceView = ProvenanceGraph(_blue_input(prefix))
    request = ApplicationRequest(
        object_candidate=prefix.object_candidates[0],
        concept=prefix.concepts[0],
        concept_schema=prefix.schemas[0],
        context=RoleContext(scope=prefix.scope, configuration=prefix.configuration),
    )
    assert _apply_using_only_the_port(request, amber) is ConditionStatus.SATISFIED
    assert _apply_using_only_the_port(request, blue) is ConditionStatus.FAILED
    assert amber.rule_for("I-1").kind is RuleKind.IDENTITY
    with pytest.raises(ValidationError, match="frozen"):
        amber.intuition_for("intuition-1").position = 99


def test_content_lookup_denies_evaluator_ids_wrong_kinds_and_unknown_ids(
    complete_trace: ProvenanceTrace,
) -> None:
    hidden = EvaluatorReference(
        evaluator_reference_id="hidden-1", description="hidden world"
    )
    view: ProvenanceView = ProvenanceGraph(
        _change(complete_trace, evaluator_references=(hidden,))
    )
    for lookup in (
        view.intuition_for,
        view.candidate_for,
        view.rule_for,
        view.forms_for,
    ):
        for entity_id in ("hidden-1", "absent", "obs-1"):
            with pytest.raises(KeyError):
                lookup(entity_id)


@pytest.mark.parametrize(("supplied", "substituted"), [(True, 1), (1, 1.0)])
@pytest.mark.parametrize("stage", ["reception", "projection"])
def test_content_preservation_includes_scalar_types(
    complete_trace: ProvenanceTrace, supplied: object, substituted: object, stage: str
) -> None:
    original = (
        ContentField(name="color", value="amber"),
        ContentField(name="x", value=supplied),
    )
    replacement = (
        ContentField(name="color", value="amber"),
        ContentField(name="x", value=substituted),
    )
    presented_content = original
    if stage == "reception":
        presented_content = replacement
    trace = _change(
        _before_application(complete_trace),
        observations=(_change(complete_trace.observations[0], content=original),),
        presented_elements=(
            _change(complete_trace.presented_elements[0], content=presented_content),
        ),
        intuitions=(_change(complete_trace.intuitions[0], content=replacement),),
    )
    with pytest.raises(InvalidProvenance, match=r"shared reception|projection replay"):
        ProvenanceGraph(trace)


def test_prose_and_unknown_instructions_cannot_replace_a_schema_procedure(
    complete_trace: ProvenanceTrace,
) -> None:
    for procedure in (
        "Always succeed without inspecting input",
        {"checks": ({"operation": "always-succeed", "condition_id": "amber-content"},)},
    ):
        data = complete_trace.model_dump(mode="python")
        data["schemas"][0]["procedure"] = procedure
        with pytest.raises(ValidationError):
            validate_provenance(data)


def test_an_amber_license_cannot_be_reused_for_blue_sensible_content(
    complete_trace: ProvenanceTrace,
) -> None:
    with pytest.raises(InvalidProvenance, match="procedure replay"):
        ProvenanceGraph(_blue_input(complete_trace))


def test_intuition_cannot_invent_content_even_with_valid_parent_ids(
    complete_trace: ProvenanceTrace,
) -> None:
    intuition = _blue_input(complete_trace).intuitions[0]
    with pytest.raises(InvalidProvenance, match="projection replay"):
        ProvenanceGraph(_change(complete_trace, intuitions=(intuition,)))


@pytest.mark.parametrize(
    "updates",
    [
        {"representation_kind": "non-intuitive-token"},
        {"conditions": ("no-receptive-test",)},
        {"conditions": ("singular", "preconceptual")},
    ],
)
def test_unsupported_projection_claims_cannot_admit_an_intuition(
    complete_trace: ProvenanceTrace, updates: dict[str, object]
) -> None:
    projection = _change(complete_trace.projections[0], **updates)
    with pytest.raises(InvalidProvenance, match=r"intuition|receptive criteria"):
        ProvenanceGraph(_change(complete_trace, projections=(projection,)))


def test_removing_temporal_form_kind_is_not_just_a_label_change(
    complete_trace: ProvenanceTrace,
) -> None:
    form = _change(complete_trace.forms[0], kind=FormKind.OTHER)
    projection = _change(complete_trace.projections[0], required_forms=(form,))
    with pytest.raises(InvalidProvenance, match="temporal form"):
        ProvenanceGraph(
            _change(complete_trace, forms=(form,), projections=(projection,))
        )


def test_projection_can_select_a_real_subset_without_copying_every_input_field(
    complete_trace: ProvenanceTrace,
) -> None:
    projection = _change(
        complete_trace.projections[0], procedure=FieldProjection(fields=("color",))
    )
    content = project_content(complete_trace.presented_elements[0], projection)
    assert content == (ContentField(name="color", value="amber"),)
    trace = _change(
        complete_trace,
        projections=(projection,),
        intuitions=(_change(complete_trace.intuitions[0], content=content),),
        manifolds=(),
        retained_sequences=(),
        candidates=(),
        object_candidates=(),
        applications=(),
        proposals=(),
        unity_checks=(),
        judgments=(),
        limit_reports=(),
        outcomes=(),
    )
    ProvenanceGraph(trace)
    missing = _change(
        projection, procedure=FieldProjection(fields=("hidden-identity",))
    )
    with pytest.raises(ValueError, match="absent from presentation"):
        project_content(complete_trace.presented_elements[0], missing)


@pytest.mark.parametrize("field", ["identity_results", "constitutive_results"])
@pytest.mark.parametrize("updates", [{"condition_id": "unrelated"}, {"evidence": ()}])
def test_object_licenses_must_match_the_selected_rules_and_sensible_evidence(
    complete_trace: ProvenanceTrace, field: str, updates: dict[str, object]
) -> None:
    obj = complete_trace.object_candidates[0]
    result = _change(getattr(obj, field)[0], **updates)
    with pytest.raises(InvalidProvenance, match="procedure replay"):
        ProvenanceGraph(
            _change(
                complete_trace, object_candidates=(_change(obj, **{field: (result,)}),)
            )
        )


@pytest.mark.parametrize("resource", ["concept", "rule"])
def test_constitutive_resources_cannot_launder_regulative_conditions(
    complete_trace: ProvenanceTrace, resource: str
) -> None:
    concept = complete_trace.concepts[0]
    rules = complete_trace.rules
    if resource == "concept":
        condition = _change(
            concept.applicability_conditions[0], authority=RuleAuthority.REGULATIVE
        )
        concept = _change(concept, applicability_conditions=(condition,))
    else:
        condition = _change(rules[0].conditions[0], authority=RuleAuthority.REGULATIVE)
        rules = (_change(rules[0], conditions=(condition,)), rules[1])
    with pytest.raises(InvalidProvenance, match="constitutive"):
        ProvenanceGraph(_change(complete_trace, concepts=(concept,), rules=rules))
    with pytest.raises(ValidationError, match="constitutive"):
        UnderstandingRepertoire(
            rules=rules,
            concepts=(concept,),
            schemas=complete_trace.schemas,
            scope=complete_trace.scope,
            configuration=complete_trace.configuration,
        )


def test_schema_must_cover_new_required_conditions_not_just_known_condition_ids(
    complete_trace: ProvenanceTrace,
) -> None:
    concept = complete_trace.concepts[0]
    extra = _change(
        concept.applicability_conditions[0], condition_id="additional-required"
    )
    concept = _change(
        concept, applicability_conditions=(*concept.applicability_conditions, extra)
    )
    application = complete_trace.applications[0]
    extra_result = _change(
        application.condition_results[0], condition_id=extra.condition_id
    )
    application = _change(
        application, condition_results=(*application.condition_results, extra_result)
    )
    with pytest.raises(InvalidProvenance, match="all declared conditions"):
        ProvenanceGraph(
            _change(complete_trace, concepts=(concept,), applications=(application,))
        )
    with pytest.raises(ValidationError, match="all declared conditions"):
        UnderstandingRepertoire(
            rules=complete_trace.rules,
            concepts=(concept,),
            schemas=complete_trace.schemas,
            scope=complete_trace.scope,
            configuration=complete_trace.configuration,
        )


def test_empirical_color_test_cannot_be_relabelled_as_category_mediation(
    complete_trace: ProvenanceTrace,
) -> None:
    concept = _change(complete_trace.concepts[0], kind=ConceptKind.CATEGORY_INSPIRED)
    with pytest.raises(InvalidProvenance, match="temporal mediation"):
        ProvenanceGraph(_change(complete_trace, concepts=(concept,)))
    with pytest.raises(ValidationError, match="sensible procedure"):
        _change(complete_trace.rules[0], sensible_procedure=None)
    general = _change(
        complete_trace.rules[0],
        kind=RuleKind.GENERAL,
        conditions=(),
        sensible_procedure=None,
    )
    with pytest.raises(InvalidProvenance, match="licensing role"):
        ProvenanceGraph(
            _change(complete_trace, rules=(general, complete_trace.rules[1]))
        )


def _condition() -> Condition:
    return Condition(
        condition_id="test",
        description="bounded test",
        required=True,
        authority=RuleAuthority.CONSTITUTIVE,
    )


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((0, 1, 2), ConditionStatus.SATISFIED),
        ((0, 2, 1), ConditionStatus.FAILED),
        ((0, 0, 0), ConditionStatus.FAILED),
        ((0,), ConditionStatus.UNDECIDED),
        ((0, "one"), ConditionStatus.UNDECIDED),
        ((False, True), ConditionStatus.UNDECIDED),
    ],
)
def test_temporal_motion_procedure_changes_with_successive_content(
    successful_trace: SimpleNamespace,
    values: tuple[object, ...],
    expected: ConditionStatus,
) -> None:
    intuitions = tuple(
        _change(
            successful_trace.intuition,
            intuition_id=f"sample-{position}",
            position=position,
            content=(ContentField(name="x", value=value),),
        )
        for position, value in enumerate(values)
    )
    procedure = SensibleProcedure(
        temporal_form_id="time-total",
        checks=(StrictIncrease(condition_id="test", field="x"),),
    )
    results = evaluate_procedure(
        procedure,
        (_condition(),),
        intuitions,
        successful_trace.projection.required_forms,
    )
    assert results[0].status is expected
    assert tuple(item.ground_id for item in results[0].evidence) == tuple(
        item.intuition_id for item in intuitions
    )


def test_temporal_checks_do_not_sort_reversed_inputs_or_invent_missing_forms(
    successful_trace: SimpleNamespace,
) -> None:
    first = successful_trace.intuition
    second = _change(first, intuition_id="second", position=1)
    procedure = SensibleProcedure(
        temporal_form_id="time-total",
        checks=(TemporalOrder(condition_id="test", minimum_samples=2),),
    )
    forms = successful_trace.projection.required_forms
    assert evaluate_procedure(procedure, (_condition(),), (first, second), forms)[
        0
    ].passed
    assert (
        evaluate_procedure(procedure, (_condition(),), (second, first), forms)[0].status
        is ConditionStatus.FAILED
    )
    assert (
        evaluate_procedure(procedure, (_condition(),), (first, second), ())[0].status
        is ConditionStatus.UNDECIDED
    )
    assert (
        evaluate_procedure(procedure, (_condition(),), (), forms)[0].status
        is ConditionStatus.UNDECIDED
    )
    with pytest.raises(ValueError, match="duplicates"):
        evaluate_procedure(procedure, (_condition(),), (first, first), forms)


@given(st.lists(st.integers(), min_size=2, max_size=8))
def test_generated_numeric_order_matches_pairwise_increase(values: list[int]) -> None:
    # Independent oracle; the test never asks replay to generate its expectation.
    trace = make_successful_trace()
    intuitions = tuple(
        _change(
            trace.intuition,
            intuition_id=f"sample-{position}",
            position=position,
            content=(ContentField(name="x", value=value),),
        )
        for position, value in enumerate(values)
    )
    procedure = SensibleProcedure(
        temporal_form_id="time-total",
        checks=(StrictIncrease(condition_id="test", field="x"),),
    )
    expected = all(
        values[index] < values[index + 1] for index in range(len(values) - 1)
    )
    assert (
        evaluate_procedure(
            procedure, (_condition(),), intuitions, trace.projection.required_forms
        )[0].passed
        == expected
    )


def test_commitment_and_reporting_require_the_matching_certified_trace(
    complete_trace: ProvenanceTrace,
) -> None:
    context = RoleContext(
        scope=complete_trace.scope, configuration=complete_trace.configuration
    )
    united = UnityAccepted(
        cycle_id=complete_trace.cycle_id,
        context=context,
        proposal=complete_trace.proposals[0],
        unity_check=complete_trace.unity_checks[0],
    )
    graph = ProvenanceGraph(complete_trace)
    judgment = complete_trace.judgments[0]
    committed = record_commitment(united, judgment, graph)
    assert isinstance(committed, CommitmentCompleted)
    assert (
        record_critique(committed, complete_trace.outcomes[0], graph).outcome
        == complete_trace.outcomes[0]
    )
    with pytest.raises(InvalidTransition, match="another cycle"):
        record_commitment(_change(united, cycle_id="another-cycle"), judgment, graph)
    with pytest.raises(InvalidTransition, match="certified provenance"):
        record_commitment(
            united, judgment, ProvenanceGraph(_before_application(complete_trace))
        )
    with pytest.raises(InvalidTransition, match="certified provenance"):
        record_critique(
            committed,
            complete_trace.outcomes[0],
            ProvenanceGraph(_change(complete_trace, outcomes=())),
        )
