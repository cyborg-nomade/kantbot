"""Extract declared graph edges without treating alternatives as evidence."""

from collections.abc import Iterator

from kantbot.model import (
    ApplicationResult,
    AssembledWarrant,
    CandidateRepresentation,
    CognitiveGround,
    CommittedJudgment,
    Derivation,
    GroundKind,
    LimitReport,
    RetainedSequence,
    Schema,
    SemanticModel,
)


def nested_models(value: SemanticModel) -> Iterator[SemanticModel]:
    """Walk only declared immutable model fields and tuple members, iteratively."""

    pending: list[object] = [value]
    while pending:
        current = pending.pop()
        if isinstance(current, SemanticModel):
            yield current
            pending.extend(
                getattr(current, name) for name in reversed(type(current).model_fields)
            )
        elif isinstance(current, tuple):
            pending.extend(reversed(current))


def reference(entity_id: str, kind: GroundKind) -> CognitiveGround:
    """Build a typed non-rule edge from an explicit canonical reference field."""

    return CognitiveGround(ground_id=entity_id, kind=kind)


def grounds_for(value: SemanticModel) -> tuple[CognitiveGround, ...]:
    """Include derivations, condition evidence, warrants, and direct ID links.

    Direct links such as retained intuition IDs are evidence too. Ignoring
    them would allow a broken reference to hide outside ``Derivation.grounds``.
    Repeated identical edges are normalized; conflicting kinds remain visible.
    """

    grounds = [
        item for item in nested_models(value) if isinstance(item, CognitiveGround)
    ]
    match value:
        case Schema():
            grounds.append(reference(value.concept_id, GroundKind.CONCEPT))
        case RetainedSequence():
            grounds.extend(
                reference(item.intuition_id, GroundKind.INTUITION)
                for item in value.items
            )
        case CandidateRepresentation():
            grounds.extend(
                reference(item, GroundKind.INTUITION) for item in value.intuition_ids
            )
        case CommittedJudgment():
            grounds.append(
                reference(
                    value.warrant.unity_check.unity_check_id, GroundKind.UNITY_CHECK
                )
            )
    return tuple(dict.fromkeys(grounds))


def alternatives_for(value: SemanticModel) -> tuple[str, ...]:
    """Collect comparison links separately from causal/evidence dependencies."""

    alternatives: list[str] = []
    for item in nested_models(value):
        match item:
            case Derivation():
                alternatives.extend(item.alternatives)
            case AssembledWarrant() | LimitReport():
                alternatives.extend(item.alternative_ids)
            case CandidateRepresentation():
                alternatives.extend(item.alternative_candidate_ids)
            case ApplicationResult():
                alternatives.extend(item.alternative_application_ids)
    return tuple(dict.fromkeys(alternatives))
