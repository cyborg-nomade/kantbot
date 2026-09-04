"""One semantic identity namespace, with no evaluator-to-cognitive coercion."""

from dataclasses import dataclass

from kantbot.model import (
    ApplicationResult,
    ApplicationUnderdetermined,
    CandidateRepresentation,
    CognitiveGround,
    CommittedJudgment,
    Concept,
    ConceptNotApplicable,
    ConfigurationIdentity,
    EvaluatorReference,
    Form,
    GroundKind,
    InputError,
    Intuition,
    JudgmentCommitted,
    JudgmentWithheld,
    LimitReport,
    ManifoldOfIntuition,
    NotPresentable,
    ObjectCandidate,
    Observation,
    Overreach,
    PresentedElement,
    ProposedJudgment,
    RetainedSequence,
    Rule,
    Schema,
    Scope,
    SemanticModel,
    SynthesisAmbiguous,
    SynthesisFailed,
    UnityCheck,
    UnityConflict,
    VariantProjection,
)
from kantbot.provenance.format import ExternalInputReference, ProvenanceTrace
from kantbot.provenance.references import nested_models


class InvalidProvenance(ValueError):
    """Locally valid records cannot form the claimed closed provenance graph."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidProvenance(message)


# Explicit canonical type routing; no caller-supplied kind or identifier can
# relabel a value. Non-cognitive entries reserve identity but never resolve as
# CognitiveGround (even when an evaluator guesses a legitimate-looking kind).
_IDENTITIES: dict[type[SemanticModel], tuple[str, GroundKind | None]] = {
    ExternalInputReference: ("input_id", GroundKind.EXTERNAL_INPUT),
    Observation: ("observation_id", GroundKind.OBSERVATION),
    PresentedElement: ("presented_element_id", GroundKind.PRESENTED_ELEMENT),
    VariantProjection: ("projection_id", GroundKind.VARIANT_PROJECTION),
    Intuition: ("intuition_id", GroundKind.INTUITION),
    ManifoldOfIntuition: ("manifold_id", GroundKind.MANIFOLD),
    RetainedSequence: ("retained_sequence_id", GroundKind.RETAINED_SEQUENCE),
    CandidateRepresentation: (
        "candidate_representation_id",
        GroundKind.CANDIDATE_REPRESENTATION,
    ),
    ObjectCandidate: ("object_candidate_id", GroundKind.OBJECT_CANDIDATE),
    Concept: ("concept_id", GroundKind.CONCEPT),
    Schema: ("schema_id", GroundKind.SCHEMA),
    ApplicationResult: ("application_result_id", GroundKind.APPLICATION_RESULT),
    ProposedJudgment: ("proposed_judgment_id", GroundKind.JUDGMENT),
    CommittedJudgment: ("judgment_id", GroundKind.JUDGMENT),
    UnityCheck: ("unity_check_id", GroundKind.UNITY_CHECK),
    Rule: ("rule_id", GroundKind.RULE),
    ConfigurationIdentity: ("configuration_id", GroundKind.CONFIGURATION),
    Scope: ("scope_id", None),
    Form: ("form_id", None),
    LimitReport: ("limit_report_id", None),
    EvaluatorReference: ("evaluator_reference_id", None),
    InputError: ("outcome_id", None),
    NotPresentable: ("outcome_id", None),
    SynthesisFailed: ("outcome_id", None),
    SynthesisAmbiguous: ("outcome_id", None),
    ConceptNotApplicable: ("outcome_id", None),
    ApplicationUnderdetermined: ("outcome_id", None),
    UnityConflict: ("outcome_id", None),
    JudgmentWithheld: ("outcome_id", None),
    JudgmentCommitted: ("outcome_id", None),
    Overreach: ("outcome_id", None),
}


@dataclass(frozen=True)
class Entry:
    entity_id: str
    kind: GroundKind | None
    value: SemanticModel


def entry_for(value: SemanticModel) -> Entry:
    field_name, kind = _IDENTITIES[type(value)]
    entity_id: str = getattr(value, field_name)
    return Entry(entity_id, kind, value)


def build_registry(trace: ProvenanceTrace) -> dict[str, Entry]:
    """Register each top-level entity once; embedded copies must agree exactly."""

    entries: dict[str, Entry] = {}
    for name in type(trace).model_fields:
        field: object = getattr(trace, name)
        values: tuple[object, ...] = (field,)
        if isinstance(field, tuple):
            values = field
        for value in values:
            if isinstance(value, SemanticModel):
                entry = entry_for(value)
                require(
                    entry.entity_id not in entries,
                    f"duplicate identity: {entry.entity_id}",
                )
                entries[entry.entity_id] = entry

    for value in nested_models(trace):
        if type(value) in _IDENTITIES:
            entry = entry_for(value)
            require(
                entries.get(entry.entity_id) == entry,
                f"unregistered or incompatible embedded entity: {entry.entity_id}",
            )
    return entries


def lookup[T: SemanticModel](
    entries: dict[str, Entry], entity_id: str, expected: type[T]
) -> T:
    entry = entries.get(entity_id)
    if entry is None or not isinstance(entry.value, expected):
        raise InvalidProvenance(f"{entity_id!r} must resolve as {expected.__name__}")
    return entry.value


def resolves(entry: Entry | None, ground: CognitiveGround) -> bool:
    if entry is None or entry.kind is None or entry.kind is not ground.kind:
        return False
    if isinstance(entry.value, Rule):
        return entry.value.authority is ground.authority
    return True
