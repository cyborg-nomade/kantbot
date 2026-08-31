# ADR 0004: Make limit outcomes and rule authority behaviorally distinct

- **Status:** Proposed
- **Date:** 2026-08-31
- **Deciders:** Kantbot maintainers
- **Related questions:** [RQ-06](../../RESEARCH_QUESTIONS.md#rq-06--how-will-the-model-represent-the-limits-of-cognition)
- **Related claims:** [K-009](../../CLAIMS.md#k-009), [K-014](../../CLAIMS.md#k-014), [K-019](../../CLAIMS.md#k-019), [K-020](../../CLAIMS.md#k-020), [K-023](../../CLAIMS.md#k-023)
- **Supersedes:** None
- **Superseded by:** None

## Context

The first model must distinguish uncertainty, ordinary missing data, failed
synthesis, withheld judgment, and claims that exceed their licensed scope. It
must also reserve regulative guidance for Phase 4 without letting such guidance
become object-level evidence in the meantime.

## Grounds and claim status

### Textual

Categories yield cognition only under conditions in which an object can be
given ([B146-169](../../sources/kant/deduction-b.md#b146)). Noumena mark a
boundary rather than supplying positively cognized objects
([A249-260/B294-315](../../sources/kant/critique-a.md#a249),
[B306-309](../../sources/kant/second-edition-excerpts.md#b306)). Constitutive
principles determine objects of possible experience, while regulative
principles guide inquiry without constituting their objects
([A179-180/B222-223](../../sources/kant/critique-a.md#a179),
[A509-515/B537-543](../../sources/kant/critique-a.md#a509)).

### Interpretive

An absent or violated condition should produce the most specific available
failure or withholding status. Overreach requires an illicit promotion beyond
declared presentation conditions or rule authority; it is not a synonym for
falsehood or uncertainty.

### Analogical

A regulative rule may direct future inquiry but cannot ground a present object
predicate. The model does not represent a noumenon as hidden scenario state,
and a limit report is not knowledge of what lies beyond the limit.

### Engineering

Every rule declares `constitutive`, `regulative`, or `engineering` authority.
Terminal outcomes are tagged and carry failed conditions, alternatives, scope,
and provenance. Evaluator-only hidden state cannot appear in cognitive warrant.

## Options considered

### Option A: One confidence score for all incomplete results

This is compact but collapses ambiguity, violated conditions, conflicts, and
scope errors into a single quantitative scale.

### Option B: Typed outcomes and typed rule authority

This makes failures and limits inspectable and prevents regulative guidance
from licensing object claims. It requires more explicit transitions and tests.

### Option C: Compare every claim with hidden toy-world truth

This supports conventional accuracy scoring but misrepresents inaccessible
ground truth as the model's analogue of a thing in itself.

## Decision

Choose Option B. Distinguish input error, non-presentability, synthesis failure,
synthesis ambiguity, failed or underdetermined application, unity conflict,
withholding, commitment, and overreach. Use hidden scenario state only for
external evaluation. A regulative rule may organize inquiry but never supply an
object-level ground.

## Consequences

- Confidence may qualify an admissible path but cannot replace typed outcomes.
- Overreach requires a traceable scope or authority violation.
- The first cycle reserves regulative metadata while deferring reason's active
  inquiry to Phase 4.
- Negative cases become successful, testable outputs rather than exceptions.
- Evaluation must distinguish model warrant from evaluator knowledge.

## Observable consequences

A regulative preference can cause one follow-up observation to be requested
before another, but adding it to a predicate's warrant causes `overreach` and
blocks judgment. A hidden scenario label may reveal that a withheld judgment
would have been true, yet the system must still withhold it when presentation
or synthesis conditions are absent.

## Follow-up

If accepted, make K-020 Current and link this record from its grounds. Keep
K-019 Deferred until Phase 4 implements reason, while using this record to
constrain the reserved overreach status. Phase 2 must define the typed result
and rule-authority fields.
