# Claims Register

## Purpose

This register records the substantive claims Kantbot currently relies upon or
expects to test. It keeps three questions separate:

1. **What kind of claim is this?** Textual, interpretive, analogical, or
   engineering.
2. **What is its project status?** Current, provisional, open, deferred, or
   retired.
3. **What does it constrain?** A reading, architecture decision, behavior,
   invariant, evaluation, or scope boundary.

The [glossary](GLOSSARY.md) defines terms. The
[primary-source map](PRIMARY_SOURCES.md) organizes passages by question. This
register instead tracks complete statements that can be supported, challenged,
revised, implemented, or withdrawn.

## Labels

- **Textual:** intended as a close, edition-sensitive restatement of Kant's
  text. Its grounds must include primary citations.
- **Interpretive:** selects among, combines, or develops plausible readings of
  the text. It must identify what the text underdetermines.
- **Analogical:** uses a Kantian distinction to constrain a computational model
  without claiming that software literally has the corresponding human faculty.
- **Engineering:** introduced for testability, inspectability, usability, or
  experimental control and not attributed to Kant.

Every registered claim has one primary label. If a sentence needs two labels,
split it into the textual or interpretive claim and the computational claim.

## Statuses

- **Current:** the project presently relies on this claim. Changing it requires
  an explicit update here and to affected documents or decisions.
- **Provisional:** a working commitment suitable for continued design, but
  expected to be tested or refined in a named later phase.
- **Open:** alternatives remain live; no implementation should silently settle
  the question.
- **Deferred:** relevant to the project but outside the present implementation
  scope.
- **Retired:** no longer endorsed. Retired claims remain in the register with a
  replacement or reason so that the change is visible.

`Current` does not mean philosophically indisputable, and `Open` does not mean
unsupported. Status describes project commitment, not certainty.

## Register

### Textual claims

| ID | Claim | Status | Grounds | Consequence |
| --- | --- | --- | --- | --- |
| <a id="k-001"></a>K-001 | Human cognition requires both receptive sensibility, through which objects are given in intuition, and spontaneous understanding, through which they are thought by concepts. | Current | [A19-20/B33-34](sources/kant/critique-a.md#a19); [A50-51/B74-75](sources/kant/critique-a.md#a50) | Any Kantbot analogy must preserve a distinction between presentation and conceptual determination. |
| <a id="k-002"></a>K-002 | Synthesis is the act of putting a manifold of representations together and apprehending their manifoldness in one cognition. | Current | [A77-79/B102-104](sources/kant/critique-a.md#a77) | Mere receipt or storage of inputs does not by itself model synthesis. |
| <a id="k-003"></a>K-003 | The A Deduction distinguishes syntheses of apprehension, reproduction, and recognition as subjective grounds involved in cognition. | Current | [A98-110](sources/kant/deduction-a.md#a98) | The threefold synthesis is textually grounded as an A-edition account, not yet mandated as the software architecture. |
| <a id="k-004"></a>K-004 | Imagination performs a synthesis of the sensible manifold and mediates sensibility and understanding, though the A and B deductions present its role differently. | Current | [A120-126](sources/kant/deduction-a.md#a120); [B151-152](sources/kant/deduction-b.md#b151) | An account of synthesis must address imagination, while its component boundary remains interpretive. |
| <a id="k-005"></a>K-005 | In the B Deduction, the "I think" must be able to accompany representations, whose manifold must be combinable in one self-consciousness. | Current | [B131-136](sources/kant/deduction-b.md#b131) | Apperception constrains claims about unity but does not by itself license claims about machine consciousness. |
| <a id="k-006"></a>K-006 | Judgment relates cognitions through the objective unity of apperception rather than through merely subjective association. | Current | [B140-142](sources/kant/deduction-b.md#b140) | A Kantian account of judgment must distinguish objective purport from contingent association. |
| <a id="k-007"></a>K-007 | Categories yield cognition only in relation to sensible intuition and objects of possible experience. | Current | [B146-169](sources/kant/deduction-b.md#b146) | Purely conceptual combination cannot be treated as cognition of an object without declared conditions of possible presentation. |
| <a id="k-008"></a>K-008 | Schemata mediate the application of categories to appearances and at the same time restrict categories to sensible conditions. | Current | [A137-147/B176-187](sources/kant/critique-a.md#a137) | Any appeal to schematism must include both applicability and limitation, not only matching. |
| <a id="k-009"></a>K-009 | Constitutive principles determine objects of possible experience, whereas regulative principles guide inquiry without constituting the corresponding object. | Current | [A179-180/B222-223](sources/kant/critique-a.md#a179); [A509-515/B537-543](sources/kant/critique-a.md#a509) | The project must not present a regulative goal as if it established an object-level fact. |

### Interpretive claims

| ID | Claim | Status | Grounds | Consequence |
| --- | --- | --- | --- | --- |
| <a id="k-010"></a>K-010 | The initial specification should read the A Deduction primarily for its analysis of synthesis and the B Deduction primarily for objective unity and category application, without treating either as dispensable. | Current | [Edition-sensitive fault lines](PRIMARY_SOURCES.md#edition-sensitive-fault-lines); [ADR 0002](docs/decisions/0002-a-b-synthesis.md) | Every synthesis trace must name its edition-sensitive variant, with variants introduced when the difference changes behavior. |
| <a id="k-011"></a>K-011 | For the initial architecture, an object should be understood as requiring rule-governed unity of a manifold rather than mere aggregation or similarity. | Current | [A103-110](sources/kant/deduction-a.md#a103); [B137-142](sources/kant/deduction-b.md#b137); [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md) | Candidate-object formation requires explicit unity and identity conditions. |
| <a id="k-012"></a>K-012 | Schematism is best treated as an applicability procedure connecting a concept or category to a temporally structured presentation. | Current | [A132-147/B171-187](sources/kant/critique-a.md#a132); [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md) | Category-like rules require inspectable temporal applicability procedures that expose both application and limitation. |
| <a id="k-013"></a>K-013 | Objective validity requires more than a representation being internally consistent or repeatedly associated; it requires declared conditions relating synthesis to an object. | Current | [B137-142](sources/kant/deduction-b.md#b137); [A89-95/B122-129](sources/kant/critique-a.md#a89); [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md) | A trace must expose the conditions licensing object reference, not only successful processing. |
| <a id="k-014"></a>K-014 | In the initial model, noumena and things in themselves should function as limit concepts, not as hidden objects or privileged ground-truth records. | Current | [A249-260](sources/kant/critique-a.md#a249); [B306-309](sources/kant/second-edition-excerpts.md#b306) | The model must not represent cognitive limits by inventing an accessible noumenal layer. |

### Analogical claims

| ID | Claim | Status | Grounds | Consequence |
| --- | --- | --- | --- | --- |
| <a id="k-015"></a>K-015 | The accepted Kantian variant uses "intuition" as theory-internal terminology for a representation explicitly projected from a shared presented element under declared receptive-role criteria, without thereby claiming that the whole model is a human mind. | Current | [Glossary: sensibility and intuition](GLOSSARY.md#sensibility-sinnlichkeit); [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md) | Traces must preserve both the shared presented element and the Kantian intuition projection; relabeling without structural or behavioral work is insufficient. |
| <a id="k-016"></a>K-016 | A provenance-preserving transformation that combines and retains variant-projected representations may serve as a computational analogue of synthesis. | Current | [A77-83/B102-116](sources/kant/critique-a.md#a77); [Glossary: synthesis](GLOSSARY.md#synthesis-synthesis); [ADRs 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md) and [0002](docs/decisions/0002-a-b-synthesis.md) | The implementation must distinguish variant projection and synthesis from parsing, relabeling, concatenation, or opaque feature extraction. |
| <a id="k-017"></a>K-017 | Concept application and judgment should initially be modeled as distinguishable, inspectable roles even if a later implementation combines them. | Current | [A68-70/B93-95](sources/kant/critique-a.md#a68); [B140-142](sources/kant/deduction-b.md#b140); [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md) | Traces must separately expose applicability grounds and the resulting commitment. |
| <a id="k-018"></a>K-018 | A functional unity constraint may be compared to apperception only if the project explicitly denies that state coherence establishes consciousness or a transcendental subject. | Current | [A107-110](sources/kant/deduction-a.md#a107); [B131-136](sources/kant/deduction-b.md#b131); [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md) | The unity check must reject incompatible provenance or scope while avoiding the false equivalence with consciousness. |
| <a id="k-019"></a>K-019 | A system failure that promotes an inference or regulative goal beyond its declared experiential conditions may model transcendental overreach. | Deferred | [A293-298/B349-355](sources/kant/critique-a.md#a293); [A509-515/B537-543](sources/kant/critique-a.md#a509) | Phase 4 must distinguish overreach from falsehood, low confidence, missing data, and ordinary software error. |
| <a id="k-020"></a>K-020 | Declaring a rule's authority as constitutive or regulative may constrain how the system uses the rule and reports its results. | Current | [A179-180/B222-223](sources/kant/critique-a.md#a179); [A509-515/B537-543](sources/kant/critique-a.md#a509); [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md) | A regulative rule may organize inquiry but cannot supply an object-level ground; Phase 4 implements active regulative inquiry. |

### Engineering claims

| ID | Claim | Status | Grounds | Consequence |
| --- | --- | --- | --- | --- |
| <a id="k-021"></a>K-021 | The first usable Kantbot should be a small local program operating in a deliberately bounded world, not a general-purpose assistant. | Current | [Roadmap](ROADMAP.md#destination-a-usable-philosophical-instrument) | Initial scenarios and interfaces must remain finite, reproducible, and inspectable. |
| <a id="k-022"></a>K-022 | Every meaningful judgment should carry a structured provenance trace from presented observations through transformations, rules, alternatives, and remaining limits. | Current | [Manifest](MANIFEST.md#the-process-must-be-inspectable); [Roadmap](ROADMAP.md#phase-2--define-an-executable-formal-model) | Provenance is part of the data model and acceptance criteria, not optional explanatory prose. |
| <a id="k-023"></a>K-023 | Ambiguity, failed synthesis, failed concept application, conflict, and refusal to overclaim are first-class outcomes. | Current | [Manifest](MANIFEST.md#limits-are-part-of-cognition); [Roadmap](ROADMAP.md#phase-3--implement-the-minimal-cognitive-cycle) | APIs, traces, scenarios, and tests must represent these outcomes explicitly. |
| <a id="k-024"></a>K-024 | Disputed philosophical assumptions should be replaceable variants when they produce meaningful differences in behavior or traces. | Current | [Manifest](MANIFEST.md#interpretations-must-remain-visible); [Roadmap](ROADMAP.md#phase-2--define-an-executable-formal-model) | Interfaces should preserve live alternatives selectively, and evaluation must compare their consequences. |
| <a id="k-025"></a>K-025 | The first release does not require language-model integration, open-world perception, or later philosophers. | Current | [Research questions and non-goals](RESEARCH_QUESTIONS.md#non-goals-for-the-first-usable-release); [Roadmap](ROADMAP.md#destination-a-usable-philosophical-instrument) | These integrations must not become hidden prerequisites for the minimal cognitive cycle. |
| <a id="k-026"></a>K-026 | Consequential design statements must carry a claim label and links to their grounds or decision record. | Current | [Contribution guide](CONTRIBUTING.md#documentation-conventions); [Decision records](docs/decisions/README.md#required-connections); [Manifest objectives](MANIFEST.md#objectives) | Specifications, decisions, and architecture documentation must keep textual warrant distinct from implementation authority. |
| <a id="k-027"></a>K-027 | A declared Kantian architecture should be treated as an executable hypothesis: if the account is correct and sufficiently complete, increasing implementation fidelity should approach corresponding features of human cognition in bounded settings. | Current | [Manifest premise](MANIFEST.md#premise); [Manifest inspiration](MANIFEST.md#inspiration) | Evaluation must compare behavior and structure, while divergence remains material for criticism rather than being hidden by theory-neutral terminology. |

## Decision clusters

The following clusters collect claims that Phase 1 must settle together and
record which accepted decision, if any, currently governs them. They are not
additional claims.

| Cluster | Claims | Required outcome |
| --- | --- | --- |
| Presentation and intuition | K-001, K-015, K-027 | Resolved by [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md): preserve shared observations and presented elements, then project them into variant-specific representations; the accepted Kantian variant uses `intuition`. |
| Synthesis architecture | K-002, K-003, K-004, K-016 | Resolved for the initial model by [ADR 0002](docs/decisions/0002-a-b-synthesis.md): use the threefold A-edition analysis in an A/B hybrid default and preserve a behaviorally meaningful B-led variant. |
| Objects and objective validity | K-006, K-011, K-013, K-017 | Resolved by [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md): keep candidate formation, application, proposed judgment, and commitment distinct. |
| Schematism and categories | K-007, K-008, K-012 | Resolved for the minimal repertoire by [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md): use inspectable temporal procedures and only category-inspired constraints with observable work. |
| Apperception and unity | K-005, K-018 | Resolved by [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md): use a cycle-wide provenance and scope check without treating it as proof of consciousness. |
| Limits and rule authority | K-009, K-014, K-019, K-020 | Initially resolved by [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md): use typed outcomes and rule authority; K-019 remains Deferred until Phase 4. |

## Maintenance rules

1. Give each new claim the next stable `K-###` identifier; never reuse an ID.
2. Write one proposition per entry and assign exactly one primary claim label.
3. Link textual claims to primary passages. Interpretive claims must name what
   remains underdetermined. Analogical claims must state the false equivalence
   they reject. Engineering claims must identify the behavior or workflow they
   require.
4. Update a claim's status when a decision record adopts, revises, defers, or
   rejects it. Link the decision record from the claim's grounds or consequence.
5. Do not delete a superseded claim. Mark it **Retired** and identify its
   replacement or the reason for withdrawal.
6. A component name, glossary definition, citation, or open question is not by
   itself a registered claim. Add an entry only when the statement can affect
   architecture, behavior, evaluation, or project scope.
