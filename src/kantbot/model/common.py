"""Shared immutable values used by every stage of the formal model."""

from enum import StrEnum
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

# This alias validates lexical form only.  A complete trace owns semantic
# identity, kind resolution, and evaluator-boundary checks.
Identifier = Annotated[
    str,
    Field(min_length=1, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$"),
]
NonEmptyText = Annotated[str, Field(min_length=1)]
ScalarValue = str | bool | int | float | None


class SemanticModel(BaseModel):
    """Strict, immutable base for canonical semantic values.

    Tuples and frozen child models are required because Pydantic's ``frozen``
    setting alone cannot make a mutable object nested in a field immutable.
    """

    model_config = ConfigDict(
        allow_inf_nan=False,
        extra="forbid",
        frozen=True,
        revalidate_instances="always",
        strict=True,
        validate_default=True,
    )


def require_unique(values: tuple[object, ...], field_name: str) -> None:
    """Reject duplicate immutable values with a domain-oriented error."""

    if len(values) != len(set(values)):
        raise ValueError(f"{field_name} must not contain duplicates")


class RuleAuthority(StrEnum):
    """What a rule may license, following ADR 0004."""

    CONSTITUTIVE = "constitutive"
    REGULATIVE = "regulative"
    ENGINEERING = "engineering"


class ConditionStatus(StrEnum):
    SATISFIED = "satisfied"
    FAILED = "failed"
    UNDECIDED = "undecided"


class FormKind(StrEnum):
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    OTHER = "other"


class GroundKind(StrEnum):
    """Kinds that may participate in cognitive provenance.

    Evaluator-only state is deliberately absent.  It has a separate type and
    therefore cannot enter a cognitive warrant by ordinary construction.
    """

    EXTERNAL_INPUT = "external-input"
    OBSERVATION = "observation"
    PRESENTED_ELEMENT = "presented-element"
    VARIANT_PROJECTION = "variant-projection"
    INTUITION = "intuition"
    MANIFOLD = "manifold"
    RETAINED_SEQUENCE = "retained-sequence"
    CANDIDATE_REPRESENTATION = "candidate-representation"
    OBJECT_CANDIDATE = "object-candidate"
    CONCEPT = "concept"
    SCHEMA = "schema"
    APPLICATION_RESULT = "application-result"
    JUDGMENT = "judgment"
    UNITY_CHECK = "unity-check"
    RULE = "rule"
    CONFIGURATION = "configuration"


class ConfigurationIdentity(SemanticModel):
    """Stable identity of the frozen configuration governing one cycle."""

    configuration_id: Identifier
    variant_id: Identifier
    revision: Annotated[int, Field(ge=1)] = 1


class Scope(SemanticModel):
    """The presentation boundary within which a claim may be licensed."""

    scope_id: Identifier
    episode_id: Identifier
    description: NonEmptyText
    presentation_conditions: tuple[NonEmptyText, ...] = Field(min_length=1)
    excluded_claims: tuple[NonEmptyText, ...] = ()


class ContentField(SemanticModel):
    """One named, scalar piece of supplied or carried content."""

    name: Identifier
    value: ScalarValue


class Form(SemanticModel):
    """A declared form under which presented content is ordered."""

    form_id: Identifier
    kind: FormKind
    description: NonEmptyText


class Rule(SemanticModel):
    """A named rule together with its authority and declared scope."""

    rule_id: Identifier
    name: NonEmptyText
    description: NonEmptyText
    authority: RuleAuthority
    scope: Scope


class Condition(SemanticModel):
    """A condition whose result remains explicit in later traces."""

    condition_id: Identifier
    description: NonEmptyText
    required: bool
    authority: RuleAuthority


class CognitiveGround(SemanticModel):
    """A typed reference that may be resolved as cognitive provenance.

    Local construction checks its declared kind and authority.  Only the
    complete-trace validator can prove that the identifier resolves to one
    canonical node of that kind and not to evaluator-only state.
    """

    ground_id: Identifier
    kind: GroundKind
    authority: RuleAuthority | None = None

    @model_validator(mode="after")
    def authority_belongs_only_to_rules(self) -> Self:
        if self.kind is GroundKind.RULE and self.authority is None:
            raise ValueError("rule grounds must declare their authority")
        if self.kind is not GroundKind.RULE and self.authority is not None:
            raise ValueError("only rule grounds may declare rule authority")
        return self


class ConditionResult(SemanticModel):
    condition_id: Identifier
    required: bool
    status: ConditionStatus
    explanation: NonEmptyText
    evidence: tuple[CognitiveGround, ...] = ()

    @model_validator(mode="after")
    def evidence_is_unique(self) -> Self:
        require_unique(
            tuple(item.ground_id for item in self.evidence), "condition evidence"
        )
        return self

    @property
    def passed(self) -> bool:
        """Whether this condition positively succeeded."""

        return self.status is ConditionStatus.SATISFIED


class EvaluatorReference(SemanticModel):
    """A hidden-world reference available only to external evaluation.

    It may be reported when diagnosing an authority violation, but it cannot
    resolve as a ``CognitiveGround`` in a valid complete trace.
    """

    evaluator_reference_id: Identifier
    description: NonEmptyText


class Derivation(SemanticModel):
    """Local provenance carried by one derived semantic value.

    The separate provenance package connects these records into a validated
    graph. This value intentionally does not claim graph closure.
    """

    operation: NonEmptyText
    grounds: tuple[CognitiveGround, ...] = Field(min_length=1)
    alternatives: tuple[Identifier, ...] = ()
    unmet_conditions: tuple[Identifier, ...] = ()
    scope: Scope
    configuration: ConfigurationIdentity

    @model_validator(mode="after")
    def references_are_unique(self) -> Self:
        require_unique(tuple(item.ground_id for item in self.grounds), "grounds")
        require_unique(self.alternatives, "alternatives")
        require_unique(self.unmet_conditions, "unmet_conditions")
        return self

    def has_ground(self, ground_id: str, kind: GroundKind | None = None) -> bool:
        """Query provenance without exposing mutable internal collections."""

        return any(
            ground.ground_id == ground_id and (kind is None or ground.kind is kind)
            for ground in self.grounds
        )
