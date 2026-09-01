"""Represent the boundary of reason without activating Phase 4 behavior."""

from enum import StrEnum
from typing import Self

from pydantic import model_validator

from kantbot.model.common import (
    Derivation,
    Identifier,
    NonEmptyText,
    Rule,
    RuleAuthority,
    SemanticModel,
)


class ReasonStatus(StrEnum):
    RESERVED = "reserved"


class Reason(SemanticModel):
    """Regulative guidance that is representable but inactive until Phase 4."""

    reason_id: Identifier
    principle: Rule
    guidance: NonEmptyText
    status: ReasonStatus = ReasonStatus.RESERVED
    derivation: Derivation

    @model_validator(mode="after")
    def first_cycle_reason_is_only_regulative(self) -> Self:
        if self.principle.authority is not RuleAuthority.REGULATIVE:
            raise ValueError("reserved reason must have regulative authority")
        return self
