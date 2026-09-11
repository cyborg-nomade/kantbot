"""Pure replay of the formal model's deliberately small sensible procedures.

These operations verify particular content against declared instructions.
They do not select candidates, invent concepts, or commit judgments.
"""

from itertools import pairwise

from kantbot.model import (
    CognitiveGround,
    Condition,
    ConditionResult,
    ConditionStatus,
    ContentField,
    FieldConstant,
    FieldEquals,
    Form,
    FormKind,
    GroundKind,
    Intuition,
    PresentedElement,
    SensibleProcedure,
    StrictIncrease,
    TemporalOrder,
    VariantProjection,
)
from kantbot.model.common import ScalarValue, require_unique
from kantbot.model.procedures import SensibleCheck


def project_content(
    presented: PresentedElement, projection: VariantProjection
) -> tuple[ContentField, ...]:
    """Replay supported receptive criteria; unsupported projections fail closed."""

    if projection.representation_kind != "intuition":
        raise ValueError("projection does not produce an intuition")
    if set(projection.conditions) != {"singular", "preconceptual", "temporal-order"}:
        raise ValueError("unsupported or incomplete receptive criteria")
    if not any(form.kind is FormKind.TEMPORAL for form in projection.required_forms):
        raise ValueError("intuition projection requires a temporal form")
    supplied = {item.name: item for item in presented.content}
    if not set(projection.procedure.fields) <= supplied.keys():
        raise ValueError("projection requires fields absent from presentation")
    return tuple(supplied[name] for name in projection.procedure.fields)


def _temporal_status(
    procedure: SensibleProcedure,
    intuitions: tuple[Intuition, ...],
    forms: tuple[Form, ...],
) -> ConditionStatus:
    form_id = procedure.temporal_form_id
    if form_id is None:
        return ConditionStatus.SATISFIED
    if not any(
        form.form_id == form_id and form.kind is FormKind.TEMPORAL for form in forms
    ):
        return ConditionStatus.UNDECIDED
    if any(form_id not in intuition.form_ids for intuition in intuitions):
        return ConditionStatus.UNDECIDED
    if any(left.position >= right.position for left, right in pairwise(intuitions)):
        return ConditionStatus.FAILED
    return ConditionStatus.SATISFIED


def _same_value(left: ScalarValue, right: ScalarValue) -> bool:
    # Python's True == 1 must not turn a presented boolean into a numeric fact.
    return type(left) is type(right) and left == right


def _values_status(
    check: FieldEquals | FieldConstant | StrictIncrease,
    values: tuple[ScalarValue, ...],
) -> ConditionStatus:
    if isinstance(check, FieldEquals):
        satisfied = all(_same_value(value, check.expected) for value in values)
    elif isinstance(check, FieldConstant):
        satisfied = all(_same_value(value, values[0]) for value in values)
    else:
        numbers: list[int | float] = []
        for value in values:
            if isinstance(value, bool) or not isinstance(value, int | float):
                return ConditionStatus.UNDECIDED
            numbers.append(value)
        satisfied = all(left < right for left, right in pairwise(numbers))
    if satisfied:
        return ConditionStatus.SATISFIED
    return ConditionStatus.FAILED


def _check_status(
    check: SensibleCheck, intuitions: tuple[Intuition, ...]
) -> ConditionStatus:
    minimum_samples = 1
    if not isinstance(check, FieldEquals):
        minimum_samples = check.minimum_samples
    if len(intuitions) < minimum_samples:
        return ConditionStatus.UNDECIDED
    if isinstance(check, TemporalOrder):
        return ConditionStatus.SATISFIED
    values: list[ScalarValue] = []
    for intuition in intuitions:
        content = {item.name: item.value for item in intuition.content}
        if check.field not in content:
            return ConditionStatus.UNDECIDED
        values.append(content[check.field])
    return _values_status(check, tuple(values))


def evaluate_procedure(
    procedure: SensibleProcedure,
    conditions: tuple[Condition, ...],
    intuitions: tuple[Intuition, ...],
    forms: tuple[Form, ...],
) -> tuple[ConditionResult, ...]:
    """Compute results and exact sensible evidence, never trust supplied statuses.

    Input order is meaningful and is never silently sorted. Missing fields,
    forms, or samples yield undecided; a witnessed failed test yields failed.
    """

    procedure.validate_conditions(conditions)
    require_unique(tuple(item.condition_id for item in conditions), "conditions")
    require_unique(tuple(item.intuition_id for item in intuitions), "procedure inputs")
    if len({item.episode_id for item in intuitions}) > 1:
        raise ValueError("procedure inputs must share an episode")
    temporal_status = _temporal_status(procedure, intuitions, forms)
    declarations = {condition.condition_id: condition for condition in conditions}
    evidence = tuple(
        CognitiveGround(ground_id=item.intuition_id, kind=GroundKind.INTUITION)
        for item in intuitions
    )
    results: list[ConditionResult] = []
    for check in procedure.checks:
        status = temporal_status
        if status is ConditionStatus.SATISFIED:
            status = _check_status(check, intuitions)
        results.append(
            ConditionResult(
                condition_id=check.condition_id,
                required=declarations[check.condition_id].required,
                status=status,
                explanation=(
                    f"{check.operation}: {status.value} "
                    "on the declared sensible sequence"
                ),
                evidence=evidence,
            )
        )
    return tuple(results)
