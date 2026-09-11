# ADR 0007: Require replayable sensible licenses

- **Status:** Accepted
- **Date:** 2026-09-08
- **Deciders:** Kantbot maintainers
- **Related questions:** [RQ-01](../../RESEARCH_QUESTIONS.md#rq-01--what-can-be-given-to-the-model), [RQ-03](../../RESEARCH_QUESTIONS.md#rq-03--what-makes-a-representation-count-as-an-object), [RQ-04](../../RESEARCH_QUESTIONS.md#rq-04--how-are-concepts-applied-and-judgments-licensed)
- **Related claims:** [K-008](../../CLAIMS.md#k-008), [K-011](../../CLAIMS.md#k-011), [K-012](../../CLAIMS.md#k-012), [K-015](../../CLAIMS.md#k-015), [K-020](../../CLAIMS.md#k-020), [K-022](../../CLAIMS.md#k-022), [K-027](../../CLAIMS.md#k-027), [K-028](../../CLAIMS.md#k-028)
- **Supersedes:** None; strengthens the implementation of ADRs 0001–0004 and 0006
- **Superseded by:** None

## Context

The Phase 2 epistemology audit found that a closed, well-typed trace could
certify an amber application over blue input. Schema procedures were prose;
object conditions were not bound to rules; temporal form kinds and projection
criteria did no mechanical work. The cognitive lookup protocol exposed IDs
and grounds but not the sensible contents needed to apply a schema.

These are defects in the executable hypothesis, not reasons to abandon its
Kantian terminology or cognitive ambition. The maintainer authorized corrective
implementation before the deterministic toy-world item. This record adopts
the cross-cutting implementation choice approved by the maintainer; it does
not claim that the full cognitive cycle or the theory of schematism has been
implemented.

## Grounds and claim status

### Textual

At [A137–140/B176–179](../../sources/kant/critique-a.md#a137), sensible
conditions mediate the cognitive use of categories. At
[A141–144/B180–183](../../sources/kant/critique-a.md#a141), a schema is a
general procedure rather than an image; permanence and rule-governed succession
are examples of temporal determination. At
[A145–147/B184–187](../../sources/kant/critique-a.md#a145), schemata both
realize and restrict categories. These passages are from the shared Schematism
chapter, not a choice between the A and B Deductions.

### Interpretive

We retain ADR 0003's separation of object formation and empirical predication.
Earlier identity and category-inspired constraints must themselves have
temporal mediation; a later empirical predicate is not their substitute.
This preserves the adopted reading in K-012 without requiring all twelve
categories or treating the engineering sequence as a literal chronology of
faculties. Supplying rules remains distinct from applying them.

### Analogical

The initial executable analogue is a general instruction applied to a
particular, ordered sensible sequence. The instruction is neither the sequence
itself nor its reported success. Declared temporal order, field invariance,
and successive increase make selected dependencies experimentally concrete.
Field invariance alone does not establish substance; successive increase does
not establish causality. These remain restricted experiments toward K-027,
whose adequacy can be challenged independently of correct execution.

### Engineering

Replaying finite, deterministic instructions can detect invented condition
statuses at the serialized-trace boundary. Typed immutable lookups make actual
content available without widening access to hidden evaluator data. Python
functions perform replay; Pydantic values describe instructions and enforce
local invariants. No callable, import path, or executable source is loaded from
a trace. This is a validation correction, not a new world or role scheduler.

## Options considered

### Option A: Add content lookups and leave procedure execution to Phase 3

Lowest cost and least restrictive for later algorithms. It repairs the
impossible interface but leaves imported licenses self-certified. Negative
tests would have to document accepted forgeries rather than prevent them.
This does not adequately address the audit.

### Option B: Register arbitrary Python procedures by versioned identifier

Most expressive and closest to future swappable role implementations. A
repertoire could use readable functions for segmentation and rich temporal
rules. However, replay would require an external, version-pinned registry;
an identifier alone would not establish which implementation ran. Portable
validation, dependency management, and extension trust would become part of
the correction. Revisit when concrete experiments need this flexibility.

### Option C: Use a small typed instruction vocabulary and replay it

More work than A, but deterministic, inspectable, and self-contained in a
versioned trace. General constraints, particular inputs, and computed evidence
stay separate. Unknown operations fail closed. The cost is limited expressive
power: adding a genuinely new procedure requires reviewed code and wire-format
consideration. Reusing a few checks must not become an excuse to force every
Kantian concept into them.

## Decision

Adopt **Option C**, approved with PR #18 on 2026-09-08:

1. Extend `ProvenanceView` with typed intuition, candidate, rule, and form
   lookups. Keep semantic reference IDs and the evaluator boundary.
2. Give projections an explicit field-selection procedure. Successful
   intuition admission checks receptive criteria, temporal form, exact selected
   content, and preserved position. Other projection declarations can be
   represented, but unsupported ones cannot license an intuition.
3. Distinguish empirical/category-inspired concepts and general/identity/
   category-inspired rules. Object-licensing rules declare required conditions
   and a temporal procedure. General rules cannot be relabeled by a ground ID
   into an object license.
4. Bind each schema's procedure to **all** its concept conditions, including
   optional ones. Category-inspired use requires an actual temporal check,
   not just a temporal form label. Check nested condition authority at use.
   The initial constancy and temporal-order checks require at least two
   samples: a singleton cannot witness a comparison across moments. This
   evidence minimum is an engineering constraint on the chosen procedures,
   not a general philosophical claim about all category application.
5. Replay object and application results against the referenced candidate's
   actual intuitions. Require exact condition IDs, required flags, statuses,
   and sensible evidence. Explanatory prose is not executable authority.
6. Require a matching validated graph for successful `record_commitment` and
   `record_critique`. Earlier snapshots remain local records, not certificates.
7. Publish these incompatible contracts as provenance format version 2. Do not
   silently upgrade version 1's prose into an executable license.

## Consequences

The general constraints belong to understanding; their sensible mediation is
executable before objecthood as well as during predication. The graph can now
reject the audit's reported-success counterexamples. A valid failed or
undecided result remains representable; invalid provenance remains an error.

The instruction set and its missing-data policy are engineering commitments,
documented in [Sensible Procedures](../../SENSIBLE_PROCEDURES.md). Field
selection deliberately excludes segmentation, inferred attributes, and arbitrary
transformations for now. Temporal samples are supplied in explicit order;
validation does not sort a candidate to make a failing procedure succeed.

Replay costs grow with checked conditions and their input sequences, in
addition to graph validation. That is acceptable for the bounded initial model.
It proves agreement with the declared instructions, not their philosophical
adequacy, correspondence to the external world, the truth of free-text
propositions, or the completeness of the unity policy. More powerful temporal
schemata and comparative variants remain meaningful later work.

## Observable consequences

- The same application request distinguishes amber and blue through the
  cognitive port; an unchanged amber license over blue input is rejected.
- Unknown procedures, unsupported projection criteria, invented intuition
  content, absent temporal form, unbound conditions, and regulative condition
  authority cannot license a committed trace.
- `[0, 1, 2]` and `[0, 2, 1]` produce different moving-right applicability while
  retaining the same valid color-based identity license (BP-001-style probe).
- Breaking the declared color invariant prevents objecthood before empirical
  application. Removing a result's sensible evidence prevents certification.
- A singleton remains presentable, but its temporal results are undecided;
  declarations that lower the temporal sample minimum to one are rejected.

## Follow-up

- Keep the deterministic toy world as the next independent Roadmap item.
- In Phase 3, implement role policies and translate computed failures into
  explicit refusal paths; revisit the finite instruction vocabulary when a
  concrete interpretation needs more than these bounded checks.
- In Phase 5, compare philosophical adequacy and behavior, including ablations;
  replay correctness does not discharge that evaluation.
