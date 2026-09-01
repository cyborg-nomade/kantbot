# ADR 0005: Publish readable source with closed contributions

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** Kantbot maintainer
- **Related questions:** None; this record governs publication and repository operations
- **Related claims:** None; this record does not change a philosophical claim
- **Supersedes:** None
- **Superseded by:** None

## Context

Kantbot is intended to be a public research project. Readers should be able to
inspect the source, history, arguments, models, and later implementation in the
way that they can inspect a published book. Public inspection does not imply
that the project is free software, open source, open content, or open to public
development. Only the maintainer and explicitly invited collaborators should
be able to propose or make changes to the canonical repository.

The repository is currently private and owned by a personal GitHub account.
Only the owner has access. It has no software or content license, but its README
and contribution guide currently invite public contributions. GitHub's public-
repository [Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#5-license-grant-to-other-users)
necessarily permit users to view and fork public content through GitHub.
Publication therefore cannot literally prevent copying or changes in somebody
else's fork; it can withhold additional copyright permissions and prevent those
changes from becoming proposals against the canonical repository.

This decision concerns repository publication, upstream participation, and
protection of the canonical history. It does not determine how readers may
quote or otherwise use material under applicable law, and it does not alter the
public-domain status of the Kant source texts under `sources/kant/`.

## Grounds and claim status

### Textual

Not applicable. This is a publication and repository-governance decision, not
an interpretation of Kant's text.

### Interpretive

Not applicable to the interpretation implemented by Kantbot. The book analogy
expresses the intended relationship between publication and editorial control:
the work is open to inspection and criticism without making its canonical text
open to unsolicited revision.

### Analogical

The repository is analogous to a publicly accessible research edition. The
analogy supports public reading and stable, maintainer-controlled editions. It
does not imply that Git hosting can prevent lawful quotation, local copying, or
the forking rights required by GitHub's service.

### Engineering

GitHub permits a public repository to
[restrict pull-request creation to collaborators or disable it](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/disabling-pull-requests).
It also provides [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule),
private vulnerability reporting, secret scanning, and controls for disabling
Issues, Projects, Discussions, and the wiki. Public repositories nevertheless
remain forkable under GitHub's Terms of Service. Protection must therefore
combine an explicit rights notice with access controls; either layer alone
would misstate the policy.

## Options considered

### Option A: Keep the canonical repository private and publish exports

Publish rendered documents, release archives, or selected snapshots while the
working Git repository remains private.

This most closely controls the editorial boundary and avoids publishing the
development history. It weakens inspectability, makes reproducibility harder,
and creates a release process in which the public artifact can drift from the
canonical source.

### Option B: Make the canonical repository public and close upstream contributions

Publish the canonical Git repository with no open-source or open-content
license. Restrict pull requests to collaborators, disable public issue and
project surfaces, and protect `main` against direct or destructive updates.

This provides the strongest inspectability and provenance with one canonical
history. Its unavoidable cost is that GitHub users may view and fork the work
through GitHub, and no technical control can prevent local copies or proposals
made outside the canonical repository.

### Option C: Maintain a private canonical repository and an archived public mirror

Keep development private and periodically update a separate public repository,
then archive the mirror so that it is read-only.

Archiving disables upstream interaction more completely and gives readers a
Git history. It introduces two repositories, synchronization and provenance
risks, and repeated unarchive-update-rearchive operations. Public discussion
would also attach to a mirror rather than the canonical history.

### Option D: Publish as an open-source community project

Adopt an open-source license and accept public issues and pull requests.

This maximizes reuse and outside participation but directly contradicts the
chosen editorial and rights model.

## Decision

Choose Option B.

The canonical `cyborg-nomade/kantbot` repository will become public. Its
original contents remain all rights reserved except where a file or directory
states otherwise. The repository will contain no open-source or open-content
license and will prominently explain that public readability grants no rights
beyond applicable law and the permissions required by GitHub's Terms of
Service.

Only the owner and explicitly invited collaborators may propose upstream
changes. Pull-request creation will be restricted to collaborators. Issues,
Projects, Discussions, and the wiki will be disabled as contribution surfaces.
Private vulnerability reporting may remain available because a confidential
security report is not a proposed patch.

The `main` branch will require changes to arrive through pull requests, reject
force pushes and deletion, and require conversations to be resolved. The
repository currently has only one GitHub identity with access, so GitHub review
approval cannot be required without making the maintainer workflow impossible;
maintainer approval remains recorded in the project review process.

## Publication audit

The pre-publication audit found:

- one collaborator, the repository owner, and no pending invitations;
- no unmerged remote branches, tags, releases, Issues, Actions workflows, or
  Actions runs;
- no suspicious credential filenames or common secret patterns in reachable
  Git history, pull-request bodies, or comments;
- only project Markdown files in reachable history; and
- two author email addresses in existing commit metadata. The maintainer
  explicitly accepted their public visibility and selected
  `uriel.fiori@gmail.com` for future commits in this repository.

## Consequences

- Anyone may read and clone the public repository, and GitHub users may fork it
  under GitHub's Terms of Service.
- No additional permission to modify, redistribute, sublicense, sell, or create
  derivative works is granted for original Kantbot material.
- Public users cannot open pull requests or use repository Issues, Projects,
  Discussions, or the wiki to propose changes.
- Only invited collaborators have write access; the owner is initially the only
  collaborator.
- The full Git history, commit metadata, merged pull requests, and any Actions
  history become public and must be audited before the visibility change, as
  required by GitHub's documented
  [visibility-change consequences](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility#changing-from-private-to-public).
- Branch protection reduces accidental or destructive changes to `main`, but
  the owner necessarily retains administrative control over the repository.
- External criticism can occur in scholarly or public venues without becoming
  an upstream contribution workflow.
- If the project later invites a collaborator, that person gains the ability to
  open upstream pull requests and must explicitly accept the rights and review
  policy before contributing.

## Observable consequences

After publication, a signed-out reader can view and clone the repository. A
GitHub user who is not a collaborator can fork it but cannot open a pull request
against `cyborg-nomade/kantbot`, create an issue, or push a branch to the
canonical repository. The maintainer can open a pull request from a canonical
branch, while `main` rejects force pushes, deletion, and ordinary direct
updates.

## Follow-up

Before publication:

1. Update the README and maintainer guide and add the copyright/access notice.
2. Audit the full Git history, remote branches, pull requests, Actions history,
   filenames, secrets, and author metadata for public exposure.
3. Obtain maintainer approval and merge this decision through the existing
   review workflow.

At publication:

1. Change visibility to public while restricting pull requests to
   collaborators and disabling Issues and Projects.
2. Protect `main` and enable the appropriate public-repository security
   features.
3. Verify visibility and contribution controls from the public repository
   metadata and record any platform limitation that cannot be enforced.
