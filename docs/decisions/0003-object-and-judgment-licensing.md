# ADR 0003: Separate object formation, applicability, and judgment licensing

- **Status:** Proposed
- **Date:** 2026-08-31
- **Deciders:** Kantbot maintainers
- **Related questions:** [RQ-03](../../RESEARCH_QUESTIONS.md#rq-03--what-makes-a-representation-count-as-an-object), [RQ-04](../../RESEARCH_QUESTIONS.md#rq-04--how-are-concepts-applied-and-judgments-licensed), [RQ-05](../../RESEARCH_QUESTIONS.md#rq-05--what-functional-unity-can-the-model-require)
- **Related claims:** [K-005](../../CLAIMS.md#k-005), [K-006](../../CLAIMS.md#k-006), [K-007](../../CLAIMS.md#k-007), [K-008](../../CLAIMS.md#k-008), [K-011](../../CLAIMS.md#k-011), [K-012](../../CLAIMS.md#k-012), [K-013](../../CLAIMS.md#k-013), [K-017](../../CLAIMS.md#k-017), [K-018](../../CLAIMS.md#k-018)
- **Supersedes:** None
- **Superseded by:** None

## Context

A conventional pipeline can cluster inputs, attach a label, and emit a
sentence. Kantbot needs criteria that make candidate unity, concept
applicability, propositional commitment, and objective purport inspectably
different. It also needs a functional unity constraint that does work without
being mislabeled machine consciousness.

## Grounds and claim status

### Textual

Concepts refer to objects mediately and function in judgments
([A68-69/B93-94](../../sources/kant/critique-a.md#a68)). Judgment relates
representations through objective unity
([B140-142](../../sources/kant/deduction-b.md#b140)). Schemata mediate and limit
the application of categories to appearances
([A137-147/B176-187](../../sources/kant/critique-a.md#a137)), and category use is
restricted to sensible intuition and possible experience
([B146-169](../../sources/kant/deduction-b.md#b146)).

### Interpretive

Object candidates require rule-governed identity and unity; concept application
requires an inspectable procedure over formed content; a judgment additionally
requires a coherent cycle-wide warrant. The text underdetermines the precise
executable tests and does not prescribe this sequence as software stages.

### Analogical

The unity check requires all grounds of a proposed judgment to belong to one
compatible cognitive trace. It is analogous to a constraint associated with
apperception, but it is not consciousness, self-awareness, a transcendental
subject, or a process identifier.

### Engineering

Represent object candidates, application results, proposed judgments, and
committed judgments as distinct semantic states. Require temporal application
procedures for constitutive category-like rules and structured provenance for
every transition.

## Options considered

### Option A: Classification is judgment

This is simple but collapses applicability, commitment, and warrant, making a
high score sufficient for object-directed assertion.

### Option B: Object formation and application are distinct, with a final unity check

This exposes where object identity, predicate applicability, and coherent
commitment can independently fail. It introduces more states and more negative
cases.

### Option C: Treat every coherent internal record as an object

This makes tracing easy but confuses stored structure with objective validity
and lets upstream identifiers settle objecthood.

## Decision

Choose Option B. A candidate becomes an object candidate through explicit
identity and constitutive-unity rules. A schema or other inspectable procedure
tests concept applicability. A proposed judgment commits only after its entire
provenance graph passes the unity and scope check. The minimal category-inspired
constraints cover unity/plurality, persistence, and—only where needed—lawful
succession; they are not presented as the complete category table.

## Consequences

- Successful concept application may end in a withheld judgment.
- A coherent object candidate may remain without an applicable predicate.
- Schemas expose both matching conditions and limits of application.
- The unity role spans stages instead of becoming a simulated self component.
- Phase 2 must model rival candidates and failed grounds explicitly.
- The additional semantic states make the model less compact than a classifier.

## Observable consequences

Two incompatible identity syntheses may each satisfy the same empirical
predicate. The application results remain successful, but the cycle withholds
an object-level judgment because no single compatible provenance graph can
ground the commitment.

## Follow-up

If accepted, make K-011, K-012, K-013, K-017, and K-018 Current and link this
record from their grounds. Later Phase 1 deliverables must supply success,
ambiguity, applicability-failure, and unity-conflict traces.
