# Kantbot Roadmap

## Destination: a usable philosophical instrument

The first usable release will be a small, local program—not a general-purpose
AI—that can operate in a deliberately limited world. It will accept a stream of
structured observations, synthesize them into candidate objects or events,
apply concepts and rules, form judgments, and expose a complete trace of what
licensed each judgment and where its confidence or authority ends.

A minimal interactive interface will let a user:

1. submit or replay observations;
2. inspect the system's representations at each cognitive stage;
3. ask what the system judges and why;
4. observe ambiguity, failed synthesis, conflict, and refusal to overclaim;
5. switch or remove selected philosophical assumptions and compare the result.

This definition keeps the first implementation falsifiable and inspectable.
Language-model integration, open-world perception, and other philosophers are
valuable later experiments, not prerequisites for the first usable system.

## Phase 0 — Establish the ground

**Purpose:** make the inquiry precise enough for several later chats and
contributors to work without silently adopting incompatible assumptions.

Deliverables:

- a [project glossary](GLOSSARY.md) that distinguishes Kant's terms from their
  computational interpretations;
- a [primary-source map](PRIMARY_SOURCES.md) covering the passages and editions
  relevant to the initial architecture;
- a [claims register](CLAIMS.md) labeling statements as textual, interpretive,
  analogical, or engineering choices;
- a short set of [research questions and explicit non-goals](RESEARCH_QUESTIONS.md);
- lightweight [repository and documentation conventions](CONTRIBUTING.md),
  including [decision records](docs/decisions/README.md).

Exit criterion: the central terms are defined well enough to identify genuine
disagreements, even if those disagreements remain unresolved.

## Phase 1 — Write the philosophical specification

**Purpose:** decide what account of Kantian cognition the first model will try
to express before choosing implementation details.

Questions to resolve:

- What counts as the manifold, an intuition, a concept, a judgment, and an
  object *for this model*?
- Which role belongs to sensibility, imagination, understanding, judgment,
  apperception, and reason?
- How will the forms of intuition, synthesis, schematism, and the categories be
  represented, and which of them are necessary for the first experiment?
- How should the project handle differences between the A and B editions and
  disputes among major interpretations?
- What makes a rule constitutive rather than regulative in computational terms?
- What should count as a model of cognitive limits rather than ordinary
  uncertainty or missing data?

Deliverables:

- a [prose specification of faculties, representations, and cognitive
  flow](PHILOSOPHICAL_SPECIFICATION.md);
- [diagrams of component boundaries and transformations](COGNITIVE_ARCHITECTURE.md);
- [worked examples traced by hand from observation to judgment](WORKED_EXAMPLES.md);
- [decision records](docs/decisions/README.md#index) for disputed or especially
  consequential readings;
- a [catalog of behavioral predictions](BEHAVIORAL_PREDICTIONS.md) that
  distinguishes this architecture from a simpler pipeline.

Exit criterion: two implementers could build recognizably equivalent toy
models from the specification, and each design choice has a declared status.

## Phase 2 — Define an executable formal model

**Purpose:** turn the philosophical specification into types, interfaces,
invariants, and testable transitions without yet optimizing for intelligence.

Deliverables:

- [canonical data structures](CANONICAL_DATA_STRUCTURES.md) for observations,
  manifolds, synthesized representations, concepts, judgments, reasons, and
  limits;
- [explicit interfaces between cognitive roles](ROLE_INTERFACES.md);
- a [state-transition model for one cognitive cycle](STATE_TRANSITION_MODEL.md);
- a structured provenance format that records every transformation;
- invariants and property tests for philosophical and software constraints;
- one deterministic toy world with reproducible observation sequences.

The formal model should preserve alternative interpretations behind explicit
interfaces where doing so clarifies a live dispute. It should not create an
abstraction layer for every philosophical nuance.

Exit criterion: complete example traces can be executed as data transformations
and rejected when they violate a declared invariant.

## Phase 3 — Implement the minimal cognitive cycle

**Purpose:** produce the smallest end-to-end system whose behavior depends on
the philosophical architecture.

Provisional cycle:

1. **Reception:** accept a bounded manifold of observations through a defined
   form of presentation.
2. **Synthesis:** combine and retain elements across a sequence so that stable
   candidate objects or events can appear.
3. **Concept application:** determine which concepts can organize the candidate
   representation, including cases of ambiguity or failed application.
4. **Judgment:** form a proposition only when its required conditions are met.
5. **Unity check:** ensure that the judgment and its grounds belong to a
   coherent state that the system can treat as its own.
6. **Critique:** attach scope, warrant, uncertainty, conflicts, and reasons for
   withholding stronger claims.

Deliverables:

- a library implementing the cycle with swappable policies at identified points
  of interpretation;
- deterministic unit and integration tests based on the worked examples;
- negative cases in which synthesis or judgment must fail;
- machine-readable and human-readable traces;
- a basic command-line or notebook demonstration.

Exit criterion: a user can run several scenarios and see non-trivial differences
between successful judgment, ambiguity, contradiction, and overreach.

## Phase 4 — Add reason and self-limitation

**Purpose:** move beyond isolated judgments to rule-governed inquiry while
making the boundary between legitimate and illegitimate inference observable.

Deliverables:

- chains of inference whose premises retain links to their experiential
  conditions;
- regulative goals that guide inquiry without being misreported as known
  objects;
- detection or representation of selected conflicts produced by incompatible
  commitments;
- explicit responses for insufficient grounds and transcendental overreach;
- scenario tests showing how reason improves coherence and how it can exceed
  its proper use.

Exit criterion: the system can pursue greater systematic unity while reporting
the different status of observed, inferred, and merely regulative content.

## Phase 5 — Evaluate the philosophical contribution

**Purpose:** test whether the architecture does more than redescribe an ordinary
symbolic pipeline.

Evaluation should combine:

- **trace review:** can readers locate the grounds and limits of every judgment?
- **behavioral tests:** do declared philosophical commitments produce their
  predicted behavior?
- **ablations:** what changes when synthesis, unity checks, schemata, or
  critique are removed or replaced?
- **baselines:** how does the model differ from a simpler rules engine or
  perception-to-label pipeline?
- **interpretive variants:** do rival readings yield intelligible and
  philosophically relevant differences?
- **failure analysis:** where does the model collapse distinctions it claims to
  preserve?

Deliverables:

- a repeatable scenario suite and evaluation report;
- documented ablation and baseline results;
- a revised claims register that withdraws or narrows unsupported claims;
- a list of philosophical and engineering limitations.

Exit criterion: the team can state with evidence which aspects are distinctively
Kantian, merely conventional, unsuccessful, or still undecided.

## Phase 6 — Package the first usable release

**Purpose:** make the experiment understandable and runnable by someone who did
not build it.

Deliverables:

- a stable command-line or local visual interface for running scenarios and
  exploring traces;
- installation and five-minute quick-start instructions;
- a guided example that connects a source passage, an interpretation, its
  implementation, and an observed behavior;
- reference documentation for extension points and trace formats;
- versioned sample scenarios, expected results, and known limitations.

Release criterion: a new user can install the project, run a scenario, inspect
and challenge a judgment, and compare at least one architectural variant
without reading the source code.

## Beyond the first release

Only after the core instrument is usable should the project widen its scope.
Possible directions include:

- richer simulated worlds and eventually perceptual or linguistic inputs;
- learning processes and the acquisition or revision of empirical concepts;
- reflective and aesthetic judgment;
- practical reason, action, and autonomy, with care not to equate rule-following
  software with moral agency;
- Hegelian critiques of fixed faculties and the development of concepts through
  contradiction;
- Nietzschean critiques of unity, truth, perspective, and the status of reason;
- Deleuzian alternatives centered on difference, synthesis, and individuation;
- comparative experiments in which a critique changes the architecture rather
  than merely changing its vocabulary.

Each extension should begin with a new philosophical specification and a claim
about what behavior ought to change.

## Work that continues through every phase

- Keep source citations and interpretive notes adjacent to consequential design
  choices.
- Preserve a clear boundary between philosophical claims and engineering
  conveniences.
- Prefer small, deterministic examples before opaque or large-scale models.
- Treat failed cases and unresolved disputes as documented outputs.
- Update the Manifest only when the project's purpose changes; update this
  Roadmap whenever evidence changes the route.
