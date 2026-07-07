#!/usr/bin/env node
// Replay gate: detects behavior drift of transform() over real logged inputs.
//
//   node replay/run.mjs --update   freeze current behavior as the snapshot
//   node replay/run.mjs            compare current behavior to the snapshot;
//                                  0 diffs = safe, any diff = exact records that moved
//
// Wire-up: replace corpus.jsonl with a representative sample of real logged
// inputs ({"input": ...} per line), and transform() with the step you are
// changing (parser, regex, prompt post-processor). Deterministic per input.
// Re-run --update ONLY after eyeballing an intended behavior change.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const snapshotPath = join(here, 'snapshot.jsonl');
const update = process.argv.includes('--update');

// REPLACE ME with the step under change.
async function transform(input) {
  return input.trim().toLowerCase().replace(/\s+/g, ' ');
}

const corpus = readFileSync(join(here, 'corpus.jsonl'), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line));

if (corpus.length === 0) {
  console.error('replay: corpus.jsonl is empty — refusing to freeze or compare nothing');
  process.exit(1);
}

const results = [];
for (const c of corpus) {
  results.push({ input: c.input, output: await transform(c.input) });
}

if (update) {
  writeFileSync(snapshotPath, results.map((r) => JSON.stringify(r)).join('\n') + '\n');
  console.log(`replay: snapshot frozen (${results.length} records)`);
  process.exit(0);
}

if (!existsSync(snapshotPath)) {
  console.error('replay: no snapshot found — run `node replay/run.mjs --update` to freeze current behavior first');
  process.exit(1);
}

const frozen = readFileSync(snapshotPath, 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line));

const diffs = [];
const n = Math.max(frozen.length, results.length);
for (let i = 0; i < n; i++) {
  const before = frozen[i];
  const after = results[i];
  if (JSON.stringify(before) !== JSON.stringify(after)) {
    diffs.push({ index: i, input: after?.input ?? before?.input, before: before?.output, after: after?.output });
  }
}

console.log(`replay: ${results.length} records, ${diffs.length} diffs vs snapshot`);
for (const d of diffs.slice(0, 10)) {
  console.log(`  DIFF #${d.index} ${JSON.stringify(d.input)}`);
  console.log(`    before: ${JSON.stringify(d.before)}`);
  console.log(`    after:  ${JSON.stringify(d.after)}`);
}
if (diffs.length > 10) console.log(`  ... ${diffs.length - 10} more diffs`);

process.exit(diffs.length === 0 ? 0 : 1);
