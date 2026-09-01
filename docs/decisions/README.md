# Decision Records

Decision records preserve why Kantbot adopted a consequential philosophical or
engineering choice, which alternatives remained live, and what behavior the
choice is expected to change. They keep an implementation default from
silently becoming the project's interpretation of Kant.

## When to write a record

Write a decision record when a choice:

- adopts one of several plausible readings of a source passage;
- determines the boundary or interaction of cognitive roles;
- defines a representation, invariant, rule authority, or failure condition;
- changes observable behavior, traces, or evaluation criteria;
- accepts, revises, retires, or operationalizes a registered claim; or
- is cross-cutting or sufficiently costly to reverse that future contributors
  will need its rationale.

Do not write a record merely to preserve meeting notes, restate a glossary
definition, correct a source transcription, or document a small reversible
implementation detail. Those changes belong in the document or commit they
affect.

## File and identifier convention

Copy [the template](0000-template.md) to the next unused four-digit identifier
and a short descriptive slug:

```text
0001-example-decision.md
0002-another-decision.md
```

The identifier is permanent. Do not renumber records or reuse the identifier
of a rejected or superseded record. Keep one primary decision per file and add
it to the index below.

## Status lifecycle

- **Proposed:** open for discussion and not yet authoritative.
- **Accepted:** governs current project work.
- **Rejected:** considered but not adopted; retained with its rationale.
- **Superseded:** replaced by a named later record.

A new record begins as **Proposed**. A pull request that adopts it must change
the status to **Accepted** before merge. Approval and merge establish the
decision; later changes require a new record that links back and marks the old
one **Superseded**. Do not rewrite an accepted record to make it appear that a
later choice was always intended.

## Required connections

Every record should link to the research questions, registered claims, source
passages, and earlier decisions it affects. Its grounds must separate:

- what the text supports;
- what interpretation the project chooses;
- what computational analogy is introduced; and
- what engineering behavior or constraint follows.

When a record is accepted, update affected claims and documentation in the
same pull request. Record at least one observable consequence when the decision
is supposed to matter to model behavior.

## Index

| ID | Decision | Status |
| --- | --- | --- |
| [0001](0001-variant-scoped-receptive-terminology.md) | Use variant-scoped receptive terminology | Accepted |
| [0002](0002-a-b-synthesis.md) | Use an A/B hybrid synthesis default | Accepted |
| [0003](0003-object-and-judgment-licensing.md) | Separate object formation, applicability, and judgment licensing | Accepted |
| [0004](0004-limit-outcomes-and-rule-authority.md) | Make limit outcomes and rule authority behaviorally distinct | Accepted |
| [0005](0005-publish-readable-source-with-closed-contributions.md) | Publish readable source with closed contributions | Accepted |
| [0006](0006-canonical-model-representation.md) | Choose the canonical model representation | Accepted |

The [record template](0000-template.md) is not itself a decision.
