# Canonical Data Structures

## Status and scope

This document is the readable map to the first executable Phase 2 artifact:
the immutable semantic values in [`kantbot.model`](src/kantbot/model). The
types implement the representational distinctions fixed by the
[philosophical specification](PHILOSOPHICAL_SPECIFICATION.md#representations-carried-by-the-cycle)
and ADRs [0001–0004](docs/decisions/README.md#index). Their Python and Pydantic
representation is governed by
[ADR 0006](docs/decisions/0006-canonical-model-representation.md).

**Engineering.** This Roadmap item defines values and local construction
invariants. It does not yet define the interfaces between cognitive roles, run
a cognitive cycle, validate a complete provenance graph, add property tests, or
implement the deterministic toy world. Those are the remaining independently
reviewable Phase 2 items.

## How the Python model uses objects and functions

**Engineering.** A canonical value is an immutable object when the data and a
small invariant or query belong together. For example, an `ApplicationResult`
can answer whether it is applicable, but it cannot turn itself into a judgment.
Construction validates the value and then closes it against mutation.

**Engineering.** Transformations use a functional style: later operations will
accept explicit values and return new values rather than modifying an earlier
representation. The first pure boundary functions validate and serialize the
terminal-outcome union. Effects such as reading input or storing traces belong
outside the domain model.

This deliberately uses both parts of Python without simulating every Kantian
faculty as a stateful class. The choice makes an object-oriented or functional
reading inspectable without treating either programming paradigm as evidence
that Kant's account is correct or that cognition has been reduced to
computation ([K-027](CLAIMS.md#k-027)).

## Shared foundations

[`common.py`](src/kantbot/model/common.py) defines the values used across the
whole model:

| Value | Purpose |
| --- | --- |
| `ConfigurationIdentity` | Identifies the one frozen interpretation and revision governing a cycle |
| `Scope` | States the episode, presentation conditions, and claims excluded from its authority |
| `Form` | Names temporal, spatial, or other declared form without treating it as inferred object content |
| `Rule` and `RuleAuthority` | Distinguish `constitutive`, `regulative`, and `engineering` authority |
| `Condition` and `ConditionResult` | Preserve required, satisfied, failed, and undecided conditions explicitly |
| `CognitiveGround` | Admits only declared kinds of cognitive evidence into provenance |
| `EvaluatorReference` | Represents hidden evaluation state as a separate, inadmissible warrant type |
| `Derivation` | Carries immediate grounds, operation, alternatives, unmet conditions, scope, and configuration |

`Derivation` is local provenance attached to one value. It does not claim that
all references form a reachable, acyclic, cycle-wide graph. The later structured
provenance item will connect and validate these records under K-022.

## Values along the cognitive path

The modules follow the order of the specified cognitive path so that a reader
can inspect the model without first learning a framework hierarchy.

### Reception and variant projection

[`reception.py`](src/kantbot/model/reception.py) keeps three boundaries
structurally distinct:

1. `Observation` is supplied external content with source, episode position,
   and quality metadata.
2. `PresentedElement` is shared admitted content whose derivation must identify
   its observation.
3. `Intuition` is the accepted Kantian variant's representation. Its derivation
   must identify both a presented element and a substantive
   `VariantProjection`.

`ManifoldOfIntuition` is a non-empty, bounded plurality with explicit sensible
forms and intuition grounds. These constraints operationalize ADR 0001 without
letting a type rename count as a projection.

### Synthesis and object formation

[`synthesis.py`](src/kantbot/model/synthesis.py) defines:

- `RetainedSequence`, whose reproduced intuitions require a named retention
  rule in their provenance;
- `CandidateRepresentation`, which declares either the default
  A-analysis/B-constraint policy or the comparable B-led figurative policy and
  names its identity and constitutive rules; and
- `ObjectCandidate`, which can be constructed only when every required local
  identity and constitutive-unity result is satisfied.

The types therefore preserve manifold, retained sequence, candidate
representation, and object candidate as different licensed states. Object
formation still does not apply a concept or commit a proposition, as required
by ADR 0003.

### Concepts, schemata, and application

[`concepts.py`](src/kantbot/model/concepts.py) separates:

- a `Concept` and its general applicability conditions and consequences;
- a `Schema` and its inspectable mediation procedure and sensible conditions;
  and
- an `ApplicationResult` containing the result of every tested condition.

An application is `applicable`, `not-applicable`, or `underdetermined` according
to its required condition results. Supplying a contradictory status is invalid.
Even a successful result contains no operation that commits a judgment.

### Proposal, unity, and commitment

[`judgments.py`](src/kantbot/model/judgments.py) makes commitment a structural
addition rather than a flag:

- `ProposedJudgment` contains a proposition and `AssembledWarrant` but has no
  successful unity result.
- `UnityCheck` exposes cycle-wide success or conflict without simulating a
  self.
- `CompleteWarrant` requires successful unity plus a limit-report identity.
- `CommittedJudgment` requires that complete warrant and grounds itself in a
  distinct proposed judgment.

Warrant fields use typed cognitive grounds rather than arbitrary evidence
objects. Identity and constitutive-rule grounds must declare constitutive
authority. An `EvaluatorReference` cannot validate in any warrant field, and a
regulative rule cannot be promoted to object-level warrant.

### Reason's reserved boundary

[`reason.py`](src/kantbot/model/reason.py) makes `Reason` representable only as
`reserved` regulative guidance. There is no active reason status or inference
operation in the first cycle. Phase 4 may supersede this deliberately narrow
boundary when it implements inference and systematic inquiry.

### Limits and terminal outcomes

[`outcomes.py`](src/kantbot/model/outcomes.py) defines one discriminated union
with exactly the ten outcomes required by ADR 0004:

| Outcome | Required specific evidence |
| --- | --- |
| `input-error` | Invalid input references and validation errors |
| `not-presentable` | Presented elements and failed projection conditions |
| `synthesis-failed` | The manifold and failed rules |
| `synthesis-ambiguous` | At least two candidate representations retained as alternatives |
| `concept-not-applicable` | Object candidate, application result, and failed conditions |
| `application-underdetermined` | Object candidate, application result, and undecided conditions |
| `unity-conflict` | Proposed judgment and conflicting grounds |
| `judgment-withheld` | Strongest representations and unmet licensing conditions |
| `judgment-committed` | A committed judgment with complete warrant |
| `overreach` | The rejected claim and its scope, authority, or evaluator-state violation |

Every outcome also carries one `OutcomeContext`: configuration identity, local
derivation, scope, alternatives, and `LimitReport`. The discriminator and the
report's strongest licensed status must agree. JSON validation and serialization
are pure functions over the union.

## Local invariants enforced now

All canonical values inherit a project-owned configuration that:

- uses strict Pydantic validation and rejects unknown fields;
- freezes model fields and uses tuples for nested collections;
- validates defaults and revalidates nested model instances; and
- rejects non-finite numeric content.

The model additionally enforces stage-specific grounding, unique references,
retention licensing, synthesis-rule presence, successful local object
conditions, application-status consistency, constitutive warrant authority,
successful unity before commitment, and agreement between outcomes and their
limit reports.

These are local construction invariants. The absence of evaluator state from a
warrant is structural, but proving reachability from presented observations or
compatibility across a complete trace belongs to the later provenance and
state-transition validators.

## Verification

The ordinary development checks are:

```bash
uv sync --dev
uv run ruff check src tests
uv run pytest
```

The unit tests construct one compact successful chain, exercise the main local
rejections, and round-trip all ten terminal variants through JSON. They are
example-based invariant tests, not the property-test Roadmap deliverable.
