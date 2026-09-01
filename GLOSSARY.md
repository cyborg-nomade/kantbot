# Kantbot Glossary

## Purpose

This glossary fixes a shared vocabulary for the first Kantbot experiments. It
is not a dictionary of Kant's philosophy and does not assume in advance that
computational structures either do or do not realize Kantian cognitive roles.
It records, for each load-bearing term:

- a concise textual sense;
- the provisional role the term may play in Kantbot;
- a warning against likely false equivalences;
- the status of the proposed interpretation; and
- primary-text anchors for later source work.

The entries are working constraints. Phase 1 may revise them, but revisions
should be explicit rather than silently changing the meaning of an interface or
data structure.

## Conventions

Primary references to the *Critique of Pure Reason* use the standard A/B
pagination. References identify useful anchors, not exhaustive textual support.
German terms are included where they prevent ambiguity; capitalization follows
ordinary English usage rather than treating every technical term as a proper
noun.

### What A and B mean

**A** refers to the first edition of the *Critique of Pure Reason*, published in
1781; **B** refers to the substantially revised second edition, published in
1787. Thus `A103` means page 103 of the first edition, while `B129` means page
129 of the second. A reference such as `A50/B74` points to corresponding text in
both editions. Modern scholarly editions preserve these page markers so that a
passage can be located across different translations.

Kant rewrote important parts of the book rather than merely adding corrections.
Most importantly for Kantbot, the Transcendental Deduction of the Categories
has two distinct versions. The shared lead-in occupies A84-95/B116-129; what is
usually called the **A Deduction** then runs from A95 to A130, while the **B
Deduction** runs from B129 to B169. The public-domain source texts used by this
glossary are reproduced in this repository:

- [First-edition text, A1-A856](sources/kant/critique-a.md)
- [Second-edition excerpts, B1-5 and B294-315](sources/kant/second-edition-excerpts.md)
- [A Deduction (1781)](sources/kant/deduction-a.md)
- [B Deduction (1787)](sources/kant/deduction-b.md)

Every primary anchor below is clickable. Deduction citations open the focused
deduction files; other parallel A/B citations open the corresponding passage in
the locally copied first-edition text. B-only citations outside the deduction
open the relevant second-edition excerpt. A linked range opens at its first page
or at the beginning of the section containing it.

The repository copies use F. Max Müller's public-domain English translation,
which prints the first-edition text as its main text and the rewritten B
Deduction as Supplement XIV. See the [source and transcription
notes](sources/kant/README.md) before quoting them. The original German is also
freely available in separate [1781](https://www.gutenberg.org/ebooks/6342) and
[1787](https://www.gutenberg.org/ebooks/6343) editions.

Each Kantbot interpretation has one of these claim labels. Substantive project
statements and their current status are tracked in the [claims
register](CLAIMS.md).

- **Textual:** intended as a close restatement of Kant's text.
- **Interpretive:** selects among, or builds upon, plausible readings of Kant.
- **Analogical:** uses a Kantian distinction to constrain a computational model
  without asserting an identity between minds and software.
- **Engineering:** introduced to make the program testable, inspectable, or
  usable; it is not attributed to Kant.

Implementation labels describe the current roadmap:

- **Foundation:** needed to specify the minimal cognitive cycle.
- **Decision required:** its exact role must be settled in Phase 1.
- **Deferred:** expected in a later phase, not required in the first cycle.
- **Context only:** needed to state limits or disagreements but not presently
  planned as a software component.

## Faculties and capacities

### Sensibility (*Sinnlichkeit*)

- **Textual sense:** The receptive capacity through which objects are given to
  us by affecting us; it supplies intuitions rather than concepts.
- **Kantbot role:** The constrained reception boundary that presents a manifold
  in a specified spatial, temporal, or otherwise ordered form.
- **Not equivalent to:** A hardware sensor, a generic input parser, or an
  unstructured store of raw facts.
- **Status:** **Interpretive / Analogical**; **Foundation**. The accepted
  Kantian variant uses this role to project shared presented elements into
  intuitions under [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md).
- **Primary anchors:** [A19/B33](sources/kant/critique-a.md#a19); [A50/B74](sources/kant/critique-a.md#a50).

### Understanding (*Verstand*)

- **Textual sense:** The spontaneous faculty of concepts, rules, and judgment;
  it thinks what sensibility gives but does not itself intuit.
- **Kantbot role:** The role responsible for applying concepts and rules to
  synthesized representations and making them available for judgment.
- **Not equivalent to:** General intelligence, all computation, or an opaque
  classifier whose output is merely renamed a concept.
- **Status:** **Analogical**; **Foundation**. Its division from imagination and
  the power of judgment follows [ADRs 0002](docs/decisions/0002-a-b-synthesis.md)
  and [0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchors:** [A50-51/B74-75](sources/kant/critique-a.md#a50); [A69/B94](sources/kant/critique-a.md#a69).

### Imagination (*Einbildungskraft*)

- **Textual sense:** The capacity to represent an object even when it is not
  present in intuition and, in its transcendental role, to synthesize the
  manifold of intuition in a way that mediates sensibility and understanding.
- **Kantbot role:** The synthesis role that combines and retains presented
  elements so that candidate objects or events can become available for
  conceptual determination.
- **Not equivalent to:** Image generation, fantasy, free-form creativity, or a
  cache with a philosophical name.
- **Status:** **Interpretive / Analogical**; **Foundation**. The A/B hybrid
  default and its shared boundary with understanding are fixed by
  [ADR 0002](docs/decisions/0002-a-b-synthesis.md).
- **Primary anchors:** [A120](sources/kant/deduction-a.md#a120); [B151-152](sources/kant/deduction-b.md#b151).

### Power of judgment (*Urteilskraft*)

- **Textual sense:** The capacity to subsume a particular under a universal,
  that is, to determine whether something stands under a given rule.
- **Kantbot role:** The role that tests whether a candidate representation meets
  the conditions for applying a concept or rule and for forming a judgment.
- **Not equivalent to:** A judgment as output, a scoring function alone, or
  unrestricted practical decision-making.
- **Status:** **Analogical**; **Foundation**. Its applicability role remains
  semantically distinct even if later types combine it with another component,
  as fixed by [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchor:** [A132/B171](sources/kant/critique-a.md#a132).

### Apperception (*Apperzeption*)

- **Textual sense:** Self-consciousness; in its original or transcendental
  unity, the condition under which the "I think" can accompany representations
  and a manifold can belong to one consciousness.
- **Kantbot role:** A unity constraint requiring a judgment and its grounds to
  belong to one coherent cognitive state and trace.
- **Not equivalent to:** Machine consciousness, a user account, object identity,
  or a globally unique process ID.
- **Status:** **Analogical**; **Foundation**. Kantbot models the cycle-wide
  provenance and scope check fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md), without
  treating it as proof of self-consciousness.
- **Primary anchors:** [B131-136](sources/kant/deduction-b.md#b131).

### Reason (*Vernunft*)

- **Textual sense:** The faculty of principles and inference that seeks the
  unconditioned and systematic unity of cognition.
- **Kantbot role:** A later role that links judgments into inferences and uses
  regulative goals while preserving the experiential conditions of its claims.
- **Not equivalent to:** The whole cognitive system, generic logical
  correctness, or a license to convert explanatory ideals into known objects.
- **Status:** **Analogical**; **Deferred** to Phase 4.
- **Primary anchors:** [A299-302/B355-359](sources/kant/critique-a.md#a299); [A307/B364](sources/kant/critique-a.md#a307).

## Representations and organization

### Representation (*Vorstellung*)

- **Textual sense:** The most general term in Kant's hierarchy for a mental
  item; intuitions and concepts are different kinds of representation.
- **Kantbot role:** The general family of typed cognitive states produced or
  transformed inside the model.
- **Not equivalent to:** Any arbitrary datum, its external referent, or one
  fixed vector format.
- **Status:** **Analogical**; **Foundation**.
- **Primary anchor:** [A320/B376-377](sources/kant/critique-a.md#a320).

### Manifold (*Mannigfaltige*)

- **Textual sense:** The plurality given in intuition that must be combined for
  cognition of an object.
- **Kantbot role:** In the accepted Kantian variant, a bounded and ordered
  plurality of intuitions made available to synthesis through successful
  variant projections.
- **Not equivalent to:** An already identified object's attributes, a bag of
  facts, or raw data with no form of presentation.
- **Status:** **Interpretive / Analogical**; **Foundation**. Its boundaries,
  ordering, and projection grounds must be visible in the trace; shared
  presented elements do not constitute it automatically.
- **Primary anchors:** [A77/B102](sources/kant/critique-a.md#a77); [B129-130](sources/kant/deduction-b.md#b129).

### Intuition (*Anschauung*)

- **Textual sense:** An immediate, singular representation through which an
  object is given, contrasted with the mediate and general representation of a
  concept.
- **Kantbot role:** The structured presentation of particular content to the
  cognitive cycle before it is determined as an object under concepts.
- **Not equivalent to:** A hunch, an unexplained model output, a mental image,
  or simply one row of input data.
- **Status:** **Interpretive / Analogical**; **Foundation** within the accepted
  Kantian variant. [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md)
  makes this theory-internal terminology for an explicit projection from a
  shared presented element, not a label applied at the shared boundary.
- **Primary anchors:** [A19/B33](sources/kant/critique-a.md#a19); [A50/B74](sources/kant/critique-a.md#a50); [A68/B93](sources/kant/critique-a.md#a68).

### Empirical intuition (*empirische Anschauung*)

- **Textual sense:** Intuition related to an object through sensation.
- **Kantbot role:** A particular presentation whose content depends on a
  recorded observation rather than solely on the model's ordering constraints.
- **Not equivalent to:** A verified fact or a fully recognized empirical
  object.
- **Status:** **Interpretive / Analogical**; **Foundation** within the accepted
  Kantian variant under
  [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md). The
  first model records observation-dependent content but must declare that it
  does not yet reproduce human sensation.
- **Primary anchor:** [A20/B34](sources/kant/critique-a.md#a20).

### Pure intuition (*reine Anschauung*)

- **Textual sense:** The form of sensibility considered without sensation;
  space and time are Kant's pure forms of sensible intuition.
- **Kantbot role:** A configured form that constrains how observations may be
  presented and related before concept application.
- **Not equivalent to:** Synthetic training data, a blank record, or arbitrary
  prior knowledge.
- **Status:** **Interpretive / Analogical**; **Foundation** within the accepted
  Kantian variant under
  [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md).
- **Primary anchors:** [A20-22/B34-36](sources/kant/critique-a.md#a20); [A30-32/B46-49](sources/kant/critique-a.md#a30).

### Space and time (*Raum und Zeit*)

- **Textual sense:** The pure forms of outer and inner intuition respectively,
  conditioning how appearances can be given.
- **Kantbot role:** Explicit ordering constraints for a toy world—at minimum,
  temporal succession; spatial relations only where the chosen world requires
  them.
- **Not equivalent to:** Database coordinates and timestamps merely because
  those fields happen to exist.
- **Status:** **Interpretive / Analogical**; **Foundation** as ordering
  constraints. Under
  [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md), the
  accepted Kantian variant treats them as its declared sensible form while
  recording the limits of the computational realization.
- **Primary anchors:** [A22-25/B37-41](sources/kant/critique-a.md#a22); [A30-32/B46-49](sources/kant/critique-a.md#a30).

### Appearance (*Erscheinung*)

- **Textual sense:** The indeterminate object of an empirical intuition; its
  matter corresponds to sensation and its form orders the manifold.
- **Kantbot role:** Presented content insofar as it can be synthesized and
  determined as an object within the model's conditions of presentation.
- **Not equivalent to:** A deceptive look, an external thing as it is in itself,
  or every unprocessed input value.
- **Status:** **Interpretive / Analogical**; **Decision required**. ADR 0001
  does not decide whether the accepted Kantian variant should name this
  pre-object content an appearance.
- **Primary anchor:** [A20/B34](sources/kant/critique-a.md#a20).

### Object of experience (*Gegenstand der Erfahrung*)

- **Textual sense:** An object cognized through the lawful synthesis of
  appearances in possible experience, rather than something known apart from
  the conditions of experience.
- **Kantbot role:** A stable candidate whose identity and properties are
  licensed by synthesis, applicable concepts, and the model's unity conditions.
- **Not equivalent to:** A record created by the program, an external entity in
  itself, or any cluster that crosses a similarity threshold.
- **Status:** **Interpretive / Analogical**; **Foundation**. Testable identity,
  constitutive-unity, applicability, and unity-check criteria are fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchors:** [B137](sources/kant/deduction-b.md#b137); [B146-148](sources/kant/deduction-b.md#b146); [A93/B126](sources/kant/critique-a.md#a93).

### Concept (*Begriff*)

- **Textual sense:** A mediate, general representation that can apply to many
  representations and function as a predicate in judgment.
- **Kantbot role:** An explicit set of applicability conditions and inferential
  consequences by which representations may be organized.
- **Not equivalent to:** A string label, an embedding, a class in source code,
  or a detected object type by itself.
- **Status:** **Analogical**; **Foundation**. The representation must expose what
  licenses and follows from application.
- **Primary anchors:** [A68-69/B93-94](sources/kant/critique-a.md#a68); [A320/B377](sources/kant/critique-a.md#a320).

### Empirical concept (*empirischer Begriff*)

- **Textual sense:** A concept whose content arises through reflection on and
  comparison of experience rather than being supplied a priori.
- **Kantbot role:** A concept whose applicability criteria are derived or
  revised from observation histories within declared learning rules.
- **Not equivalent to:** Any user-defined label or any statistically learned
  feature.
- **Status:** **Analogical**; **Decision required**. Concept acquisition may be
  deferred even if applying fixed empirical concepts is foundational.
- **Primary anchors:** [A220/B267](sources/kant/critique-a.md#a220); compare [A50-51/B74-75](sources/kant/critique-a.md#a50).

### Pure concept of the understanding / category (*Kategorie*)

- **Textual sense:** An a priori concept through which the understanding thinks
  the manifold of intuition and which has objective validity only under the
  conditions established in the deduction.
- **Kantbot role:** A candidate family of constitutive constraints on how
  synthesized representations may count as objects and enter judgments.
- **Not equivalent to:** A taxonomy label, database category, or universally
  valid rule merely declared by the implementation.
- **Status:** **Interpretive / Analogical**; **Foundation**. The minimal
  category-inspired constraints fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md) cover
  unity/plurality, persistence, and lawful succession only where needed; they
  do not implement all twelve categories.
- **Primary anchors:** [A79-83/B104-116](sources/kant/critique-a.md#a79); [B129-169](sources/kant/deduction-b.md#b129).

### Schema (*Schema*)

- **Textual sense:** A rule or procedural representation mediating between a
  concept and sensible intuition; transcendental schemata are determinations of
  time that make categories applicable to appearances.
- **Kantbot role:** An explicit, inspectable applicability procedure mediating
  between a concept or category and a temporally structured representation.
- **Not equivalent to:** A database schema, a static template, a prototype
  image, or an arbitrary feature extractor.
- **Status:** **Interpretive / Analogical**; **Foundation** as fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchors:** [A137-142/B176-181](sources/kant/critique-a.md#a137).

### Rule (*Regel*)

- **Textual sense:** A representation of a universal condition under which a
  manifold can be brought into unity; the understanding is characterized as a
  faculty of rules.
- **Kantbot role:** A declarative or executable condition whose inputs, scope,
  result, and authority are inspectable.
- **Not equivalent to:** Any line of program logic or an exception-free law of
  the external world.
- **Status:** **Analogical**; **Foundation**. Rule authority follows
  [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md).
- **Primary anchors:** [A69/B94](sources/kant/critique-a.md#a69); [A126](sources/kant/deduction-a.md#a126); [A132/B171](sources/kant/critique-a.md#a132).

## Operations

### Synthesis (*Synthesis*)

- **Textual sense:** The act of putting different representations together and
  comprehending their manifoldness in one cognition.
- **Kantbot role:** A provenance-preserving transformation that combines and
  retains elements of a manifold to produce a candidate representation.
- **Not equivalent to:** Concatenation, aggregation, clustering, or data fusion
  unless the operation performs the declared unifying role.
- **Status:** **Analogical**; **Foundation**.
- **Primary anchors:** [A77-78/B102-104](sources/kant/critique-a.md#a77).

### Synthesis of apprehension in intuition

- **Textual sense:** The successive running through and taking together of a
  manifold so that it can be represented as a unity in intuition.
- **Kantbot role:** A possible reception-stage operation that segments and
  orders presented elements into a sequence available for retention.
- **Not equivalent to:** Input validation or parsing alone.
- **Status:** **Interpretive / Analogical**; **Foundation** in the A/B hybrid
  default fixed by [ADR 0002](docs/decisions/0002-a-b-synthesis.md). This
  threefold account is especially prominent in the A-edition deduction.
- **Primary anchor:** [A98-100](sources/kant/deduction-a.md#a98).

### Synthesis of reproduction in imagination

- **Textual sense:** The reproduction of prior representations according to
  rules of association so that they can be combined with present ones.
- **Kantbot role:** A possible retention operation that makes relevant earlier
  presentations available during synthesis of a sequence.
- **Not equivalent to:** Exact record replay, unrestricted memory retrieval, or
  probabilistic association by itself.
- **Status:** **Interpretive / Analogical**; **Foundation** in the A/B hybrid
  default fixed by [ADR 0002](docs/decisions/0002-a-b-synthesis.md).
- **Primary anchors:** [A100-102](sources/kant/deduction-a.md#a100); compare [B151-152](sources/kant/deduction-b.md#b151).

### Synthesis of recognition in a concept

- **Textual sense:** Consciousness that what is being thought now is the same
  combination being successively produced, enabling cognition under a concept.
- **Kantbot role:** A possible identity-and-unity operation that treats retained
  elements as belonging to one candidate and makes conceptual determination
  possible.
- **Not equivalent to:** Classification accuracy or object tracking alone.
- **Status:** **Interpretive / Analogical**; **Foundation** in the A/B hybrid
  default fixed by [ADR 0002](docs/decisions/0002-a-b-synthesis.md).
- **Primary anchors:** [A103-110](sources/kant/deduction-a.md#a103).

### Schematism (*Schematismus*)

- **Textual sense:** The procedure by which the imagination supplies schemata,
  mediating the application of concepts—especially categories—to appearances.
- **Kantbot role:** The process that runs a schema against a synthesized,
  temporally ordered representation and records why application succeeds,
  fails, or remains ambiguous.
- **Not equivalent to:** Schema validation or ordinary pattern matching without
  a mediating architectural role.
- **Status:** **Interpretive / Analogical**; **Foundation** as fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchors:** [A137-147/B176-187](sources/kant/critique-a.md#a137).

### Concept application / subsumption

- **Textual sense:** Bringing a particular under a general concept or rule;
  subsumption is the characteristic task of the power of judgment.
- **Kantbot role:** A testable operation that returns its candidate concept,
  satisfied and unsatisfied conditions, alternatives, and scope.
- **Not equivalent to:** Attaching the highest-scoring label regardless of
  whether its applicability conditions are met.
- **Status:** **Analogical** with a close textual anchor; **Foundation**.
- **Primary anchors:** [A68/B93](sources/kant/critique-a.md#a68); [A132/B171](sources/kant/critique-a.md#a132).

### Judgment (*Urteil*)

- **Textual sense:** A mediate cognition of an object—a representation of a
  representation—and the act by which representations are brought to the
  objective unity of apperception.
- **Kantbot role:** A structured proposition formed only when its required
  presentation, synthesis, concept-application, and unity conditions are met.
- **Not equivalent to:** The faculty called the power of judgment, any emitted
  sentence, a confidence score, or a moral verdict.
- **Status:** **Analogical**; **Foundation**.
- **Primary anchors:** [A68-69/B93-94](sources/kant/critique-a.md#a68); [B140-142](sources/kant/deduction-b.md#b140).

### Inference (*Schluss*)

- **Textual sense:** The cognition of the necessity of a proposition through
  its relation to other judgments; reason is the faculty of inference.
- **Kantbot role:** A traceable transition from judgments to another judgment,
  preserving premises, rules, experiential conditions, and claim status.
- **Not equivalent to:** Every internal computation or unconstrained generation
  of a plausible conclusion.
- **Status:** **Analogical**; **Deferred** to Phase 4.
- **Primary anchors:** [A303-304/B359-361](sources/kant/critique-a.md#a303).

## Categories and forms of judgment

The two tables below record Kant's architecturally relevant pairing. They do
not imply that Kantbot has adopted Kant's derivation of the categories, that
the tables are interchangeable, or that all twelve categories will appear in
the first model.

| Heading | Forms/functions of judgment | Categories |
| --- | --- | --- |
| Quantity | Universal, particular, singular | Unity, plurality, totality |
| Quality | Affirmative, negative, infinite | Reality, negation, limitation |
| Relation | Categorical, hypothetical, disjunctive | Inherence and subsistence (substance and accident), causality and dependence (cause and effect), community (reciprocity) |
| Modality | Problematical, assertoric, apodictic | Possibility/impossibility, existence/non-existence, necessity/contingency |

- **Forms/functions of judgment:** Logical functions by which the understanding
  unifies representations in judgments. They are not output formats.
- **Categories:** Pure concepts corresponding to those functions and directed
  toward objects of intuition in general. They are not a domain taxonomy.
- **Kantbot status:** **Interpretive / Analogical**; **Foundation** under
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md). Any adopted
  category-inspired constraint must alter behavior, not merely rename a
  familiar operation.
- **Primary anchors:** [A70-76/B95-101](sources/kant/critique-a.md#a70); [A79-83/B104-116](sources/kant/critique-a.md#a79).

## Epistemic status and limits

### Cognition (*Erkenntnis*)

- **Textual sense:** An objective representation; cognition is either intuition
  or concept and purports to relate to an object.
- **Kantbot role:** A representation with a licensed relation to an object
  within the model's declared conditions, rather than merely an internal state.
- **Not equivalent to:** Stored information, successful prediction, or any
  representation the system happens to produce.
- **Status:** **Interpretive / Analogical**; **Decision required**.
- **Primary anchor:** [A320/B376-377](sources/kant/critique-a.md#a320).

### Experience (*Erfahrung*)

- **Textual sense:** Empirical cognition produced through the synthetic unity
  of perceptions under rules, not a mere aggregate of sensations.
- **Kantbot role:** A coherent sequence of observation-grounded cognitions whose
  connections satisfy the model's constitutive constraints.
- **Not equivalent to:** A dataset, execution history, or isolated observation.
- **Status:** **Analogical**; **Decision required**.
- **Primary anchors:** [B147](sources/kant/deduction-b.md#b146); [A176/B218](sources/kant/critique-a.md#a176); [A189/B232](sources/kant/critique-a.md#a189).

### Objective validity (*objektive Gültigkeit*)

- **Textual sense:** The legitimate relation of a representation, concept, or
  judgment to an object, as distinct from merely subjective association.
- **Kantbot role:** The status of a claim whose declared object-directed
  conditions and scope have been satisfied within the model.
- **Not equivalent to:** High confidence, majority agreement, factual truth in
  every possible context, or successful execution.
- **Status:** **Interpretive / Analogical**; **Foundation**. Its initial test is
  the combined licensing and unity check fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchors:** [A89-90/B122-123](sources/kant/critique-a.md#a89); [B140-142](sources/kant/deduction-b.md#b140).

### Objective unity

- **Textual sense:** Unity of representations in the transcendental unity of
  apperception according to rules, contrasted with merely subjective
  association.
- **Kantbot role:** The constraint that representations combined in a judgment
  must be attributable to one coherent state under shared rules.
- **Not equivalent to:** Deduplication, internal consistency alone, or a single
  memory address.
- **Status:** **Analogical**; **Foundation**. The cycle-wide provenance and
  scope test is fixed by
  [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md).
- **Primary anchors:** [B139-142](sources/kant/deduction-b.md#b139).

### A priori / a posteriori

- **Textual sense:** A priori cognition is independent of experience in its
  justification; a posteriori cognition has its source in experience.
- **Kantbot role:** Metadata distinguishing constraints supplied as conditions
  of the model from claims derived from observation histories.
- **Not equivalent to:** Hard-coded versus dynamically loaded, or old versus new
  data. A hard-coded empirical rule does not thereby become a priori.
- **Status:** **Analogical**; **Decision required**.
- **Primary anchors:** [B1-5](sources/kant/second-edition-excerpts.md#b1).

### Empirical / transcendental

- **Textual sense:** Empirical cognition concerns objects through experience;
  transcendental cognition concerns our mode of cognizing objects insofar as
  that mode is possible a priori.
- **Kantbot role:** A distinction between observation-dependent content and
  inquiry into the model's conditions for presenting, synthesizing, and judging
  such content.
- **Not equivalent to:** Runtime versus configuration, physical versus virtual,
  or ordinary versus mystical. "Transcendental" does not mean "transcendent."
- **Status:** **Analogical**; **Context only**, but required when stating claims
  about the architecture.
- **Primary anchors:** [A11-12/B25](sources/kant/critique-a.md#a11); [A56/B80](sources/kant/critique-a.md#a56).

### Analytic / synthetic judgment

- **Textual sense:** An analytic judgment explicates what is already contained
  in the subject concept; a synthetic judgment adds a predicate not so
  contained and connects representations.
- **Kantbot role:** A possible classification of why a judgment is licensed:
  concept-explication versus a connection requiring grounds beyond containment.
- **Not equivalent to:** Deductive versus probabilistic, cached versus newly
  computed, or true by definition versus empirically true without qualification.
- **Status:** **Interpretive / Analogical**; **Context only** for the first cycle.
- **Primary anchors:** [A6-10/B10-14](sources/kant/critique-a.md#a6).

### Constitutive / regulative use

- **Textual sense:** Constitutive principles determine objects of possible
  experience; regulative principles guide inquiry toward systematic unity
  without constituting corresponding objects as known.
- **Kantbot role:** A mandatory status distinction between rules that license
  object-level judgments and goals that guide search, comparison, or unification
  without adding known objects.
- **Not equivalent to:** Required versus optional configuration, or enforced
  versus advisory lint rules.
- **Status:** **Interpretive / Analogical**; the authority distinction is
  **Foundation** under
  [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md), while
  active regulative reasoning is **Deferred** to Phase 4.
- **Primary anchors:** [A179-180/B222-223](sources/kant/critique-a.md#a179); [A509-515/B537-543](sources/kant/critique-a.md#a509); [A642-668/B670-696](sources/kant/critique-a.md#a642).

### Phenomenon / noumenon (*Phaenomenon / Noumenon*)

- **Textual sense:** A phenomenon is an appearance considered as an object under
  the unity of the categories; a noumenon is a problematic thought of an object
  not given to sensible intuition, not an object available to theoretical
  knowledge.
- **Kantbot role:** A boundary marker between objects licensed under the model's
  conditions of presentation and merely thinkable supposed objects outside
  those conditions.
- **Not equivalent to:** Visible versus hidden data, public versus private
  state, or known versus merely unknown database records.
- **Status:** **Interpretive**; **Context only** for overreach detection.
- **Primary anchors:** [A235-260/B294-315](sources/kant/critique-a.md#a235).

### Thing in itself (*Ding an sich selbst*)

- **Textual sense:** A thing considered independently of the conditions under
  which it appears to us; not thereby an object of possible sensible cognition.
- **Kantbot role:** A limit concept warning that the model's object
  representations do not amount to unrestricted access to what exists
  independently of its presentation conditions.
- **Not equivalent to:** Ground-truth labels, hidden state in the toy world, or
  the source object before serialization.
- **Status:** **Interpretive**; **Context only**.
- **Primary anchors:** [A30/B45](sources/kant/critique-a.md#a30); [A249-252](sources/kant/critique-a.md#a249); [B306-309](sources/kant/second-edition-excerpts.md#b306).

### Idea of reason (*Idee*)

- **Textual sense:** A concept of reason directed toward an unconditioned
  totality for which no adequate corresponding object can be given in sensible
  experience.
- **Kantbot role:** A candidate regulative representation that directs inquiry
  or organization without being reported as an observed or constituted object.
- **Not equivalent to:** Any goal, hypothesis, latent variable, or generated
  idea.
- **Status:** **Analogical**; **Deferred** to Phase 4.
- **Primary anchors:** [A311-320/B367-377](sources/kant/critique-a.md#a311).

### Transcendental illusion (*transzendentaler Schein*)

- **Textual sense:** The persistent tendency to treat subjective principles of
  reason as objectively determining things beyond possible experience.
- **Kantbot role:** A failure class in which a regulative goal or inference is
  promoted to an object-level claim without the required experiential grounds.
- **Not equivalent to:** Hallucination in general, low confidence, a software
  bug, or any false statement.
- **Status:** **Analogical**; **Deferred** to Phase 4, but used now to define a
  principal kind of overreach.
- **Primary anchors:** [A293-298/B349-355](sources/kant/critique-a.md#a293).

### Warrant

- **Textual sense:** This is project vocabulary, not a claim about one uniquely
  Kantian technical term. It names the grounds and conditions licensing a
  judgment or inference.
- **Kantbot role:** Structured evidence linking an output to observations,
  transformations, applicable concepts, rules, scope, and unresolved limits.
- **Not equivalent to:** Confidence, explanation text generated after the fact,
  or proof of truth outside the toy world's declared conditions.
- **Status:** **Engineering**, informed by Kantian questions of objective validity;
  **Foundation**.
- **Primary anchors:** No single textual equivalent; compare [B137-142](sources/kant/deduction-b.md#b137) and
  [A89-90/B122-123](sources/kant/critique-a.md#a89).

## Kantbot implementation vocabulary

The terms in this section are explicitly computational. They must not acquire
Kantian authority merely by appearing near Kantian concepts.

### Observation

A typed, immutable record of something presented by the toy world's input
boundary, including source and ordering metadata. An observation supplies
content to reception; it is not by itself an intuition, appearance, fact, or
object. **Claim label: Engineering.**

### Input

The serialized material accepted by an interface. Parsing input may produce
observations, but the transport format has no cognitive status of its own.
**Claim label: Engineering.**

### Presented element

A minimal shared-boundary representation derived from an observation. It keeps
source, episode, ordering, and provenance identity available for comparison but
has no licensed object identity, concept, or variant-specific cognitive status.
It is not automatically an intuition. **Claim label: Engineering.**

### Variant projection

An explicit transformation from shared presented elements into the
representations required by one declared philosophical architecture. It must
add or validate variant-specific structure, invariants, and behavioral
conditions; changing only a type or display label does not count. The accepted
Kantian projection produces intuitions under its sensibility and form criteria.
**Claim label: Engineering and interpretive.**

### Cognitive state

The versioned collection of representations, transformations, applicable
constraints, and open conflicts available during one cognitive cycle. It is a
functional unit of inspection, not a claim that the program is conscious.
**Claim label: Engineering.**

### Synthesized representation

The explicit result of a synthesis operation, retaining links to every source
element and transformation. It may support a candidate object or event but is
not automatically a cognition or judgment. **Claim label: Engineering and
analogical.**

### Candidate object or event

A provisional unity proposed by synthesis and awaiting concept application and
unity checks. "Candidate" prevents the program from treating every cluster or
sequence as an already constituted object. **Claim label: Engineering.**

### Confidence

A quantitative or ordinal estimate attached to an operation or candidate. It
must remain distinct from objective validity and warrant: high confidence does
not license a claim whose constitutive conditions are absent. **Claim label:
Engineering.**

### Uncertainty

A represented lack of determinacy among alternatives or about an operation's
result. It should identify what remains unresolved; it is not a catch-all for
failed synthesis, conflict, or overreach. **Claim label: Engineering.**

### Provenance / trace

The machine-readable history of what was presented, which transformations were
performed, which rules were considered, and why an output was formed or
withheld. A trace is evidence for auditing a warrant, not itself a philosophical
justification. **Claim label: Engineering.**

### Conflict

A state in which concurrently relevant representations, rules, or judgments
cannot all be maintained under declared constraints. Conflict is reported as a
first-class result rather than silently resolved. **Claim label: Engineering.**

### Failed synthesis

A result in which the manifold cannot be combined into the requested candidate
unity under the selected synthesis policy. It is not equivalent to malformed
input or low confidence. **Claim label: Engineering and analogical.**

### Failed concept application

A result in which no candidate concept satisfies its declared applicability
conditions, or in which multiple applications remain unresolved. It should
preserve rejected alternatives and reasons. **Claim label: Engineering and
analogical.**

### Overreach

A claim or inference that exceeds the scope of its warrant—for example, by
treating a regulative goal as constitutive or by discarding required links to
conditions of presentation. Overreach is broader than simple factual error.
**Claim label: Engineering and analogical.**

### Policy / architectural variant

An explicit, replaceable implementation of a disputed operation or
philosophical assumption. Variants must declare their claim labels and should
be compared through behavior and traces, not only through terminology.
**Claim label: Engineering.**

## Phase 1 glossary decisions

The glossary keeps both the remaining disagreement and accepted answers
visible:

1. **Accepted:** [ADR 0001](docs/decisions/0001-variant-scoped-receptive-terminology.md)
   preserves a minimal shared presented-element boundary and requires explicit
   variant projections; the accepted Kantian variant uses `intuition`
   theory-internally.
2. **Accepted:** [ADR 0002](docs/decisions/0002-a-b-synthesis.md) uses
   apprehension, reproduction, and recognition in an A/B hybrid default, with
   a behaviorally meaningful B-led variant.
3. **Accepted:** [ADR 0003](docs/decisions/0003-object-and-judgment-licensing.md)
   fixes the minimal category-inspired constraints, schematized applicability,
   power-of-judgment role, and cycle-wide unity check.
4. **Accepted:** [ADR 0004](docs/decisions/0004-limit-outcomes-and-rule-authority.md)
   distinguishes constitutive, regulative, and engineering rule authority and
   the initial typed limit outcomes.
5. **Deferred:** reason's active regulative inquiry and transcendental overreach
   remain Phase 4 work even though their reserved rule and outcome fields are
   constrained by ADR 0004.

## Editorial rule

New philosophical terms should be added only when they constrain data flow,
operations, invariants, observable behavior, or the scope of a claim. Every new
computational analogy must state where it departs from or underdetermines the
textual concept. Terms used only for historical context may be added, but must
remain marked **Context only** so that the glossary does not silently expand
the implementation scope.
