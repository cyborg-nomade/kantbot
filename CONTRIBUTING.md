# Contributing to Kantbot

Kantbot is a publicly readable research project maintained by its owner and
explicitly invited collaborators. It does not accept unsolicited patches,
pull requests, source corrections, documentation, examples, specifications,
or code. Public visibility is an invitation to read, inspect, cite, and
criticize the work, not an open call for collaborative development.

GitHub is configured so that only collaborators can open pull requests against
the canonical repository. Issues, Discussions, Projects, and the wiki are not
public contribution channels. Creating a fork under GitHub's Terms of Service
does not grant rights beyond those terms or the rights supplied independently
by applicable law. See the [copyright and access notice](COPYRIGHT.md).

The workflow below governs maintainers and people who have been explicitly
invited to collaborate. Do not submit unsolicited changes through another
channel to circumvent the repository controls.

## Before a maintainer proposes a change

1. Locate the relevant phase and deliverable in the [Roadmap](ROADMAP.md).
2. Check the [glossary](GLOSSARY.md) for established vocabulary and open
   terminological decisions.
3. Check the [claims register](CLAIMS.md) for current commitments and live
   alternatives.
4. Use the [primary-source map](PRIMARY_SOURCES.md) to find controlling
   passages when a change depends on Kant's text.
5. Decide whether the change requires a
   [decision record](docs/decisions/README.md#when-to-write-a-record).

## Maintainer delivery workflow

Each itemized Roadmap to-do is an independently reviewable unit:

1. Begin from an up-to-date `main` and create a branch named
   `feature/phase-N-short-name`.
2. Keep the branch focused on one Roadmap item and make coherent commits.
3. Push the branch and open a pull request describing its grounds, scope, and
   checks.
4. Do not merge until the maintainer has reviewed and approved the pull
   request.
5. After merge, update local `main` before beginning another item.

Small corrections that are not Roadmap deliverables may use a descriptive
`docs/`, `fix/`, or `chore/` branch, but they still go through review.

## Documentation conventions

- Link to an existing definition, source discussion, or claim instead of
  restating it in several files.
- Use repository-relative Markdown links. Add a stable explicit HTML anchor
  when other documents must link to a location whose heading may change.
- Cite the *Critique of Pure Reason* with standard A/B pagination. Link the
  citation to the nearest local anchor and name the edition when a difference
  affects the argument.
- Keep quoted primary text in `sources/`; keep definitions in the glossary,
  passage routing in the source map, complete propositions in the claims
  register, and adopted choices in decision records.
- Label consequential statements as textual, interpretive, analogical, or
  engineering. Add a stable `K-###` entry when a proposition will constrain
  architecture, behavior, evaluation, or scope across documents.
- State where a computational analogy fails. A shared functional description
  does not establish that software literally possesses a human faculty.
- Prefer short sections, one proposition per claim, and examples or predicted
  behavior where an abstract distinction might otherwise remain decorative.
- Update inbound links and related claims in the same pull request when a
  document is renamed, superseded, or materially revised.

## Decision conventions

Use [decision records](docs/decisions/README.md) for choices that adopt a
contested interpretation, define an architectural boundary, change observable
behavior, revise a current claim, or would be costly to reverse. Records
explain why a choice governs the project; they do not replace the source map or
claims register.

Minor editorial changes, source transcription corrections, and local,
reversible implementation details normally do not need a record.

## Python readability and static analysis

Python should remain legible to readers who are following the philosophical
model rather than studying programming technique. Follow the object-oriented
and functional division in
[ADR 0006](docs/decisions/0006-canonical-model-representation.md#decision):
keep local invariants and queries with immutable domain values, express
transformations with explicit inputs and returned values, and keep effects at
the boundary.

- Prefer explicit control flow over nested conditional expressions or dense
  expression-level branching.
- Prefer descriptive intermediate names when they expose a philosophical or
  validation decision.
- Avoid deep inheritance, hidden mutation, clever metaprogramming, and
  point-free constructions that obscure the traceable operation.
- Run the repository's complete Ruff configuration and tests before pushing;
  do not narrow or suppress a rule merely to make a warning disappear.
- Treat SonarQube for IDE findings on changed files as review findings. When a
  stable, applicable Sonar rule is not covered by Ruff, prefer a small
  repository-owned check over relying on one maintainer's editor state.

The `Quality` GitHub Actions workflow runs the same formatting, lint, and test
checks for pull requests and `main`, produces branch-coverage data, and sends
the source and coverage report to the public SonarQube Cloud project. Run its
local equivalent with:

```text
uv sync --locked --all-groups
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run coverage run -m pytest -W error
uv run coverage report
```

These conventions apply the Zen of Python's preference for explicit,
readable code without treating aphorisms as substitutes for concrete review.

## Review checklist

Before requesting review, check that:

- the change belongs to the branch's declared Roadmap item;
- links and A/B anchors resolve to the intended material;
- new or revised claims have the correct label, status, grounds, and
  consequence;
- disputed choices remain visible and consequential choices have a decision
  record;
- non-goals have not become implicit prerequisites; and
- formatting checks, tests, or manual verification relevant to the change are
  reported in the pull request.
