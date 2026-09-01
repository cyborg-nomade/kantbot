# ADR 0006: Choose the canonical model representation

- **Status:** Proposed
- **Date:** 2026-09-01
- **Deciders:** Kantbot maintainers
- **Related questions:** None; this record governs the executable representation of already accepted Phase 1 semantics
- **Related claims:** [K-021](../../CLAIMS.md#k-021), [K-022](../../CLAIMS.md#k-022), [K-023](../../CLAIMS.md#k-023), [K-024](../../CLAIMS.md#k-024), [K-026](../../CLAIMS.md#k-026), [K-027](../../CLAIMS.md#k-027)
- **Supersedes:** None
- **Superseded by:** None

## Context

Phase 2 must turn the accepted philosophical specification into canonical,
executable data structures for observations, manifolds, synthesized
representations, concepts, judgments, reasons, limits, and their provenance.
Those structures must preserve the distinctions established in ADRs 0001–0004
rather than recovering them from loosely structured dictionaries or prose.

The repository does not yet select a programming language, runtime type system,
serialization format, validation library, or owner for the canonical schema.
Choosing any of them silently while adding the first structures would make a
costly engineering decision appear incidental. The choice also affects how
directly future contributors can inspect philosophical distinctions, how early
invalid states are rejected, and whether traces can cross process boundaries
without a second hand-maintained model.

This record chooses the source of truth for Phase 2 semantic structures. It does
not choose the complete role interfaces, state-transition model, property-test
suite, toy-world representation, command-line interface, persistence format, or
long-term public protocol. Those remain separate Roadmap work. It also does not
permit a serialization representation to erase variant, authority, scope, or
provenance distinctions.

## Requirements and selection criteria

The representation must support:

- explicit tagged alternatives for variant-scoped receptive representations,
  proposed and committed judgments, and all typed terminal outcomes;
- recursive, inspectable provenance with stable identity, scope, configuration,
  alternatives, and rule authority;
- rejection of unknown fields and malformed values at trusted construction
  boundaries;
- immutable or effectively immutable semantic values so a trace cannot change
  after it has licensed a later result;
- deterministic equality and serialization suitable for tests and trace
  comparison;
- local validation close to each type without pretending that graph-wide or
  transition-wide invariants are merely field constraints;
- readable definitions that can be reviewed alongside philosophical documents;
  and
- rapid revision while the executable interpretation is still experimental.

No criterion alone decides the matter. Semantic fidelity and inspectability are
primary; runtime validation, experimental velocity, interchange, and tooling
cost follow closely. Raw execution speed is secondary for the first bounded,
local model described by K-021.

## Grounds and claim status

### Textual

Kant's text supplies constraints on the roles and relations represented by the
model, not on programming languages or schema technologies. Nothing in the
primary sources decides among these options. The accepted textual and
interpretive grounds remain those recorded in ADRs 0001–0004.

### Interpretive

The canonical structures must make the accepted distinctions structurally
visible. In particular, external observations, shared presented elements, and
variant-specific intuitions must not become aliases; concepts, schemata, and
application results must remain distinct; and commitment must add licensing
that a proposed judgment does not possess. A framework that makes these states
awkward to express risks pressuring the interpretation toward whatever the
framework represents most conveniently.

The implementation is an executable hypothesis under K-027. Strong types do
not insulate that hypothesis from revision: variant interpretations must remain
replaceable, and disagreement should produce comparable behavioral or trace
differences under K-024.

### Analogical

Program values stand for roles in the implemented account of cognition. A
class named `Concept`, for example, is the model's operational concept role; it
is not a claim that a library class exhausts human conceptual capacity. The
chosen technology must not itself be treated as a psychological or
transcendental explanation.

### Engineering

The first model benefits from executable validation, exhaustive handling of
tagged alternatives, immutable values, and a machine-readable interchange
description. It also benefits from keeping domain definitions near the Python
experiments and tests likely to exercise them. Graph-wide conditions—such as
provenance reachability, legal stage transitions, and absence of evaluator-only
state from cognitive warrant—should be checked by an explicit validation layer
rather than hidden inside field parsing.

## Options considered

### Option A: Make JSON Schema the canonical source of truth

Define the domain first as versioned JSON Schemas. Generate or hand-write
runtime types in whichever implementation language is later selected. Treat
schema-valid JSON as the canonical interchange and persistence form.

The strongest argument for this option is neutrality. The public semantic
contract would not belong to one runtime, schemas would be directly inspectable,
and independent tools could validate traces without importing Kantbot. JSON
Schema offers conditional and composed schemas that can encode tagged
alternatives and many local structural constraints.

Its central liability is that the first model is more relational than JSON
validation alone. Identity references, provenance reachability, authority
flow, evaluator-state exclusion, and legal cross-stage combinations require
additional code. Semantic operations would live in generated or parallel
runtime types, creating a drift boundary at the start of the project. JSON's
native arrays and objects also do not themselves provide immutable values or
domain-specific construction. This option gives the transport form authority
over the executable model before Kantbot has a public protocol to justify that
priority.

If chosen, generated runtime types must be verified against the schemas, custom
semantic validation must remain explicit, and no runtime may add canonical
fields that are absent from the schemas.

### Option B: Use frozen Python standard-library dataclasses

Define the canonical domain as `@dataclass(frozen=True)` classes, Python enums,
tuples, and explicit union aliases. Write constructors, validators, and JSON
codecs as ordinary project code without a model-framework dependency.

The strongest argument for this option is explicitness. Definitions and
validation would contain little framework magic, import quickly, and remain
easy to debug. Python is accessible for philosophical experiments, and frozen
dataclasses give clear value semantics with minimal infrastructure. The project
would own every coercion and error rather than inheriting library defaults.

The cost is substantial repeated machinery. Python type annotations are not
runtime validation, so recursive input parsing, unknown-field rejection,
discriminated unions, error locations, schema publication, and serialization
must all be built or delegated separately. Frozen dataclasses only prevent
field rebinding; mutable values nested in a field can still change. The burden
of maintaining codecs beside evolving definitions is likely to grow exactly
where Phase 2 needs rapid, reliable revision.

If chosen, canonical fields must use immutable containers, all external input
must pass through explicit checked constructors, and serialization parity must
be covered by tests from the first structure onward.

### Option C: Use strict, frozen Pydantic models in Python

Define the canonical domain as Pydantic models configured with strict
validation, `frozen=True`, and `extra='forbid'`. Use immutable nested containers
and explicit discriminators for alternative states. Generate JSON Schema from
the models as a review and interchange artifact, while keeping the Python domain
models authoritative.

The strongest argument for this option is balance. It preserves Python's low
barrier to experimentation while adding runtime validation, recursive parsing,
located validation errors, discriminated unions, and generated JSON Schema.
One definition can serve implementation, tests, trace inspection, and an early
machine-readable description. Pydantic's custom validators can enforce local
domain rules close to the fields they govern.

The library's defaults are unsafe for this project unless deliberately
constrained. Coercion can conceal invalid inputs, extra fields are ignored by
default, and `frozen` is only faux immutability if nested mutable values remain.
Pydantic adds a dependency and version coupling, and framework validation can
become opaque if complex cycle-wide semantics are forced into model hooks.
Its `model_construct()` API can bypass validation altogether.

If chosen, all canonical base models must inherit one project-owned strict,
frozen, extra-forbidding configuration; fields must prefer tuples, frozensets,
and frozen child models; normal code must not call `model_construct()`; and
graph-wide or state-transition validation must remain a named, separate layer.
Generated JSON Schema will be derivative rather than a second source of truth.

### Option D: Use TypeScript discriminated unions with Zod schemas

Define the canonical domain in TypeScript, infer static types from Zod runtime
schemas, and use discriminated unions for variants and terminal outcomes. Run
the model and tests on a JavaScript runtime.

The strongest argument for this option is the close fit between TypeScript's
discriminated unions and the model's many named alternatives. Exhaustive
switches make omitted outcomes visible during development, Zod validates at
runtime, and the result is naturally positioned for a future browser-based
trace viewer. Inferring types from schemas reduces one common source of drift.

The costs are a JavaScript/TypeScript toolchain and a schema DSL layered over
the language. Compile-time `readonly` does not by itself guarantee immutable
runtime graphs, and Zod's readonly parsing must still be combined with careful
nested schemas. JSON Schema export and recursive domain behavior introduce
additional library-specific choices. For a first local research program, the
web advantage is prospective while the toolchain and runtime choices are
immediate.

If chosen, Zod schemas—not separately written interfaces—must own runtime
shape, parsed results must be recursively protected by construction, and
exhaustive handling must be enforced in compilation and tests.

### Option E: Use Rust structs and enums with Serde

Define the canonical domain as Rust structs and enums, derive serialization
with Serde, and use exhaustive pattern matching for every alternative.

The strongest argument for this option is the strongest construction-time
model of the five. Rust enums naturally encode states with variant-specific
payloads, exhaustive matching exposes omitted cases, values are immutable by
default, and Serde offers explicit tagged representations. The compiler would
prevent broad classes of illegal or incomplete handling before tests run.

The costs are iteration time and contributor accessibility. Domain changes
would require more ownership, trait, lifetime, and build decisions than the
bounded model presently needs. Semantic graph validation would still require
custom code, and publishing JSON Schema would require another dependency and
another set of representation choices. Rust's performance and memory safety
advantages do not currently answer a demonstrated Phase 2 constraint.

If chosen, domain enums must remain separate from transport DTOs where Serde
annotations would distort semantics, and compiler-level exhaustiveness must be
supplemented by explicit provenance and transition validators.

## Comparison

| Criterion | A: JSON Schema | B: Dataclasses | C: Pydantic | D: TypeScript/Zod | E: Rust/Serde |
| --- | --- | --- | --- | --- | --- |
| Semantic alternatives | Expressible, verbose | Expressible | Direct | Direct | Strongest |
| Runtime boundary validation | Strong locally | Manual | Strong locally | Strong locally | Strong after deserialization |
| Immutable value graphs | Runtime-dependent | By convention plus frozen fields | By convention plus frozen models | Requires runtime care | Strong default |
| Interchange description | Canonical | Manual | Generated | Library-dependent | Library-dependent |
| Inspectability for experiments | Schema plus runtime | High | High | High | High, but more ceremony |
| Early revision cost | Medium/high | Low initially, rising with codecs | Low/medium | Medium | Highest |
| Principal risk | Schema/runtime drift | Hand-built validation drift | Framework defaults or magic | Premature web/toolchain commitment | Premature systems-language commitment |

## Proposed decision

Choose **Option C: strict, frozen Pydantic models in Python**.

This is a working recommendation only. While this record remains Proposed, it
does not authorize the implementation or establish Python or Pydantic as a
project standard.

If accepted, the canonical semantic source of truth will be a project-owned
hierarchy of Pydantic domain models with these non-optional safeguards:

1. strict validation, forbidden extra fields, and frozen models by default;
2. immutable nested collections and explicit tagged unions;
3. checked public constructors only, with validation bypass prohibited in
   production model paths;
4. stable semantic identifiers separated from display labels and storage
   positions;
5. local field and object invariants in model validation;
6. graph-wide, authority-flow, evaluator-boundary, and transition invariants in
   a separate explicit validation layer; and
7. generated JSON Schema treated as a derivative review/interchange artifact,
   not an independently edited source.

This choice best matches the first model's need for rapid philosophical
revision and inspectable runtime enforcement. It intentionally accepts a
dependency and weaker compile-time guarantees than Rust in exchange for a
smaller experimental loop. It also delays making a transport schema or a future
trace-viewer language the owner of the internal semantics.

## Consequences if accepted

- Python and Pydantic become required development dependencies for the first
  executable model.
- The canonical model package will own a common configuration base and semantic
  identifiers; ad hoc dictionaries will not cross trusted model boundaries.
- Invalid local states fail at construction with structured errors.
- Generated schemas can support review and later interchange, but consumers
  must not assume they encode whole-graph or transition validity.
- Framework upgrades become architecture-sensitive maintenance and require
  validation and serialization compatibility checks.
- Faux immutability remains a known limitation; immutable child values and
  containers are part of correctness, not style.
- The later role-interface and state-transition Roadmap items must use these
  domain models without moving their cross-stage rules into parsing hooks.

## Observable consequences if accepted

- Constructing a committed judgment without its licensing grounds is rejected;
  a proposed judgment with the appropriate incomplete state remains valid.
- Each terminal result parses through exactly one explicit discriminator, and
  adding an eleventh result makes unhandled exhaustive tests fail.
- An unknown field, a string supplied where a strict integer is required, or a
  regulative authority value outside the declared enum is rejected rather than
  silently ignored or coerced.
- A successfully created trace cannot be changed by appending to a nested
  provenance collection.
- Serializing, validating, and reconstructing a value preserves its semantic
  identity, variant, alternatives, scope, configuration identity, and
  authority.
- Separate semantic validation rejects a provenance graph that imports
  evaluator-only hidden state even when every individual node is locally
  well-formed.

## Follow-up

After maintainer selection:

1. Change this record to Accepted and revise the proposed decision if another
   option is chosen.
2. Add only the minimum language and dependency scaffolding needed for this
   Roadmap item.
3. Implement the canonical semantic structures and their local invariants.
4. Cross-link affected Phase 1 documents without rewriting their accepted
   distinctions.
5. Defer full role interfaces, state transitions, property tests, and the
   deterministic toy world to their own independently reviewable Roadmap work.

Primary engineering references for the compared capabilities are the official
[Python dataclasses documentation](https://docs.python.org/3/library/dataclasses.html),
[Pydantic model documentation](https://docs.pydantic.dev/latest/concepts/models/),
[Pydantic union documentation](https://docs.pydantic.dev/latest/concepts/unions/),
[TypeScript union documentation](https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html),
[Zod API documentation](https://zod.dev/api),
[Rust enum documentation](https://doc.rust-lang.org/book/ch06-00-enums.html),
[Serde enum documentation](https://serde.rs/enum-representations.html), and the
[JSON Schema reference](https://json-schema.org/understanding-json-schema/reference).
