#!/usr/bin/env node
// Golden gate: measures a judgment step (classify / extract / route) against
// hand-labeled ground truth. Exits 0 iff accuracy >= --min (default 0.85).
//
// Wire-up (details in the ground-truth-gates SKILL.md):
//   1. Replace cases.jsonl with 30-50 REAL hand-labeled examples,
//      one {"input": ..., "label": ...} per line. Tiny sets are gameable.
//   2. Replace classify() with a call to your real system (API call, CLI,
//      imported function). Keep it deterministic for a given input.
//   3. Set MIN_DEFAULT below to the bar your team holds — run-all.sh (and any
//      hook/CI built on it) enforces MIN_DEFAULT. `--min` overrides ad hoc only.
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MIN_DEFAULT = 0.85; // the team's bar; enforced by run-all.sh

const here = dirname(fileURLToPath(import.meta.url));
const minArg = process.argv.indexOf('--min');
const min = minArg === -1 ? MIN_DEFAULT : Number(process.argv[minArg + 1]);

// REPLACE ME with the real judgment step under test.
async function classify(input) {
  return /refund|charged|invoice|billing/i.test(input) ? 'billing' : 'general';
}

const cases = readFileSync(join(here, 'cases.jsonl'), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line));

if (cases.length === 0) {
  console.error('golden: cases.jsonl is empty — refusing to score nothing');
  process.exit(1);
}

const misses = [];
for (const c of cases) {
  const got = await classify(c.input);
  if (got !== c.label) misses.push({ input: c.input, expected: c.label, got });
}

const correct = cases.length - misses.length;
const accuracy = correct / cases.length;
console.log(`golden: ${correct}/${cases.length} correct (${accuracy.toFixed(3)}), min ${min}`);
for (const m of misses.slice(0, 10)) {
  console.log(`  MISS ${JSON.stringify(m.input)} expected=${m.expected} got=${m.got}`);
}
if (misses.length > 10) console.log(`  ... ${misses.length - 10} more misses`);

process.exit(accuracy >= min ? 0 : 1);
