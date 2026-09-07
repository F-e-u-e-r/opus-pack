# c12 orientation — pre-committed expectations (written before probe results)

Probe A (two-level spawn, inert):
- E1 Agent tool visible to general-purpose child: EXPECT yes (harness type def Tools:*)
- E2 child can actually spawn grandchild: EXPECT succeed (no documented depth cap;
  listing-not-callable lesson demands the real call)
- E3 grandchild visibility to orchestrator: EXPECT none except via child's own report
Observed so far: E1 yes; E2 SUCCEEDED (child reported spawn success + running);
E3 confirmed PLUS stronger-than-expected: harness default-backgrounds the child's
Agent call, child returned while grandchild still running (orphan-principal window).
Awaiting child's final 4-line report.

Doctrine reading notes: see ANALYSIS.md

FINAL probe result (child's 4-line report, second turn):
AGENT-TOOL-VISIBLE: yes / GRANDCHILD-SPAWN: succeeded /
GRANDCHILD-REPLY: "Agent still running — no completion notification received" /
SELF-MODEL: claude-haiku-4-5-20251001
=> E1/E2/E3 all as expected; BONUS: orphan window confirmed live — grandchild
result consumed by nobody unless someone re-resumes the child; orchestrator
holds no handle to the grandchild at all. Probe closed (no further resumes —
spawn-accepted fact established; grandchild completion is itself the
orphan-window evidence).
