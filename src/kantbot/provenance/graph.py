"""Validated immutable graph and the narrow cognitive lookup interface."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from graphlib import CycleError, TopologicalSorter
from types import MappingProxyType

from kantbot.model import (
    CandidateRepresentation,
    CognitiveGround,
    Concept,
    ConfigurationIdentity,
    Derivation,
    GroundKind,
    Rule,
    RuleAuthority,
    Schema,
    Scope,
)
from kantbot.provenance.format import ProvenanceTrace
from kantbot.provenance.references import alternatives_for, grounds_for, nested_models
from kantbot.provenance.registry import (
    Entry,
    InvalidProvenance,
    build_registry,
    require,
    resolves,
)
from kantbot.provenance.validation import (
    validate_applications,
    validate_commitments,
    validate_context,
    validate_outcomes,
    validate_proposals,
    validate_reception,
    validate_synthesis,
)

_SENSIBLE_DERIVATIVES = frozenset(
    {
        GroundKind.MANIFOLD,
        GroundKind.RETAINED_SEQUENCE,
        GroundKind.CANDIDATE_REPRESENTATION,
        GroundKind.OBJECT_CANDIDATE,
        GroundKind.APPLICATION_RESULT,
        GroundKind.JUDGMENT,
    }
)
_SYNTHESIS_KINDS = frozenset(
    {
        GroundKind.MANIFOLD,
        GroundKind.RETAINED_SEQUENCE,
        GroundKind.CANDIDATE_REPRESENTATION,
        GroundKind.OBJECT_CANDIDATE,
    }
)


def _edges(entries: dict[str, Entry]) -> dict[str, tuple[CognitiveGround, ...]]:
    edges: dict[str, tuple[CognitiveGround, ...]] = {}
    for entity_id, entry in entries.items():
        grounds = grounds_for(entry.value)
        for ground in grounds:
            require(
                resolves(entries.get(ground.ground_id), ground),
                f"{entity_id}: unresolved, mistyped, or unauthorized ground "
                f"{ground.ground_id!r}",
            )
        for alternative_id in alternatives_for(entry.value):
            alternative = entries.get(alternative_id)
            require(
                alternative is not None and alternative.kind is not None,
                f"{entity_id}: missing or non-cognitive alternative {alternative_id!r}",
            )
        edges[entity_id] = grounds
    return edges


def _ancestry(
    edges: dict[str, tuple[CognitiveGround, ...]],
) -> dict[str, frozenset[str]]:
    dependencies = {
        entity_id: tuple(ground.ground_id for ground in grounds)
        for entity_id, grounds in edges.items()
    }
    try:
        order = tuple(TopologicalSorter(dependencies).static_order())
    except CycleError as error:
        raise InvalidProvenance("circular evidence cannot ground a trace") from error
    ancestors: dict[str, frozenset[str]] = {}
    for entity_id in order:
        inherited = set(dependencies[entity_id])
        for parent in dependencies[entity_id]:
            inherited.update(ancestors[parent])
        ancestors[entity_id] = frozenset(inherited)
    return ancestors


def _validate_sensible_ancestry(
    entries: dict[str, Entry], ancestors: dict[str, frozenset[str]]
) -> None:
    for entity_id, entry in entries.items():
        if entry.kind in _SENSIBLE_DERIVATIVES:
            ancestor_kinds = {entries[item].kind for item in ancestors[entity_id]}
            require(
                {GroundKind.INTUITION, GroundKind.PRESENTED_ELEMENT} <= ancestor_kinds,
                f"{entity_id}: unreachable from a successful sensible projection",
            )


def _validate_committed_ancestry(
    trace: ProvenanceTrace,
    entries: dict[str, Entry],
    ancestors: dict[str, frozenset[str]],
) -> None:
    for judgment in trace.judgments:
        lineage = tuple(
            entries[item] for item in sorted(ancestors[judgment.judgment_id])
        )
        candidate_ids = {
            entry.entity_id
            for entry in lineage
            if isinstance(entry.value, CandidateRepresentation)
        }
        for entry in lineage:
            _validate_committed_ground(entry, candidate_ids)
        assembled = judgment.warrant.assembled
        application_lineage = ancestors[assembled.application_result_id]
        required_groups = (
            (_SYNTHESIS_KINDS, assembled.synthesis_grounds),
            (frozenset({GroundKind.OBSERVATION}), assembled.observation_grounds),
            (frozenset({GroundKind.VARIANT_PROJECTION}), assembled.projection_grounds),
        )
        for kinds, grounds in required_groups:
            required_ids = {
                item for item in application_lineage if entries[item].kind in kinds
            }
            require(
                required_ids <= {item.ground_id for item in grounds},
                "committed warrant omits required application ancestry",
            )


def _validate_committed_ground(entry: Entry, candidate_ids: set[str]) -> None:
    value = entry.value
    if isinstance(value, Rule | Concept | Schema):
        require(
            value.authority is RuleAuthority.CONSTITUTIVE,
            "non-constitutive authority in committed ancestry",
        )
    if isinstance(value, CandidateRepresentation):
        require(
            not (set(value.alternative_candidate_ids) & candidate_ids),
            "committed ancestry merges rival identity candidates",
        )
        require(
            not value.conflict_ids, "committed ancestry contains a candidate conflict"
        )
    for nested in nested_models(value):
        if isinstance(nested, Derivation):
            require(
                not nested.unmet_conditions,
                "committed ancestry contains unmet conditions",
            )


@dataclass(frozen=True)
class ProvenanceGraph:
    """A validated trace with immutable indexes implementing ``ProvenanceView``.

    This certifies structural provenance, not the correctness of a cognitive
    algorithm or the truth of its condition results. Construction always runs
    both canonical validation and the explicit graph-validation layer.
    """

    trace: ProvenanceTrace
    _entries: Mapping[str, Entry] = field(init=False, repr=False, compare=False)
    _grounds: Mapping[str, tuple[CognitiveGround, ...]] = field(
        init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        trace = ProvenanceTrace.model_validate(self.trace)
        validate_context(trace)
        entries = build_registry(trace)
        grounds = _edges(entries)
        ancestors = _ancestry(grounds)
        validate_reception(trace, entries)
        validate_synthesis(trace, entries)
        validate_applications(trace, entries)
        validate_proposals(trace, entries)
        validate_commitments(trace, entries)
        validate_outcomes(trace, entries)
        _validate_sensible_ancestry(entries, ancestors)
        _validate_committed_ancestry(trace, entries, ancestors)
        object.__setattr__(self, "trace", trace)
        object.__setattr__(self, "_entries", MappingProxyType(entries))
        object.__setattr__(self, "_grounds", MappingProxyType(grounds))

    def _cognitive_entry(self, entity_id: str) -> Entry:
        entry = self._entries.get(entity_id)
        if entry is None or entry.kind is None:
            raise KeyError(f"no cognitive entity: {entity_id}")
        return entry

    def resolves(self, ground: CognitiveGround, /) -> bool:
        """Resolve identity, actual cognitive kind, and declared rule authority."""

        return resolves(self._entries.get(ground.ground_id), ground)

    def immediate_grounds(self, entity_id: str, /) -> tuple[CognitiveGround, ...]:
        """Return all declared evidence links, never comparison alternatives."""

        self._cognitive_entry(entity_id)
        return self._grounds[entity_id]

    def scope_for(self, entity_id: str, /) -> Scope:
        """Return the validated scope, denying non-cognitive lookups."""

        self._cognitive_entry(entity_id)
        return self.trace.scope

    def configuration_for(self, entity_id: str, /) -> ConfigurationIdentity:
        """Return the frozen configuration, denying non-cognitive lookups."""

        self._cognitive_entry(entity_id)
        return self.trace.configuration


def validate_provenance(value: object) -> ProvenanceGraph:
    """Parse and validate Python data as a closed provenance graph."""

    return ProvenanceGraph(ProvenanceTrace.model_validate(value))


def validate_provenance_json(value: str | bytes) -> ProvenanceGraph:
    """Reject invalid shape and invalid references at the JSON trust boundary."""

    return ProvenanceGraph(ProvenanceTrace.model_validate_json(value))


def dump_provenance(graph: ProvenanceGraph) -> str:
    """Serialize a validated graph deterministically, without storage effects."""

    return graph.trace.model_dump_json()
