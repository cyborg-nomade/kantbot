# Cognitive Role Interfaces

## Status and scope

This document maps the accepted cognitive-role boundaries to executable Python
contracts in [`kantbot.interfaces`](src/kantbot/interfaces.py). It completes the
second Phase 2 Roadmap item without yet choosing algorithms, ordering the whole
cycle, or implementing the provenance graph.

The interfaces inherit their philosophical boundaries from the
[specification](PHILOSOPHICAL_SPECIFICATION.md#cognitive-roles), the
[architecture](COGNITIVE_ARCHITECTURE.md#2-cognitive-role-ownership), and ADRs
[0001–0004](docs/decisions/README.md#index). Their callable `Protocol`
representation follows the object/functional division accepted in
[ADR 0006](docs/decisions/0006-canonical-model-representation.md#decision).

## Interface shape

**Engineering.** Each transformation is an operation-shaped callable protocol,
not a stateful class for an alleged faculty. A plain function can implement a
protocol structurally; it does not inherit from Kantbot, acquire hidden state,
or gain philosophical authority from its class name. Inputs and outputs remain
the immutable canonical values defined in the preceding Roadmap item.

Every operation receives its `Scope` and `ConfigurationIdentity` explicitly.
Operations that must inspect earlier grounds receive a read-only
`ProvenanceView`; none receives an evaluator-state lookup. The later provenance
item may choose its graph representation provided that it implements this view
and the identity contract in the
[canonical structures](CANONICAL_DATA_STRUCTURES.md#identity-and-reference-integrity).

## Boundary map

| Role boundary | Callable protocol | Consumes | Produces |
| --- | --- | --- | --- |
| Shared reception | `PresentObservation` | Valid `Observation` | `PresentedElement` |
| Sensibility | `ProjectIntuition` | Presented element and substantive variant projection | `Intuition` or `not-presentable` |
| Sensibility | `FormManifold` | Non-empty tuple of intuitions | `ManifoldOfIntuition` |
| Understanding | `SupplyUnderstanding` | Scope and frozen configuration only | Validated `UnderstandingRepertoire` |
| Imagination | `RetainIntuitions` | Manifold, its intuitions, and a retention rule | `RetainedSequence` or `synthesis-failed` |
| Imagination under understanding | `RecognizeCandidates` | Retained sequence, supplied identity and constitutive rules, policy, and provenance | Candidate tuple, `synthesis-failed`, or `synthesis-ambiguous` |
| Object-formation gate | `ConstituteObject` | Candidate, identity and constitutive results, and provenance | `ObjectCandidate` or `synthesis-failed` |
| Power of judgment | `ApplyConcept` | Object candidate, concept, schema, and provenance | `ApplicationResult` with satisfied, failed, or undecided conditions |
| Proposal boundary | `ProposeJudgment` | Object candidate, successful application, proposition, and assembled warrant | `ProposedJudgment` or `judgment-withheld` |
| Apperception | `CheckUnity` | Proposal and its complete provenance view | `UnityCheck`, `unity-conflict`, or `overreach` |
| Commitment gate | `CommitJudgment` | Proposal, successful unity, limit report, and derivation | `CommittedJudgment` or `judgment-withheld` |
| Critique and reporting | `CritiqueAndReport` | Validated `TerminalOutcome` | Stable machine-readable report |

The result unions expose refusal and ambiguity as ordinary typed results rather
than exceptions. They do not prescribe the cycle's branching or decide when an
application status becomes terminal; the next Roadmap item owns that transition
model.

## Understanding as supplied constraints

**Interpretive.** `UnderstandingRepertoire` makes the understanding's role
causally present without allowing it to inspect raw observations or declare its
concepts applicable. It contains only constitutive rules, concepts, and
schemata for one scope and configuration. Every schema must name a concept and
conditions present in that same repertoire.

The imagination receives selected rules from this repertoire when recognizing
candidates. The power of judgment receives a selected concept and schema when
testing applicability. Thus understanding supplies general constraints while
the consuming role performs the operation, preserving the shared boundary
adopted in [ADR 0002](docs/decisions/0002-a-b-synthesis.md).

## Provenance and evaluator boundary

**Engineering.** `ProvenanceView` supplies only four read operations: resolve a
typed cognitive ground, retrieve immediate cognitive grounds, and retrieve an
entity's scope and configuration. It intentionally supplies no mutation,
storage position, unrestricted node access, or evaluator-reference lookup.

This interface does not itself prove graph closure. The structured-provenance
Roadmap item must still reject unresolved or mistyped grounds, incompatible ID
reuse, unreachable transformations, and evaluator-only ancestry. Restricting
the read interface prevents downstream roles from depending on a concrete graph
library or acquiring hidden evaluator state while that implementation remains
open.

## Deliberate absences

- Parsing remains outside the cognitive roles. A constructed `Observation` has
  already crossed that boundary; invalid external data becomes `input-error`.
- Reason has no active callable interface in the first cycle. Its representable
  but reserved value remains governed by Phase 4.
- These protocols do not instantiate or order a cycle. The next item will make
  legal transitions and terminalization explicit.
- No protocol supplies an implementation algorithm. Later variants may replace
  an operation while preserving its boundary and comparable trace evidence.

## Verification

Mypy checks concrete function signatures against every public protocol in
[`typechecks/role_interfaces.py`](typechecks/role_interfaces.py). Runtime tests
check the understanding repertoire's authority, scope, concept, condition, and
identity invariants. Ruff, pytest, coverage, and SonarQube remain the shared
repository checks.
