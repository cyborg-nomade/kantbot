"""General rules and the sensible procedures that license object formation."""

from enum import StrEnum
from typing import Self

from pydantic import model_validator

from kantbot.model.common import (
    Condition,
    Identifier,
    NonEmptyText,
    RuleAuthority,
    Scope,
    SemanticModel,
    require_unique,
)
from kantbot.model.procedures import SensibleProcedure


class RuleKind(StrEnum):
    GENERAL = "general"
    IDENTITY = "identity"
    CATEGORY_INSPIRED = "category-inspired"


class Rule(SemanticModel):
    """Authority alone never turns a general rule into an object license."""

    rule_id: Identifier
    name: NonEmptyText
    description: NonEmptyText
    authority: RuleAuthority
    scope: Scope
    kind: RuleKind = RuleKind.GENERAL
    conditions: tuple[Condition, ...] = ()
    sensible_procedure: SensibleProcedure | None = None

    @model_validator(mode="after")
    def object_licensing_requires_bound_temporal_conditions(self) -> Self:
        require_unique(
            tuple(item.condition_id for item in self.conditions), "rule condition IDs"
        )
        if self.sensible_procedure is not None:
            self.sensible_procedure.validate_conditions(self.conditions)
        if self.kind is not RuleKind.GENERAL:
            if not self.conditions or self.sensible_procedure is None:
                raise ValueError("object-licensing rules require a sensible procedure")
            self.sensible_procedure.require_temporal_mediation()
            if any(not item.required for item in self.conditions):
                raise ValueError("object-licensing conditions must be required")
        return self
