# Primary-Source Map

## Purpose

This map connects the initial Kantbot architecture questions to passages in
Kant's *Critique of Pure Reason*. It is an index for specification and decision
work, not a substitute for interpretation. Each entry identifies what a passage
can constrain, which edition matters, and where a later decision must go beyond
what the text alone settles.

Use this map when writing a claim, specification, or decision record:

1. follow the linked passage and read enough surrounding context;
2. retain its standard A/B citation in the resulting document;
3. state whether the resulting claim is textual, interpretive, analogical, or
   engineering; and
4. name the edition when a difference between A and B affects the claim.

Definitions and provisional computational interpretations remain in the
[glossary](GLOSSARY.md). Edition provenance and transcription limitations are
documented with the [local source texts](sources/kant/README.md).

## Local source inventory

| Local text | Coverage | Best use |
| --- | --- | --- |
| [First-edition text](sources/kant/critique-a.md) | A1-A856, except seven page boundaries absent from the digital source | Shared A/B passages and material outside the deductions |
| [A Deduction](sources/kant/deduction-a.md) | A95-A130 | The threefold synthesis, imagination, apperception, and the subjective grounds of experience |
| [B Deduction](sources/kant/deduction-b.md) | B129-B169 | Objective unity, judgment, category application, and the conditions of experience |
| [Second-edition excerpts](sources/kant/second-edition-excerpts.md) | B1-5 and B294-315 | The B introduction and the revised discussion of phenomena and noumena |

For paired citations such as A19/B33, the local link normally opens the A text.
The citation still records the corresponding B location. The two deductions are
kept separate because Kant substantially rewrote the argument rather than
merely correcting its wording.

## Core reading path for the initial architecture

The following sequence moves from what is given to the limits of legitimate
cognition. It is the minimum primary-source packet for Phase 1.

| Order | Topic | Passages | What to extract |
| --- | --- | --- | --- |
| 1 | Sensibility and intuition | [A19-25/B33-41](sources/kant/critique-a.md#a19), [A30-32/B46-49](sources/kant/critique-a.md#a30) | Affecting, sensation, empirical intuition, appearance, and the forms under which objects can be given |
| 2 | Understanding and judgment | [A50-51/B74-75](sources/kant/critique-a.md#a50), [A68-76/B93-101](sources/kant/critique-a.md#a68) | Receptivity versus spontaneity, concepts as functions, and judgment as the mediate use of representations |
| 3 | Synthesis and categories | [A77-83/B102-116](sources/kant/critique-a.md#a77) | The manifold, synthesis, imagination, conceptual unity, and the table of categories |
| 4 | Need for a deduction | [A84-95/B116-129](sources/kant/critique-a.md#a84) | Why concepts not derived from experience require a justification of their objective validity and limits |
| 5 | A-edition deduction | [A95-130](sources/kant/deduction-a.md#a95) | Apprehension, reproduction, recognition, transcendental imagination, apperception, and the subjective grounds of experience |
| 6 | B-edition deduction | [B129-169](sources/kant/deduction-b.md#b129) | Original apperception, objective unity, judgment, category application, imagination, and the restriction to possible experience |
| 7 | Judgment and schematism | [A132/B171](sources/kant/critique-a.md#a132), [A137-147/B176-187](sources/kant/critique-a.md#a137) | Subsumption, schemata, time determination, and mediation between categories and appearances |
| 8 | Experience and objective use | [A176/B218](sources/kant/critique-a.md#a176), [A189/B232](sources/kant/critique-a.md#a189), [A220/B267](sources/kant/critique-a.md#a220) | Conditions under which concepts and principles acquire objective reality in possible experience |
| 9 | Cognitive limits | [A235-260/B294-315](sources/kant/critique-a.md#a235), [B306-309](sources/kant/second-edition-excerpts.md#b306) | Phenomena, noumena, things in themselves, empty concepts, and the boundary of category use |

## Architecture questions and controlling passages

### What is presented to the model?

| Question | Primary passages | Constraint supplied by the text | What remains a project decision |
| --- | --- | --- | --- |
| What counts as being given? | [A19-20/B33-34](sources/kant/critique-a.md#a19) | Sensibility is receptive; intuition is the immediate way an object is given | Whether structured program input is a strong analogy to intuition or should be called constrained presentation |
| What is a manifold? | [A77-79/B102-104](sources/kant/critique-a.md#a77) | A manifold is supplied for synthesis and does not organize itself into cognition | Its computational boundaries, granularity, and temporal extent |
| What makes an intuition empirical? | [A20/B34](sources/kant/critique-a.md#a20) | Empirical intuition includes sensation and presents an appearance | Whether the toy world models anything analogous to affection or sensation |
| What role do space and time play? | [A22-25/B37-41](sources/kant/critique-a.md#a22), [A30-32/B46-49](sources/kant/critique-a.md#a30) | They are forms of sensible intuition rather than empirical properties abstracted from objects | Whether the first model implements spatial form, temporal form, both, or a weaker ordering constraint |

### How does a candidate object become possible?

| Question | Primary passages | Constraint supplied by the text | What remains a project decision |
| --- | --- | --- | --- |
| Why is synthesis required? | [A77-83/B102-116](sources/kant/critique-a.md#a77) | Cognition requires putting a manifold together and representing its unity | Which transformations count as synthesis rather than ordinary aggregation |
| Should synthesis have three stages? | [A98-110](sources/kant/deduction-a.md#a98) | The A Deduction distinguishes apprehension, reproduction, and recognition | Whether this becomes the default architecture or an explicit A-edition variant |
| What does imagination contribute? | [A120-126](sources/kant/deduction-a.md#a120), [B151-152](sources/kant/deduction-b.md#b151) | Imagination synthesizes the sensible manifold and mediates sensibility and understanding | Whether it is a component, an operation shared across stages, or a family of policies |
| What makes the result an object rather than a bundle? | [A103-110](sources/kant/deduction-a.md#a103), [B137-142](sources/kant/deduction-b.md#b137) | Object relation requires rule-governed unity rather than arbitrary association | The executable identity and unity tests for candidate objects or events |

### What licenses concepts and judgments?

| Question | Primary passages | Constraint supplied by the text | What remains a project decision |
| --- | --- | --- | --- |
| What is the understanding's role? | [A68-69/B93-94](sources/kant/critique-a.md#a68) | Understanding is discursive, works through concepts, and is characterized through judgment | Its software boundary relative to imagination and judgment |
| What is a category? | [A79-83/B104-116](sources/kant/critique-a.md#a79), [B143-146](sources/kant/deduction-b.md#b143) | Categories are pure functions of unity that condition the synthesis of sensible intuitions | Which, if any, must be implemented and what behavior distinguishes them from generic rules |
| Why do categories require a deduction? | [A84-95/B116-129](sources/kant/critique-a.md#a84) | A priori concepts require a justification of their objective validity and legitimate range | What evidence warrants each adopted category or category-like constraint in the model |
| What is a judgment? | [A68-70/B93-95](sources/kant/critique-a.md#a68), [B140-142](sources/kant/deduction-b.md#b140) | Judgment relates cognitions through the objective unity of apperception | Whether judgment is a distinct component, an interface, or the result of concept application |
| How are concepts applied to appearances? | [A132/B171](sources/kant/critique-a.md#a132), [A137-147/B176-187](sources/kant/critique-a.md#a137) | Schematism supplies a mediating procedure and restricts categories to sensible conditions | What an inspectable schema is and which applicability failures it must expose |

### What makes cognition objectively valid?

| Question | Primary passages | Constraint supplied by the text | What remains a project decision |
| --- | --- | --- | --- |
| What is the unity of apperception? | [A107-110](sources/kant/deduction-a.md#a107), [B131-136](sources/kant/deduction-b.md#b131) | Representations must be combinable in one self-consciousness for cognition | What functional unity can be modeled without implying consciousness or a metaphysical self |
| What is objective unity? | [B137-142](sources/kant/deduction-b.md#b137) | Objective validity depends on necessary unity in synthesis, not contingent association | The test by which a trace demonstrates more than internal consistency |
| Why do categories apply to experience? | [B143-148](sources/kant/deduction-b.md#b143), [B159-169](sources/kant/deduction-b.md#b159) | Their legitimate use is tied to objects of possible sensible experience | What counts as the toy world's analogue of possible experience |
| What is cognition rather than thought alone? | [B146-148](sources/kant/deduction-b.md#b146), [A220/B267](sources/kant/critique-a.md#a220) | A concept without a corresponding intuition may be thinkable but does not thereby yield cognition of an object | How the system distinguishes a candidate, a thought, a judgment, and a licensed object claim |

### Where must the system stop?

| Question | Primary passages | Constraint supplied by the text | What remains a project decision |
| --- | --- | --- | --- |
| What is the boundary of possible cognition? | [B146-169](sources/kant/deduction-b.md#b146), [A235-260/B294-315](sources/kant/critique-a.md#a235) | Categories yield cognition only under conditions in which an object can be given | Which missing conditions cause refusal rather than uncertainty or low confidence |
| What is a noumenon or thing in itself doing here? | [A249-260](sources/kant/critique-a.md#a249), [B306-309](sources/kant/second-edition-excerpts.md#b306) | These concepts mark limits; they do not license positive cognition outside sensible intuition | How to represent a boundary without inventing hidden ground-truth objects |
| What is transcendental illusion? | [A293-298/B349-355](sources/kant/critique-a.md#a293), [A311-320/B367-377](sources/kant/critique-a.md#a311) | Reason is naturally drawn toward claims exceeding possible experience | Which executable failures genuinely model overreach rather than ordinary error |
| What is constitutive rather than regulative? | [A179-180/B222-223](sources/kant/critique-a.md#a179), [A509-515/B537-543](sources/kant/critique-a.md#a509) | Constitutive principles determine objects of experience; regulative principles direct inquiry without constituting an object | How rules declare their authority and how traces prevent regulative aims from becoming object claims |

## Edition-sensitive fault lines

These are the places where Phase 1 must make a visible choice instead of citing
"Kant" as if the text supplied one uncontested architecture.

1. **Threefold synthesis:** apprehension, reproduction, and recognition organize
   the A Deduction, but the B Deduction does not preserve that architecture in
   the same form.
2. **Imagination and understanding:** the editions emphasize their relationship
   differently. Component boundaries must therefore be presented as an
   interpretation, not a direct transcription of faculty names.
3. **Apperception:** the A Deduction develops it through the subjective sources
   of experience; the B Deduction foregrounds the objective unity expressed by
   the "I think." A computational unity check cannot simply inherit the name.
4. **Objective validity:** the B Deduction offers the sharper route from
   apperception through judgment and the categories to possible experience.
   The A account remains relevant where the project models synthesis and
   imagination.
5. **Noumena:** the B-edition revisions sharpen distinctions among negative and
   positive senses and the limits of category use. Claims about cognitive
   boundaries should check the B material rather than relying on the A wording
   alone.

The default Phase 1 reading should use both deductions: the A text for its
analysis of synthesis and the B text for its account of objective unity and
category application. If their different emphases produce different executable
behavior, the alternatives should become named architectural variants.

## Deferred but relevant sources

These passages belong to the source map because they constrain later phases,
but they should not expand the first cognitive cycle prematurely.

| Later concern | Passages | Planned use |
| --- | --- | --- |
| Reason and inference | [A299-304/B355-361](sources/kant/critique-a.md#a299) | Phase 4 chains of inference and the distinction between understanding and reason |
| Ideas and the unconditioned | [A311-320/B367-377](sources/kant/critique-a.md#a311) | Phase 4 regulative goals and overreach |
| Regulative inquiry | [A509-515/B537-543](sources/kant/critique-a.md#a509) | Phase 4 rules that guide continuation without constituting an object |
| Systematic unity | [A642-668/B670-696](sources/kant/critique-a.md#a642) | Phase 4 organization of inquiry and Phase 5 evaluation of regulative behavior |

## Coverage limits and maintenance

- This map covers speculative cognition relevant to the initial architecture.
  It does not cover practical reason, moral agency, reflective or aesthetic
  judgment, or Kant's broader corpus.
- The local Max Müller translation is useful for reproducible links, but wording
  that bears interpretive weight should be checked against the German and a
  current scholarly translation.
- A citation identifies evidence, not a settled interpretation. Competing
  readings belong in the [claims register](CLAIMS.md) or a decision record.
- Add a passage here only when it constrains a declared architecture question,
  claim, invariant, behavior, or limit. Add definitions to the glossary instead.
- When a Roadmap decision is settled, link its decision record back to the
  controlling row in this map rather than duplicating the source discussion.
