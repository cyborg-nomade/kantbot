# Structured Provenance

## Status and scope

This is the fourth Phase 2 deliverable: a versioned, immutable trace format and
a separately validated graph in [`kantbot.provenance`](src/kantbot/provenance).
It implements the identity contract in the
[canonical structures](CANONICAL_DATA_STRUCTURES.md#identity-and-reference-integrity)
and the already accepted [`ProvenanceView`](ROLE_INTERFACES.md#provenance-and-evaluator-boundary).

**Engineering.** This operationalizes [K-022](CLAIMS.md#k-022), the typed limits
of [K-023](CLAIMS.md#k-023), and the graph-validation boundary accepted in
[ADR 0006](docs/decisions/0006-canonical-model-representation.md#decision).
It introduces no new reading of Kant. Rules, representations, and licensing
remain governed by ADRs [0001–0004](docs/decisions/README.md#index).

The graph checks structural provenance. It does not implement the cognitive
roles, determine whether a reported condition is true, prove a proposition's
modality, or replace the cycle-wide unity policy. Property-based tests and the
deterministic toy world remain separate Roadmap items.

## Two validation boundaries

```text
Python data or JSON
        |
        v
ProvenanceTrace — canonical, strict, immutable record shape
        |
        v
ProvenanceGraph — identity, typed links, context, evidence DAG, licensing checks
        |
        +--> ProvenanceView — cognitive lookup only
        +--> dump_provenance — deterministic JSON for inspection and storage
```

`ProvenanceTrace` construction checks canonical shape, not graph closure.
`ProvenanceGraph` always revalidates that shape and then applies the separate
graph validators. `validate_provenance` and `validate_provenance_json` perform
both steps at the trust boundary. Shape errors raise Pydantic validation errors;
cross-node errors raise `InvalidProvenance` with the offending identity or
constraint. Neither is a cognitive refusal: those remain typed outcomes stored
inside valid traces.

For an adapter receiving serialized trace data, the complete boundary is:

```python
from kantbot.provenance import dump_provenance, validate_provenance_json


def checked_trace_json(received_json: str) -> str:
    graph = validate_provenance_json(received_json)
    return dump_provenance(graph)
```

Invalid data raises at validation; a successful result can also be passed to a
role expecting `ProvenanceView`. The complete fixture in the
[provenance tests](tests/test_provenance.py) shows how to register a trace from
canonical Python values.

## Format version 1

The envelope contains `format_version`, `cycle_id`, one `Scope`, and one
`ConfigurationIdentity`. Its immutable tuples register canonical values by
their existing semantic IDs:

| Collections | Purpose |
| --- | --- |
| `external_inputs`, `observations` | Supplied input identities and parsed content; malformed input can be referenced without pretending it is an observation |
| `forms`, `projections`, `rules`, `concepts`, `schemas` | Frozen interpretive and constitutive resources |
| `presented_elements`, `intuitions`, `manifolds` | Shared reception and substantive variant projection |
| `retained_sequences`, `candidates`, `object_candidates` | Retention, alternative identities, and local object formation |
| `applications`, `proposals`, `unity_checks`, `judgments` | Separate applicability, proposal, unity, and commitment evidence |
| `limit_reports`, `outcomes` | Explicit boundaries and all ten terminal kinds |
| `evaluator_references` | Diagnostic identities only; never cognitive grounds |

Each derived canonical value retains its operation and grounds in `Derivation`.
The unity-check operation is represented by its canonical `UnityCheck` and
condition evidence, which must identify one checked proposal. Thus the format
stores transformation evidence with its product, not in a second, independently
editable edge table. Outcomes and embedded warrants remain the canonical types;
there is no parallel graph-specific definition of a judgment.

Register forms, unity checks, judgments, and limit reports explicitly even when
another value embeds a copy. Every embedded copy must equal the registered
value. Registration is unique; multiple references to one registered value are
allowed. Incompatible copies or ID reuse across semantic kinds are rejected.

Tuple order is preserved by serialization but is not execution order. Temporal
position belongs to observations and intuitions; causal order belongs to the
evidence graph. The [transition model](STATE_TRANSITION_MODEL.md) still governs
legal operational sequencing. This format is not a scheduler or an event log.

## Evidence, alternatives, and diagnostic labels

**Engineering.** Evidence edges include all typed grounds in derivations,
condition results, and warrants, plus explicit canonical dependencies such as
retained intuition IDs and the committed unity-check reference. Ignoring a
reference because it lives outside `Derivation.grounds` would let a dangling
or mistyped link escape validation. Identical repeated evidence edges normalize
to one lookup edge without rewriting the original values.

Alternative IDs are comparison links, not evidence. They must resolve, but are
excluded from causal ordering. Consequently two candidates can name each other
as alternatives without creating circular evidence. A committed judgment may
retain those alternatives as metadata; it cannot merge rival candidates into
its own ancestry.

Condition IDs, conflict IDs, source labels, episode IDs, and variant labels are
not automatically independent cognitive nodes. Missing conditions and conflicts
remain diagnostic labels. Typed entity references, form IDs, and limit-report
IDs are resolved according to their declared roles rather than treating every
string as an interchangeable graph edge.

## Checks performed

- One semantic ID has one registered definition and kind. Embedded copies must
  agree; evaluator, form, report, and scope IDs cannot masquerade as cognitive
  entities.
- Every cognitive ground resolves with its declared kind and, for a rule, its
  actual authority. All nodes and nested warrants share the frozen scope and
  configuration; observations share the episode and projections the variant.
- Evidence is acyclic. Sensible derivatives have ancestry through an intuition
  and admitted presentation, not merely a raw-input or resource node.
- Shared reception preserves supplied content, source, and position. Projection
  and manifold forms are available; retention and candidate membership agree.
- Schemata refer to declared concepts and conditions. Applications cover their
  concept's condition declarations and sensible forms; proposals agree with the
  applicable object/concept/schema result.
- Commitment preserves the proposal, assembled warrant, registered successful
  unity check, and nonblocking limit report. Required synthesis, observation,
  and projection ancestry appears in the warrant. Committed ancestry cannot
  contain non-constitutive authorities, declared candidate conflicts, unresolved
  derivation conditions, or rival identity candidates used together.
- Outcome references resolve with the appropriate kind. Application limits
  agree with actual failed or undecided conditions; ambiguity identifies its
  candidates and their one retained-sequence input.

These checks cannot discover an undeclared alternative or tell whether an
algorithm fabricated a condition result. They enforce recorded commitments;
the later implementations and behavioral tests must establish that those
commitments are causally produced by the cognitive roles.

## Evaluator and failure boundary

`ProvenanceGraph` implements the four read operations of `ProvenanceView`:
`resolves`, `immediate_grounds`, `scope_for`, and `configuration_for`.
Evaluator-only IDs return false from `resolves`; the three lookup operations
raise `KeyError` for them, just as for missing cognitive IDs. The view has no
mutation or evaluator lookup operation.

An `Overreach` report may retain an `AuthorityViolation` naming a registered
evaluator reference or a rule's actual authority. It records the rejected use
without inserting that rejected use as cognitive evidence. The same evaluator
ID forged as an observation ground is rejected even when other valid evidence
is present.

The protocol is an architectural boundary, not a security sandbox against
hostile Python code. External adapters can inspect the complete serialized
trace; cognitive operations should depend only on `ProvenanceView`. Hidden
world payloads belong outside this format, not in `external_inputs` or ordinary
observation content under a false label.

## Prefixes, trade-offs, and revisit points

A trace can be closed over all its references without yet having an outcome.
Such a prefix supplies the graph needed by recognition, applicability, and
unity. Adding a result creates a new `ProvenanceTrace` and validated graph;
there is no mutable append API or partially trusted lookup mode.

**Engineering.** Named typed collections are more verbose than generic node
dictionaries but reuse canonical validation and keep the wire format readable.
Python's standard-library topological ordering avoids a graph dependency.
Immutable lookup indexes are derived, not serialized. Transitive ancestry is
computed during validation; worst-case ancestry storage is quadratic in the
number of entities. That is acceptable for the deliberately small finite
episodes, but should be revisited for large traces or incremental execution.

JSON serialization is deterministic for an unchanged trace, not a cryptographic
canonicalization protocol: differently ordered registrations can serialize
differently without changing graph meaning. No hashes, signatures, storage
backend, retry policy, or migration of earlier wire versions is promised here.
Revisit those only when a concrete persistence or comparison requirement needs
them. The generated Pydantic JSON Schema describes wire shape, not graph validity.

## Verification

[`tests/test_provenance.py`](tests/test_provenance.py) registers a complete
canonical chain and exercises closure, read-only lookup, all terminal kinds,
prefixes, serialization, evaluator isolation, identity conflicts, circular
evidence, alternatives, and invalid commitment ancestry.
[`typechecks/provenance.py`](typechecks/provenance.py) checks compatibility with
the accepted `ProvenanceView` contract. The separate
[property-test suite](INVARIANTS_AND_PROPERTY_TESTS.md) generates evidence
cycles, registration orders, evaluator-ground kinds, and reception content.
