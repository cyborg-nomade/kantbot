# ADR 0001: Use constrained presentation at the input boundary

- **Status:** Proposed
- **Date:** 2026-08-31
- **Deciders:** Kantbot maintainers
- **Related questions:** [RQ-01](../../RESEARCH_QUESTIONS.md#rq-01--what-can-be-given-to-the-model)
- **Related claims:** [K-001](../../CLAIMS.md#k-001), [K-015](../../CLAIMS.md#k-015)
- **Supersedes:** None
- **Superseded by:** None

## Context

The first model must name what its input becomes at the reception boundary and
must define a form under which particulars can be available for synthesis. The
choice affects all later representations without deciding how external sensors
or parsers work.

## Grounds and claim status

### Textual

Sensibility is receptive and gives objects through intuition; intuition is
singular and immediate in contrast to discursive concepts
([A19-20/B33-34](../../sources/kant/critique-a.md#a19),
[A50/B74](../../sources/kant/critique-a.md#a50)). Space and time are forms of
human sensible intuition ([A22-25/B37-41](../../sources/kant/critique-a.md#a22),
[A30-32/B46-49](../../sources/kant/critique-a.md#a30)). The text does not say
that structured software input is intuition.

### Interpretive

The model preserves receptivity, particularity, and prior form without treating
an API record as literally given to a human mind. Temporal order is the minimum
form required for the first cycle; spatial order is scenario-dependent.

### Analogical

`Constrained presentation` names content admitted under a configured form. It
is analogous to the receptive role of sensibility but is not human sensibility,
intuition, affection, sensation, or access to a thing in itself.

### Engineering

Observations remain immutable external records. Reception adds episode,
ordering, and form metadata, while the trace exposes those choices. Parsing and
input validation remain outside the cognitive role.

## Options considered

### Option A: Call admitted inputs intuitions

This keeps the vocabulary close to Kant but invites a false literal
equivalence and hides the difference between serialized records and sensible
affection.

### Option B: Use constrained presentation

This preserves the functional distinction while keeping the analogy explicit
and contestable. It is less compact but makes the project's claim status clear.

### Option C: Treat input as an unformed fact stream

This is computationally simple but loses the priority of form and silently
turns already-described facts into objects before synthesis.

## Decision

Choose Option B. Implementation-facing documents use `constrained
presentation`; philosophical discussion may compare that role to intuition
only with an Analogical label. Require temporal form, and require spatial form
only for scenarios whose rules depend on it.

## Consequences

- The specification distinguishes observations, presented elements, and a
  manifold.
- Input records do not arrive with philosophically licensed object identity.
- Every trace declares its episode boundary and form.
- The model does not attempt to reproduce sensation or affection.
- A future variant may strengthen or reject the analogy without renaming its
  external input format.

## Observable consequences

The same observation content under different admissible temporal orderings can
produce different candidate events. Content lacking the required ordering form
is `not-presentable`, rather than being silently coerced into an object record.

## Follow-up

If accepted, make K-015 Current and link this record from its grounds. Phase 2
must define the observation, presented-element, manifold, and form types.
