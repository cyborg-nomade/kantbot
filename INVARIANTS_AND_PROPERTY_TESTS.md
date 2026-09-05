# Invariants and Property Tests

## Status and scope

This is the fifth Phase 2 deliverable. It makes selected philosophical and
software constraints executable over generated families of values in
[`tests/test_properties.py`](tests/test_properties.py). It complements the
hand-chosen examples for the [canonical values](CANONICAL_DATA_STRUCTURES.md),
[state transitions](STATE_TRANSITION_MODEL.md), and
[provenance graph](STRUCTURED_PROVENANCE.md); it does not replace them.

**Engineering.** The suite uses
[Hypothesis](https://hypothesis.readthedocs.io/en/latest/) as a development-only
dependency. A property states an invariant over a declared input domain;
Hypothesis explores that domain and shrinks a failure to a smaller
counterexample. Passing generated cases is evidence that the implementation
preserves the stated invariant, not a proof that Kant's theory is correct or
complete. This item introduces no new interpretation or cognitive algorithm.

The deterministic toy world remains the final Phase 2 Roadmap item.

## Why these properties

Example tests are clearest for the ten distinct terminal outcomes and a complete
successful trace. Generated tests are more useful where the constraint should
survive many values, lengths, orders, or combinations. The suite therefore
keeps one readable oracle or boundary per property and pairs successful cases
with a nearby invalid construction where that distinction matters.

| Constraint | Generated variation | Observable property | Grounds |
| --- | --- | --- | --- |
| Shared presentation does not rewrite supplied content | Finite scalar records and arbitrary integer positions | An exact presentation validates; altered content is rejected graph-wide | [K-015](CLAIMS.md#k-015), [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md) |
| Required sensible conditions control applicability | Nonempty vectors of satisfied, failed, and undecided results | Failure takes precedence, then undecided status, then applicability; every contrary reported status is rejected | [K-007](CLAIMS.md#k-007), [K-008](CLAIMS.md#k-008), [K-012](CLAIMS.md#k-012) |
| Rule authority remains typed | Every cognitive-ground kind and optional authority | Rule grounds require authority; non-rule grounds cannot claim it | [K-009](CLAIMS.md#k-009), [K-020](CLAIMS.md#k-020), [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md) |
| Evaluator state cannot become cognitive evidence | Every declared cognitive-ground kind | A registered evaluator identity resolves as none of them | [K-014](CLAIMS.md#k-014), [K-022](CLAIMS.md#k-022) |
| Evidence has causal rather than circular structure | Cycles containing two through eight derived elements | Every generated evidence cycle is rejected | [K-016](CLAIMS.md#k-016), [K-022](CLAIMS.md#k-022) |
| Registration order is not cognitive meaning | One through eight distinct observations in forward and reverse order | Resolution and immediate grounds are identical across registration orders | [K-022](CLAIMS.md#k-022), [structured provenance trade-offs](STRUCTURED_PROVENANCE.md#prefixes-trade-offs-and-revisit-points) |
| Withholding preserves explicit limits | Nonempty sets of strongest representations and unmet conditions | JSON round-trips without losing limits; an outcome whose report omits its unmet conditions is rejected | [K-023](CLAIMS.md#k-023), [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md) |
| One cycle retains its bounded episode | Finite observation sequences, positions, and scalar records | Opening and JSON round-trip preserve order; a foreign-episode observation is rejected | [K-021](CLAIMS.md#k-021), [K-022](CLAIMS.md#k-022) |

## Generated domains

Identifiers use the canonical ASCII grammar and are composed without filtering,
so generation does not discard malformed intermediate examples. Content covers
strings, booleans, integers, finite floats, and `None`, matching `ScalarValue`.
Collections are nonempty where the model requires them and are bounded at five
or eight members to keep the ordinary suite fast. Those size bounds are test
budgets, not philosophical or model limits.

The status property uses a small independent truth table as its oracle:

1. any failed required condition means `not-applicable`;
2. otherwise, any undecided required condition means `underdetermined`;
3. otherwise all required conditions are satisfied and the result is
   `applicable`.

Generated values always enter through ordinary public constructors or wire
validators. The tests do not use `model_construct`, mutate frozen instances,
or bypass validation to manufacture a failure.

## Layers and deliberate gaps

The testing pyramid for the current formal model is deliberately shallow:

- generated unit properties cover local value rules and wire round-trips;
- generated integration properties cover trace closure and the cycle boundary;
- deterministic examples retain the complete success path, every terminal
  kind, rival alternatives, cross-stage failures, and detailed commitment
  ancestry.

There is no end-to-end cognitive algorithm to fuzz in Phase 2. Properties about
recognition accuracy, schema procedure behavior, unity-policy soundness, or
differences between interpretive variants would invent implementations that
belong to Phase 3 or require the toy world. Phase 5 will need behavioral,
baseline, and ablation evidence; this suite cannot stand in for that evaluation.

## Running and reproducing

Run the generated properties alone, including exploration statistics, with:

```text
uv run pytest tests/test_properties.py -W error --hypothesis-show-statistics
```

They also run in the ordinary `pytest` and coverage commands. Hypothesis reports
a replayable counterexample when a property fails and locally stores examples
under `.hypothesis/`; that machine-local database is ignored by Git. A shrunk
counterexample that reveals a distinct regression should be promoted to a named
deterministic example test before the defect is fixed, while the general
property remains.

The suite has no network, wall-clock, randomness, or external-state oracle. Its
generated search can vary between runs, but every individual failing example is
ordinary serialized or canonical input that can be inspected and replayed.
