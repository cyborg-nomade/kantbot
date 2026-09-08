"""A temporal license needs witnessed succession, not a singleton identity."""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from kantbot.model import (
    ConditionStatus,
    FieldConstant,
    FieldEquals,
    SemanticModel,
    SensibleProcedure,
    TemporalOrder,
)
from kantbot.procedures import evaluate_procedure
from kantbot.provenance import InvalidProvenance, ProvenanceGraph, ProvenanceTrace

_MINIMUM_TEMPORAL_SAMPLES = 2


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


@pytest.mark.parametrize("operation", ["field-constant", "temporal-order"])
def test_temporal_declarations_reject_a_single_sample_minimum(operation: str) -> None:
    check = {
        "operation": operation,
        "condition_id": "temporal-test",
        "minimum_samples": 1,
    }
    if operation == "field-constant":
        check["field"] = "x"
    with pytest.raises(ValidationError, match="greater_than_equal"):
        SensibleProcedure.model_validate(
            {"temporal_form_id": "time-total", "checks": (check,)}
        )


@pytest.mark.parametrize(
    "check",
    [
        FieldConstant(condition_id="amber-content", field="x"),
        TemporalOrder(condition_id="amber-content"),
    ],
)
def test_temporal_defaults_leave_one_sample_undecided(
    successful_trace: SimpleNamespace, check: FieldConstant | TemporalOrder
) -> None:
    assert check.minimum_samples == _MINIMUM_TEMPORAL_SAMPLES
    procedure = SensibleProcedure(temporal_form_id="time-total", checks=(check,))
    procedure.require_temporal_mediation()
    result = evaluate_procedure(
        procedure,
        successful_trace.concept.applicability_conditions,
        (successful_trace.intuition,),
        successful_trace.projection.required_forms,
    )
    assert result[0].status is ConditionStatus.UNDECIDED
    assert len(result[0].evidence) == 1


def test_one_sample_still_supports_an_empirical_field_test(
    successful_trace: SimpleNamespace,
) -> None:
    procedure = SensibleProcedure(
        checks=(
            FieldEquals(condition_id="amber-content", field="color", expected="amber"),
        )
    )
    result = evaluate_procedure(
        procedure,
        successful_trace.concept.applicability_conditions,
        (successful_trace.intuition,),
        successful_trace.projection.required_forms,
    )
    assert result[0].passed
    with pytest.raises(ValueError, match="temporal mediation"):
        procedure.require_temporal_mediation()


def test_singleton_candidate_cannot_reuse_successful_temporal_object_licenses(
    complete_trace: ProvenanceTrace,
) -> None:
    candidate = _change(
        complete_trace.candidates[0],
        intuition_ids=(complete_trace.intuitions[0].intuition_id,),
    )
    obj = complete_trace.object_candidates[0]
    # Keep the reported success and supply honest singleton evidence. Replay
    # must reject the status itself, not merely a missing or wrong reference.
    identity = tuple(
        _change(item, evidence=item.evidence[:1]) for item in obj.identity_results
    )
    constitutive = tuple(
        _change(item, evidence=item.evidence[:1]) for item in obj.constitutive_results
    )
    trace = _change(
        complete_trace,
        candidates=(candidate,),
        object_candidates=(
            _change(obj, identity_results=identity, constitutive_results=constitutive),
        ),
        applications=(),
        proposals=(),
        unity_checks=(),
        judgments=(),
        outcomes=(),
        limit_reports=(),
    )
    with pytest.raises(InvalidProvenance, match="procedure replay"):
        ProvenanceGraph(trace)
    # A singleton remains a presentable candidate; it simply lacks this license.
    ProvenanceGraph(_change(trace, object_candidates=()))
