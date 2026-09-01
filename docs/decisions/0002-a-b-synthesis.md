# ADR 0002: Use an A/B hybrid synthesis default

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** Kantbot maintainers
- **Related questions:** [RQ-02](../../RESEARCH_QUESTIONS.md#rq-02--what-work-belongs-to-synthesis-and-imagination), [RQ-07](../../RESEARCH_QUESTIONS.md#rq-07--which-disagreements-deserve-executable-variants)
- **Related claims:** [K-002](../../CLAIMS.md#k-002), [K-003](../../CLAIMS.md#k-003), [K-004](../../CLAIMS.md#k-004), [K-010](../../CLAIMS.md#k-010), [K-016](../../CLAIMS.md#k-016), [K-024](../../CLAIMS.md#k-024)
- **Supersedes:** None
- **Superseded by:** None

## Context

The A Deduction gives Phase 1 a concrete analysis of apprehension,
reproduction, and recognition. The B Deduction foregrounds objective unity,
judgment, category application, and the restriction to sensible conditions.
Neither edition presents a software component diagram, and collapsing them
would hide a consequential interpretive choice.

## Grounds and claim status

### Textual

The A Deduction distinguishes three syntheses as subjective grounds of
cognition ([A98-110](../../sources/kant/deduction-a.md#a98)) and assigns
synthesis of the sensible manifold to imagination
([A120-126](../../sources/kant/deduction-a.md#a120)). The B Deduction treats
figurative synthesis and imagination in relation to understanding
([B151-152](../../sources/kant/deduction-b.md#b151)) and ties objective unity to
judgment and possible experience
([B137-148](../../sources/kant/deduction-b.md#b137),
[B159-169](../../sources/kant/deduction-b.md#b159)).

### Interpretive

Use the A analysis to expose synthesis operations and the B account to govern
judgment licensing and unity. This division is a project reading of the two
editions, not a claim that they are interchangeable or cumulative drafts.

### Analogical

Apprehension, reproduction, and recognition name provenance-preserving
operations over presented content. They are not mental acts, independent
software agents, generic parsing, cache retrieval, or classification.

### Engineering

One synthesis boundary owns the three operations. Understanding supplies or
constrains identity and unity rules; imagination executes them over presented
content. A named B-led variant may compress the stage vocabulary but must emit
comparable trace evidence.

## Options considered

### Option A: Threefold A-edition architecture only

This is inspectable and close to the A analysis, but it risks making a
substantially revised argument the project's unqualified account of Kant.

### Option B: B-edition architecture only

This sharpens objective unity and category use, but it provides less explicit
operational vocabulary for retention and recognition in a toy sequence.

### Option C: Hybrid default with an executable B-led variant

This uses each edition for a declared purpose and makes their difference
testable. Its cost is that the composite architecture requires careful labels
and cannot be attributed to either edition as written.

## Decision

Choose Option C. The default trace distinguishes apprehension, reproduction,
and recognition inside an imagination-led synthesis boundary, then applies
B-led judgment and unity constraints. Preserve a B-led variant only where it
changes trace stages or observable behavior; do not create variants for verbal
differences alone.

## Consequences

- Every synthesis trace names its edition-sensitive variant.
- Faculty boundaries are functional and shared rather than one-to-one code
  translations of Kant's names.
- Phase 2 needs an interface for synthesis policies, not separate services for
  each named operation.
- Evaluation must compare the variants on at least one retention-and-identity
  scenario.
- The project accepts the interpretive cost of a composite default.

## Observable consequences

With a sequence that requires retention of an earlier presentation for object
identity, the default trace exposes reproduction and recognition as separate
grounds. A B-led variant may combine them into figurative synthesis but must
still show why the manifold is combined under objective-unity constraints.

## Follow-up

K-010 and K-016 are Current and link this record from their grounds. The diagram
and worked-example deliverables must show both the default and the behaviorally
significant variant.
