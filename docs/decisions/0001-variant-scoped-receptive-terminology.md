# ADR 0001: Use variant-scoped receptive terminology

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** Kantbot maintainers
- **Related questions:** [RQ-01](../../RESEARCH_QUESTIONS.md#rq-01--what-can-be-given-to-the-model)
- **Related claims:** [K-001](../../CLAIMS.md#k-001), [K-015](../../CLAIMS.md#k-015), [K-016](../../CLAIMS.md#k-016), [K-027](../../CLAIMS.md#k-027)
- **Supersedes:** None
- **Superseded by:** None

## Context

The first model must name the representation produced at its receptive
boundary. The name will appear in types, traces, diagrams, examples, and
comparisons with later interpretations. It therefore does more than prevent a
terminological misunderstanding: it declares how strongly the implementation
claims to instantiate the Kantian role.

Kantbot treats Kant's account as an executable hypothesis. If that account is
correct and sufficiently complete, a faithful implementation should approach
corresponding structures and behaviors of human cognition in bounded settings
([K-027](../../CLAIMS.md#k-027)). Calling a model-internal representation an
`intuition` can express that experimental commitment without claiming that the
whole program is already a human mind. Conversely, replacing every Kantian
term with weaker engineering language can prejudge the experiment by treating
the relation as merely metaphorical from the outset.

The decision must keep three questions distinct:

1. What conditions define the receptive role in a selected interpretation?
2. What should the resulting representation be called inside that model?
3. What additional evidence would show that the model approaches human
   cognition?

No terminology can answer the third question by itself. The present decision
concerns the first two and the relation between them.

## Grounds and claim status

### Textual

Sensibility is receptive and gives objects through intuition; intuition is
singular and immediate in contrast to discursive concepts
([A19-20/B33-34](../../sources/kant/critique-a.md#a19),
[A50/B74](../../sources/kant/critique-a.md#a50)). Empirical intuition involves
sensation, while space and time are forms of human sensible intuition
([A20/B34](../../sources/kant/critique-a.md#a20),
[A22-25/B37-41](../../sources/kant/critique-a.md#a22), and
[A30-32/B46-49](../../sources/kant/critique-a.md#a30)). The text supplies
constraints on the role but does not settle whether a software realization can
satisfy them or what such a realization should call its internal states.

### Interpretive

The live disagreement is not simply whether readers might anthropomorphize the
program. It is whether receptivity, singularity, sensible content, and prior
form can be specified functionally enough for a software representation to
count as an intuition within a declared reconstruction. One interpretation may
treat the role as realizable across substrates; another may hold that affection
or specifically human sensibility is constitutive in a way the model does not
reproduce. Terminology should expose rather than settle that disagreement.

### Analogical

Using `intuition` can be a theory-internal attribution: the implementation is
intended to occupy the role that the selected Kantian model assigns to
intuition. This is stronger than a loose metaphor, yet it does not entail that
the entire system is conscious, human, or a complete reproduction of cognition.
Using `constrained presentation` avoids the attribution but is not philosophically
neutral if it implies in advance that the role cannot be realized.

### Engineering

All options retain an external **observation** record and a distinct receptive
transformation. The resulting internal representation carries episode, source,
form, order, and provenance metadata and arrives without licensed object
identity. Parsing remains outside the cognitive role. The chosen terminology
must be stable enough for Phase 2 types while allowing interpretation variants
and later critiques to declare different role criteria.

## Decision drivers

- **Experimental force:** Does the vocabulary make Kant's account a claim the
  implementation can meaningfully support or fail to support?
- **Role precision:** Does the name keep receptivity, particularity, form, and
  preconceptual presentation visible?
- **Non-circular evaluation:** Can the project test whether the role succeeds
  without treating the chosen label as evidence?
- **Interpretive visibility:** Can a critic identify which conditions were used
  and which disputed conditions were omitted?
- **Variant comparability:** Can Kantian alternatives and later critiques share
  observations without being forced into one ontology?
- **Terminological stability:** Can types and traces remain intelligible as the
  model becomes more faithful or is revised?

## Options considered

### Option A: Use intuition as theory-internal terminology

The representation produced by the receptive role is an `intuition`, its
plurality is a `manifold of intuition`, and the role that produces it is
`sensibility`. These terms state what the selected Kantian architecture is
trying to realize, not what an external evaluator has already proven about it.

**Best argument.** Kant's theory makes claims about the necessary organization
of cognition. A serious implementation should be allowed to instantiate the
theory's kinds, just as a model of a scientific theory uses the theory's terms
before the theory has been vindicated. Withholding `intuition` solely because
someone might infer "human mind" makes terminology track public-relations risk
rather than architectural role. It also weakens falsifiability: a state called
only `presentation` can always be defended as an analogy when its behavior
departs from what an intuition should make possible.

This option supports the project's longer experiment. Rival Kantian readings
can propose different conditions for intuition, and later critiques can argue
that the kind is malformed, incomplete, or unnecessary. Improvements and
regressions are then changes to a claimed cognitive architecture rather than
changes to a vocabulary mapping outside it.

**Costs and failure modes.** The name may import conditions the first model has
not implemented, especially affection, sensation, and the specifically human
forms of intuition. It can make a contested interpretation look settled at the
type boundary and can obscure degrees of fidelity: both a minimal timestamped
record and a richer receptive state might bear the same name. Readers may also
mistake a local role attribution for evidence of consciousness or human-level
cognition, even though that inference does not follow.

**Required safeguards.** Every model must declare its criteria for intuition,
list material departures from the textual account, and keep external
observations distinct from the internal intuition they occasion. Evaluation
must test the role's behavioral consequences; the identifier `intuition` is
never evidence that those tests pass.

### Option B: Use constrained presentation throughout implementation

The internal state is a `constrained presentation`; Kantian documents say that
it is analogous to intuition, while types and traces retain the weaker name.
This was the terminology used provisionally in the initial prose-specification
draft.

**Best argument.** The first model does not reproduce obvious elements of
Kant's account, including affection by independently existing objects and
human sensation. Calling its records intuitions can therefore beg the most
important interpretive question. A weaker term forces every mapping to be
argued explicitly and keeps the implementation from acquiring philosophical
authority merely through identifiers. It also gives later non-Kantian variants
a common representation vocabulary and makes changes of interpretation less
disruptive to serialized data.

This option distinguishes building a model *of* an account from claiming that
the modeled kinds have been realized. That distance can be methodologically
valuable during early phases, when behavioral comparisons are sparse and the
architecture is expected to change.

**Costs and failure modes.** The caution is not neutral. It may encode the
conclusion that software cannot instantiate intuition before the experiment has
begun, thereby reducing a constructive test to analogy by stipulation. Generic
terms can also conceal a generic pipeline: an implementation may satisfy weak
requirements for presentation while never confronting the stronger conditions
that `intuition` would impose. As the model becomes more faithful, the weaker
name offers no principled point at which the project should strengthen its
claim.

**Required safeguards.** `Constrained presentation` must have explicit Kantian
role criteria and behavioral obligations rather than serving as a neutral data
bucket. Documentation must explain whether the weaker name expresses temporary
epistemic caution, an interpretation about realization, or only a stable
cross-variant interface.

### Option C: Make intuition a criterion-governed status

The receptive role first produces a `receptive representation` or `candidate
intuition`. It becomes an `intuition` only when declared criteria for
receptivity, singularity, sensible content, form, and independence from concept
application are satisfied. Different interpretation variants may declare
different criteria, but each must expose them.

**Best argument.** This option connects philosophical terminology to inspectable
achievement rather than caution or aspiration. It gives the project a concrete
way to improve its approach to cognition: later implementations can satisfy
more demanding criteria, and traces can state exactly why a representation
qualifies. Failure to form an intuition becomes a meaningful result rather than
an input exception or retrospective disclaimer.

It also separates local success from global success. A representation can earn
the role status `intuition` while the system still fails at synthesis,
judgment, consciousness, or human-level cognition.

**Costs and failure modes.** Kant's intuition is a kind of representation, not
obviously an honorific awarded after validation. Making it a status may distort
the receptive relation into a downstream certification step. The criteria
themselves embed an interpretation and may be circular: the project would need
to know what computational intuition is before using the experiment to clarify
that question. Changing criteria can also make trace vocabularies unstable and
create misleading comparisons across versions.

**Required safeguards.** Criteria must be versioned, interpretation-specific,
and divided into necessary conditions, currently modeled conditions, and open
conditions. A failed criterion must not imply malformed input when it instead
reveals a limitation of the architecture.

### Option D: Use variant-scoped Kantian and neutral vocabularies

A theory-neutral boundary exposes `presented elements`, while each
interpretation projects those elements into its own vocabulary. A Kantian
variant may call its internal state an `intuition`; another Kantian reading may
call it a `candidate intuition`; a later critique may reject the kind entirely.
Traces preserve both the shared observation identity and the variant's
theory-internal term.

**Best argument.** The Roadmap requires replaceable interpretations and later
critiques. A shared boundary makes their results comparable without forcing
every architecture to accept or reject Kant's ontology. At the same time, the
Kantian model can state the strong theory-internal claim that it realizes
intuition. This option distinguishes interoperability vocabulary from
philosophical vocabulary rather than making one do both jobs.

**Costs and failure modes.** Two vocabularies add indirection to every type,
diagram, and trace. The shared layer may become the real architecture while
Kantian terms survive only as aliases, violating the commitment that philosophy
change behavior. Conversely, variants may use different names for identical
operations and create the appearance of philosophical disagreement without an
observable difference.

**Required safeguards.** A variant projection must declare transformations,
invariants, and behavioral consequences beyond renaming. Shared boundary types
must remain minimal and must not preconstitute objects or concepts that a
variant is supposed to explain.

## Trade-off comparison

| Driver | Option A: intuition | Option B: constrained presentation | Option C: earned status | Option D: scoped vocabularies |
| --- | --- | --- | --- | --- |
| Experimental force | Strongest initial commitment | Weaker, unless obligations compensate | Strong and explicitly testable | Strong inside each variant |
| Risk of begging the question | Highest | Lowest | Shifted into the criteria | Shifted into the projection |
| Fidelity can improve by degrees | Requires an explicit deviation ledger | No natural promotion point | Built into versioned criteria | Expressed through variant revisions |
| Cross-variant comparison | Requires adapters | Easy at the data-model level | Hard when criteria differ | Explicit design goal |
| Type and trace stability | High within a Kantian model | High across models | Lowest as criteria evolve | Stable boundary, more complex traces |
| Risk of decorative terminology | Moderate | Risk becomes decorative analogy | Moderate | Highest if projections only rename |

## Decision

Choose Option D. Use a minimal shared boundary vocabulary for interoperability
and variant-specific philosophical vocabulary inside each declared
architecture.

The shared boundary distinguishes:

- an external `observation`, which is serialized content plus source and
  episode metadata; and
- a `presented element`, which is admitted at the common boundary but carries
  no licensed object identity, concept, or variant-specific cognitive status.

Each interpretation then performs an explicit **variant projection**. The
accepted A/B hybrid Kantian variant projects presented elements into
`intuition` and `manifold of intuition` under its declared sensibility, form,
singularity, and preconceptuality constraints. A projection must add or validate
interpretation-specific structure and may fail; an alias or display-label
change does not count. Later Kantian readings may impose different criteria,
and later critiques may introduce different representations or reject the
intuition kind.

Traces preserve both layers: the stable observation and presented-element
identities used for comparison, and the variant-specific representation,
transformation, invariants, omissions, and terminology. The default Kantian
variant may therefore claim to realize the role of intuition without treating
that identifier as evidence that the role, the wider architecture, or human
cognition has been reproduced successfully.

The following constraints are common ground and do not depend on any one
variant's terminology:

- serialized input remains an external observation, not an already constituted
  object;
- the receptive representation precedes concept application and carries a
  declared temporal and, where required, spatial form;
- episode boundaries, ordering, source, and transformation provenance remain
  inspectable;
- using a Kantian term does not by itself prove that the whole system is human,
  conscious, or complete; and
- avoiding a Kantian term does not make an architecture philosophically
  neutral or release it from behavioral criteria.

`Constrained presentation` is not the accepted public type name. It may remain
ordinary explanatory prose for the shared boundary, but implementation-facing
documents use `presented element` for that boundary and `intuition` within the
accepted Kantian variant.

## Consequences

- Phase 2 must define the shared `observation` and `presented element` types plus
  an explicit variant-projection interface.
- The accepted Kantian variant uses `intuition` theory-internally and declares
  the conditions and omissions attached to that use.
- Diagrams, examples, and traces must show both the shared boundary and the
  variant-specific transformation; merely relabeling a shared record violates
  this decision.
- Cross-variant comparison becomes easier at the cost of an additional
  representation layer and more complex traces. The project accepts that cost.
- Evaluation must test what the Kantian projection changes and what evidence
  bears on fidelity to human cognition beyond the presence of its identifier.
- New variants may reuse the shared boundary but cannot inherit objecthood,
  concepts, or other commitments that their interpretation is meant to
  explain.

## Observable consequences

Two variants can receive the same observation and preserve the same presented-
element identifier while producing different cognitive traces. The accepted
Kantian variant admits an `intuition` only through its declared form and role
constraints; a competing variant may produce another representation or reject
the element. If temporal form required by the Kantian variant is absent, the
shared presented element remains inspectable but the Kantian projection fails
and cannot enter its manifold of intuition. A trace that changes only the label
while retaining identical structure, invariants, and behavior fails this
decision's safeguard.

## Follow-up

K-015, the glossary, prose specification, primary-source map, and RQ-01 now
record the accepted vocabulary. Future Phase 1 diagrams and examples must show
the two layers. Phase 2 must define shared-boundary types, the variant-
projection interface, and variant-specific representation metadata.
