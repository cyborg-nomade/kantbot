"""Replay the sensible licenses for object formation and concept application."""

from kantbot.model import (
    CandidateRepresentation,
    Concept,
    Condition,
    ConditionResult,
    Form,
    FormKind,
    Intuition,
    ObjectCandidate,
    Rule,
    RuleAuthority,
    RuleKind,
    Schema,
    SensibleProcedure,
)
from kantbot.procedures import evaluate_procedure
from kantbot.provenance.format import ProvenanceTrace
from kantbot.provenance.registry import Entry, InvalidProvenance, lookup, require


def _require_constitutive(conditions: tuple[Condition, ...]) -> None:
    require(
        all(item.authority is RuleAuthority.CONSTITUTIVE for item in conditions),
        "object-level conditions must have constitutive authority",
    )


def _validate_temporal_form(
    procedure: SensibleProcedure, entries: dict[str, Entry]
) -> None:
    if procedure.temporal_form_id is not None:
        form = lookup(entries, procedure.temporal_form_id, Form)
        require(form.kind is FormKind.TEMPORAL, "procedure requires a temporal form")


def _intuitions(
    entries: dict[str, Entry], candidate: CandidateRepresentation
) -> tuple[Intuition, ...]:
    return tuple(lookup(entries, item, Intuition) for item in candidate.intuition_ids)


def _require_replayed_results(
    recorded: tuple[ConditionResult, ...], replayed: tuple[ConditionResult, ...]
) -> None:
    # Explanatory prose may vary, but neither status nor evidence may do so.
    def claims(results: tuple[ConditionResult, ...]) -> dict[str, object]:
        return {
            result.condition_id: (result.required, result.status, result.evidence)
            for result in results
        }

    require(
        claims(recorded) == claims(replayed),
        "condition results or sensible evidence disagree with procedure replay",
    )


def _rule_results(
    rule_ids: tuple[str, ...],
    kind: RuleKind,
    intuitions: tuple[Intuition, ...],
    trace: ProvenanceTrace,
    entries: dict[str, Entry],
) -> tuple[ConditionResult, ...]:
    results: list[ConditionResult] = []
    for rule_id in rule_ids:
        rule = lookup(entries, rule_id, Rule)
        require(rule.kind is kind, "synthesis rule has the wrong licensing role")
        _require_constitutive(rule.conditions)
        procedure = rule.sensible_procedure
        if procedure is None:
            raise InvalidProvenance("object-licensing rule lacks a sensible procedure")
        results.extend(
            evaluate_procedure(procedure, rule.conditions, intuitions, trace.forms)
        )
    require(
        len({item.condition_id for item in results}) == len(results),
        "selected rules reuse a condition identity",
    )
    return tuple(results)


def validate_sensible_licenses(
    trace: ProvenanceTrace, entries: dict[str, Entry]
) -> None:
    """Reject self-certified licenses even when their graph references resolve."""

    for rule in trace.rules:
        if rule.sensible_procedure is not None:
            _validate_temporal_form(rule.sensible_procedure, entries)
    for schema in trace.schemas:
        concept = lookup(entries, schema.concept_id, Concept)
        try:
            schema.validate_concept(concept)
        except ValueError as error:
            raise InvalidProvenance(str(error)) from error
        _validate_temporal_form(schema.procedure, entries)
    for obj in trace.object_candidates:
        candidate = lookup(
            entries, obj.candidate_representation_id, CandidateRepresentation
        )
        intuitions = _intuitions(entries, candidate)
        identity = _rule_results(
            candidate.identity_rule_ids, RuleKind.IDENTITY, intuitions, trace, entries
        )
        constitutive = _rule_results(
            candidate.constitutive_rule_ids,
            RuleKind.CATEGORY_INSPIRED,
            intuitions,
            trace,
            entries,
        )
        _require_replayed_results(obj.identity_results, identity)
        _require_replayed_results(obj.constitutive_results, constitutive)
    for application in trace.applications:
        obj = lookup(entries, application.object_candidate_id, ObjectCandidate)
        candidate = lookup(
            entries, obj.candidate_representation_id, CandidateRepresentation
        )
        concept = lookup(entries, application.concept_id, Concept)
        schema = lookup(entries, application.schema_id, Schema)
        require(
            concept.authority is RuleAuthority.CONSTITUTIVE
            and schema.authority is RuleAuthority.CONSTITUTIVE,
            "application resources must have constitutive authority",
        )
        _require_constitutive(concept.applicability_conditions)
        replayed = evaluate_procedure(
            schema.procedure,
            concept.applicability_conditions,
            _intuitions(entries, candidate),
            trace.forms,
        )
        _require_replayed_results(application.condition_results, replayed)
