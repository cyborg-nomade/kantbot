"""Observation, shared reception, and variant-scoped intuition values."""

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from kantbot.model.common import (
    ContentField,
    Derivation,
    Form,
    GroundKind,
    Identifier,
    NonEmptyText,
    SemanticModel,
    require_unique,
)


class ObservationQuality(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    IMPAIRED = "impaired"


class Observation(SemanticModel):
    """Immutable external input; it has no cognitive status or objecthood."""

    observation_id: Identifier
    episode_id: Identifier
    position: int
    source: Identifier
    content: tuple[ContentField, ...] = Field(min_length=1)
    quality: ObservationQuality
    quality_notes: NonEmptyText | None = None

    @model_validator(mode="after")
    def content_names_are_unique(self) -> Self:
        require_unique(tuple(item.name for item in self.content), "content names")
        return self


class PresentedElement(SemanticModel):
    """Shared admitted content before any variant-specific projection."""

    presented_element_id: Identifier
    observation_id: Identifier
    episode_id: Identifier
    position: int
    source: Identifier
    content: tuple[ContentField, ...] = Field(min_length=1)
    derivation: Derivation

    @model_validator(mode="after")
    def descends_from_its_observation(self) -> Self:
        if not self.derivation.has_ground(self.observation_id, GroundKind.OBSERVATION):
            raise ValueError("presented element must ground itself in its observation")
        if self.episode_id != self.derivation.scope.episode_id:
            raise ValueError("presented element and derivation must share an episode")
        return self


class VariantProjection(SemanticModel):
    """Declared transformation from shared presentation to a variant kind."""

    projection_id: Identifier
    variant_id: Identifier
    name: NonEmptyText
    representation_kind: Identifier
    required_forms: tuple[Form, ...] = Field(min_length=1)
    conditions: tuple[Identifier, ...] = Field(min_length=1)
    declared_omissions: tuple[NonEmptyText, ...] = ()

    @model_validator(mode="after")
    def references_are_unique(self) -> Self:
        require_unique(
            tuple(item.form_id for item in self.required_forms), "required forms"
        )
        require_unique(self.conditions, "projection conditions")
        return self


class Intuition(SemanticModel):
    """A singular Kantian-variant representation under sensible form."""

    intuition_id: Identifier
    presented_element_id: Identifier
    projection_id: Identifier
    episode_id: Identifier
    position: int
    content: tuple[ContentField, ...] = Field(min_length=1)
    form_ids: tuple[Identifier, ...] = Field(min_length=1)
    derivation: Derivation

    @model_validator(mode="after")
    def projection_is_substantive_and_traceable(self) -> Self:
        require_unique(self.form_ids, "form_ids")
        if not self.derivation.has_ground(
            self.presented_element_id, GroundKind.PRESENTED_ELEMENT
        ):
            raise ValueError("intuition must ground itself in a presented element")
        if not self.derivation.has_ground(
            self.projection_id, GroundKind.VARIANT_PROJECTION
        ):
            raise ValueError("intuition must name its variant projection as a ground")
        if self.episode_id != self.derivation.scope.episode_id:
            raise ValueError("intuition and derivation must share an episode")
        return self


class ManifoldOfIntuition(SemanticModel):
    """A bounded plurality available together for one synthesis attempt."""

    manifold_id: Identifier
    episode_id: Identifier
    intuition_ids: tuple[Identifier, ...] = Field(min_length=1)
    form_ids: tuple[Identifier, ...] = Field(min_length=1)
    derivation: Derivation

    @model_validator(mode="after")
    def intuitions_are_distinct_and_grounded(self) -> Self:
        require_unique(self.intuition_ids, "intuition_ids")
        require_unique(self.form_ids, "form_ids")
        missing = [
            intuition_id
            for intuition_id in self.intuition_ids
            if not self.derivation.has_ground(intuition_id, GroundKind.INTUITION)
        ]
        if missing:
            raise ValueError(f"manifold has ungrounded intuitions: {missing}")
        if self.episode_id != self.derivation.scope.episode_id:
            raise ValueError("manifold and derivation must share an episode")
        return self
