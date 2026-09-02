"""Immutable products of retention, synthesis, and object formation."""

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from kantbot.model.common import (
    ConditionResult,
    Derivation,
    GroundKind,
    Identifier,
    SemanticModel,
    require_unique,
)


class RetentionStatus(StrEnum):
    CURRENT = "current"
    REPRODUCED = "reproduced"


class RetainedIntuition(SemanticModel):
    """An intuition's explicit status within a retained sequence."""

    intuition_id: Identifier
    status: RetentionStatus
    retention_rule_id: Identifier | None = None

    @model_validator(mode="after")
    def reproduced_items_require_a_rule(self) -> Self:
        if self.status is RetentionStatus.REPRODUCED and self.retention_rule_id is None:
            raise ValueError("a reproduced intuition requires a retention rule")
        if (
            self.status is RetentionStatus.CURRENT
            and self.retention_rule_id is not None
        ):
            raise ValueError("a current intuition must not claim a retention rule")
        return self


class RetainedSequence(SemanticModel):
    """Current and licensed reproduced intuitions in explicit order."""

    retained_sequence_id: Identifier
    manifold_id: Identifier
    items: tuple[RetainedIntuition, ...] = Field(min_length=1)
    derivation: Derivation

    @model_validator(mode="after")
    def sequence_is_distinct_and_grounded(self) -> Self:
        intuition_ids = tuple(item.intuition_id for item in self.items)
        require_unique(intuition_ids, "retained intuition IDs")
        if not self.derivation.has_ground(self.manifold_id, GroundKind.MANIFOLD):
            raise ValueError("retained sequence must ground itself in its manifold")
        rule_ground_ids = {
            item.ground_id
            for item in self.derivation.grounds
            if item.kind is GroundKind.RULE
        }
        missing_rules = {
            item.retention_rule_id
            for item in self.items
            if item.retention_rule_id is not None
            and item.retention_rule_id not in rule_ground_ids
        }
        if missing_rules:
            raise ValueError(
                f"retention rules are absent from provenance: {missing_rules}"
            )
        return self


class SynthesisPolicy(StrEnum):
    """The edition-sensitive policies retained by ADR 0002."""

    A_ANALYSIS_B_CONSTRAINT = "a-analysis-b-constraint"
    B_LED_FIGURATIVE = "b-led-figurative"


class CandidateRepresentation(SemanticModel):
    """A proposed unity that does not yet license objecthood."""

    candidate_representation_id: Identifier
    retained_sequence_id: Identifier
    intuition_ids: tuple[Identifier, ...] = Field(min_length=1)
    policy: SynthesisPolicy
    identity_rule_ids: tuple[Identifier, ...] = Field(min_length=1)
    constitutive_rule_ids: tuple[Identifier, ...] = Field(min_length=1)
    conflict_ids: tuple[Identifier, ...] = ()
    alternative_candidate_ids: tuple[Identifier, ...] = ()
    derivation: Derivation

    @model_validator(mode="after")
    def synthesis_references_are_explicit(self) -> Self:
        require_unique(self.intuition_ids, "intuition_ids")
        require_unique(self.identity_rule_ids, "identity_rule_ids")
        require_unique(self.constitutive_rule_ids, "constitutive_rule_ids")
        require_unique(self.conflict_ids, "conflict_ids")
        require_unique(self.alternative_candidate_ids, "alternative_candidate_ids")
        if not self.derivation.has_ground(
            self.retained_sequence_id, GroundKind.RETAINED_SEQUENCE
        ):
            raise ValueError(
                "candidate representation must ground itself in a retained sequence"
            )
        rule_ground_ids = {
            item.ground_id
            for item in self.derivation.grounds
            if item.kind is GroundKind.RULE
        }
        missing_rules = (
            set(self.identity_rule_ids) | set(self.constitutive_rule_ids)
        ) - rule_ground_ids
        if missing_rules:
            raise ValueError(
                f"synthesis rules are absent from provenance: {missing_rules}"
            )
        return self


class ObjectCandidate(SemanticModel):
    """A candidate whose local identity and constitutive tests all pass."""

    object_candidate_id: Identifier
    candidate_representation_id: Identifier
    identity_results: tuple[ConditionResult, ...] = Field(min_length=1)
    constitutive_results: tuple[ConditionResult, ...] = Field(min_length=1)
    unresolved_condition_ids: tuple[Identifier, ...] = ()
    derivation: Derivation

    @model_validator(mode="after")
    def required_object_conditions_pass(self) -> Self:
        all_results = self.identity_results + self.constitutive_results
        require_unique(
            tuple(result.condition_id for result in all_results),
            "object condition IDs",
        )
        if any(not result.required or not result.passed for result in all_results):
            raise ValueError(
                "object candidates require satisfied identity and constitutive results"
            )
        require_unique(self.unresolved_condition_ids, "unresolved_condition_ids")
        if not self.derivation.has_ground(
            self.candidate_representation_id,
            GroundKind.CANDIDATE_REPRESENTATION,
        ):
            raise ValueError(
                "object candidate must ground itself in a candidate representation"
            )
        return self
