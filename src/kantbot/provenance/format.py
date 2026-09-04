"""Versioned immutable wire format; graph validation is a separate layer."""

from typing import Literal

from kantbot.model import (
    ApplicationResult,
    CandidateRepresentation,
    CommittedJudgment,
    Concept,
    ConfigurationIdentity,
    EvaluatorReference,
    Form,
    Intuition,
    LimitReport,
    ManifoldOfIntuition,
    ObjectCandidate,
    Observation,
    PresentedElement,
    ProposedJudgment,
    RetainedSequence,
    Rule,
    Schema,
    Scope,
    SemanticModel,
    TerminalOutcome,
    UnityCheck,
    VariantProjection,
)
from kantbot.model.common import Identifier, NonEmptyText


class ExternalInputReference(SemanticModel):
    """Identity of supplied input, including a record rejected before parsing."""

    input_id: Identifier
    description: NonEmptyText


class ProvenanceTrace(SemanticModel):
    """A closed trace prefix or terminal trace of one configured cycle.

    Named, typed collections reuse canonical values rather than introducing a
    second ontology of node payloads. Construction proves local shape only;
    use ``ProvenanceGraph`` to validate references and cross-node constraints.
    Collection order is preserved for deterministic round trips, not treated
    as execution order. Observation position and derivations own that meaning.
    """

    format_version: Literal[1] = 1
    cycle_id: Identifier
    scope: Scope
    configuration: ConfigurationIdentity
    external_inputs: tuple[ExternalInputReference, ...] = ()
    observations: tuple[Observation, ...] = ()
    forms: tuple[Form, ...] = ()
    projections: tuple[VariantProjection, ...] = ()
    rules: tuple[Rule, ...] = ()
    concepts: tuple[Concept, ...] = ()
    schemas: tuple[Schema, ...] = ()
    presented_elements: tuple[PresentedElement, ...] = ()
    intuitions: tuple[Intuition, ...] = ()
    manifolds: tuple[ManifoldOfIntuition, ...] = ()
    retained_sequences: tuple[RetainedSequence, ...] = ()
    candidates: tuple[CandidateRepresentation, ...] = ()
    object_candidates: tuple[ObjectCandidate, ...] = ()
    applications: tuple[ApplicationResult, ...] = ()
    proposals: tuple[ProposedJudgment, ...] = ()
    unity_checks: tuple[UnityCheck, ...] = ()
    judgments: tuple[CommittedJudgment, ...] = ()
    limit_reports: tuple[LimitReport, ...] = ()
    outcomes: tuple[TerminalOutcome, ...] = ()
    evaluator_references: tuple[EvaluatorReference, ...] = ()
