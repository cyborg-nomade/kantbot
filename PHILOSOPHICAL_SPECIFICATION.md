# Philosophical Specification: Faculties, Representations, and Cognitive Flow

## Status and purpose

This document defines the philosophical contract for Kantbot's first cognitive
cycle. Its audience is the implementer who must decide what each stage may
receive, produce, and claim before choosing data structures or algorithms. It
answers [RQ-01 through RQ-07](RESEARCH_QUESTIONS.md#research-questions) only far
enough to fix that contract; the companion
[cognitive-architecture diagrams](COGNITIVE_ARCHITECTURE.md) expose its
boundaries and transformations, and the companion
[hand-worked traces](WORKED_EXAMPLES.md) instantiate its success and limit
paths. The later behavioral-prediction catalog will test and refine it.

[ADRs 0001–0004](docs/decisions/README.md#index) are Accepted and govern
receptive terminology, the synthesis default, judgment licensing, and cognitive
limits. [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md)
fixes `observation` and `presented element` as shared-boundary vocabulary and
uses `intuition` theory-internally within the accepted Kantian variant. None of
the decisions should be treated as Kant's uniquely correct architecture.
Definitions retain the senses fixed in the
[glossary](GLOSSARY.md), source routing comes from the
[primary-source map](PRIMARY_SOURCES.md), and stable cross-document commitments
retain their status in the [claims register](CLAIMS.md).

## How to read the claim labels

Each consequential paragraph begins with one of the project's four claim
labels:

- **Textual** reports what the cited text supports, with edition differences
  made visible.
- **Interpretive** states how this specification reads material the text does
  not turn into a ready-made software architecture.
- **Analogical** states the computational role borrowed from a Kantian
  distinction and the literal equivalence rejected.
- **Engineering** introduces a constraint for a finite, inspectable experiment;
  it is not attributed to Kant.

A paragraph with several labels separates the claims sentence by sentence. The
labels identify authority, not confidence or implementation priority.

## Scope of the first cycle

**Engineering.** One cognitive cycle operates on a finite observation episode
in a deterministic toy world. The episode has an explicit start, end, source,
ordering relation, and configuration. The first release does not require
open-world perception, natural-language input, learned concepts, practical
reason, or machine consciousness ([K-021](CLAIMS.md#k-021),
[K-025](CLAIMS.md#k-025)).

**Engineering.** The architecture is also an executable hypothesis: increasing
fidelity should approach corresponding features of human cognition if the
selected account is correct and sufficiently complete ([K-027](CLAIMS.md#k-027)).
Using Kantian terminology inside a declared model can express that intended
role without counting as evidence that the model has already succeeded.

**Interpretive.** The default combines the A Deduction's analysis of synthesis
with the B Deduction's account of objective unity, judgment, and the restriction
of category use to possible experience ([K-010](CLAIMS.md#k-010)). This is an
edition-sensitive construction, not a claim that Kant presents the combined
sequence as a numbered architecture. The rationale and the alternative B-led
variant are recorded in [ADR 0002](docs/decisions/0002-a-b-synthesis.md).

**Analogical.** The cycle models relations among presentation, synthesis,
concept application, judgment, unity, and limitation. It does not establish
that a program literally senses, imagines, understands, judges, apperceives, or
reasons. Each faculty name below is therefore the name of a constrained role,
not the name of a software subject's mental power.

## What is given

### Observation episode

**Engineering.** An **observation** is an immutable input record with content,
source, position in the episode, and quality metadata. Input parsing validates
that record but performs no cognitive synthesis. An **episode** bounds the
observations available to one cycle and declares whether order is total,
partial, or unavailable.

**Engineering.** Shared reception first derives a **presented element** from a
valid observation. It preserves source, episode, ordering, and provenance
identity for comparison, but it has no licensed object identity, concept, or
variant-specific cognitive status.

**Interpretive.** Each declared architecture then performs an explicit
**variant projection**. The accepted A/B Kantian variant projects a presented
element into an **intuition** under its sensibility, sensible-form, singularity,
and preconceptuality constraints. The projection must add or validate those
conditions and may fail; changing only a type or display label does not count
([ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md)).

**Analogical.** `Intuition` is theory-internal terminology for the role this
Kantian variant attempts to realize. It preserves the receptive-before-
conceptual distinction in [K-001](CLAIMS.md#k-001) and is governed by
[K-015](CLAIMS.md#k-015). The identifier is not evidence that the projection,
the wider architecture, or human cognition has already been reproduced.

### Form and manifold

**Textual.** Sensibility gives objects in intuition; the manifold supplied for
synthesis does not organize itself into cognition. Space and time are forms of
human sensible intuition, not properties inferred from already constituted
objects ([A19-25/B33-41](sources/kant/critique-a.md#a19),
[A30-32/B46-49](sources/kant/critique-a.md#a30), and
[A77-79/B102-104](sources/kant/critique-a.md#a77)).

**Interpretive.** Temporal order is necessary for the first model because
retention, persistence, succession, and schematized application otherwise have
no common form. Spatial order is required only in scenarios whose object rules
depend on spatial relations. This models a constrained role of form; it does
not claim that arbitrary timestamps and coordinates are Kant's pure intuitions.

**Analogical.** A **manifold of intuition** is the bounded plurality of
successfully projected intuitions available together for synthesis under the
episode's form. Shared presented elements do not become members merely by
crossing the common boundary. The manifold is not an already-segmented object,
a bag of attributes, or the toy world's hidden state. Its boundary, granularity,
form, and projection grounds remain visible in the trace.

### Reception failures

**Engineering.** Reception and variant projection distinguish four outcomes:

1. `presented`: the observation is admitted at the shared boundary;
2. `projected`: the selected variant produces its declared representation—an
   intuition in the accepted Kantian variant;
3. `projection-ambiguous`: more than one admissible form, ordering, or
   segmentation remains, so all alternatives continue; or
4. `not-presentable`: the shared element cannot enter the selected variant
   because a required form or role condition is absent or contradictory.

When a Kantian projection fails, the shared presented element remains
inspectable for comparison but cannot enter its manifold of intuition. Invalid
serialization is an input error before reception. Missing content is ordinary
absence of data. Neither is by itself a model of a transcendental limit.

## Representations carried by the cycle

**Engineering.** The following are semantic roles, not Phase 2 type
definitions. A later formal model may combine storage structures only if its
trace still preserves these distinctions.

| Representation | What it contains | What it does not yet license |
| --- | --- | --- |
| Observation | Immutable supplied content plus source and ordering metadata | Presentation, objecthood, or truth |
| Presented element | Minimal shared content plus source, episode, order, and provenance identity | Variant-specific cognitive status, objecthood, or a concept |
| Variant projection | A declared transformation with interpretation-specific structure, invariants, omissions, and possible failure | Success merely from renaming the shared element |
| Intuition | In the accepted Kantian variant, singular content admitted under declared sensibility and sensible-form criteria | A constituted object, concept, or proof of human cognition |
| Manifold of intuition | A bounded plurality of Kantian intuitions available to one synthesis attempt | Unity merely from shared-boundary co-occurrence |
| Retained sequence | Current intuitions plus explicitly reproduced earlier intuitions and the rule licensing reproduction | Identity or an object candidate |
| Candidate representation | A proposed rule-governed combination with provenance, rival combinations, and unresolved conflicts | A licensed object claim |
| Object candidate | A candidate representation that has passed local identity and constitutive-unity tests | A judgment or unrestricted external object |
| Concept | General applicability conditions, inferential consequences, scope, and authority | Application merely by being named |
| Schema | An inspectable procedure relating a concept or category-like rule to temporally formed content | Truth or objecthood merely from a match |
| Application result | Satisfied, failed, and undecided conditions for every tested concept, including alternatives | Commitment to a proposition |
| Proposed judgment | A structured proposition with subject candidate, predicate, scope, and assembled warrant | Assertoric output before the unity check |
| Judgment | A proposition committed within the model after presentation, synthesis, application, and unity conditions pass | Truth beyond the declared toy world and presentation conditions |
| Limit report | Missing conditions, conflicts, alternatives, scope boundary, and strongest licensed status | A hidden noumenal explanation of the failure |

**Interpretive.** An **object for this model** is an object candidate that can
enter a licensed judgment because a rule-governed synthesis, applicable
concept, constitutive conditions, and the cycle-wide unity check converge on
the same traceable candidate. Objecthood is therefore neither input ontology
nor similarity alone ([K-011](CLAIMS.md#k-011),
[K-013](CLAIMS.md#k-013)). It is objective only relative to the model's declared
conditions of possible presentation; this does not establish access to a thing
as it is independently of those conditions.

**Engineering.** Every derived representation carries provenance by
construction: identifiers of its immediate grounds, the transformation or
rule used, the alternatives considered, the conditions not met, and its claim
scope. Explanatory prose generated after the fact is not a substitute for this
structure ([K-022](CLAIMS.md#k-022)).

## Cognitive roles

### Sensibility: Kantian variant projection

**Textual.** Human sensibility is receptive and supplies intuitions rather than
concepts ([A19/B33](sources/kant/critique-a.md#a19),
[A50/B74](sources/kant/critique-a.md#a50)).

**Interpretive.** Kantbot's accepted **sensibility role** performs the Kantian
variant projection: it admits shared presented elements only under the
configured form and produces intuitions and a manifold of intuition. It does
not identify objects, apply concepts, or repair invalid input.

**Analogical.** The sensibility role is not a sensor or parser, and its theory-
internal name does not establish that the role or the wider model has
succeeded.

### Imagination: provenance-preserving synthesis

**Textual.** Synthesis puts different representations together in one
cognition, and imagination synthesizes the sensible manifold. The A Deduction
articulates apprehension, reproduction, and recognition; the B Deduction
describes figurative synthesis while emphasizing its relation to understanding
([A77-79/B102-104](sources/kant/critique-a.md#a77),
[A98-110](sources/kant/deduction-a.md#a98),
[A120-126](sources/kant/deduction-a.md#a120), and
[B151-152](sources/kant/deduction-b.md#b151)).

**Interpretive.** The default **imagination role** coordinates three
inspectable operations:

1. **Apprehension** traverses and takes together intuitions under the
   declared form.
2. **Reproduction** makes earlier intuitions available under an explicit
   retention rule; unrestricted retrieval is forbidden.
3. **Recognition** proposes that retained elements belong to the same
   combination under an identity rule, yielding one or more candidates.

**Interpretive.** These are operations within one synthesis boundary, not
independent homunculi and not a claim that the B Deduction repeats the
A-edition threefold account.
The understanding supplies or constrains rules used in recognition; the
imagination executes the synthesis over sensible content. This shared boundary
is deliberate rather than an attempt to assign every line of code to exactly
one faculty.

**Analogical.** Synthesis is implemented only by transformations that alter the
available unity of the manifold while retaining provenance and alternatives.
Parsing, concatenation, caching, clustering, and feature extraction do not
count merely because they precede classification ([K-016](CLAIMS.md#k-016)).

### Understanding: concepts and constitutive rules

**Textual.** Understanding is discursive, operates through concepts, and is
characterized as a faculty of judgment and rules
([A68-69/B93-94](sources/kant/critique-a.md#a68)). Categories supply functions
of unity but gain cognitive use only in relation to sensible intuition and
possible experience ([B143-148](sources/kant/deduction-b.md#b143),
[B159-169](sources/kant/deduction-b.md#b159)).

**Interpretive.** The **understanding role** owns the repository of concepts
and constitutive rules available to a cycle. It supplies general conditions
for candidate unity and predication; it does not receive raw observations or
declare that its own concepts apply. Fixed empirical concepts are permitted in
the first experiment, but their acquisition is deferred.

**Interpretive.** The minimal constitutive repertoire contains:

- **unity and plurality constraints** that state how many intuitions
  may belong to one candidate;
- **persistence constraints** that state which changes preserve the identity
  of a candidate through time; and
- **lawful-succession constraints** only in scenarios that make event or causal
  judgments.

These are category-inspired constraints, not an implementation of the complete
table or a derivation of its twelve members. Each included constraint must
change a candidate, judgment, or refusal; unused category names are omitted.

### Power of judgment and schematism: applicability

**Textual.** The power of judgment determines whether a particular stands
under a rule, and schemata mediate the application of categories to appearances
while restricting that application to sensible conditions
([A132/B171](sources/kant/critique-a.md#a132),
[A137-147/B176-187](sources/kant/critique-a.md#a137)).

**Interpretive.** The **power-of-judgment role** runs schemas against candidate
representations and records satisfied, failed, and undecided conditions. Every
constitutive category-like rule requires a temporal applicability procedure.
An ordinary empirical concept may use a simpler inspectable procedure, but the
trace must still distinguish the procedure from the concept's general content.
This adopts the working reading in [K-012](CLAIMS.md#k-012); see
[ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).

**Analogical.** A schema is not a database schema, prototype image, generic
validator, or unexplained score. It plays the mediating role only when it both
connects a general rule to formed particular content and records the sensible
conditions that limit application.

### Apperception: cycle-wide unity constraint

**Textual.** In the B Deduction, the "I think" must be able to accompany the
manifold, and judgment relates representations through objective rather than
merely subjective unity ([B131-142](sources/kant/deduction-b.md#b131)).

**Analogical.** Kantbot's **apperception role** is a unity check over a proposed
judgment and its entire provenance subgraph. It requires:

1. one declared cycle and configuration governs every ground;
2. every transformation is reachable from admitted presented elements through
   a successful variant projection;
3. identity references do not assign incompatible identities to the same
   element or silently merge rival candidates;
4. rule authorities and scopes are mutually compatible; and
5. the proposition commits to no stronger status than its grounds support.

Failure blocks commitment and yields a conflict report. This does more than
validate serialization because it can reject individually valid intermediate
states whose combined commitments cannot belong to one coherent cognitive
trace. It does **not** establish consciousness, self-awareness, a transcendental
subject, or the numerical identity of a software self ([K-018](CLAIMS.md#k-018)).

### Reason: represented boundary, deferred operation

**Textual.** Reason draws inferences and seeks principles and systematic unity;
its pursuit of the unconditioned can exceed possible experience
([A299-304/B355-361](sources/kant/critique-a.md#a299),
[A311-320/B367-377](sources/kant/critique-a.md#a311)).

**Engineering.** Phase 1 reserves rule-authority and provenance fields needed
for reason, but the first cognitive cycle does not chain judgments, pursue
systematic unity, or instantiate ideas of reason. Those operations remain
deferred to Phase 4. A single-cycle refusal caused by absent presentation is
therefore not automatically transcendental illusion.

## Rule authority

**Textual.** Constitutive principles determine objects of possible experience;
regulative principles guide inquiry without constituting the corresponding
object ([A179-180/B222-223](sources/kant/critique-a.md#a179),
[A509-515/B537-543](sources/kant/critique-a.md#a509)).

**Analogical.** Every rule declares one of three authorities:

- `constitutive`: may help license candidate objecthood or an object-level
  judgment within a declared scope;
- `regulative`: may rank, continue, or organize inquiry but may not add an
  object, predicate, or object-level warrant; or
- `engineering`: controls execution or validation and has no philosophical
  authority over objecthood.

**Analogical.** Promoting a regulative result into a judgment's object-level
grounds is a unity failure and, once reason is implemented, a candidate case of
overreach. Merely ignoring a regulative suggestion is not failed cognition.
The choice is recorded in
[ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md).

## The cognitive flow

**Engineering.** One cycle proceeds as follows. "Stop" below means no stronger
representation is licensed; the trace and limit report are still successful
outputs.

1. **Open the cycle.** Freeze the episode boundary, form configuration,
   available concepts, schemas, rule authorities, and interpretation variant.
2. **Receive and project.** Derive shared presented elements from valid
   observations, then run the selected variant projection. The accepted
   Kantian variant places admissible particulars under sensible form as
   intuitions. Stop an affected path at `not-presentable`; preserve competing
   projections as alternatives.
3. **Apprehend.** Traverse and take together the manifold of intuition according
   to its form.
   Record segmentation choices rather than treating them as given objects.
4. **Reproduce.** Retrieve only earlier intuitions licensed by the
   retention rule. Record omissions and rival retrievals.
5. **Recognize and synthesize.** Apply identity and constitutive-unity rules to
   propose candidate representations. Stop at `synthesis-failed` when no
   admissible unity exists; retain multiple candidates as `synthesis-ambiguous`.
6. **Apply concepts through schemas.** For every relevant candidate, expose
   successful, failed, and undecided applicability conditions. A score alone
   cannot force application.
7. **Propose a judgment.** Assemble a proposition only from a candidate and
   application result whose required constitutive conditions pass. Preserve
   the difference between applicability and commitment
   ([K-017](CLAIMS.md#k-017)).
8. **Check unity.** Validate the proposed judgment and its grounds as one
   coherent, scope-respecting trace. On conflict, emit `unity-conflict` and do
   not commit the proposition.
9. **Commit or withhold.** Commit a judgment only when all required conditions
   pass. Otherwise emit the strongest licensed non-judgmental result.
10. **Critique and report.** Attach alternatives, uncertainty, failed
    conditions, rule authority, scope, and limits to every terminal result.

**Engineering.** Concept application and the unity check may request a return
to an earlier stage with a narrowed candidate, but the trace must record the
revision. A loop may not erase its earlier alternatives or turn repeated
failure into warrant.

## Licensing conditions

### Candidate object

**Interpretive.** A candidate counts as an object candidate only if all of the
following hold:

- its content descends from admitted presented elements through successful
  variant projections;
- its elements can be combined under the episode's form;
- an explicit identity rule explains their proposed unity across the relevant
  interval;
- required constitutive constraints pass;
- incompatible candidates remain separate alternatives; and
- the trace records the candidate's scope and unresolved conditions.

**Interpretive.** Co-occurrence, repeated association, similarity, internal
consistency, or an upstream toy-world identifier is insufficient by itself.

### Judgment

**Analogical.** A judgment is licensed only if:

- a qualifying object candidate is available;
- the predicate concept's applicability procedure succeeds;
- required schema and constitutive-rule conditions succeed;
- the proposition's modality does not exceed those grounds;
- the cycle-wide unity check succeeds; and
- a complete warrant and limit report can be emitted.

**Analogical.** An application result can be successful while judgment is
withheld—for example, if rival identity syntheses support the same predicate
but no single object candidate wins. Conversely, a coherent candidate does not
license a predicate whose schema fails. This separation is essential to
distinguishing a judgment from a classification result.

### Warrant and objective validity

**Interpretive.** Within this experiment, **objective validity** names the
licensed relation of a judgment to an object under the declared conditions of
presentation, synthesis, applicability, and unity. It is not high confidence,
successful execution, majority agreement, or truth in every context.

**Engineering.** A warrant contains at least the observation grounds,
presentation form, variant projection, synthesis operations, identity rule,
concept and schema results, constitutive rules, unity-check result,
alternatives, scope, and limit status. If any required field is unavailable,
the system withholds the judgment rather than inventing an explanation.

## Terminal outcomes and cognitive limits

**Engineering.** The cycle must distinguish these outcomes:

| Outcome | Meaning | Permitted next claim |
| --- | --- | --- |
| `input-error` | Serialized material violates the external interface | No cognitive result about the supplied content |
| `not-presentable` | A shared element cannot enter the selected variant under its declared form and role conditions | No object candidate from that variant path |
| `synthesis-failed` | No candidate satisfies identity and unity constraints | Report the manifold and failed rules |
| `synthesis-ambiguous` | Several candidates remain admissible | Report alternatives; do not silently choose |
| `concept-not-applicable` | Required applicability conditions fail | Retain the candidate without that predicate |
| `application-underdetermined` | Available grounds do not decide applicability | Report missing grounds or interval |
| `unity-conflict` | Individually valid states cannot ground one coherent commitment | Withhold the judgment and expose the conflict |
| `judgment-withheld` | One or more licensing conditions remain unmet | Report the strongest candidate or application status |
| `judgment-committed` | All required conditions pass within scope | Assert only the scoped proposition with warrant |
| `overreach` | A claim exceeds its declared presentation conditions or uses regulative guidance constitutively | Reject the promotion and identify the authority violation |

**Analogical.** Uncertainty varies support within an admissible path;
ambiguity preserves multiple admissible paths; failure identifies a violated
condition; withholding refuses commitment; overreach diagnoses an illicit
change of scope or authority. Missing data can cause any of the first four
states but is not itself a transcendental limit.

**Interpretive.** Noumena and things in themselves appear only as reminders
that the model's object claims are limited to its conditions of presentation.
They are never represented as hidden toy-world records, privileged labels, or
causes accessible to the evaluator ([K-014](CLAIMS.md#k-014)). An evaluator may
use hidden scenario state to score behavior, but Kantbot cannot cite that state
as cognitive warrant.

## Required behavioral consequences

**Engineering.** The separate Phase 1 prediction catalog will supply full
scenarios. This specification already requires the following observable
differences:

1. Reordering an episode can change a persistence or succession judgment even
   when the multiset of observation content is unchanged.
2. Removing licensed reproduction can prevent an identity synthesis that a
   stateless classifier would still emit.
3. Two locally coherent candidates can force ambiguity rather than a highest-
   score choice.
4. A concept can apply to a candidate while the final judgment is withheld for
   a cycle-wide unity conflict.
5. A regulative rule can change which inquiry is attempted next but cannot by
   itself change an object predicate or create a judgment.
6. A proposed claim about content outside the configured presentation form is
   rejected as out of scope even when an evaluator knows the hidden state.
7. A B-led synthesis variant may produce fewer stage distinctions in its trace,
   but it must preserve reception, figurative synthesis, objective-unity, and
   sensible-use constraints.
8. The same presented-element identity can project into a Kantian intuition, a
   different variant representation, or a variant-specific refusal; a variant
   that changes only the label fails the projection safeguard.

**Engineering.** If a later executable model cannot display these differences,
its vocabulary does not yet implement this specification.

## Deliberate omissions and follow-up work

**Engineering.** This document does not define serialized types, interfaces,
algorithms, confidence mathematics, learning rules, or a full category table.
The companion [worked examples](WORKED_EXAMPLES.md) instantiate the cognitive
flow without fixing Phase 2 serialization or algorithms. The companion
[diagrams](COGNITIVE_ARCHITECTURE.md) visualize the semantic contract without
turning it into Phase 2 types or services. The remaining omissions belong to
later Roadmap deliverables and Phase 2. This specification also does not claim
to resolve scholarly disputes about the deductions, imagination, schematism,
or apperception.

The decision records governing this specification are:

- [ADR 0001: Use variant-scoped receptive terminology](docs/decisions/0001-variant-scoped-receptive-terminology.md)
- [ADR 0002: Use an A/B hybrid synthesis default](docs/decisions/0002-a-b-synthesis.md)
- [ADR 0003: Separate object formation, applicability, and judgment licensing](docs/decisions/0003-object-and-judgment-licensing.md)
- [ADR 0004: Make limit outcomes and rule authority behaviorally distinct](docs/decisions/0004-limit-outcomes-and-rule-authority.md)

All four records are Accepted and their affected claims are Current and linked
in the [claims register](CLAIMS.md). Phase 2 must formalize the shared-boundary
and variant-projection types without collapsing them, following the
[decision-record lifecycle](docs/decisions/README.md#status-lifecycle).
