"""Concepts, schemata, and their distinct application results."""

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from kantbot.model.common import (
    Condition,
    ConditionResult,
    ConditionStatus,
    Derivation,
    GroundKind,
    Identifier,
    NonEmptyText,
    RuleAuthority,
    Scope,
    SemanticModel,
    require_unique,
)
from kantbot.model.procedures import SensibleProcedure


class ConceptKind(StrEnum):
    EMPIRICAL = "empirical"
    CATEGORY_INSPIRED = "category-inspired"


class Concept(SemanticModel):
    """General conditions and consequences; naming it does not apply it."""

    concept_id: Identifier
    name: NonEmptyText
    kind: ConceptKind
    applicability_conditions: tuple[Condition, ...] = Field(min_length=1)
    inferential_consequences: tuple[NonEmptyText, ...] = ()
    scope: Scope
    authority: RuleAuthority

    @model_validator(mode="after")
    def condition_ids_are_unique(self) -> Self:
        require_unique(
            tuple(item.condition_id for item in self.applicability_conditions),
            "concept condition IDs",
        )
        return self


class Schema(SemanticModel):
    """An inspectable procedure mediating concept and formed particulars."""

    schema_id: Identifier
    concept_id: Identifier
    name: NonEmptyText
    procedure: SensibleProcedure
    condition_ids: tuple[Identifier, ...] = Field(min_length=1)
    sensible_form_ids: tuple[Identifier, ...] = Field(min_length=1)
    scope: Scope
    authority: RuleAuthority

    @model_validator(mode="after")
    def references_are_unique(self) -> Self:
        require_unique(self.condition_ids, "schema condition IDs")
        require_unique(self.sensible_form_ids, "sensible form IDs")
        if set(self.condition_ids) != set(self.procedure.condition_ids):
            raise ValueError("schema conditions must match its procedure checks")
        temporal_form_id = self.procedure.temporal_form_id
        if (
            temporal_form_id is not None
            and temporal_form_id not in self.sensible_form_ids
        ):
            raise ValueError("schema omits its procedure's temporal form")
        return self

    def validate_concept(self, concept: Concept) -> None:
        """Bind the selected procedure to this concept, not just a subset."""

        if self.concept_id != concept.concept_id:
            raise ValueError("schema belongs to another concept")
        self.procedure.validate_conditions(concept.applicability_conditions)
        if concept.kind is ConceptKind.CATEGORY_INSPIRED:
            self.procedure.require_temporal_mediation()


class ApplicationStatus(StrEnum):
    APPLICABLE = "applicable"
    NOT_APPLICABLE = "not-applicable"
    UNDERDETERMINED = "underdetermined"


class ApplicationResult(SemanticModel):
    """Condition-level applicability without judgment commitment."""

    application_result_id: Identifier
    object_candidate_id: Identifier
    concept_id: Identifier
    schema_id: Identifier
    status: ApplicationStatus
    condition_results: tuple[ConditionResult, ...] = Field(min_length=1)
    alternative_application_ids: tuple[Identifier, ...] = ()
    derivation: Derivation

    @model_validator(mode="after")
    def status_matches_required_conditions(self) -> Self:
        require_unique(
            tuple(item.condition_id for item in self.condition_results),
            "application condition IDs",
        )
        require_unique(self.alternative_application_ids, "alternative_application_ids")
        required = tuple(item for item in self.condition_results if item.required)
        if not required:
            raise ValueError("application requires at least one required condition")

        has_failed = any(item.status is ConditionStatus.FAILED for item in required)
        has_undecided = any(
            item.status is ConditionStatus.UNDECIDED for item in required
        )
        if has_failed:
            expected = ApplicationStatus.NOT_APPLICABLE
        elif has_undecided:
            expected = ApplicationStatus.UNDERDETERMINED
        else:
            expected = ApplicationStatus.APPLICABLE
        if self.status is not expected:
            raise ValueError(
                f"application status {self.status.value!r} does not match "
                "its required condition results"
            )
        if not self.derivation.has_ground(
            self.object_candidate_id, GroundKind.OBJECT_CANDIDATE
        ):
            raise ValueError("application must ground itself in its object candidate")
        if not self.derivation.has_ground(self.concept_id, GroundKind.CONCEPT):
            raise ValueError("application must name its concept as a ground")
        if not self.derivation.has_ground(self.schema_id, GroundKind.SCHEMA):
            raise ValueError("application must name its schema as a ground")
        return self

    @property
    def applicable(self) -> bool:
        return self.status is ApplicationStatus.APPLICABLE
