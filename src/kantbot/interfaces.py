"""Side-effect-free contracts between the first cycle's cognitive roles.

The protocols describe operations, not stateful faculty objects.  A plain
function satisfies one of these contracts when its signature does, so later
implementations need neither inheritance nor hidden mutable context.
"""

from typing import Protocol, Self

from pydantic import Field, model_validator

from kantbot.model import (
    ApplicationResult,
    AssembledWarrant,
    CandidateRepresentation,
    CommittedJudgment,
    Concept,
    ConditionResult,
    ConfigurationIdentity,
    Derivation,
    Intuition,
    JudgmentWithheld,
    LimitReport,
    ManifoldOfIntuition,
    NotPresentable,
    ObjectCandidate,
    Observation,
    Overreach,
    PresentedElement,
    ProposedJudgment,
    Proposition,
    RetainedSequence,
    Rule,
    RuleAuthority,
    Schema,
    Scope,
    SemanticModel,
    SynthesisAmbiguous,
    SynthesisFailed,
    SynthesisPolicy,
    TerminalOutcome,
    UnityCheck,
    UnityConflict,
    VariantProjection,
)
from kantbot.model.common import CognitiveGround, Identifier, require_unique


class UnderstandingRepertoire(SemanticModel):
    """The concepts and constitutive rules available to one cycle.

    Supplying this value is the understanding role's only interface here.  The
    value does not inspect observations or declare any concept applicable.
    """

    rules: tuple[Rule, ...] = Field(min_length=1)
    concepts: tuple[Concept, ...] = Field(min_length=1)
    schemas: tuple[Schema, ...] = Field(min_length=1)
    scope: Scope
    configuration: ConfigurationIdentity

    @model_validator(mode="after")
    def identities_are_unique(self) -> Self:
        require_unique(tuple(rule.rule_id for rule in self.rules), "rule IDs")
        require_unique(
            tuple(concept.concept_id for concept in self.concepts), "concept IDs"
        )
        require_unique(tuple(schema.schema_id for schema in self.schemas), "schema IDs")
        return self

    @model_validator(mode="after")
    def resources_are_constitutive(self) -> Self:
        has_nonconstitutive_resource = (
            any(rule.authority is not RuleAuthority.CONSTITUTIVE for rule in self.rules)
            or any(
                concept.authority is not RuleAuthority.CONSTITUTIVE
                for concept in self.concepts
            )
            or any(
                schema.authority is not RuleAuthority.CONSTITUTIVE
                for schema in self.schemas
            )
        )
        if has_nonconstitutive_resource:
            raise ValueError("understanding resources must be constitutive")
        return self

    @model_validator(mode="after")
    def schemas_refer_to_declared_concepts_and_conditions(self) -> Self:
        concepts = {concept.concept_id: concept for concept in self.concepts}
        for schema in self.schemas:
            concept = concepts.get(schema.concept_id)
            if concept is None:
                raise ValueError(
                    f"schema {schema.schema_id!r} refers to an unavailable concept"
                )
            available_conditions = {
                condition.condition_id for condition in concept.applicability_conditions
            }
            missing_conditions = set(schema.condition_ids) - available_conditions
            if missing_conditions:
                raise ValueError(
                    f"schema {schema.schema_id!r} has unavailable conditions: "
                    f"{sorted(missing_conditions)}"
                )
        return self

    @model_validator(mode="after")
    def resources_share_the_cycle_scope(self) -> Self:
        has_mismatched_scope = (
            any(rule.scope != self.scope for rule in self.rules)
            or any(concept.scope != self.scope for concept in self.concepts)
            or any(schema.scope != self.scope for schema in self.schemas)
        )
        if has_mismatched_scope:
            raise ValueError("understanding resources must share one cycle scope")
        return self


class ProvenanceView(Protocol):
    """Read-only graph capabilities required by downstream roles.

    The separate provenance package supplies the concrete validated graph.
    This boundary exposes no evaluator-reference lookup.
    """

    def resolves(self, ground: CognitiveGround, /) -> bool:
        """Return whether a cognitive ground resolves with its declared kind."""

        ...

    def immediate_grounds(
        self, entity_id: Identifier, /
    ) -> tuple[CognitiveGround, ...]:
        """Return the entity's cognitive grounds without permitting mutation."""

        ...

    def scope_for(self, entity_id: Identifier, /) -> Scope:
        """Return the registered scope for an entity."""

        ...

    def configuration_for(self, entity_id: Identifier, /) -> ConfigurationIdentity:
        """Return the registered configuration for an entity."""

        ...


type ProjectionResult = Intuition | NotPresentable
type RetentionResult = RetainedSequence | SynthesisFailed
type RecognitionResult = (
    tuple[CandidateRepresentation, ...] | SynthesisFailed | SynthesisAmbiguous
)
type ObjectFormationResult = ObjectCandidate | SynthesisFailed
type ProposalResult = ProposedJudgment | JudgmentWithheld
type UnityResult = UnityCheck | UnityConflict | Overreach
type CommitmentResult = CommittedJudgment | JudgmentWithheld


class RoleContext(SemanticModel):
    """The explicit scope and frozen configuration supplied to an operation."""

    scope: Scope
    configuration: ConfigurationIdentity


class ReceptionRequest(SemanticModel):
    observation: Observation
    context: RoleContext


class ProjectionRequest(SemanticModel):
    presented_element: PresentedElement
    projection: VariantProjection
    context: RoleContext


class ManifoldRequest(SemanticModel):
    intuitions: tuple[Intuition, ...] = Field(min_length=1)
    context: RoleContext


class RetentionRequest(SemanticModel):
    manifold: ManifoldOfIntuition
    intuitions: tuple[Intuition, ...] = Field(min_length=1)
    retention_rule: Rule
    context: RoleContext


class RecognitionRequest(SemanticModel):
    retained_sequence: RetainedSequence
    identity_rules: tuple[Rule, ...] = Field(min_length=1)
    constitutive_rules: tuple[Rule, ...] = Field(min_length=1)
    policy: SynthesisPolicy
    context: RoleContext


class ObjectFormationRequest(SemanticModel):
    candidate: CandidateRepresentation
    identity_results: tuple[ConditionResult, ...] = Field(min_length=1)
    constitutive_results: tuple[ConditionResult, ...] = Field(min_length=1)
    context: RoleContext


class ApplicationRequest(SemanticModel):
    object_candidate: ObjectCandidate
    concept: Concept
    concept_schema: Schema
    context: RoleContext


class ProposalRequest(SemanticModel):
    object_candidate: ObjectCandidate
    application: ApplicationResult
    proposition: Proposition
    warrant: AssembledWarrant
    context: RoleContext


class UnityRequest(SemanticModel):
    proposal: ProposedJudgment
    context: RoleContext


class CommitmentRequest(SemanticModel):
    proposal: ProposedJudgment
    unity_check: UnityCheck
    limit_report: LimitReport
    derivation: Derivation
    context: RoleContext


class PresentObservation(Protocol):
    """Shared reception: valid observation to minimally presented element."""

    def __call__(self, request: ReceptionRequest, /) -> PresentedElement: ...


class ProjectIntuition(Protocol):
    """Sensibility: apply one substantive variant projection."""

    def __call__(self, request: ProjectionRequest, /) -> ProjectionResult: ...


class FormManifold(Protocol):
    """Sensibility: make projected intuitions available as one manifold."""

    def __call__(self, request: ManifoldRequest, /) -> ManifoldOfIntuition: ...


class SupplyUnderstanding(Protocol):
    """Understanding: supply a frozen repertoire without applying it."""

    def __call__(self, context: RoleContext, /) -> UnderstandingRepertoire: ...


class RetainIntuitions(Protocol):
    """Imagination: retain intuitions only under a supplied rule."""

    def __call__(self, request: RetentionRequest, /) -> RetentionResult: ...


class RecognizeCandidates(Protocol):
    """Imagination under understanding: propose unity without objecthood."""

    def __call__(
        self,
        request: RecognitionRequest,
        provenance: ProvenanceView,
        /,
    ) -> RecognitionResult: ...


class ConstituteObject(Protocol):
    """License an object candidate only from passing local conditions."""

    def __call__(
        self,
        request: ObjectFormationRequest,
        provenance: ProvenanceView,
        /,
    ) -> ObjectFormationResult: ...


class ApplyConcept(Protocol):
    """Power of judgment: test one concept through its schema."""

    def __call__(
        self,
        request: ApplicationRequest,
        provenance: ProvenanceView,
        /,
    ) -> ApplicationResult: ...


class ProposeJudgment(Protocol):
    """Assemble a proposition without granting it committed status."""

    def __call__(self, request: ProposalRequest, /) -> ProposalResult: ...


class CheckUnity(Protocol):
    """Apperception: check a proposal against its entire provenance view."""

    def __call__(
        self,
        request: UnityRequest,
        provenance: ProvenanceView,
        /,
    ) -> UnityResult: ...


class CommitJudgment(Protocol):
    """Commit only a proposal accompanied by successful unity and limits."""

    def __call__(self, request: CommitmentRequest, /) -> CommitmentResult: ...


class CritiqueAndReport(Protocol):
    """Expose one validated terminal outcome without inventing new grounds."""

    def __call__(self, outcome: TerminalOutcome, /) -> str: ...
