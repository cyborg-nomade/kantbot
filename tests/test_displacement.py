"""Independent displacement oracles and rejection of forged spatial licenses."""

from itertools import accumulate, pairwise

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from conftest import make_successful_trace
from kantbot.cycle import run_cycle, strip_plan
from kantbot.model import (
    BoundedDisplacement,
    Condition,
    ConditionStatus,
    ContentField,
    Form,
    FormKind,
    Intuition,
    RuleAuthority,
    SemanticModel,
    SensibleProcedure,
)
from kantbot.procedures import evaluate_procedure
from kantbot.provenance import InvalidProvenance, ProvenanceGraph, ProvenanceTrace
from kantbot.worlds import load_scenario, observe_world


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


CONDITION = Condition(
    condition_id="distance",
    description="At most two units per tick",
    required=True,
    authority=RuleAuthority.CONSTITUTIVE,
)
SPACE = Form(
    form_id="test-space", kind=FormKind.SPATIAL, description="Declared spatial order"
)
PROCEDURE = SensibleProcedure(
    temporal_form_id="time-total",
    checks=(
        BoundedDisplacement(
            condition_id="distance",
            field="x",
            maximum_per_tick=2,
            spatial_form_id=SPACE.form_id,
        ),
    ),
)


def _samples(
    trace: ProvenanceTrace, positions: tuple[int, ...], xs: tuple[object, ...]
) -> tuple[Intuition, ...]:
    return tuple(
        _change(
            trace.intuitions[0],
            intuition_id=f"sample-{index}",
            position=position,
            content=(ContentField(name="x", value=x),),
            form_ids=("time-total", SPACE.form_id),
        )
        for index, (position, x) in enumerate(zip(positions, xs, strict=True))
    )


@pytest.mark.parametrize(
    ("positions", "xs", "status"),
    [
        ((0, 1), (0, 2), ConditionStatus.SATISFIED),
        ((0, 1), (2, 0), ConditionStatus.SATISFIED),
        ((0, 1), (0, 3), ConditionStatus.FAILED),
        ((0, 3), (0, 5), ConditionStatus.SATISFIED),
        ((0, 3), (0, 7), ConditionStatus.FAILED),
        ((0, 1), (0.0, 2.0), ConditionStatus.SATISFIED),
        ((0, 1), (-1e308, 1e308), ConditionStatus.FAILED),
        ((0, 1), (0, True), ConditionStatus.UNDECIDED),
        ((0, 1), (0, None), ConditionStatus.UNDECIDED),
        ((0, 1), (0, "2"), ConditionStatus.UNDECIDED),
        ((0,), (0,), ConditionStatus.UNDECIDED),
        ((1, 0), (0, 1), ConditionStatus.FAILED),
        ((0, 0), (0, 1), ConditionStatus.FAILED),
    ],
)
def test_displacement_obeys_rate_type_and_form_conditions(
    complete_trace: ProvenanceTrace,
    positions: tuple[int, ...],
    xs: tuple[object, ...],
    status: ConditionStatus,
) -> None:
    samples = _samples(complete_trace, positions, xs)
    result = evaluate_procedure(
        PROCEDURE, (CONDITION,), samples, (*complete_trace.forms, SPACE)
    )[0]
    assert result.status is status
    assert tuple(item.ground_id for item in result.evidence) == tuple(
        item.intuition_id for item in samples
    )


def test_missing_spatial_form_or_content_remains_undecided(
    complete_trace: ProvenanceTrace,
) -> None:
    samples = _samples(complete_trace, (0, 1), (0, 1))
    for forms in (
        complete_trace.forms,
        (*complete_trace.forms, _change(SPACE, kind=FormKind.OTHER)),
    ):
        assert (
            evaluate_procedure(PROCEDURE, (CONDITION,), samples, forms)[0].status
            is ConditionStatus.UNDECIDED
        )
    wrong_forms = tuple(_change(item, form_ids=("time-total",)) for item in samples)
    assert (
        evaluate_procedure(
            PROCEDURE, (CONDITION,), wrong_forms, (*complete_trace.forms, SPACE)
        )[0].status
        is ConditionStatus.UNDECIDED
    )
    missing = (
        samples[0],
        _change(samples[1], content=(ContentField(name="other", value=1),)),
    )
    assert (
        evaluate_procedure(
            PROCEDURE, (CONDITION,), missing, (*complete_trace.forms, SPACE)
        )[0].status
        is ConditionStatus.UNDECIDED
    )


@given(
    st.lists(
        st.tuples(st.integers(-1000, 1000), st.integers(1, 20)), min_size=2, max_size=8
    )
)
def test_integer_displacement_matches_independent_arithmetic_oracle(
    values: list[tuple[int, int]],
) -> None:
    source = make_successful_trace()
    complete_trace = ProvenanceTrace(
        cycle_id="test-template",
        scope=source.scope,
        configuration=source.configuration,
        forms=source.projection.required_forms,
        intuitions=source.intuitions,
    )
    xs = tuple(item[0] for item in values)
    times = tuple(accumulate(item[1] for item in values))
    expected = all(
        abs(right - left) <= 2 * (after - before)
        for (left, right), (before, after) in zip(
            pairwise(xs), pairwise(times), strict=True
        )
    )
    results = evaluate_procedure(
        PROCEDURE,
        (CONDITION,),
        _samples(complete_trace, times, xs),
        (*complete_trace.forms, SPACE),
    )
    assert results[0].passed is expected


def test_displacement_cannot_be_declared_without_temporal_evidence() -> None:
    check = PROCEDURE.checks[0]
    with pytest.raises(ValidationError):
        _change(check, minimum_samples=1)
    with pytest.raises(ValidationError):
        _change(check, maximum_per_tick=-1)
    with pytest.raises(ValidationError):
        _change(check, maximum_per_tick=True)
    with pytest.raises(ValidationError):
        _change(PROCEDURE, temporal_form_id=None)


def test_imported_object_license_replays_the_actual_displacement_bound() -> None:
    observations = observe_world(load_scenario("rightward")).observations
    trace = run_cycle(observations, strip_plan("strip-demo")).trace
    identity = trace.rules[1]
    procedure = identity.sensible_procedure
    assert procedure is not None
    tightened = _change(
        procedure,
        checks=(procedure.checks[0], _change(procedure.checks[1], maximum_per_tick=0)),
    )
    forged = _change(
        trace,
        rules=(
            trace.rules[0],
            _change(identity, sensible_procedure=tightened),
            *trace.rules[2:],
        ),
    )
    with pytest.raises(InvalidProvenance, match="procedure replay"):
        ProvenanceGraph(forged)
    invalid_form = _change(
        procedure,
        checks=(
            procedure.checks[0],
            _change(procedure.checks[1], spatial_form_id="strip-time"),
        ),
    )
    with pytest.raises(InvalidProvenance, match="spatial form"):
        ProvenanceGraph(
            _change(
                trace,
                rules=(
                    trace.rules[0],
                    _change(identity, sensible_procedure=invalid_form),
                    *trace.rules[2:],
                ),
            )
        )
