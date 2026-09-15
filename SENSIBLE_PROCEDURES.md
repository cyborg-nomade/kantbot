# Replayable Sensible Procedures

## Scope

**Engineering.** The corrective Phase 2 implementation associated with
[accepted ADR 0007](docs/decisions/0007-replayable-sensible-licenses.md) makes
declared sensible licenses replayable. It strengthens the existing contracts;
the [toy-world input boundary](TOY_WORLD.md) is a separate deliverable, and the
complete cognitive-role implementation remains Phase 3 work.

The separation is now executable:

```text
Understanding: rule/concept + declared conditions + general procedure
                                      |
Sensibility: presented content -> intuition under form -> ordered manifold
                                      |
                procedure applied to selected sensible sequence
                                      |
                computed conditions + actual intuition evidence
                     /                              \
       object-formation license            empirical applicability
```

Object formation uses the selected identity and category-inspired rules'
procedures. Later empirical predication uses its own schema; passing the latter
cannot repair a failed object license. This implements the distinction in
[K-012](CLAIMS.md#k-012), not a derivation of all categories.

## Inputs and receptive admission

`ProvenanceView.intuition_for` exposes immutable content, position, and grounds.
`candidate_for` exposes the selected ordered intuition IDs; `rule_for` exposes
general conditions and procedures; `forms_for` returns an intuition's actual
registered forms. Recognition can resolve its retained IDs and application can
resolve its object's candidate. None of these operations can return evaluator
state or coerce an observation ID into an intuition.

`FieldProjection` lists supplied fields to select, in output order. Successful
Kantian admission requires representation kind `intuition`, exactly the supported
criteria `singular`, `preconceptual`, and `temporal-order`, and a temporal form.
The output must reproduce that selection and preserve the supplied position.
One presented particular is selected, without consulting concepts or inferring
properties. These are deliberately minimal operational readings of singularity
and preconceptuality, not a solution to their philosophical interpretation.

Selection may omit fields but cannot rename, invent, or alter them. Missing
selected fields prevent successful projection. Declarations that fail admission
can remain in a trace ending in `not-presentable`; a phase-3 role will construct
that refusal. Different segmentation or representation kinds need explicit
reviewed operations rather than silently reusing this license.

## General procedures

[`SensibleProcedure`](src/kantbot/model/procedures.py) contains one typed check
per declared condition, plus an explicit temporal form reference when needed.
[`evaluate_procedure`](src/kantbot/procedures.py) computes results from the
provided intuitions and forms. It neither chooses a candidate nor commits a
judgment.

| Check | Executable requirement | Sensible limitation |
| --- | --- | --- |
| `FieldEquals` | Every sample's named field equals a fixed empirical value, including its scalar type | No samples or an absent field is undecided; `True` is not numeric `1` |
| `FieldConstant` | The field retains the same typed value across the ordered sequence | Requires a temporal form and at least two samples (default two) |
| `StrictIncrease` | Numeric field values strictly increase at every adjacent sample | Requires temporal form, at least two samples, and numeric values; booleans are not numbers here |
| `TemporalOrder` | Enough samples occupy strictly increasing positions | Requires temporal form and at least two samples (default two) |

All temporal procedures check the actual registered `FormKind.TEMPORAL` and its
availability to every input. They never sort inputs. Unavailable temporal form
produces undecided in standalone evaluation; claiming a successful projection
without that form is invalid graph provenance. Non-increasing positions fail a
temporal procedure. Too few samples, absent fields, or nonnumeric inputs to
increase produce undecided; comparisons run only after those prerequisites.

Manifolds preserve nondecreasing positions. Retention and candidate selection
preserve subsequence order. Simultaneous positions can be represented in a
manifold but cannot satisfy these initial strictly successive procedures.
Registration order in the trace's top-level collections remains irrelevant.

`FieldConstant` and `TemporalOrder` reject declarations with a sample minimum
below two. With only one actual sample, a valid temporal procedure returns
undecided and cannot license objecthood. The base success fixture now carries
two observed moments, with both preserved in the warrant and replay evidence.
A single observation may still be projected or tested with `FieldEquals`;
being presentable does not itself establish constancy or succession.

This is an engineering evidence floor for these initial procedures, not a
claim that every possible Kantian category requires two empirical observations.
Neither field constancy nor numerical increase alone establishes substance or
causality. Those adequacy questions remain visible under the adopted
[philosophical specification](PHILOSOPHICAL_SPECIFICATION.md#power-of-judgment-and-schematism-applicability).

## Certification, errors, and failures

The graph resolves the actual candidate and uses **all** its intuition IDs as
procedure input. No caller can replace that sequence with convenient evidence.
Recorded results must match recomputed condition IDs, required flags, statuses,
and ordered intuition evidence. Rule conditions have the same authority checks
as concept conditions; top-level constitutive authority cannot launder a
regulative condition.

General rules have no object-licensing role. Identity rules and category-inspired
rules must supply required conditions and temporal mediation. An empirical
concept may use `FieldEquals`; calling that concept category-inspired requires
an actual temporal check, not just a renamed class or form.

A failed/undecided application can be stored and reported through the existing
typed outcomes. It cannot ground a proposal. A failed object condition cannot
produce an `ObjectCandidate`; the weaker candidate and its sensible ancestry
remain available. A fabricated success raises `InvalidProvenance` rather than
being converted into a cognitive refusal.

Successful commitment and reporting require a matching `ProvenanceGraph` in
addition to adjacent stage values. Serialized stage snapshots still validate
local shape only; loading one is not certification of its history. See the
[state model](STATE_TRANSITION_MODEL.md#invalid-transitions-versus-cognitive-limits).

## Version 2 and limits

Version 1 traces are rejected. To rebuild an old trace, explicitly add the
projection operation and supported criteria, distinguish concept/rule kinds,
bind rule and schema conditions to executable checks, and recompute results
and evidence. Changing only the version number must not grant a new license.

Procedure descriptions and proposition text are not parsed as programs. The
validator proves agreement with the supported instructions, not that the
selected instructions capture their descriptions, that input reports reality,
or that the complete model approaches human cognition. Those are experimental
questions, not conclusions to be hidden by successful serialization or tests.

## Verification

- [Audit regressions](tests/test_sensible_contracts.py): the eight counterexample
  families, typed content lookup, authority, missing data, and certification.
- [Temporal licenses](tests/test_temporal_licenses.py): separate pre-object
  identity failure and post-object motion failure over multiple observations.
- [Minimum temporal evidence](tests/test_temporal_minimum.py): singleton
  declarations are rejected, singleton evaluations remain undecided, and a
  singleton candidate cannot reuse a temporal object license.
- A generated numerical-order property compares `StrictIncrease` against an
  independent pairwise arithmetic oracle.

Run `uv run pytest tests/test_sensible_contracts.py tests/test_temporal_licenses.py
-W error` as one command, then the complete checks in
[CONTRIBUTING](CONTRIBUTING.md#python-readability-and-static-analysis).
