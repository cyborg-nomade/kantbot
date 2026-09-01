# Hand-Worked Cognitive Traces

## Status and use

These examples are the worked-trace companion to the
[philosophical specification](PHILOSOPHICAL_SPECIFICATION.md) and
[cognitive architecture](COGNITIVE_ARCHITECTURE.md). They instantiate the
accepted Phase 1 decisions in a small marker-tracking world and show what each
stage may use, produce, and license.

The traces are normative where they preserve a semantic boundary, rule
authority, provenance requirement, or typed outcome fixed by the specification
and [ADRs 0001–0004](docs/decisions/README.md#index). Scenario values, record
shapes, identifiers, and rule notation are illustrative. They are not the
canonical types, algorithms, or scenario format that Phase 2 must define.

Each example ends at the strongest licensed result. A non-judgment is therefore
a successful trace when it correctly exposes failed conditions, alternatives,
scope, and authority. Phase 2 can use these traces as formal-model fixtures;
Phase 3 can turn them into deterministic integration tests following the
[behavioral-prediction catalog](BEHAVIORAL_PREDICTIONS.md).

## Shared toy world and frozen configuration

The toy world is a one-dimensional observation strip. A sensor frame may
present one or more colored patches at integer positions. The cognitive cycle
does not receive the world's object identifiers or future state.

An observation is abbreviated as follows:

| Field | Meaning |
| --- | --- |
| `id` | Stable external observation identity |
| `t` | Position in the episode's total temporal order |
| `content` | Supplied color and strip position, or an explicitly unreadable frame |
| `source` | Sensor that supplied the frame |
| `quality` | Declared completeness or impairment of the supplied content |

Unless an example overrides it, one cycle freezes this configuration:

| Item | Illustrative setting | Authority and role |
| --- | --- | --- |
| Interpretation | Accepted A-analysis/B-constraint Kantian variant | Projects shared presented elements into intuitions; does not alter their shared identities |
| Sensible form | Total temporal order plus one-dimensional spatial order | Conditions presentation and every temporal or spatial comparison |
| Retention rule `R-1` | Earlier intuitions in the same episode may be reproduced until the cycle closes | Constitutive for this retention-and-identity experiment |
| Identity rule `I-1` | Same color; displacement no greater than two positions per tick; no two positions at one time within one branch | Constitutive candidate-identity constraint |
| Unity rule `U-1` | Each candidate uses one compatible alternative at every branch and one frozen cycle configuration | Constitutive candidate and cycle-wide constraint |
| Concept `moving-right` | A general empirical concept whose schema tests ordered position change | The concept alone licenses no application |
| Schema `S-right` | At least three positions from one candidate, all temporally ordered, with every successive difference greater than zero | Inspectable applicability procedure |
| Regulative preference `Q-1` | Prefer follow-up observations of patches likely to persist | Reserved for later inquiry; never an object-level ground in the first cycle |
| Scope | Supplied frames in the current episode | No claim about an unobserved object, hidden identity, or later episode |

`I-1` and `S-right` deliberately do different work. `I-1` can form a
stationary or left-moving object candidate; only `S-right` decides whether the
empirical predicate `moving-right` applies. Neither rule may use the evaluator's
hidden object identifier.

<a id="trace-1"></a>
## Trace 1 — A committed rightward-motion judgment

### Episode

| Observation | `t` | Content | Source | Quality |
| --- | ---: | --- | --- | --- |
| `obs-1` | 0 | amber patch at `x=0` | `strip-camera` | complete |
| `obs-2` | 1 | amber patch at `x=1` | `strip-camera` | complete |
| `obs-3` | 2 | amber patch at `x=2` | `strip-camera` | complete |

No input field says that the three patches are one object. That identity must
be synthesized.

### Default A-analysis/B-constraint trace

| Step | Role and operation | Grounds used | Result and licensing effect |
| ---: | --- | --- | --- |
| 1 | External validation | Three serialized observations | All records are valid; no cognitive status is added |
| 2 | Shared reception | `obs-1`–`obs-3` | Presented elements `pe-1`–`pe-3` preserve observation, source, order, and content identities |
| 3 | Sensibility projection | Presented elements plus temporal and spatial form | Intuitions `i-1`–`i-3`; each is singular, preconceptual content under the declared form |
| 4 | Manifold formation | `i-1`–`i-3` and episode boundary | Manifold `m-1`; co-membership does not yet make one object |
| 5 | Apprehension | `m-1` in temporal order | Traversal `[i-1, i-2, i-3]`, with the segmentation choice recorded |
| 6 | Reproduction | Current `i-3`, earlier `i-1` and `i-2`, and `R-1` | Retained sequence `r-1`; earlier positions remain available by an explicit rule |
| 7 | Recognition | `r-1`, `I-1`, and `U-1` | Candidate `cand-1 = [i-1, i-2, i-3]`; color is stable and each displacement is one |
| 8 | Object formation | `cand-1` and its complete local provenance | Object candidate `obj-1`; identity and constitutive unity pass within the episode |
| 9 | Concept application | `obj-1`, `moving-right`, and `S-right` | Application `app-1`: three ordered positions and differences `[+1, +1]`; all required conditions pass |
| 10 | Judgment proposal | `obj-1`, `app-1`, constitutive grounds, and scope | Proposed judgment `pj-1`: “The amber marker moved right from `t=0` through `t=2`” |
| 11 | Apperception | `pj-1` and its entire provenance subgraph | One configuration, one identity branch, compatible authorities, and no stronger modality than the grounds support |
| 12 | Commitment and critique | Successful unity check plus complete report fields | `judgment-committed` within this episode and strip; no claim about hidden identity or later motion |

### Warrant and limit report

| Report field | Value |
| --- | --- |
| Observation grounds | `obs-1`, `obs-2`, `obs-3` |
| Presentation | Temporal order `0 < 1 < 2`; spatial strip positions `0, 1, 2`; successful Kantian projections |
| Synthesis | Apprehension in order; reproduction under `R-1`; recognition under `I-1` and `U-1` |
| Applicability | `S-right` satisfied with differences `[+1, +1]` |
| Alternatives | None admissible under the supplied frames and rules |
| Authority | `R-1`, `I-1`, `U-1`, and `S-right` are constitutive in this configured experiment |
| Scope and limit | The supplied episode only; no numerical world identity, future persistence, or motion outside the strip is asserted |
| Terminal outcome | `judgment-committed` |

The judgment is licensed because every stage contributes a distinct required
ground. A classifier that merely notices the three amber patches may reach the
same sentence, but it has not reproduced this warrant.

<a id="trace-2"></a>
## Trace 2 — The same episode under the B-led synthesis variant

[ADR 0002](docs/decisions/0002-a-b-synthesis.md) requires a B-led variant only
where it changes trace stages or observable behavior. This trace changes the
observable stage structure while preserving the grounds needed for comparison.
It uses the observations and frozen rules from Trace 1.

| Step | B-led role and operation | Grounds used | Result and required evidence |
| ---: | --- | --- | --- |
| 1 | Validate, receive, and project | `obs-1`–`obs-3`, shared reception, and sensible form | The same presented-element identities, intuitions, and manifold `m-1` as the default trace |
| 2 | Figurative synthesis | `m-1`, `R-1`, `I-1`, and `U-1` | Candidate `cand-b1`; its trace records the reception basis, retained earlier intuitions, combination rule, identity grounds, and objective-unity constraints |
| 3 | Object formation and schema-mediated application | `cand-b1`, `moving-right`, and `S-right` | Object candidate `obj-b1`; application differences `[+1, +1]` pass |
| 4 | Proposed judgment and objective-unity check | Complete provenance for `obj-b1` and its application | The same scoped proposition passes one-cycle, identity, authority, and scope constraints |
| 5 | Commitment and critique | Passing unity check | `judgment-committed` with the same claim scope as Trace 1 |

The variants are observably different but comparable:

| Question | Default hybrid | B-led variant |
| --- | --- | --- |
| Are apprehension, reproduction, and recognition separate trace stages? | Yes | No; figurative synthesis combines them |
| Is retention evidence visible? | `R-1` appears in the reproduction step | `R-1` and the reproduced intuition IDs remain fields of figurative synthesis |
| Is proposed identity inspectable? | Recognition emits `cand-1` under `I-1` | Figurative synthesis emits `cand-b1` with the same identity grounds |
| Does objective unity constrain the result? | In object formation and the final unity check | Within figurative synthesis and again at commitment |
| Terminal result | `judgment-committed` | `judgment-committed` |

If a B-led implementation merely renames a generic combination step while
omitting retention or objective-unity evidence, it is not this variant.

<a id="trace-3"></a>
## Trace 3 — Rival identity syntheses remain ambiguous

### Episode

| Observation | `t` | Content | Source | Quality |
| --- | ---: | --- | --- | --- |
| `obs-a1` | 0 | amber patch at `x=0` | `strip-camera` | complete |
| `obs-a2` | 1 | amber patches at `x=1` and `x=2` | `strip-camera` | complete |
| `obs-a3` | 2 | amber patch at `x=3` | `strip-camera` | complete |

The middle frame contains two indistinguishable patches. The input supplies no
object IDs and no ground for preferring one path.

| Step | Role and operation | Result |
| ---: | --- | --- |
| 1 | Validate, receive, and project | Three presented frame elements project into four patch intuitions under one temporal-spatial form; the middle frame is segmented into two simultaneous particulars |
| 2 | Apprehend and reproduce | The `t=0` and both `t=1` intuitions remain available when the `t=2` intuition is traversed |
| 3 | Recognize under `I-1` | `cand-a = [x0@t0, x1@t1, x3@t2]` and `cand-b = [x0@t0, x2@t1, x3@t2]`; both have stable color and permitted displacement |
| 4 | Preserve alternatives under `U-1` | The candidates are incompatible identity branches because one putative object cannot occupy both middle positions at once |
| 5 | Critique and report | No rule selects a branch; report both complete candidate provenances |

**Terminal outcome:** `synthesis-ambiguous`.

The strongest licensed result is the pair of candidate representations, not a
single object candidate and not the highest-scoring path. The ambiguity is
structural even if an implementation assigns equal or unequal confidence to
the branches.

<a id="trace-4"></a>
## Trace 4 — Object formation succeeds but the concept does not apply

### Episode

| Observation | `t` | Content | Source | Quality |
| --- | ---: | --- | --- | --- |
| `obs-s1` | 0 | amber patch at `x=2` | `strip-camera` | complete |
| `obs-s2` | 1 | amber patch at `x=2` | `strip-camera` | complete |
| `obs-s3` | 2 | amber patch at `x=2` | `strip-camera` | complete |

| Step | Role and operation | Result |
| ---: | --- | --- |
| 1 | Validate, receive, project, and form the manifold | Three intuitions under the episode's temporal-spatial form |
| 2 | Apprehend, reproduce, and recognize | Candidate `[x2@t0, x2@t1, x2@t2]` under `R-1` and `I-1` |
| 3 | Apply local unity conditions | Object candidate `obj-s`; stable position is compatible with persistence |
| 4 | Run `S-right` | Three positions are present, but successive differences are `[0, 0]`, not greater than zero |
| 5 | Critique and report | Preserve `obj-s` and the failed schema conditions; do not assemble a rightward-motion proposition |

**Terminal outcome:** `concept-not-applicable`.

This trace separates object formation from predication. The stationary marker
does not cease to be an object candidate merely because `moving-right` fails,
and successful object identity cannot force a failed concept to apply.

<a id="trace-5"></a>
## Trace 5 — Application succeeds on alternatives, but judgment is withheld

This trace continues the two alternatives from Trace 3 rather than stopping at
the first ambiguity report. Continuing alternatives is permitted only while
their provenance remains separate.

| Step | Role and operation | Result |
| ---: | --- | --- |
| 1 | Preserve rival candidates | `cand-a` and `cand-b` remain distinct; neither is promoted as the unique identity path |
| 2 | Form branch-relative object candidates | `obj-a` and `obj-b` each pass local identity and unity conditions within its own branch |
| 3 | Run `S-right` separately | `obj-a` has differences `[+1, +2]`; `obj-b` has `[+2, +1]`; `moving-right` applies to both |
| 4 | Attempt to select a subject for a singular proposition | No constitutive rule determines whether `obj-a` or `obj-b` is the object candidate to which the judgment commits |
| 5 | Critique and report | Retain both successful application results and refuse an arbitrary branch choice |

**Terminal outcome:** `judgment-withheld`.

This result retains more than a synthesis failure while still refusing
judgment: both branch-relative applications succeeded, but no one object
candidate can ground a singular commitment. Agreement on a predicate does not
erase disagreement about its subject.

<a id="trace-6"></a>
## Trace 6 — The final unity check rejects merged alternatives

This adversarial continuation uses the same episode as Traces 3 and 5. It tests
the final unity gate if an upstream proposal incorrectly combines otherwise
valid branch-relative states.

| Step | Role and operation | Result |
| ---: | --- | --- |
| 1 | Start from valid branch-relative results | `obj-a` with `app-a`, and `obj-b` with `app-b`; each pair has a coherent local provenance graph |
| 2 | Assemble a defective proposal | Subject identity references `obj-a`, while its middle-position warrant includes both `x=1` from `cand-a` and `x=2` from `cand-b` at `t=1` |
| 3 | Check the whole provenance subgraph | Each application result is locally valid, but their merged identity commitments cannot belong to one trace under `U-1` |
| 4 | Critique and report | Preserve both alternatives and identify the incompatible provenance edges; do not repair the proposal by silently dropping one |

**Terminal outcome:** `unity-conflict`.

The conflict is not a serialization error and not evidence of a simulated
self. It is the functional result of checking that every ground of one proposed
judgment can belong to one compatible cognitive cycle. The normal path in
Trace 5 withholds before constructing this defective proposal; this trace shows
why the final check must still exist.

<a id="trace-7"></a>
## Trace 7 — A true hidden label still cannot ground a judgment

Use the successful object candidate from Trace 1. The evaluator additionally
knows that the toy world's hidden identifier is `calibration-target-17` and
that this identifier denotes a calibration target. Neither fact was presented
by the strip camera. Regulative preference `Q-1` is present only as metadata
reserved for later inquiry.

| Step | Role and operation | Result |
| ---: | --- | --- |
| 1 | Form the presented object candidate | `obj-1` remains licensed for its observed color, positions, and interval |
| 2 | Ask whether it is a calibration target | No presented content or schema connects `obj-1` to that predicate; ordinary application is underdetermined |
| 3 | Illicitly promote evaluator state or `Q-1` | A proposed warrant cites the hidden identifier, or treats the regulative ranking as constitutive evidence |
| 4 | Check scope and authority | The proposed ground is unreachable from admitted presented elements and has no object-level authority |
| 5 | Critique and report | Reject the promotion, name the offending ground and authority, and retain the valid presentation trace |

**Terminal outcome:** `overreach`.

External evaluation may record that the rejected sentence would have matched
the hidden world. That truth comparison does not improve the cognitive warrant.
Had the cycle merely reported the absent presentation grounds at Step 2, its
proper result would have been `application-underdetermined`; the attempt to
promote inaccessible or regulative material is what makes this `overreach`.

## Boundary-case seeds for every terminal outcome

The detailed traces above exercise the Phase 1 distinctions required by the
accepted decisions. The remaining rows make the full outcome vocabulary
concrete and provide minimal seeds for later executable fixtures.

| Outcome | Minimal variation | Strongest reportable state |
| --- | --- | --- |
| `input-error` | An observation omits its required episode position and therefore fails external validation | Invalid record plus validation failure; no cognitive result |
| `not-presentable` | Valid records carry position labels, but the episode declares their ordering unavailable in a variant whose temporal form is required | Presented element plus failed temporal-projection condition; no intuition |
| `synthesis-failed` | A requested persistence path contains only `x=0@t0` and `x=5@t1`, violating `I-1`, with no admissible alternative identity | Manifold plus failed identity rule; no candidate on that path |
| `synthesis-ambiguous` | Use Trace 3 and preserve both admissible paths | Rival candidate representations and their grounds |
| `concept-not-applicable` | Use Trace 4; `[0, 0]` fails the positive-change condition of `S-right` | Object candidate plus failed applicability conditions |
| `application-underdetermined` | Supply only `x=0@t0` and `x=1@t1`; `S-right` requires three ordered positions | Object candidate plus the missing third position or interval |
| `unity-conflict` | Use Trace 6 and merge incompatible branch-relative grounds | Proposed judgment plus conflicting provenance edges |
| `judgment-withheld` | Use Trace 5; both applications pass but no subject branch is licensed | Both application results and the unresolved subject alternatives |
| `judgment-committed` | Use Trace 1 or Trace 2 | Scoped proposition, complete warrant, and limit report |
| `overreach` | Use Trace 7 and promote evaluator-only or regulative material | Valid in-scope trace plus the rejected authority or scope promotion |

These cases keep ordinary absence, violated conditions, alternatives,
conflicting commitments, withholding, and illicit promotion distinct. A single
confidence number cannot replace any row.

## Handoff to the formal model

The Phase 2 model may change names and storage structures, but replaying these
examples must make the following questions answerable from structured data:

1. Which observations and presented elements ground each variant projection?
2. Which earlier intuitions were reproduced, and under which retention rule?
3. Which identity candidates and alternatives were considered?
4. Did object formation, concept applicability, and commitment pass or fail
   independently?
5. Does every proposed judgment have one compatible provenance subgraph?
6. Which rules are constitutive, regulative, or engineering, and did any rule
   exceed its authority?
7. What is the strongest licensed terminal outcome, scope, and limit report?
8. Can the default and B-led synthesis traces be compared without pretending
   that their stage vocabularies are identical?

An implementation that emits the expected sentence but cannot answer these
questions has not reproduced the examples' cognitive path.
