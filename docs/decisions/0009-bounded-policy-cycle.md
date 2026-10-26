# ADR 0009: Execute a bounded cognitive cycle with explicit policies

- **Status:** Proposed
- **Date:** 2026-10-26
- **Deciders:** Project maintainer
- **Related questions:** [RQ-02](../../RESEARCH_QUESTIONS.md#rq-02--what-work-belongs-to-synthesis-and-imagination), [RQ-03](../../RESEARCH_QUESTIONS.md#rq-03--what-makes-a-representation-count-as-an-object), [RQ-05](../../RESEARCH_QUESTIONS.md#rq-05--what-functional-unity-can-the-model-require)
- **Related claims:** [K-011](../../CLAIMS.md#k-011), [K-012](../../CLAIMS.md#k-012), [K-018](../../CLAIMS.md#k-018), [K-022](../../CLAIMS.md#k-022), [K-024](../../CLAIMS.md#k-024), [K-028](../../CLAIMS.md#k-028), [K-029](../../CLAIMS.md#k-029), [K-030](../../CLAIMS.md#k-030)
- **Supersedes:** None; implements the accepted roles and extends ADR 0007's instruction vocabulary
- **Superseded by:** None

## Context

Phase 2 supplies immutable representations, callable protocols, checked
transitions, graph validation, and a deterministic sensor. Its tests largely
hand-author cognitive products. The first Phase 3 item must compute those
products from observations through a reusable cycle with meaningful policy
variation.

The worked strip examples leave necessary implementation choices open: which
interval recognition covers, whether a predicate can select between identity
branches, how the B-led variant changes execution, how missing presentation
affects the cycle, and how a bounded search reports exhaustion. The finite
procedure vocabulary also lacks the examples' displacement bound.

## Grounds and claim status

### Textual

The existing grounds remain the A analysis of synthesis
([A98–110](../../sources/kant/deduction-a.md#a98)), B-led figurative synthesis
and objective unity ([B137–152](../../sources/kant/deduction-b.md#b137)), and
sensible schematization ([A137–147/B176–187](../../sources/kant/critique-a.md#a137)).
These passages do not prescribe a cartesian search, a displacement constant,
Python callables, or episode budgets.

### Interpretive

Retain the A-analysis/B-constraint default and meaningful B-led alternative
from [ADR 0002](0002-a-b-synthesis.md). Preserve
[ADR 0003](0003-object-and-judgment-licensing.md)'s independent object,
applicability, and commitment gates, and
[ADR 0004](0004-limit-outcomes-and-rule-authority.md)'s distinct limits and
rule authority. Supplying segmented patches under
[ADR 0008](0008-deterministic-strip-sensor.md) leaves cross-time identity to
the cycle rather than the sensor.

### Analogical

The library's synthesis changes which sensible combinations are available as
candidate unities. Unity checks determine whether all grounds can license one
scoped commitment. These constrained operations make the executable hypothesis
in [K-027](../../CLAIMS.md#k-027) experimentally concrete. Their adequacy for
cognition depends on what these restrictions explain or fail to explain.

### Engineering

The new commitments are the bounded whole-interval path domain, explicit policy
callables with common licensing checks, and an additional replayable spatial
instruction. They are proposed under [K-030](../../CLAIMS.md#k-030), with limits
and costs documented in the [library guide](../../COGNITIVE_CYCLE.md).

## Options considered

### Option A: Separate complete executors for each interpretation

Each variant could implement the whole cycle as an explicit function. This
makes each reading easy to follow in isolation and allows large differences
without forcing them through one role bundle. It is attractive when variants
really disagree about the representation sequence.

The present variants share most representations and licensing requirements.
Duplicating reception, provenance, application, and commitment would make
comparative changes harder to isolate and corrections harder to propagate.
Retain this option when a later critique changes the architecture enough to
outgrow the current shared cycle.

### Option B: A registry or event framework for arbitrary cognitive components

A registry could support plugins, dynamic procedures, incremental execution,
and broadly different graphs. It would scale to experiments whose operations
and scheduling are not yet known, and could associate implementations with
versioned names.

It would also introduce lifecycle, dispatch, loading, and trust machinery before
this bounded experiment needs them. Such flexibility would not itself prove
that a loaded procedure preserved the declared warrant. Portable replay would
still require the safeguards discussed in
[ADR 0007](0007-replayable-sensible-licenses.md).

### Option C: Explicit pure roles and a bounded checked coordinator

Use a frozen data plan and a frozen bundle of ordinary callable policies.
Compose them through the existing transitions, validate each graph prefix, and
keep the original domain values authoritative. This permits controlled changes
to retention, recognition, projection, and unity without a framework or mutable
faculty objects.

The costs are explicit orchestration code, repeated graph validation, and a
deliberately narrow domain for completeness checking. The shared cycle also
limits which interpretations can fit without changing contracts. These costs
are acceptable for the first bounded experiment if they remain visible and
are revisited when a concrete variant requires a different domain.

## Decision

Propose **Option C**. The branch implements it for review:

1. One cycle receives a finite admitted observation tuple, freezes its resources,
   and tests one selected concept through its schema. World and evaluator
   capabilities stay outside cognitive arguments.
   Separate nominal form definitions from episode availability using an optional
   `ProjectionRequest.available_form_ids`; its original default means all
   required forms are available. An unavailable required form produces an
   explicit projection refusal, while the nominal resource remains defined.
2. In the initial strip domain, a path chooses one retained intuition per
   temporal moment across the available interval. Enumerate every combination
   within the declared budget and preserve every admitted rival. A replacement
   recognizer must agree with this domain and the selected rules; changing the
   domain requires an explicit model revision.
3. The A-led default exposes apprehension, reproduction, and recognition before
   the object gate. B-led figurative synthesis jointly reproduces and forms
   candidates under both identity and constitutive-unity rules, retaining the
   canonical intermediate evidence in one operation. Both use final unity.
4. Add `BoundedDisplacement` to the finite instruction vocabulary. Require
   temporal and spatial form, two samples, numeric content, and an explicit
   maximum displacement per elapsed tick. Replay the instruction for imported
   object licenses as well as during recognition. This is an additive version-2
   operation; old readers reject unsupported operations.
5. Preserve the three licensing gates. Predicate success cannot select a
   singular subject among several licensed objects. Stop at synthesis ambiguity
   by default; a declared continuation policy evaluates the branches and
   withholds an unresolved singular judgment.
6. Earlier samples must be reproduced under the selected retention rule.
   Retention must preserve every presentation at the final admitted moment.
   Mandatory reception, procedure-replay, candidate-completeness, and unity
   checks remain in force around replaceable roles. Additional unity policies
   can strengthen the common checks; their successful conditions join the
   committed warrant.
7. Preserve empty/unreadable shared input and each successful projection, but
   stop the initial episode before synthesis if any required patch projection
   fails. More permissive partial-episode continuation needs a revised contract.
8. Default to at most 64 observations and 256 possible identity combinations.
   Exceeding a budget raises an engineering capacity error before candidate
   truncation; it is not a proof of synthesis failure.

## Consequences

The library can compute complete warranted results and inspectable refusals
from sensor observations, while the accepted immutable types, role signatures,
and graph validation remain usable independently. No runtime dependency or
arbitrary procedure loading is added.

The strip domain does not discover object births, deaths, occluded paths, or
maximal subintervals. The constants and sample minima belong to this experiment.
Graph validation alone still cannot certify arbitrary Python implementations
or the meaning of free-text propositions. Configuration IDs must be managed
explicitly by experiments; they are not hashes of code. Repeated validation and
mutual alternative links can become quadratic. Broader environments should
revisit those costs and the shared representation sequence before scaling.

## Observable consequences

- Rightward motion commits; stationary and reordered inputs preserve object
  formation but fail the motion predicate; a short interval remains undecided.
- Removing reproduction prevents both variants from manufacturing identity
  through raw batch access. Excess displacement or broken color prevents
  objecthood before empirical application.
- Rival paths survive. Successful predicates on rivals withhold a singular
  subject; a greedy callback that drops an admitted path is rejected.
- A stricter local unity condition changes where the A-led and B-led variants
  fail and which candidate records survive.
- Merged identity grounds or excessive modality fail unity; regulative
  promotion yields overreach. Replacement policies cannot waive these checks.
- Missing patch fields remain explicit refusals, and search-budget exhaustion
  remains distinct from a cognitive terminal outcome.

## Follow-up

On maintainer approval, accept this record and promote K-030 from Provisional.
Later Phase 3 items extend the worked-example suite, negative-case coverage,
dedicated trace presentation, and demonstration interface as separately
reviewable work. Later experiments should revisit partial presentation,
tracking subintervals, broader policy domains, and the computational costs.
