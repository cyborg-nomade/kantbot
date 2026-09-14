# ADR 0008: Replay a scripted strip through an anonymous patch sensor

- **Status:** Proposed
- **Date:** 2026-09-14
- **Deciders:** Project maintainer
- **Related questions:** [RQ-01](../../RESEARCH_QUESTIONS.md#rq-01--what-can-be-given-to-the-model), [RQ-02](../../RESEARCH_QUESTIONS.md#rq-02--what-work-belongs-to-synthesis-and-imagination), [RQ-06](../../RESEARCH_QUESTIONS.md#rq-06--how-will-the-model-represent-the-limits-of-cognition)
- **Related claims:** [K-014](../../CLAIMS.md#k-014), [K-015](../../CLAIMS.md#k-015), [K-022](../../CLAIMS.md#k-022), [K-028](../../CLAIMS.md#k-028), [K-029](../../CLAIMS.md#k-029)
- **Supersedes:** None
- **Superseded by:** None

## Context

The last Phase 2 item requires a deterministic world with reproducible
observations. The [worked examples](../../WORKED_EXAMPLES.md#shared-toy-world-and-frozen-configuration)
already use a one-dimensional strip. They illustrate whole frames, including
frames with several patches, but leave the executable input format to Phase 2.

Canonical observation content is scalar. Accepted
[ADR 0007](0007-replayable-sensible-licenses.md) supports field selection, not
frame segmentation. The sensor must not silently implement a new projection
operation or pre-solve persistent identity. It must also separate the
experimenter's hidden marker identity from admitted cognitive grounds.

## Grounds and claim status

### Textual

The registered distinction between receptive presentation and thought constrains
this boundary ([K-001](../../CLAIMS.md#k-001),
[A19–20/B33–34](../../sources/kant/critique-a.md#a19),
[A50–51/B74–75](../../sources/kant/critique-a.md#a50)). These passages do not
specify cameras, coordinates, structured records, or a sensor algorithm.

### Interpretive

[ADR 0001](0001-variant-scoped-receptive-terminology.md) still governs admission
as intuition, and [ADR 0003](0003-object-and-judgment-licensing.md) still requires
separate object and judgment licenses. No new interpretation of a faculty is
adopted here. A patch sample cannot count as an already synthesized persistent
object.

### Analogical

Anonymous momentary patches offer bounded material for an experiment in
synthesis. Their presegmentation and discrete coordinates simplify what can be
given. That cost matters to evaluating how closely implementation approaches
cognition; it must remain visible and revisable. Hidden simulation identities
serve external experiments, not a computational identification of noumena
([K-014](../../CLAIMS.md#k-014)).

### Engineering

The finite script, anonymous sensor, stable frame-local IDs, and separate
evaluator export implement proposed [K-029](../../CLAIMS.md#k-029). This adds no
runtime dependency or arbitrary executable scenario code, and does not change
the cognitive provenance wire version.

## Options considered

### Option A: Store only canonical observation fixtures

Literal JSON observations are the smallest implementation and easiest for a
non-programmer to inspect. Existing traces can consume them directly, with
little code to maintain. They suffice to replay many fixed cases.

They do not implement the world-to-observation boundary. Hidden-identity
invariance becomes a fixture convention rather than a test of an actual sensor;
preferred identity paths can be embedded in IDs unnoticed. Retain observation
oracles in tests, but do not use fixture storage alone as the world.

### Option B: Simulate dynamics and render complete frames for segmentation

A simulator with velocities, collisions, occlusion, and frame-level perception
would let behavior emerge from general world rules. Keeping segmentation in a
reviewed receptive operation could expose more of the problem of individuation
instead of supplying patches. This is the strongest option for extending the
eventual perceptual experiment.

It introduces an environment dynamics policy and a substantive projection
operation now. Rendering, collision, and segmentation assumptions could dominate
the initial results. Scalar projection cannot implement it without extending
ADR 0007. Defer this scope, not its philosophical value; it deserves its own
reviewed work.

### Option C: Script world snapshots and apply a fixed anonymous patch sensor

Keep immutable snapshots with evaluator-only marker IDs, then derive ordinary
observations from visible coordinate/color pairs. The sensor becomes executable
and testable while preserving exact control over worked examples. Readable
Python values and pure functions suffice; no seed, physics engine, or mutable
runtime is needed.

The sensor supplies segmentation at one moment, simplifying receptive
individuation. The world is scripted rather than a theory of physical dynamics,
and its symbolic treatment of coincident colors is not optics. These costs are
acceptable for the bounded Phase 2 experiment only if documented and kept out
of claims about the adequacy of the full model.

## Decision

Propose **Option C** for maintainer review. The branch implements it, but this
record remains Proposed until approved.

- Hidden IDs belong to the external world. Canonical observations contain only
  momentary visible content and public metadata.
- One readable distinct `(x, color)` pair produces one sample. Identical
  coincident pairs collapse; different pairs are sorted by visible values only.
- Empty and unreadable frames produce distinct status observations, not
  fabricated patches, hidden counts, or silently skipped frames.
- Observation IDs depend on public episode, temporal position, and local slot,
  never hidden identity, storage order, previous identity, or future snapshots.
- No cognitive rule, expected outcome, interpretation policy, or world state
  travels in the observation envelope. Evaluator references have a separate
  export and namespace.
- Scope this item to input generation, replay, and compatibility tests. Existing
  procedures may be exercised through test-only structural fixtures;
  cognitive-role implementations remain Phase 3 work.

## Consequences

The input boundary is inspectable and reproducible without an implicit tracker.
Rival paths remain available even when the experimenter knows which marker
persisted. An empty or impaired frame records a limit of supplied content,
not already a cognitive terminal outcome.

The cost is idealized within-frame segmentation. Later raw frame perception
must revisit this decision with a replayable projection operation; it cannot
inherit a proof of adequacy from these tests. The package is an API separation,
not a security sandbox. Replay drivers must keep world state and unadmitted
future inputs outside a cycle's arguments.

## Observable consequences

1. Repeated export, JSON round-trip, and separate processes reproduce identical
   observation bytes under the locked environment.
2. Hidden renaming, identity swaps across time, and marker storage reordering
   leave observations unchanged with fixed visible content. Hidden coincident
   multiplicity and unreadable content do not leak.
3. Simultaneous middle-frame patches have distinct sample IDs but one temporal
   position; their slots supply no persistent identity path.
4. `0, 1, 2` versus `0, 2, 1` changes the increase check while preserving color
   constancy. These are procedure results, not complete judgments or the full
   identity rule `I-1`.
5. Empty/unreadable records survive reception but cannot invent fields required
   by the patch projection. Evaluator references do not resolve as cognitive
   grounds in the existing graph validator.

## Follow-up

- On approval, accept this record and update K-029 and the guide's review status
  in the same PR before merge.
- Phase 3 implements cognitive roles, including complete identity conditions,
  branch alternatives, projection refusals, and worked-example contrasts. It
  must not receive hidden world state.
- Later perceptual experiments should compare presegmented input with explicit
  frame-level segmentation and report what changes.
