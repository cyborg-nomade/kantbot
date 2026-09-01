# Kantbot

> [!IMPORTANT]
> Kantbot is a publicly readable research work, not open-source or free
> software. Its original material is published with all rights reserved, and
> the canonical repository does not accept public change proposals. See the
> [copyright and access notice](COPYRIGHT.md) and
> [maintainer policy](CONTRIBUTING.md).

Kantbot is an experiment in executable philosophy: a small, inspectable model
whose organization is constrained by a declared interpretation of Kantian
cognition. Its first goal is not a general-purpose AI, but a bounded system in
which inputs can be synthesized into candidate objects, concepts can be
applied, judgments can be licensed or withheld, and every result exposes its
grounds and limits.

The repository contains the Phase 0 foundations, the completed Phase 1
philosophical specification, and the first Phase 2 executable artifact:
canonical immutable data structures and local invariants. The model does not
yet execute a complete cognitive cycle; interfaces, transitions, complete
provenance validation, property tests, and the deterministic toy world remain
separate Phase 2 work.

## Start here

| Document | Use it to understand |
| --- | --- |
| [Manifest](MANIFEST.md) | The project's purpose, commitments, and standard of success |
| [Roadmap](ROADMAP.md) | The sequence from philosophical groundwork to a usable release |
| [Cognitive architecture](COGNITIVE_ARCHITECTURE.md) | Component boundaries, transformations, licensing gates, and variant comparison |
| [Canonical data structures](CANONICAL_DATA_STRUCTURES.md) | Executable semantic values, local invariants, and their philosophical boundaries |
| [Worked examples](WORKED_EXAMPLES.md) | Hand-traced success, ambiguity, applicability, unity, withholding, and overreach cases |
| [Behavioral predictions](BEHAVIORAL_PREDICTIONS.md) | Controlled contrasts that distinguish the architecture from a simpler pipeline |
| [Research questions](RESEARCH_QUESTIONS.md) | The questions Phase 1 must answer and the project's explicit non-goals |
| [Glossary](GLOSSARY.md) | Kant's terms, their computational interpretations, and the boundary between them |
| [Primary-source map](PRIMARY_SOURCES.md) | The passages that constrain the initial architecture |
| [Claims register](CLAIMS.md) | The status and consequences of textual, interpretive, analogical, and engineering claims |
| [Local source texts](sources/kant/README.md) | Reproducible public-domain excerpts and their provenance |

The canonical project is maintained by invited collaborators only; it does not
accept public patches or pull requests. Maintainers should follow the
[delivery and review guide](CONTRIBUTING.md). Choices that settle a disputed
reading or impose a consequential project constraint belong in
[decision records](docs/decisions/README.md).

## Repository layout

```text
.
├── docs/decisions/       Decision-record index and template
├── src/kantbot/model/    Immutable canonical semantic values
├── tests/                Local invariant and outcome-union tests
├── sources/kant/         Public-domain primary texts with linkable A/B anchors
├── BEHAVIORAL_PREDICTIONS.md Controlled architectural comparisons
├── CANONICAL_DATA_STRUCTURES.md Readable map to the executable model
├── CLAIMS.md             Claims and their project status
├── COGNITIVE_ARCHITECTURE.md Component and transformation diagrams
├── CONTRIBUTING.md       Delivery, documentation, and review conventions
├── COPYRIGHT.md          Rights, access, and participation policy
├── GLOSSARY.md           Philosophical and implementation vocabulary
├── MANIFEST.md           Purpose and standing commitments
├── PRIMARY_SOURCES.md    Architecture questions mapped to passages
├── RESEARCH_QUESTIONS.md Phase 1 agenda and scope boundaries
├── ROADMAP.md            Phases, deliverables, and exit criteria
├── WORKED_EXAMPLES.md    Hand-worked cognitive traces
└── pyproject.toml        Python dependencies and development checks
```

This layout should grow only when a new kind of artifact needs a stable home.
The executable model uses Python and strict, frozen Pydantic values under
[ADR 0006](docs/decisions/0006-canonical-model-representation.md). Run its
checks with `uv run ruff check src tests` and `uv run pytest` after
`uv sync --dev`.
