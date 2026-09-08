"""Finite, serializable instructions whose behavior can be replayed.

These are bounded engineering analogues, not a complete theory of schematism.
No instruction can execute arbitrary Python or consult evaluator-only state.
"""

from typing import Annotated, Literal, Self

from pydantic import Field, model_validator

from kantbot.model.common import (
    Condition,
    Identifier,
    ScalarValue,
    SemanticModel,
    require_unique,
)


class FieldEquals(SemanticModel):
    """Test the supplied field against a fixed empirical value at every sample."""

    operation: Literal["field-equals"] = "field-equals"
    condition_id: Identifier
    field: Identifier
    expected: ScalarValue


class FieldConstant(SemanticModel):
    """Test a declared invariant across the bounded temporal sequence."""

    operation: Literal["field-constant"] = "field-constant"
    condition_id: Identifier
    field: Identifier
    minimum_samples: Annotated[int, Field(ge=2)] = 2


class StrictIncrease(SemanticModel):
    """Require numeric increase at every successive temporal sample."""

    operation: Literal["strict-increase"] = "strict-increase"
    condition_id: Identifier
    field: Identifier
    minimum_samples: Annotated[int, Field(ge=2)] = 2


class TemporalOrder(SemanticModel):
    """Require a bounded number of samples in strictly increasing positions."""

    operation: Literal["temporal-order"] = "temporal-order"
    condition_id: Identifier
    minimum_samples: Annotated[int, Field(ge=2)] = 2


type SensibleCheck = Annotated[
    FieldEquals | FieldConstant | StrictIncrease | TemporalOrder,
    Field(discriminator="operation"),
]


class SensibleProcedure(SemanticModel):
    """A complete condition-to-operation binding, with explicit temporal form."""

    checks: tuple[SensibleCheck, ...] = Field(min_length=1)
    temporal_form_id: Identifier | None = None

    @model_validator(mode="after")
    def checks_are_distinct_and_temporal_operations_have_a_form(self) -> Self:
        require_unique(self.condition_ids, "procedure condition IDs")
        if self.has_temporal_check and self.temporal_form_id is None:
            raise ValueError("temporal operations require a temporal form reference")
        return self

    @property
    def condition_ids(self) -> tuple[str, ...]:
        return tuple(check.condition_id for check in self.checks)

    @property
    def has_temporal_check(self) -> bool:
        return any(not isinstance(check, FieldEquals) for check in self.checks)

    def validate_conditions(self, conditions: tuple[Condition, ...]) -> None:
        """One selected procedure must cover every declared condition exactly."""

        if set(self.condition_ids) != {item.condition_id for item in conditions}:
            raise ValueError("procedure must cover all declared conditions exactly")

    def require_temporal_mediation(self) -> None:
        if self.temporal_form_id is None or not self.has_temporal_check:
            raise ValueError("category-inspired use requires temporal mediation")


class FieldProjection(SemanticModel):
    """Select supplied fields in a declared order, without inventing content."""

    operation: Literal["select-fields"] = "select-fields"
    fields: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def fields_are_unique(self) -> Self:
        require_unique(self.fields, "projection fields")
        return self
