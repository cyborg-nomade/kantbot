# Repository working agreement

## Roadmap delivery workflow

Treat every itemized to-do in `ROADMAP.md` as an independently reviewable unit
of work:

1. Create a dedicated feature branch before changing files for that item.
2. Commit the item's changes to that branch until the work is satisfactory.
3. Push the branch and open a pull request for the maintainer to revise and
   approve before merge.
4. Do not merge the pull request without the maintainer's approval.
5. After the pull request is approved and merged, switch back to local `main`,
   update it from `origin/main`, and only then begin the next Roadmap item.

Use one chat for each Roadmap phase and name it `Phase N`.
