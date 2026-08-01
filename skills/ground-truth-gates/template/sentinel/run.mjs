#!/usr/bin/env node
// sentinel gate — "planted fixtures never leaked" as one executable check.
// Wire-up: (1) put your shared marker in every free-form fixture value and
// list constrained-class sentinels (grammar-valid per class) in MANIFEST;
// (2) point ARTIFACTS at the real downstream surfaces (log dumps, db
// exports, captured requests); (3) run via run-all.sh. Demo mode is
// self-contained; `node run.mjs --demo-leak` shows the failing side
// (two-sided proof that the gate can go red).
//
// Shape-constrained classes (hex keys, UUIDs, checksummed ids) cannot carry
// a free-text marker without leaving their grammar — give each class a
// grammar-valid sentinel (a fixed hex prefix, a reserved UUID stem) and a
// regression elsewhere proving the fixture still reaches its production
// parser. Scan claims are VERBATIM-only: encoded/escaped copies need a
// representation-aware sweep (add the encodings your pipeline applies).

const MARKER = "SNTL7Q-"; // shared marker for free-form fixture values
const MANIFEST = [
  // one entry per planted sentinel: [class, sentinel, note]
  ["free-form", MARKER, "prefix on every free-text fixture value"],
  ["hex-key", "f1c70e57", "grammar-valid hex stem planted in synthetic keys"],
  ["uuid", "00000000-5e97-4000-8000-", "reserved UUID stem for fixture ids"],
];

// Replace with reads of your real downstream artifacts.
const CLEAN_CORPUS = [
  "ordinary log line: user login ok",
  "db row: name=Jordan Lee email=client@example.com",
];
const ARTIFACTS = process.argv.includes("--demo-leak")
  ? ["request dump: token=SNTL7Q-abc123 sent upstream"] // failing side
  : ["request dump: token=live-r3d4ct3d sent upstream"];

let fail = 0;
// 1. collision check: no sentinel occurs in the clean corpus (safe to plant
//    for THIS suite — a corpus check, not a proof about all content).
for (const [cls, s] of MANIFEST) {
  const hit = CLEAN_CORPUS.find((l) => l.includes(s));
  if (hit) { console.log(`FAIL collision ${cls}: "${s}" occurs naturally`); fail = 1; }
}
// 2. leak scan: zero verbatim hits across downstream artifacts; the input
//    set must be non-empty (a zero-input scan is a vacuous green).
if (ARTIFACTS.length === 0) { console.log("FAIL: artifact set empty"); fail = 1; }
for (const [cls, s] of MANIFEST) {
  const hits = ARTIFACTS.filter((l) => l.includes(s));
  if (hits.length) { console.log(`FAIL leak ${cls}: ${hits.length} hit(s), e.g. "${hits[0]}"`); fail = 1; }
}
console.log(fail ? "sentinel: FAIL" : `sentinel: PASS (${MANIFEST.length} sentinels, ${ARTIFACTS.length} artifacts, verbatim-only)`);
process.exit(fail);
