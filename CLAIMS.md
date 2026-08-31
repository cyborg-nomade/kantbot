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
| <a id="k-010"></a>K-010 | The initial specification should read the A Deduction primarily for its analysis of synthesis and the B Deduction primarily for objective unity and category application, without treating either as dispensable. | Provisional | [Edition-sensitive fault lines](PRIMARY_SOURCES.md#edition-sensitive-fault-lines) | Phase 1 must name the edition behind a design and introduce variants when the difference changes behavior. |
| <a id="k-011"></a>K-011 | For the initial architecture, an object should be understood as requiring rule-governed unity of a manifold rather than mere aggregation or similarity. | Provisional | [A103-110](sources/kant/deduction-a.md#a103); [B137-142](sources/kant/deduction-b.md#b137) | Candidate-object formation needs explicit unity and identity conditions. |
| <a id="k-012"></a>K-012 | Schematism is best treated as an applicability procedure connecting a concept or category to a temporally structured presentation. | Open | [A132-147/B171-187](sources/kant/critique-a.md#a132) | Phase 1 must decide whether schemata are required and how they differ from ordinary predicates or validators. |
| <a id="k-013"></a>K-013 | Objective validity requires more than a representation being internally consistent or repeatedly associated; it requires declared conditions relating synthesis to an object. | Provisional | [B137-142](sources/kant/deduction-b.md#b137); [A89-95/B122-129](sources/kant/critique-a.md#a89) | A trace must expose the conditions licensing object reference, not only successful processing. |
| <a id="k-014"></a>K-014 | In the initial model, noumena and things in themselves should function as limit concepts, not as hidden objects or privileged ground-truth records. | Current | [A249-260](sources/kant/critique-a.md#a249); [B306-309](sources/kant/second-edition-excerpts.md#b306) | The model must not represent cognitive limits by inventing an accessible noumenal layer. |

### Analogical claims

| ID | Claim | Status | Grounds | Consequence |
| --- | --- | --- | --- | --- |
| <a id="k-015"></a>K-015 | A bounded program interface may model constrained presentation, but calling its data "intuition" remains an analogy rather than a literal attribution of sensibility. | Provisional | [Glossary: sensibility and intuition](GLOSSARY.md#sensibility-sinnlichkeit) | Phase 1 must specify what is given, its form, and where the analogy ceases to hold. |
| <a id="k-016"></a>K-016 | A provenance-preserving transformation that combines and retains presented elements may serve as a computational analogue of synthesis. | Provisional | [A77-83/B102-116](sources/kant/critique-a.md#a77); [Glossary: synthesis](GLOSSARY.md#synthesis-synthesis) | The implementation must distinguish synthesis from parsing, concatenation, or opaque feature extraction. |
| <a id="k-017"></a>K-017 | Concept application and judgment should initially be modeled as distinguishable, inspectable roles even if a later implementation combines them. | Provisional | [A68-70/B93-95](sources/kant/critique-a.md#a68); [B140-142](sources/kant/deduction-b.md#b140) | Traces must separately expose applicability grounds and the resulting commitment. |
| <a id="k-018"></a>K-018 | A functional unity constraint may be compared to apperception only if the project explicitly denies that state coherence establishes consciousness or a transcendental subject. | Open | [A107-110](sources/kant/deduction-a.md#a107); [B131-136](sources/kant/deduction-b.md#b131) | Phase 1 must decide what unity check is behaviorally meaningful and how it avoids the false equivalence. |
| <a id="k-019"></a>K-019 | A system failure that promotes an inference or regulative goal beyond its declared experiential conditions may model transcendental overreach. | Deferred | [A293-298/B349-355](sources/kant/critique-a.md#a293); [A509-515/B537-543](sources/kant/critique-a.md#a509) | Phase 4 must distinguish overreach from falsehood, low confidence, missing data, and ordinary software error. |
| <a id="k-020"></a>K-020 | Declaring a rule's authority as constitutive or regulative may constrain how the system uses the rule and reports its results. | Open | [A179-180/B222-223](sources/kant/critique-a.md#a179); [A509-515/B537-543](sources/kant/critique-a.md#a509) | Phase 1 must specify observable differences between the two rule types; Phase 4 implements regulative inquiry. |

### Engineering claims

| ID | Claim | Status | Grounds | Consequence |
| --- | --- | --- | --- | --- |
| <a id="k-021"></a>K-021 | The first usable Kantbot should be a small local program operating in a deliberately bounded world, not a general-purpose assistant. | Current | [Roadmap](ROADMAP.md#destination-a-usable-philosophical-instrument) | Initial scenarios and interfaces must remain finite, reproducible, and inspectable. |
| <a id="k-022"></a>K-022 | Every meaningful judgment should carry a structured provenance trace from presented observations through transformations, rules, alternatives, and remaining limits. | Current | [Manifest](MANIFEST.md#the-process-must-be-inspectable); [Roadmap](ROADMAP.md#phase-2--define-an-executable-formal-model) | Provenance is part of the data model and acceptance criteria, not optional explanatory prose. |
| <a id="k-023"></a>K-023 | Ambiguity, failed synthesis, failed concept application, conflict, and refusal to overclaim are first-class outcomes. | Current | [Manifest](MANIFEST.md#limits-are-part-of-cognition); [Roadmap](ROADMAP.md#phase-3--implement-the-minimal-cognitive-cycle) | APIs, traces, scenarios, and tests must represent these outcomes explicitly. |
| <a id="k-024"></a>K-024 | Disputed philosophical assumptions should be replaceable variants when they produce meaningful differences in behavior or traces. | Current | [Manifest](MANIFEST.md#interpretations-must-remain-visible); [Roadmap](ROADMAP.md#phase-2--define-an-executable-formal-model) | Interfaces should preserve live alternatives selectively, and evaluation must compare their consequences. |
| <a id="k-025"></a>K-025 | The first release does not require language-model integration, open-world perception, or later philosophers. | Current | [Research questions and non-goals](RESEARCH_QUESTIONS.md#non-goals-for-the-first-usable-release); [Roadmap](ROADMAP.md#destination-a-usable-philosophical-instrument) | These integrations must not become hidden prerequisites for the minimal cognitive cycle. |
| <a id="k-026"></a>K-026 | Consequential design statements must carry a claim label and links to their grounds or decision record. | Current | [Contribution guide](CONTRIBUTING.md#documentation-conventions); [Decision records](docs/decisions/README.md#required-connections); [Manifest objectives](MANIFEST.md#objectives) | Specifications, decisions, and architecture documentation must keep textual warrant distinct from implementation authority. |

## Unresolved clusters

The following clusters collect claims whose statuses must be settled together
in Phase 1. They are not additional claims.

| Cluster | Claims | Required outcome |
| --- | --- | --- |
| Presentation and intuition | K-001, K-015 | Define what is given, in what form, and whether the project uses "intuition" or the weaker "constrained presentation" in implementation documents. |
| Synthesis architecture | K-002, K-003, K-004, K-016 | Decide whether the threefold A-edition synthesis is the default, a variant, or source context only. |
| Objects and objective validity | K-006, K-011, K-013, K-017 | Specify the unity, applicability, and warrant conditions separating a candidate representation from an object-level judgment. |
| Schematism and categories | K-007, K-008, K-012 | Decide which categories and schemata are implemented and what observable work each performs. |
| Apperception and unity | K-005, K-018 | Define a functional unity constraint without claims of machine consciousness or a metaphysical self. |
| Limits and rule authority | K-009, K-014, K-019, K-020 | Separate uncertainty and ordinary failure from regulative guidance and transcendental overreach. |

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
