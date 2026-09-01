# Behavioral Prediction Catalog

## Status and purpose

This catalog completes the Phase 1 requirement to state how the declared
architecture should differ observably from a simpler pipeline. Each entry is a
conditional engineering prediction: if an implementation preserves the
semantic commitments in the
[philosophical specification](PHILOSOPHICAL_SPECIFICATION.md), then a controlled
change to an episode, rule, or trace should produce the difference stated here.

The predictions make the architecture refutable as an implementation. Passing
them would not prove that Kant's account is correct, complete, or faithfully
descriptive of human cognition. Failing them would show that the implementation
does not yet realize one or more declared roles, even if it uses Kantian names
or emits plausible sentences. This is the evaluation posture required by
[K-027](CLAIMS.md#k-027).

All entries are **Engineering** consequences of existing textual,
interpretive, analogical, and engineering claims. They introduce no new
philosophical decision. The scenario values and test notation are illustrative,
not Phase 2 types or algorithms. Stable prediction IDs should be retained when
the examples become executable fixtures.

## What counts as observable behavior

The committed sentence is only one observable. A comparison also includes:

- the terminal outcome;
- candidate representations and application results reached before it;
- alternatives preserved or discarded;
- the transformations and rules that causally ground each state;
- each rule's constitutive, regulative, or engineering authority;
- the scope and modality of any proposed or committed judgment; and
- the failed or missing conditions in the limit report.

A stage label or prose explanation added after a result is not evidence that
the stage did cognitive work. An architectural trace is behaviorally meaningful
only when changing or removing one of its required grounds changes the result
in the predicted way. Predictions BP-002 and BP-007 test this directly.

## Comparison pipeline

The canonical comparison is a deliberately capable but simpler
**greedy classify-and-assert pipeline**:

1. validate the external record;
2. extract features from the episode, optionally including order;
3. greedily aggregate or track the highest-scoring candidate;
4. score predicate labels against that candidate; and
5. assert the highest label above a threshold, otherwise return one generic
   unknown or low-confidence result.

The comparison pipeline may be deterministic, stateful, and accurate. What it
lacks by definition is a substantive variant-projection boundary, licensed
reproduction, explicit rival identity branches, separate object/application/
commitment gates, cycle-wide provenance unity, and typed rule authority. Its
trace may explain a result but is not required to license it.

This baseline is not claimed to represent every conventional system. A more
elaborate baseline may match individual predictions. If it matches the whole
catalog by adding the same causal distinctions and limit behavior, it has
become functionally closer to this architecture; the catalog discriminates
behavioral commitments, not class names or implementation style.

## Comparison protocol

Every executable comparison should:

1. freeze the observation episode, interpretation, form, concepts, schemas,
   rule authorities, scope, and deterministic tie-breaking policy;
2. run a control and a contrast that differ only in the named perturbation;
3. provide the same cognitive inputs to Kantbot and the comparison pipeline;
4. keep evaluator-only hidden state outside both cognitive input sets unless a
   prediction explicitly tests illicit promotion;
5. record the terminal status, proposition, candidates, applications,
   alternatives, grounds, authorities, and scope that each system can expose;
6. distinguish an absent field from an empty or passing field; and
7. report whether the predicted difference occurred and which invariant made
   it occur.

The observation dimensions above are an evaluation checklist, not a canonical
serialized result. Phase 2 must choose the formal representation.

## Catalog summary

| ID | Controlled contrast | Predicted architectural difference | Principal commitment |
| --- | --- | --- | --- |
| [BP-001](#bp-001) | Reorder one episode without changing its content multiset | Temporal application changes while a bag-of-features result does not | Form and schematized application |
| [BP-002](#bp-002) | Remove licensed reproduction from a retention-dependent episode | Identity synthesis fails despite unchanged raw observations | Synthesis and imagination |
| [BP-003](#bp-003) | Introduce two admissible identity paths | Alternatives remain explicit instead of becoming an argmax choice | Ambiguity as a first-class outcome |
| [BP-004](#bp-004) | Present a persistent but stationary candidate to `moving-right` | Object formation succeeds while concept application fails | Separate object and application gates |
| [BP-005](#bp-005) | Let the same predicate apply on rival identity branches | Application succeeds while judgment is withheld | Separate application and commitment gates |
| [BP-006](#bp-006) | Merge incompatible branch-relative grounds in one proposal | Locally valid states yield `unity-conflict` at the cycle boundary | Apperception as provenance unity |
| [BP-007](#bp-007) | Delete a required warrant edge without changing the computed sentence | Commitment is withdrawn rather than retaining a post-hoc explanation | Provenance by construction |
| [BP-008](#bp-008) | Hold scalar confidence constant across different limit cases | Typed outcomes and permitted next claims remain different | Limits are not one uncertainty score |
| [BP-009](#bp-009) | Change evaluator-only hidden identity while observations remain fixed | Cognitive output is invariant; illicit use produces `overreach` | Presentation scope and evaluator separation |
| [BP-010](#bp-010) | Toggle or promote a regulative preference | Object judgment is invariant unless promotion is rejected as an authority violation | Constitutive versus regulative rules |
| [BP-011](#bp-011) | Remove required temporal form or substitute a label-only projection | The Kantian variant refuses or exposes a failed safeguard while shared presentation survives | Shared boundary and variant projection |
| [BP-012](#bp-012) | Run one retention episode under the default and B-led policies | Stage structure changes, but retention, identity, unity, and sensible-use evidence remain comparable | Edition-sensitive synthesis variants |

## Detailed predictions

<a id="bp-001"></a>
### BP-001 — Temporal order changes applicability

**Setup.** Use the successful marker episode in
[Worked Example Trace 1](WORKED_EXAMPLES.md#trace-1):
amber positions `[0, 1, 2]` at ordered times `[0, 1, 2]`. In the contrast,
preserve the same three observation contents and identities but assign the
positions to the order `[0, 2, 1]`.

**Kantbot expectation.** The control commits `moving-right`. The contrast can
still form a locally coherent object under the illustrative identity rule, but
the schema sees differences `[+2, -1]` and returns
`concept-not-applicable`. The trace must identify temporal form and the failed
successive-difference condition as causal grounds.

**Comparison expectation.** An order-insensitive feature multiset is identical
and therefore produces the same label and confidence. A baseline configured
with temporal features may match the output difference, but it still has to be
compared on the separate application and commitment evidence.

**Falsifier.** The prediction fails if the Kantbot implementation commits the
same rightward-motion judgment after reordering without an explicit rule that
makes order irrelevant, or if the trace cannot identify which temporal
condition changed.

**Grounds.** [Specification consequence 1](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-012](CLAIMS.md#k-012), and [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).

<a id="bp-002"></a>
### BP-002 — Identity depends on licensed reproduction

**Setup.** Use the same three-frame episode. The control enables retention rule
`R-1`; the contrast leaves every observation and rule unchanged except that
earlier intuitions are not licensed for reproduction when the last intuition
is processed. The fixture's identity rule requires the prior presentations to
be available through that retention path.

**Kantbot expectation.** The control reaches `judgment-committed`. The contrast
reports `synthesis-failed` for the across-time identity path and names the
missing reproduction ground. Raw access to the serialized batch cannot silently
replace the disabled cognitive operation.

**Comparison expectation.** A batch classifier or tracker that reads all
frames directly retains the same features and emits the same identity or motion
label in both runs.

**Falsifier.** The prediction fails if Kantbot preserves the identity judgment
after `R-1` is removed without exposing another declared retention rule. A
B-led policy also fails this test if it succeeds while omitting comparable
retention evidence from figurative synthesis.

**Grounds.** [Specification consequence 2](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-016](CLAIMS.md#k-016), [ADR 0002](docs/decisions/0002-a-b-synthesis.md), and
[Worked Example Traces 1–2](WORKED_EXAMPLES.md#trace-1).

<a id="bp-003"></a>
### BP-003 — Rival identities survive a scoring tie

**Setup.** Use
[Worked Example Trace 3](WORKED_EXAMPLES.md#trace-3):
one amber patch at `t=0`, two admissible middle patches, and one at `t=2`.
Configure equal evidence for both identity paths and a deterministic baseline
tie-breaker.

**Kantbot expectation.** Both candidate representations and their separate
provenance remain visible. This fixture stops at the synthesis boundary and
returns `synthesis-ambiguous`. A separate fixture may continue branch-relative
application, but no later stage may silently erase the alternative.

**Comparison expectation.** The greedy pipeline selects the path favored by
its tie-breaker and exposes at most the chosen candidate plus a confidence
value.

**Falsifier.** The prediction fails if Kantbot emits only one candidate, treats
the tie-breaker as constitutive evidence, or reports ambiguity without the
rival grounds needed to reconstruct both paths.

**Grounds.** [Specification consequence 3](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-023](CLAIMS.md#k-023), and [ADRs 0003](docs/decisions/0003-object-and-judgment-licensing.md)
and [0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md).

<a id="bp-004"></a>
### BP-004 — Object formation does not force predication

**Setup.** Use
[Worked Example Trace 4](WORKED_EXAMPLES.md#trace-4):
an amber patch persisting at position `[2, 2, 2]`. Test the empirical concept
`moving-right`.

**Kantbot expectation.** Identity and local constitutive unity produce an
object candidate. The schema then fails on differences `[0, 0]`, producing
`concept-not-applicable` while retaining the object candidate.

**Comparison expectation.** A classifier may emit `stationary`, `not-moving`,
or a low score for `moving-right`, but its result does not independently expose
that object formation passed before predicate application failed.

**Falsifier.** The prediction fails if a failed predicate deletes the object
candidate, if objecthood is granted only after a label scores highly, or if
the implementation cannot report the passing identity grounds separately from
the failed schema conditions.

**Grounds.** [K-011](CLAIMS.md#k-011), [K-012](CLAIMS.md#k-012),
[K-017](CLAIMS.md#k-017), and [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).

<a id="bp-005"></a>
### BP-005 — Successful application can still withhold judgment

**Setup.** Continue both identity branches from BP-003 through the
`moving-right` schema, as in
[Worked Example Trace 5](WORKED_EXAMPLES.md#trace-5).
Both branches satisfy the predicate, but no constitutive rule selects one
singular subject.

**Kantbot expectation.** Both application results pass and remain attached to
their own object candidates. The cycle returns `judgment-withheld` rather than
committing a singular proposition.

**Comparison expectation.** Predicate agreement raises or preserves the
pipeline's `moving-right` score, so the greedy subject choice and classification
normally become an assertion.

**Falsifier.** The prediction fails if successful application directly commits
the predicate, if the subject ambiguity disappears from the warrant, or if
withholding is reported as though concept application itself failed.

**Grounds.** [Specification consequence 4](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-017](CLAIMS.md#k-017), and [ADR 0003 observable consequences](docs/decisions/0003-object-and-judgment-licensing.md#observable-consequences).

<a id="bp-006"></a>
### BP-006 — Locally valid states can conflict cycle-wide

**Setup.** Use the branch-relative candidates and successful applications from
BP-005. Construct the adversarial proposal in
[Worked Example Trace 6](WORKED_EXAMPLES.md#trace-6):
the subject references one branch while the warrant merges both incompatible
middle positions.

**Kantbot expectation.** Local object and application records remain valid,
but the complete provenance subgraph fails `U-1`. The terminal result is
`unity-conflict`, and neither alternative is silently deleted to repair it.

**Comparison expectation.** A pipeline that validates only record shape and
label score can accept the proposal because each local component is individually
well formed and supportive.

**Falsifier.** The prediction fails if Kantbot commits the merged proposal,
reduces the conflict to low confidence, or cannot point to the incompatible
identity edges. Rejecting the records earlier for serialization reasons also
misses the predicted cycle-wide role.

**Grounds.** [K-018](CLAIMS.md#k-018), [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md),
and the [apperception contract](PHILOSOPHICAL_SPECIFICATION.md#apperception-cycle-wide-unity-constraint).

<a id="bp-007"></a>
### BP-007 — Warrant provenance is causal, not post-hoc

**Setup.** Begin with the complete successful trace in Worked Example Trace 1.
After the application value has been calculated but before commitment, remove
the required provenance edge showing that earlier intuitions were reproduced
under `R-1`. Leave the proposed sentence and all numeric values unchanged.

**Kantbot expectation.** The proposal no longer has a complete warrant and
must return `judgment-withheld`, naming the missing retention ground. Recreating
an explanatory sentence after the fact does not restore the edge.

**Comparison expectation.** The classifier's label and confidence remain
unchanged because its explanation is not a precondition of assertion.

**Falsifier.** The prediction fails if Kantbot commits the same judgment with a
missing required warrant field, or if it fabricates a replacement provenance
edge not reachable from the original transformations.

**Grounds.** [K-022](CLAIMS.md#k-022), the
[warrant requirement](PHILOSOPHICAL_SPECIFICATION.md#warrant-and-objective-validity),
and [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md).

<a id="bp-008"></a>
### BP-008 — Equal confidence does not collapse different limits

**Setup.** Configure the same scalar support value for three cognitive cases:
rival identity branches, a two-position candidate when `S-right` requires
three, and an attempted hidden-state promotion. Add a malformed external record
as a boundary control for which no cognitive confidence is computed. The
case-specific structural conditions remain unchanged.

**Kantbot expectation.** The boundary control returns `input-error`. The three
cognitive cases remain respectively `synthesis-ambiguous`,
`application-underdetermined`, and `overreach`. Their permitted next claims
differ even though the auxiliary scalar is equal; the input error never enters
that scale.

**Comparison expectation.** A pipeline with one error channel and one
thresholded result typically collapses ambiguity and underdetermination into
the same low-confidence response while treating hidden state as another scored
feature. It does not preserve three authority- and condition-specific limits
with different permitted next claims.

**Falsifier.** The prediction fails if changing only a confidence value can
convert one typed condition into another, if the typed result is derived from
confidence bands, or if all non-commitments expose the same permitted next
action.

**Grounds.** [K-023](CLAIMS.md#k-023), [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md),
and the [terminal-outcome table](PHILOSOPHICAL_SPECIFICATION.md#terminal-outcomes-and-cognitive-limits).

<a id="bp-009"></a>
### BP-009 — Evaluator truth cannot alter cognitive warrant

**Setup.** Hold the successful presented episode and every cognitive rule
fixed. In separate evaluator records, change the hidden world identity from
`calibration-target-17` to another identity. Then attempt the illicit promotion
shown in
[Worked Example Trace 7](WORKED_EXAMPLES.md#trace-7).

**Kantbot expectation.** Before the illicit proposal, the cognitive trace is
identical across evaluator states; only the external score may differ. With no
presented calibration predicate, the strongest legitimate result is
`application-underdetermined`. If hidden identity is inserted into the warrant,
the result is `overreach` regardless of whether the hidden label makes the
sentence true.

**Comparison expectation.** A pipeline given the hidden label as an ordinary
feature changes its prediction or confidence with the evaluator record and may
be rewarded for the true assertion.

**Falsifier.** The prediction fails if evaluator-only state changes a Kantbot
candidate, application, or judgment; if a true hidden label repairs missing
presentation; or if the limit report describes the hidden object as positively
cognized.

**Grounds.** [Specification consequence 6](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-014](CLAIMS.md#k-014), and [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md).

<a id="bp-010"></a>
### BP-010 — Regulative guidance cannot become object evidence

**Setup.** Run one presented episode twice with identical constitutive rules.
The contrast adds or changes regulative preference `Q-1`, which favors
follow-up observations of likely persistent patches. In a second contrast,
deliberately insert `Q-1` into a present object predicate's warrant.

**Kantbot expectation.** In the first cognitive cycle, where active reason is
deferred, changing reserved regulative metadata does not change object
formation, predicate application, or commitment. Once Phase 4 activates
regulative inquiry, the preference may change which observation is requested
next but still cannot change the present object judgment by itself. Deliberate
promotion is rejected as `overreach`, with the authority incompatibility named
in its limit report.

**Comparison expectation.** An untyped rules pipeline may treat every rule as
another score or feature, allowing the preference to change the predicate or
cross an assertion threshold.

**Falsifier.** The prediction fails if a regulative rule creates an object,
adds a predicate, or supplies object-level warrant; it also fails if the system
cannot identify the authority violation when promotion is attempted.

**Grounds.** [Specification consequence 5](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-020](CLAIMS.md#k-020), and [ADR 0004 observable consequences](docs/decisions/0004-limit-outcomes-and-rule-authority.md#observable-consequences).

<a id="bp-011"></a>
### BP-011 — Variant projection does more than rename shared input

**Setup.** Supply valid observation records whose position labels are preserved
at shared reception while their episode declares temporal ordering unavailable.
The Kantian variant requires temporal form. Preserve the same presented-element
identities for any comparison projection. Separately, construct a diagnostic
projection that copies a presented record and changes only its displayed type
name to `intuition`.

**Kantbot expectation.** Shared reception succeeds. The accepted Kantian
projection returns `not-presentable`, preserving the presented elements and the
failed form condition; a declared comparison variant may produce another
representation or its own refusal. The label-only diagnostic fails the
projection safeguard and cannot enter a manifold of intuition.

**Comparison expectation.** A pipeline with one shared preprocessing record
either rejects the input globally or accepts it globally. A vocabulary wrapper
can rename the record without changing structure, invariants, omission, or
downstream behavior.

**Falsifier.** The prediction fails if Kantian projection succeeds without its
required temporal form, if its failure deletes the shared presented element,
or if a type alias alone is accepted as the variant transformation.

**Grounds.** [Specification consequence 8](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-015](CLAIMS.md#k-015), and [ADR 0001 observable consequences](docs/decisions/0001-variant-scoped-receptive-terminology.md#observable-consequences).

<a id="bp-012"></a>
### BP-012 — The B-led variant compresses stages without erasing grounds

**Setup.** Run the retention-dependent success episode under the default
A-analysis/B-constraint trace and the B-led trace in
[Worked Example Traces 1–2](WORKED_EXAMPLES.md#trace-1).
Then repeat BP-002's retention ablation under both policies.

**Kantbot expectation.** With retention enabled, both variants commit the same
scoped judgment. The default separately exposes apprehension, reproduction,
and recognition; the B-led variant exposes one figurative-synthesis stage.
Both traces preserve shared reception identities, retained intuition grounds,
the identity rule, objective-unity constraints, and sensible-use limits. With
retention disabled, neither may retain the identity judgment.

**Comparison expectation.** A label-only variant has an identical causal trace
with renamed stages, or it compresses operations by dropping the evidence while
leaving the output invariant under ablation.

**Falsifier.** The prediction fails if the variants differ only typographically,
if the B-led trace cannot answer which earlier presentations were retained and
why they form one candidate, or if either variant ignores the retention
ablation.

**Grounds.** [Specification consequence 7](PHILOSOPHICAL_SPECIFICATION.md#required-behavioral-consequences),
[K-024](CLAIMS.md#k-024), and [ADR 0002 observable consequences](docs/decisions/0002-a-b-synthesis.md#observable-consequences).

## Required-consequence coverage

The eight consequences already fixed by the philosophical specification are
covered without adding a new commitment:

| Specification consequence | Catalog coverage |
| --- | --- |
| Temporal reordering can change persistence or succession judgment | BP-001 |
| Removing licensed reproduction can prevent identity synthesis | BP-002 and BP-012 |
| Locally coherent candidates can force ambiguity instead of argmax | BP-003 |
| Application can succeed while cycle-wide commitment fails | BP-005 and BP-006 |
| Regulative guidance cannot create an object judgment | BP-010 |
| Claims outside presentation scope remain rejected despite hidden truth | BP-009 and BP-011 |
| A B-led variant may compress stages but must preserve required evidence | BP-002 and BP-012 |
| Shared elements can receive variant-specific projections or refusals | BP-011 |

Additional predictions BP-004, BP-007, and BP-008 test distinctions required by
the accepted ADRs but only implicit in that eight-item list.

## Terminal-outcome coverage

| Outcome | Prediction seed |
| --- | --- |
| `input-error` | BP-008 invalid-serialization case |
| `not-presentable` | BP-011 missing temporal form |
| `synthesis-failed` | BP-002 retention ablation |
| `synthesis-ambiguous` | BP-003 rival identity paths; BP-008 equal-confidence comparison |
| `concept-not-applicable` | BP-001 reordered motion; BP-004 stationary candidate |
| `application-underdetermined` | BP-008 short interval; BP-009 absent presented predicate |
| `unity-conflict` | BP-006 merged alternatives |
| `judgment-withheld` | BP-005 unresolved subject; BP-007 incomplete warrant |
| `judgment-committed` | BP-001 control; BP-002 control; BP-012 both complete variants |
| `overreach` | BP-008 hidden-state promotion; BP-009 hidden truth; BP-010 regulative promotion |

Coverage means that an executable fixture can be derived from the prediction;
it does not make confidence, failure, ambiguity, withholding, conflict, and
overreach interchangeable.

## Handoff to implementation and evaluation

Phase 2 should translate each controlled contrast into state-transition and
invariant tests. Phase 3 should replay the complete episode-level cases as
deterministic integration tests. The following acceptance targets apply:

- every one of the eight required specification consequences has at least one
  executable comparison;
- every typed terminal outcome has at least one deterministic fixture;
- every committed judgment used in evaluation has a complete causal provenance
  path rather than an optional explanation;
- the default and B-led synthesis policies share comparison identities and
  evidence requirements while retaining their declared stage difference;
- evaluator-only state is tested for cognitive-output invariance; and
- negative outcomes are asserted as successful results, not only as exceptions
  or low scores.

Exact test syntax, fixture serialization, confidence mathematics, performance
targets, and statistical comparison with human participants remain for later
phases. The present catalog specifies what must become observable before those
choices can count as implementations of the declared architecture.
