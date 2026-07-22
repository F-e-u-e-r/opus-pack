# delegation-and-review · references: settled-tree review dispatch

The dispatch protocol behind §3's settled-tree bullet (`unprobed` — see the
skill's Provenance; this entry is the protocol body, placed here per the
pack's split precedent so the skill's §3 stays lean). Load this file before
dispatching a review wave — read-only or write-capable — over a tree that
you, a hook, a user, or a sibling process may touch while it reads.

**Definitions.** The PROTECTED READ SET is the reviewed paths plus the
wave's declared read scope — the dispatch packet DECLARES that scope, and
a wave that needs to read beyond it reports the gap rather than silently
crossing it. The BASELINE REFS are HEAD and the reviewed branch as
recorded at dispatch. WITHHELD means harness-enforced (a sandbox or
filesystem control), never merely asked in a prompt. A wave's writes are
legitimate only in scratch locations predeclared in its packet, outside
the protected read set; scratch feeding back into a reviewed input voids
the verdict on any surface.

**(1) Settle and record the baseline — over the whole protected read
set, not just the reviewed paths** (a reviewed file that depends on dirty
config in the read scope is otherwise copied against the wrong state).
When the requested end-state permits a commit, commit the content under
review on the reviewed branch and note the revision — staging exactly
the content under review; unrelated dirty or untracked material is
attributed first (operational-rigor's baseline rule), never swept into
the settle commit; an end-state
requiring unchanged history or uncommitted work takes the restorable
capture — working content, index state, and untracked files across the
protected read set, plus the baseline refs — verified to hold everything
under review. Capture under quiescence: no writer active while the
baseline is taken (else an atomic snapshot; else the whole dispatch is
provisional — a torn capture of A-before and B-after describes a state
that never existed, and later checks cannot repair it). Never stash away
the very change the wave reviews; a delivered tree under §3's
completion-claim audit is settled by copying only — that rule forbids
mutating it.

**(2) Choose the read surface by what you can enforce.** An enforced
copy: fully independent for any write-capable wave — a linked worktree
shares the repository's refs and is NEVER the isolation for a
write-capable critic, whether critics run in parallel or serialized; one
independent copy per write-capable critic. Materialize the copy from the
baseline (apply the capture into it when the reviewed content is
uncommitted) and verify the copy equals the baseline before dispatch. Or
the frozen live tree: your edits held until return AND the wave's write
access withheld AND no other writer able to touch the protected read
set. Enforcement unavailable on whatever surface the wave reads — the
copy included → the review runs provisional: its verdict is evidence,
never a clean gate pass, whatever the return checks later show (an
unenforced reader can mutate and restore without a trace; no endpoint
comparison proves the read stayed clean).

**(3) On return, two comparisons, then the verdict's scope.** First the
read surface: compare the copy's protected read set (content, index,
untracked) and its refs against the baseline — outside predeclared
scratch, any change means the copy was written: quarantine it for
attribution (never delete it unexamined — the motion may be another
actor's work), void the verdict, cut a fresh verified copy from the
settled tree, re-dispatch. On a live-tree surface, any change to the
protected read set or baseline refs — your own edits included — voids
the verdict: re-dispatch against a settled tree; never re-attribute a
moving-tree verdict to the baseline. Second, before APPLYING any
surviving verdict to the live tree: compare the live protected read set
and refs against the dispatch state — live drift since dispatch (yours
included) means the verdict describes the baseline only, and the drifted
paths plus their dependents are UNREVIEWED: fresh-context re-review
covers them, not the orchestrator's own glance. Motion you did not make
is never proof the wave wrote — investigate ownership before restoring
anything (§4's edit-conflict rule protects a concurrent editor's work).

**Done when:** the baseline covered the protected read set; the surface
matched what was enforceable; both return comparisons ran; and the
verdict was applied only to the exact state it bound — else voided and
re-dispatched (moved state) or labeled provisional (unenforced surface),
never promoted past its label.
