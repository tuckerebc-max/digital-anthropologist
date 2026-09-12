# Operating a first bounded study

Use the existing Center design and observation method. These instructions make the first study executable; they do not appoint roles, change institutional authority, or enable background telemetry.

1. Record the sponsor's actual authorization, the question, time window, explicit roots/systems, privacy class, retention, and stop/correction paths. Existing explicit task authorization can be recorded as the basis; do not invent a second approval.
2. Collect the minimum metadata needed. Run `yard_inventory.py` only on those roots. Keep the JSON outside public source control. Task-history replay is a separate authorized activity; the instrument does not access it.
3. Reconstruct a small number of work episodes. Tag claims as system record, artifact state, participant report, observation, or interpretation. Separate the reported result from fresh verification.
4. Triage each candidate into recover, already integrated, duplicate, intentional fixture, active elsewhere, needs evidence, or retire proposal. Do not delete candidates as part of triage.
5. Before recovery, inspect the current remote head and whether the candidate change is already reachable from it. A checkout with old refs is not proof of orphaned work. For equivalent changes with different history, compare the actual patch/tree.
6. Route a bounded repair with an owner, source revision, reproducible failing case, acceptance check, and next event. The observer's authority ends at the proposal; an independently authorized builder can implement it.
7. Verify in a clean checkout and at the real command or user flow. Record source revision, exact commands, failures/skips, and output evidence. Record local, committed, pushed, merged, released, and running separately.
8. Re-observe the next real use. Did the original failure disappear? Did someone receive a usable artifact? Record the negative case as well as the success.

## Episode record

```text
Study / episode ID:
Question / intended outcome / authorized boundary:
Sources and exact revisions:
Intended workflow:
Observed trajectory and recovery:
Participant account and disagreement:
Finding and evidence type:
Interpretation / warrant / uncertainty / negative case:
Improvement hypothesis:
Receiving owner / next action / acceptance check:
Disposition and publication status:
Re-observation trigger:
Retention / correction / withdrawal path:
```

## Delivery hygiene

Every implementation task ends with a small receipt: canonical repository, branch and commit, relevant test/usage result, artifact location, remote status, next owner, and next event. A project may deliberately stop at a local draft or review candidate, but that choice must remain visible.

Do not treat inventory totals, tool installations, tests collected, or agent availability as deployed capability. The unit of delivery is a usable artifact accepted in its intended context. Keep work in progress small enough that review and release happen alongside implementation.

## Instrument limits

The scanner uses only local evidence and takes a non-atomic snapshot. It excludes dependency/build trees, symlinks, Windows junction/reparse directories, and bare repositories. Source roots are explicit; it neither searches the user's home implicitly nor runs recovered code. Unversioned entries are directories containing direct code files, not inferred products. Identical revisions can be grouped without erasing dirty working copies. Unknown publication status requires a separate remote check.
