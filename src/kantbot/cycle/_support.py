"""Small checked constructors shared by the cycle's pure operations."""

from kantbot.interfaces import RoleContext
from kantbot.model import (
    CognitiveGround,
    Derivation,
    GroundKind,
    LimitReport,
    OutcomeContext,
    OutcomeKind,
    Rule,
    SemanticModel,
)
from kantbot.provenance import ProvenanceTrace


def ground(entity_id: str, kind: GroundKind) -> CognitiveGround:
    return CognitiveGround(ground_id=entity_id, kind=kind)


def rule_ground(rule: Rule) -> CognitiveGround:
    return CognitiveGround(
        ground_id=rule.rule_id, kind=GroundKind.RULE, authority=rule.authority
    )


def derive(
    context: RoleContext,
    operation: str,
    grounds: tuple[CognitiveGround, ...],
    alternatives: tuple[str, ...] = (),
    missing: tuple[str, ...] = (),
) -> Derivation:
    return Derivation(
        operation=operation,
        grounds=tuple(dict.fromkeys(grounds)),
        alternatives=alternatives,
        unmet_conditions=missing,
        scope=context.scope,
        configuration=context.configuration,
    )


def outcome_context(
    context: RoleContext,
    kind: OutcomeKind,
    label: str,
    grounds: tuple[CognitiveGround, ...],
    *,
    missing: tuple[str, ...] = (),
) -> OutcomeContext:
    return OutcomeContext(
        configuration=context.configuration,
        derivation=derive(context, label, grounds, missing=missing),
        limit_report=LimitReport(
            limit_report_id=f"limit:{label}",
            strongest_licensed=kind,
            scope=context.scope,
            boundary=label,
            missing_condition_ids=missing,
        ),
    )


def replace_value[T: SemanticModel](value: T, **updates: object) -> T:
    """Revalidate edits; Pydantic's unchecked copy API is not used."""

    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def extend_trace(
    trace: ProvenanceTrace, **collections: tuple[SemanticModel, ...]
) -> ProvenanceTrace:
    """Construct a fresh prefix; the caller validates its graph before use."""

    updates = {
        name: (*getattr(trace, name), *values) for name, values in collections.items()
    }
    return replace_value(trace, **updates)
