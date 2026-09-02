"""Ten distinct terminal outcomes and their mandatory limit context."""

from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import Field, TypeAdapter, model_validator

from kantbot.model.common import (
    ConfigurationIdentity,
    Derivation,
    EvaluatorReference,
    Identifier,
    NonEmptyText,
    RuleAuthority,
    Scope,
    SemanticModel,
    require_unique,
)
from kantbot.model.judgments import CommittedJudgment


class OutcomeKind(StrEnum):
    INPUT_ERROR = "input-error"
    NOT_PRESENTABLE = "not-presentable"
    SYNTHESIS_FAILED = "synthesis-failed"
    SYNTHESIS_AMBIGUOUS = "synthesis-ambiguous"
    CONCEPT_NOT_APPLICABLE = "concept-not-applicable"
    APPLICATION_UNDERDETERMINED = "application-underdetermined"
    UNITY_CONFLICT = "unity-conflict"
    JUDGMENT_WITHHELD = "judgment-withheld"
    JUDGMENT_COMMITTED = "judgment-committed"
    OVERREACH = "overreach"


class AuthorityViolation(SemanticModel):
    """An illicit promotion kept outside the successful warrant."""

    source_id: Identifier
    attempted_use: NonEmptyText
    explanation: NonEmptyText
    declared_authority: RuleAuthority | None = None
    evaluator_reference: EvaluatorReference | None = None

    @model_validator(mode="after")
    def violation_names_its_boundary(self) -> Self:
        if self.declared_authority is None and self.evaluator_reference is None:
            raise ValueError(
                "authority violation must name rule authority or evaluator state"
            )
        return self


class LimitReport(SemanticModel):
    """What remains unlicensed at one terminal boundary."""

    limit_report_id: Identifier
    strongest_licensed: OutcomeKind
    scope: Scope
    boundary: NonEmptyText
    missing_condition_ids: tuple[Identifier, ...] = ()
    conflict_ids: tuple[Identifier, ...] = ()
    alternative_ids: tuple[Identifier, ...] = ()
    authority_violations: tuple[AuthorityViolation, ...] = ()

    @model_validator(mode="after")
    def references_are_unique(self) -> Self:
        require_unique(self.missing_condition_ids, "missing_condition_ids")
        require_unique(self.conflict_ids, "conflict_ids")
        require_unique(self.alternative_ids, "alternative_ids")
        return self


class OutcomeContext(SemanticModel):
    """Configuration, provenance, scope, and limits shared by every outcome."""

    configuration: ConfigurationIdentity
    derivation: Derivation
    limit_report: LimitReport

    @model_validator(mode="after")
    def context_is_one_scoped_trace(self) -> Self:
        if self.configuration != self.derivation.configuration:
            raise ValueError("outcome and derivation require one configuration")
        if self.derivation.scope != self.limit_report.scope:
            raise ValueError("outcome derivation and limit report require one scope")
        return self


class _TerminalOutcomeBase(SemanticModel):
    outcome_id: Identifier
    kind: OutcomeKind
    context: OutcomeContext

    @model_validator(mode="after")
    def kind_matches_limit_report(self) -> Self:
        if self.kind is not self.context.limit_report.strongest_licensed:
            raise ValueError("outcome kind must match the strongest licensed status")
        return self


class InputError(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.INPUT_ERROR] = OutcomeKind.INPUT_ERROR
    invalid_input_ids: tuple[Identifier, ...] = Field(min_length=1)
    errors: tuple[NonEmptyText, ...] = Field(min_length=1)


class NotPresentable(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.NOT_PRESENTABLE] = OutcomeKind.NOT_PRESENTABLE
    presented_element_ids: tuple[Identifier, ...] = Field(min_length=1)
    failed_condition_ids: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def failed_conditions_appear_in_report(self) -> Self:
        if not set(self.failed_condition_ids) <= set(
            self.context.limit_report.missing_condition_ids
        ):
            raise ValueError("failed presentation conditions must appear in limits")
        return self


class SynthesisFailed(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.SYNTHESIS_FAILED] = OutcomeKind.SYNTHESIS_FAILED
    manifold_id: Identifier
    failed_rule_ids: tuple[Identifier, ...] = Field(min_length=1)


class SynthesisAmbiguous(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.SYNTHESIS_AMBIGUOUS] = OutcomeKind.SYNTHESIS_AMBIGUOUS
    candidate_representation_ids: tuple[Identifier, ...] = Field(min_length=2)

    @model_validator(mode="after")
    def candidates_appear_as_alternatives(self) -> Self:
        require_unique(
            self.candidate_representation_ids, "candidate_representation_ids"
        )
        if not set(self.candidate_representation_ids) <= set(
            self.context.limit_report.alternative_ids
        ):
            raise ValueError("ambiguous candidates must appear in limit alternatives")
        return self


class ConceptNotApplicable(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.CONCEPT_NOT_APPLICABLE] = (
        OutcomeKind.CONCEPT_NOT_APPLICABLE
    )
    object_candidate_id: Identifier
    application_result_id: Identifier
    failed_condition_ids: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def failed_conditions_appear_in_report(self) -> Self:
        if not set(self.failed_condition_ids) <= set(
            self.context.limit_report.missing_condition_ids
        ):
            raise ValueError("failed applicability conditions must appear in limits")
        return self


class ApplicationUnderdetermined(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.APPLICATION_UNDERDETERMINED] = (
        OutcomeKind.APPLICATION_UNDERDETERMINED
    )
    object_candidate_id: Identifier
    application_result_id: Identifier
    undecided_condition_ids: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def undecided_conditions_appear_in_report(self) -> Self:
        if not set(self.undecided_condition_ids) <= set(
            self.context.limit_report.missing_condition_ids
        ):
            raise ValueError("undecided applicability conditions must appear in limits")
        return self


class UnityConflict(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.UNITY_CONFLICT] = OutcomeKind.UNITY_CONFLICT
    proposed_judgment_id: Identifier
    conflict_ids: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def conflicts_appear_in_report(self) -> Self:
        if not set(self.conflict_ids) <= set(self.context.limit_report.conflict_ids):
            raise ValueError("unity conflicts must appear in the limit report")
        return self


class JudgmentWithheld(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.JUDGMENT_WITHHELD] = OutcomeKind.JUDGMENT_WITHHELD
    strongest_representation_ids: tuple[Identifier, ...] = Field(min_length=1)
    unmet_condition_ids: tuple[Identifier, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unmet_conditions_appear_in_report(self) -> Self:
        if not set(self.unmet_condition_ids) <= set(
            self.context.limit_report.missing_condition_ids
        ):
            raise ValueError("withheld conditions must appear in the limit report")
        return self


class JudgmentCommitted(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.JUDGMENT_COMMITTED] = OutcomeKind.JUDGMENT_COMMITTED
    judgment: CommittedJudgment

    @model_validator(mode="after")
    def judgment_matches_outcome_context(self) -> Self:
        report = self.context.limit_report
        if (
            report.missing_condition_ids
            or report.conflict_ids
            or report.authority_violations
        ):
            raise ValueError("committed outcome cannot retain a blocking limit")
        assembled = self.judgment.warrant.assembled
        if assembled.configuration != self.context.configuration:
            raise ValueError("committed judgment and outcome require one configuration")
        if assembled.scope != self.context.limit_report.scope:
            raise ValueError("committed judgment and outcome require one scope")
        if self.judgment.warrant.limit_report_id != (
            self.context.limit_report.limit_report_id
        ):
            raise ValueError("committed judgment must name the outcome limit report")
        return self


class Overreach(_TerminalOutcomeBase):
    kind: Literal[OutcomeKind.OVERREACH] = OutcomeKind.OVERREACH
    rejected_claim: NonEmptyText
    violations: tuple[AuthorityViolation, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def violations_appear_in_report(self) -> Self:
        if not set(self.violations) <= set(
            self.context.limit_report.authority_violations
        ):
            raise ValueError("overreach violations must appear in the limit report")
        return self


TerminalOutcome = Annotated[
    InputError
    | NotPresentable
    | SynthesisFailed
    | SynthesisAmbiguous
    | ConceptNotApplicable
    | ApplicationUnderdetermined
    | UnityConflict
    | JudgmentWithheld
    | JudgmentCommitted
    | Overreach,
    Field(discriminator="kind"),
]

_TERMINAL_OUTCOME_ADAPTER = TypeAdapter(TerminalOutcome)


def validate_terminal_outcome(value: object) -> TerminalOutcome:
    """Pure checked boundary from untrusted data to a typed outcome."""

    return _TERMINAL_OUTCOME_ADAPTER.validate_python(value)


def validate_terminal_outcome_json(value: str | bytes) -> TerminalOutcome:
    """Validate a JSON wire value while retaining strict scalar semantics."""

    return _TERMINAL_OUTCOME_ADAPTER.validate_json(value)


def dump_terminal_outcome(outcome: TerminalOutcome) -> str:
    """Return deterministic compact JSON without mutating the outcome."""

    return _TERMINAL_OUTCOME_ADAPTER.dump_json(outcome).decode("utf-8")
