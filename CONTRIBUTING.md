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
