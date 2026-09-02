"""Propositions, proposed judgments, and licensed commitments."""

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from kantbot.model.common import (
    CognitiveGround,
    ConditionResult,
    ConditionStatus,
    ConfigurationIdentity,
    Derivation,
    GroundKind,
    Identifier,
    NonEmptyText,
    RuleAuthority,
    Scope,
    SemanticModel,
    require_unique,
)


class Modality(StrEnum):
    PROBLEMATIC = "problematic"
    ASSERTORIC = "assertoric"
    APODICTIC = "apodictic"


class Proposition(SemanticModel):
    subject_candidate_id: Identifier
    predicate_concept_id: Identifier
    text: NonEmptyText
    modality: Modality


class AssembledWarrant(SemanticModel):
    """The grounds available to a proposal before cycle-wide unity passes."""

    observation_grounds: tuple[CognitiveGround, ...] = Field(min_length=1)
    presentation_form_ids: tuple[Identifier, ...] = Field(min_length=1)
    projection_grounds: tuple[CognitiveGround, ...] = Field(min_length=1)
    synthesis_grounds: tuple[CognitiveGround, ...] = Field(min_length=1)
    identity_rule_grounds: tuple[CognitiveGround, ...] = Field(min_length=1)
    concept_ground: CognitiveGround
    schema_ground: CognitiveGround
    application_ground: CognitiveGround
    constitutive_rule_grounds: tuple[CognitiveGround, ...] = Field(min_length=1)
    alternative_ids: tuple[Identifier, ...] = ()
    scope: Scope
    configuration: ConfigurationIdentity

    @model_validator(mode="after")
    def warrant_references_are_unique(self) -> Self:
        ground_groups = {
            "observation_grounds": self.observation_grounds,
            "projection_grounds": self.projection_grounds,
            "synthesis_grounds": self.synthesis_grounds,
            "identity_rule_grounds": self.identity_rule_grounds,
            "constitutive_rule_grounds": self.constitutive_rule_grounds,
        }
        for field_name, grounds in ground_groups.items():
            require_unique(
                tuple(item.ground_id for item in grounds),
                field_name,
            )
        require_unique(self.presentation_form_ids, "presentation_form_ids")
        require_unique(self.alternative_ids, "alternative_ids")

        expected_kinds = (
            (self.observation_grounds, {GroundKind.OBSERVATION}),
            (self.projection_grounds, {GroundKind.VARIANT_PROJECTION}),
            (
                self.synthesis_grounds,
                {
                    GroundKind.MANIFOLD,
                    GroundKind.RETAINED_SEQUENCE,
                    GroundKind.CANDIDATE_REPRESENTATION,
                    GroundKind.OBJECT_CANDIDATE,
                },
            ),
            (self.identity_rule_grounds, {GroundKind.RULE}),
            (self.constitutive_rule_grounds, {GroundKind.RULE}),
        )
        if any(
            ground.kind not in allowed
            for grounds, allowed in expected_kinds
            for ground in grounds
        ):
            raise ValueError("warrant ground appears in the wrong semantic role")
        if self.concept_ground.kind is not GroundKind.CONCEPT:
            raise ValueError("concept_ground must identify a concept")
        if self.schema_ground.kind is not GroundKind.SCHEMA:
            raise ValueError("schema_ground must identify a schema")
        if self.application_ground.kind is not GroundKind.APPLICATION_RESULT:
            raise ValueError("application_ground must identify an application result")
        if any(
            ground.authority is not RuleAuthority.CONSTITUTIVE
            for ground in self.identity_rule_grounds + self.constitutive_rule_grounds
        ):
            raise ValueError("object-level warrant rules must be constitutive")
        return self

    @property
    def concept_id(self) -> str:
        return self.concept_ground.ground_id

    @property
    def application_result_id(self) -> str:
        return self.application_ground.ground_id


class UnityCheck(SemanticModel):
    """Cycle-wide unity result; it is not a simulated self."""

    unity_check_id: Identifier
    status: ConditionStatus
    condition_results: tuple[ConditionResult, ...] = Field(min_length=1)
    conflict_ids: tuple[Identifier, ...] = ()
    scope: Scope
    configuration: ConfigurationIdentity

    @model_validator(mode="after")
    def status_matches_conditions(self) -> Self:
        require_unique(
            tuple(item.condition_id for item in self.condition_results),
            "unity condition IDs",
        )
        require_unique(self.conflict_ids, "unity conflict IDs")
        required = tuple(item for item in self.condition_results if item.required)
        if not required:
            raise ValueError("unity check requires at least one required condition")
        if self.status is ConditionStatus.UNDECIDED:
            raise ValueError(
                "unity check must either satisfy unity or identify conflict"
            )
        if self.status is ConditionStatus.SATISFIED:
            if self.conflict_ids or any(not item.passed for item in required):
                raise ValueError(
                    "successful unity requires all conditions and no conflict"
                )
        elif not self.conflict_ids and all(item.passed for item in required):
            raise ValueError("failed unity must expose a failed condition or conflict")
        return self

    @property
    def passed(self) -> bool:
        return self.status is ConditionStatus.SATISFIED


class CompleteWarrant(SemanticModel):
    """An assembled warrant completed by unity and limit-report identity."""

    assembled: AssembledWarrant
    unity_check: UnityCheck
    limit_report_id: Identifier

    @model_validator(mode="after")
    def commitment_fields_are_compatible(self) -> Self:
        if not self.unity_check.passed:
            raise ValueError("complete warrant requires a successful unity check")
        if self.assembled.configuration != self.unity_check.configuration:
            raise ValueError("warrant and unity check require one configuration")
        if self.assembled.scope != self.unity_check.scope:
            raise ValueError("warrant and unity check require one scope")
        return self


class ProposedJudgment(SemanticModel):
    """A structured proposition that still lacks authority to commit."""

    proposed_judgment_id: Identifier
    proposition: Proposition
    warrant: AssembledWarrant
    derivation: Derivation

    @model_validator(mode="after")
    def proposal_matches_its_warrant(self) -> Self:
        if self.proposition.predicate_concept_id != self.warrant.concept_id:
            raise ValueError("proposition predicate and warrant concept must match")
        if not self.derivation.has_ground(
            self.proposition.subject_candidate_id, GroundKind.OBJECT_CANDIDATE
        ):
            raise ValueError("proposal must ground its subject object candidate")
        if not self.derivation.has_ground(
            self.warrant.application_result_id, GroundKind.APPLICATION_RESULT
        ):
            raise ValueError("proposal must ground its application result")
        if self.warrant.scope != self.derivation.scope:
            raise ValueError("proposal warrant and derivation require one scope")
        if self.warrant.configuration != self.derivation.configuration:
            raise ValueError(
                "proposal warrant and derivation require one configuration"
            )
        return self


class CommittedJudgment(SemanticModel):
    """A scoped proposition whose complete warrant licenses commitment."""

    judgment_id: Identifier
    proposed_judgment_id: Identifier
    proposition: Proposition
    warrant: CompleteWarrant
    derivation: Derivation

    @model_validator(mode="after")
    def commitment_is_traceable(self) -> Self:
        assembled = self.warrant.assembled
        if self.proposition.predicate_concept_id != assembled.concept_id:
            raise ValueError("committed predicate and warrant concept must match")
        if not self.derivation.has_ground(
            self.proposed_judgment_id, GroundKind.JUDGMENT
        ):
            raise ValueError("commitment must ground itself in the proposal")
        if assembled.scope != self.derivation.scope:
            raise ValueError("commitment warrant and derivation require one scope")
        if assembled.configuration != self.derivation.configuration:
            raise ValueError(
                "commitment warrant and derivation require one configuration"
            )
        return self
