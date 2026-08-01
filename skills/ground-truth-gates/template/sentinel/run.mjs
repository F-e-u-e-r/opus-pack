#!/usr/bin/env node
// sentinel gate — "planted fixtures never leaked" as one executable check.
// Wire-up: (1) put your shared marker in every free-form fixture value and
// list constrained-class sentinels (grammar-valid per class) in MANIFEST;
// (2) declare EVERY downstream surface in SURFACES with a loader — the
// claim is only "no verbatim occurrence in the declared surfaces over the
// retained interval", so an unqueryable declared surface is INCOMPLETE,
// never PASS; (3) run via run-all.sh. Demo mode is self-contained;
// `node run.mjs --demo-leak` shows the failing side (two-sided proof).
//
// Shape-constrained classes (hex keys, UUIDs, checksummed ids) cannot carry
// a free-text marker without leaving their grammar — give each class a
// grammar-valid sentinel and a regression elsewhere proving the fixture
// still reaches its production parser. Scans are VERBATIM-only:
// encoded/escaped copies need a representation-aware sweep.
//
// Diagnostics never republish what they guard: failure output carries the
// CLASS, a COUNT, and a source ordinal — never the sentinel value or the
// raw matched record (the boundary-diagnostic rule applies to this tool
// too); a self-check below asserts no manifest sentinel appears in this
// script's own output.

const MARKER = "SNTL7Q-"; // shared marker for free-form fixture values
const MANIFEST = [
  // one entry per planted sentinel: [class, sentinel]
  ["free-form", MARKER],
  ["hex-key", "f1c70e57"],
  ["uuid", "00000000-5e97-4000-8000-"],
];

// Declared downstream surfaces: name + loader returning lines, or null if
// the surface cannot be queried right now (-> INCOMPLETE, not PASS).
// Replace the demo loaders with reads of your real sinks, and keep the
// list synced with everywhere fixtures can propagate (logs, db exports,
// captured requests, queues) over the retention window you claim.
const CLEAN_CORPUS = [
  "ordinary log line: user login ok",
  "db row: name=Jordan Lee email=client@example.com",
];
const DEMO_LEAK = process.argv.includes("--demo-leak");
const SURFACES = [
  ["app-log", () => ["request ok", "cache warm"]],
  ["captured-requests", () => (DEMO_LEAK
    ? ["request dump: token=SNTL7Q-abc123 sent upstream"]
    : ["request dump: token=live-r3d4ct3d sent upstream"])],
];

const out = [];
const say = (s) => { out.push(s); };
let fail = 0, incomplete = 0;

// 1. collision check: no sentinel occurs in the clean corpus.
MANIFEST.forEach(([cls, s], mi) => {
  const idx = CLEAN_CORPUS.findIndex((l) => l.includes(s));
  if (idx >= 0) { say(`FAIL collision class=${cls} manifest#${mi} corpus-line#${idx}`); fail = 1; }
});
// 2. leak scan over every DECLARED surface; unqueryable -> INCOMPLETE.
for (const [name, load] of SURFACES) {
  let lines = null;
  try { lines = load(); } catch { lines = null; }
  if (!Array.isArray(lines)) { say(`INCOMPLETE surface=${name} (unqueryable)`); incomplete = 1; continue; }
  if (lines.length === 0) { say(`INCOMPLETE surface=${name} (empty read — prove the read, not just the scan)`); incomplete = 1; continue; }
  MANIFEST.forEach(([cls, s], mi) => {
    const idxs = lines.map((l, i) => (l.includes(s) ? i : -1)).filter((i) => i >= 0);
    if (idxs.length) { say(`FAIL leak class=${cls} manifest#${mi} surface=${name} count=${idxs.length} at-ordinal(s)=${idxs.join(",")}`); fail = 1; }
  });
}
// 3. self-check: this tool's own output must not republish any sentinel.
const selfLeak = MANIFEST.some(([, s]) => out.some((l) => l.includes(s)));
if (selfLeak) { say("FAIL self-check: diagnostic output republished a sentinel"); fail = 1; }

out.forEach((l) => console.log(l));
if (fail) console.log("sentinel: FAIL");
else if (incomplete) console.log("sentinel: INCOMPLETE (a declared surface was not proven)");
else console.log(`sentinel: PASS (${MANIFEST.length} sentinels; declared surfaces: ${SURFACES.map(([n]) => n).join(", ")}; verbatim-only)`);
process.exit(fail || incomplete ? 1 : 0);
