# Research Questions and Non-Goals

## Purpose

This document defines the questions that must guide Kantbot's first
philosophical specification and the boundaries that keep that inquiry small
enough to answer. It operationalizes the project's broader
[commitments and non-claims](MANIFEST.md#what-this-project-does-not-claim).

The questions are not requests for neutral summaries of Kant. Each answer must
state its textual grounds, its interpretive commitments, and the observable
difference it should make to the model. Until a question is resolved, no
implementation should settle it silently.

## Research questions

### RQ-01 — What can be given to the model?

What will count as a manifold or intuition *for this model*, under which forms
will it be presented, and where does structured program input cease to be a
useful analogue of receptive sensibility?

An answer must define the boundary, granularity, and temporal or spatial form
of an input episode. It must also choose whether implementation documents use
`intuition` or the weaker term `constrained presentation`.

Related claims: [K-001](CLAIMS.md#k-001) and [K-015](CLAIMS.md#k-015). Source map:
[what is presented to the model?](PRIMARY_SOURCES.md#what-is-presented-to-the-model)

### RQ-02 — What work belongs to synthesis and imagination?

Which transformations turn a manifold into a candidate object or event, what
must be retained across a sequence, and should apprehension, reproduction, and
recognition be the default architecture, an A-edition variant, or source
context only?

An answer must distinguish synthesis from parsing, aggregation, and storage;
locate the role of imagination; and state the failure conditions for a
synthesis.

Related claims: [K-002](CLAIMS.md#k-002), [K-003](CLAIMS.md#k-003),
[K-004](CLAIMS.md#k-004), and [K-016](CLAIMS.md#k-016). Source map:
[how does a candidate object become possible?](PRIMARY_SOURCES.md#how-does-a-candidate-object-become-possible)

### RQ-03 — What makes a representation count as an object?

Which rule-governed unity and identity conditions distinguish a candidate
object or event from a bundle, a recurring association, or an internally
consistent representation?

An answer must supply executable success, ambiguity, and failure criteria. It
must also state what the model can legitimately claim when those criteria are
only partly met.

Related claims: [K-006](CLAIMS.md#k-006), [K-011](CLAIMS.md#k-011), and
[K-013](CLAIMS.md#k-013). Source map:
[what makes cognition objectively valid?](PRIMARY_SOURCES.md#what-makes-cognition-objectively-valid)

### RQ-04 — How are concepts applied and judgments licensed?

Which concepts or categories are necessary for the first experiment, what—if
anything—plays the role of a schema, and when does successful concept
application license a judgment rather than merely produce a classification?

An answer must separate applicability grounds from the resulting commitment,
identify the authority of each rule, and expose failed or ambiguous
application in the trace.

Related claims: [K-007](CLAIMS.md#k-007), [K-008](CLAIMS.md#k-008),
[K-012](CLAIMS.md#k-012), and [K-017](CLAIMS.md#k-017). Source map:
[what licenses concepts and judgments?](PRIMARY_SOURCES.md#what-licenses-concepts-and-judgments)

### RQ-05 — What functional unity can the model require?

What consistency, ownership, or combinability condition can serve as a useful
computational analogue of apperception, and what observable work does it do
beyond ordinary state validation?

An answer must define the unity check and cases that fail it while explicitly
denying that the check establishes consciousness, self-awareness, or a
transcendental subject.

Related claims: [K-005](CLAIMS.md#k-005) and [K-018](CLAIMS.md#k-018). Source map:
[what makes cognition objectively valid?](PRIMARY_SOURCES.md#what-makes-cognition-objectively-valid)

### RQ-06 — How will the model represent the limits of cognition?

Which missing or violated conditions require uncertainty, withheld judgment,
failed cognition, or a diagnosis of overreach, and how will constitutive rules
be distinguished from regulative guidance?

An answer must make those outcomes behaviorally distinct and must not model a
noumenon or thing in itself as an accessible hidden object or ground-truth
record.

Related claims: [K-009](CLAIMS.md#k-009), [K-014](CLAIMS.md#k-014),
[K-019](CLAIMS.md#k-019), and [K-020](CLAIMS.md#k-020). Source map:
[where must the system stop?](PRIMARY_SOURCES.md#where-must-the-system-stop)

### RQ-07 — Which disagreements deserve executable variants?

Where do the A and B deductions or competing interpretations predict
meaningfully different transformations, judgments, or traces, and which
differences can remain documented without becoming software abstractions?

An answer must name a default interpretation, preserve at least one
behaviorally significant alternative where warranted, and state a comparison
scenario that could reveal the difference.

Related claims: [K-010](CLAIMS.md#k-010) and [K-024](CLAIMS.md#k-024). Source map:
[edition-sensitive fault lines](PRIMARY_SOURCES.md#edition-sensitive-fault-lines)

## Explicit non-goals

### Standing non-goals

These are not claims the project expects a later phase to establish:

- reproducing Kant's mind, personality, or voice;
- producing a definitive or interpretation-neutral reading of Kant;
- proving a philosophical interpretation correct by implementing it;
- claiming that software literally possesses human sensibility, imagination,
  apperception, reason, consciousness, or moral autonomy;
- reducing transcendental philosophy to empirical psychology or claiming that
  human cognition is literally software; or
- treating Kantian terminology as sufficient to distinguish the architecture
  from an ordinary symbolic pipeline.

### Non-goals for the first usable release

These may become separate later projects, but they are not prerequisites for
the Roadmap's first release:

- a general-purpose assistant, chatbot, or simulated Kant;
- language-model integration, natural-language understanding, open-world
  perception, or internet-scale knowledge;
- learning empirical concepts from unbounded data or optimizing performance on
  conventional AI benchmarks;
- an exhaustive implementation of every category, principle, faculty, or
  argument in the *Critique of Pure Reason*;
- practical reason, ethics, action, freedom, or moral agency;
- reflective or aesthetic judgment; or
- Hegelian, Nietzschean, Deleuzian, or other post-Kantian extensions.

Deferral does not make these topics unimportant. It means the initial
instrument must be assessable without them. Any proposal to add one before the
first release must identify which current research question cannot be answered
without it and update the Roadmap explicitly.

## Completion rule

Phase 1 may revise, split, or retire a research question through a documented
decision. It is complete only when its answer:

1. identifies the relevant claims and primary passages;
2. labels the textual, interpretive, analogical, and engineering steps;
3. defines the representations, operations, or boundaries it constrains;
4. predicts at least one observable success, failure, or comparison; and
5. records any remaining alternative rather than concealing it in an
   implementation default.
