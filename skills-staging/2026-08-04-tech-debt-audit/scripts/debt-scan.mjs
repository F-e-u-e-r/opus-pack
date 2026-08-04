#!/usr/bin/env node
// debt-scan.mjs — read-only technical-debt detector for one repository.
// Zero dependencies, Node >= 18. Never prints a secret or PII value: every
// content finding is a class + location + a one-way sha256 fingerprint (8
// hex chars) plus a coarse length bucket — never a slice, prefix, suffix,
// or exact length of the matched text, so no partial disclosure survives
// either. The scan output is safe to read into an agent's context (the
// point of the tool — see SKILL.md "Why a script and not a grep").
//
//   node debt-scan.mjs <repo-dir>            scan; exit 0 clean / 1 findings / 2 error
//   node debt-scan.mjs --self-test           build clean + planted fixture trees in a
//                                            temp dir, assert PASS on clean and the
//                                            expected finding classes on planted;
//                                            exit 0 both-sided-proven / 1 failed
//
// Detection classes (each line: CLASS severity path[:line] — note):
//   VCS-MISSING     high  no .git but ignore/credential artifacts present
//   SECRET-NAME     high  credential-named file is TRACKED by git
//   SECRET-CONTENT  high  secret-shaped string in a tracked text file (masked)
//   PII-SHAPE       high  personal-data field co-occurrence in a data file
//                         (field names + counts only; values never read out)
//   BIG-BINARY      med   file over size threshold (tracked, or on-disk w/o git)
//   DEP-UNUSED      low   package.json dependency with zero hits in source+config
//   DRIFT           info  uncommitted changes in the working tree
//   SCAN-INCOMPLETE med   no-git fallback walk hit its file cap, OR a directory
//                         or file could not be read — any cause, not a full scan
//
// Declared bounds (state them when relaying results): content scans are
// verbatim-pattern only (no decoding of encoded/derived copies); PII-SHAPE is
// a shape scan — it cannot tell real from synthetic (that is a provenance
// question for the owner: security-architect, threat-model bullet); git
// HISTORY is not scanned (a burned secret needs rotation regardless —
// security-architect "Leaked / committed secret"); the password-assignment
// pattern is suppressed under test/spec/fixture paths (high false-positive
// rate there) — the other five secret patterns are not, since they match a
// fixed high-entropy format a test fixture is unlikely to reproduce.

import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";
import { createHash } from "node:crypto";

const SIZE_LIMIT = 5 * 1024 * 1024;
const TEXT_EXT = new Set([".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".py",
  ".rb", ".go", ".sh", ".bash", ".zsh", ".json", ".yaml", ".yml", ".toml",
  ".ini", ".cfg", ".conf", ".env", ".md", ".txt", ".xml", ".html", ".css"]);
const CRED_NAME = /(^|[._-])(credentials?|secrets?)(\.(json|ya?ml|toml|ini|cfg|conf|txt|xml|properties))?$|^\.env(\..+)?$|^id_(rsa|ed25519|ecdsa|dsa)$|\.(pem|p12|pfx|keystore|jks)$|^service[-_]?accounts?([._-].*)?\.json$/i;
const SECRET_PATTERNS = [
  ["aws-access-key", /\bAKIA[0-9A-Z]{16}\b/],
  ["github-token", /\bgh[pousr]_[A-Za-z0-9]{36,}\b/],
  ["api-key-like", /\bsk-[A-Za-z0-9_-]{20,}\b/],
  ["private-key-block", /-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----/],
  ["password-assignment", /(password|passwd|pwd)["']?\s*[:=]\s*["'][^"']{6,}["']/i],
  ["bearer-token", /\bBearer\s+[A-Za-z0-9_-]{24,}\b/],
];
const PLACEHOLDER = /(\byour[-_]|xxx|example|changeme|placeholder|redacted|dummy|<[^>]+>|\$\{|process\.env)/i;
// password-assignment fires on ordinary assertions ('password.length < 6',
// a fake fixture credential) at a rate the other patterns don't share — the
// other five match a fixed high-entropy FORMAT (AKIA..., gh*_..., a PEM
// header) that a test fixture is unlikely to reproduce by accident. Confine
// the noisy one to non-test paths rather than losing it everywhere.
const TEST_PATH = /(^|\/)(tests?|specs?|__tests__|__mocks__|fixtures?)(\/|$)|\.(test|spec)\.[jt]sx?$/i;
// PII field-name classes (shape scan: names of FIELDS, never values)
const PII_FIELDS = {
  "person-name": /^(full[-_ ]?name|first[-_ ]?name|last[-_ ]?name|surname|given[-_ ]?name|name)$/i,
  "gov-id": /(hkid|ssn|passport|national[-_ ]?id|id[-_ ]?(no|num|number)|identity[-_ ]?card)/i,
  "dob": /(dob|date[-_ ]?of[-_ ]?birth|birth[-_ ]?date|birthday)/i,
  "contact": /(email|e[-_]mail|phone|mobile|contact[-_ ]?no|tel)/i,
  "financial": /(account[-_ ]?(no|num|number)|iban|card[-_ ]?(no|num|number)|policy[-_ ]?(no|num|number))/i,
};

function sh(cwd, cmd, args) {
  try {
    return execFileSync(cmd, args, { cwd, encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"], maxBuffer: 64 * 1024 * 1024 });
  } catch { return null; }
}
// ZERO-character disclosure: not one byte of the matched value may appear in
// the output, in any form (no slice, no prefix/suffix, nothing derived by a
// reversible transform). A short fixed fingerprint plus a length BUCKET (not
// the exact length, which is itself a few bits of the secret) is the whole
// disclosure. sha256 needs no dependency — node:crypto is stdlib.
function mask(s) {
  const digest = createHash("sha256").update(s).digest("hex").slice(0, 8);
  const bucket = s.length < 16 ? "short" : s.length < 32 ? "medium" : "long";
  return `[fingerprint ${digest}, ${bucket}]`;
}

function scanRepo(root) {
  const findings = [];
  const add = (cls, sev, loc, note) => findings.push({ cls, sev, loc, note });

  const hasGit = fs.existsSync(path.join(root, ".git"));
  let tracked = [];
  if (hasGit) {
    const out = sh(root, "git", ["ls-files", "-z"]);
    if (out !== null) tracked = out.split("\0").filter(Boolean);
    else add("VCS-MISSING", "high", ".", "git present but ls-files failed — repo unreadable");
  } else {
    // The .gitignore-protects-nothing trap: ignore rules or credential files
    // with no version control at all (and no recovery history for the code).
    const artifacts = fs.readdirSync(root).filter(f =>
      f === ".gitignore" || CRED_NAME.test(f));
    add("VCS-MISSING", "high", ".",
      `no .git — ${artifacts.length ? "found " + artifacts.join(", ") + "; a .gitignore protects nothing here" : "no recovery history for this tree"}`);
  }

  // SECRET-NAME: credential-named files that are TRACKED (existence is fine;
  // being committed is the finding). Metadata only — contents never opened.
  for (const f of tracked) {
    if (CRED_NAME.test(path.basename(f))) {
      if (/\.(pub|example|sample|template)$/i.test(f)) continue;
      add("SECRET-NAME", "high", f, "credential-named file is tracked — untrack + rotate whatever it held");
    }
  }

  // SECRET-CONTENT + PII-SHAPE over tracked text files (or, with no git, a
  // bounded walk). Values are matched in memory and reported MASKED.
  const WALK_CAP = 2000;
  let files = tracked;
  let dirUnreadable = 0, capHit = false;
  if (!hasGit) {
    const w = walk(root, WALK_CAP);
    files = w.out;
    dirUnreadable = w.unreadable;
    capHit = w.capHit;
  }
  // A per-file read failure (permission revoked after listing, race with a
  // delete) is coverage loss exactly like an unreadable directory — folded
  // into the same SCAN-INCOMPLETE signal below rather than silently
  // continuing, which previously left a "clean" scan that had read nothing
  // from that file (measured: the same silent-swallow shape walk()'s
  // directory case was fixed for, just not yet extended to files).
  let fileUnreadable = 0;
  for (const rel of files) {
    const abs = path.join(root, rel);
    const ext = path.extname(rel).toLowerCase();
    let st; try { st = fs.statSync(abs); } catch { fileUnreadable++; continue; }
    if (!st.isFile()) continue;
    if (st.size > SIZE_LIMIT)
      add("BIG-BINARY", "med", rel,
        `${(st.size / 1048576).toFixed(1)} MB ${hasGit ? "tracked" : "on disk (no .git — see VCS-MISSING)"}`);
    if (!TEXT_EXT.has(ext) || st.size > 2 * 1024 * 1024) continue;
    let text; try { text = fs.readFileSync(abs, "utf8"); } catch { fileUnreadable++; continue; }

    if (!CRED_NAME.test(path.basename(rel))) { // named files already flagged whole
      const lines = text.split("\n");
      const inTestPath = TEST_PATH.test(rel);
      for (let i = 0; i < lines.length; i++) {
        for (const [cls, re] of SECRET_PATTERNS) {
          if (cls === "password-assignment" && inTestPath) continue;
          const m = lines[i].match(re);
          if (m && !PLACEHOLDER.test(lines[i]))
            add("SECRET-CONTENT", "high", `${rel}:${i + 1}`, `${cls}: ${mask(m[0])}`);
        }
      }
    }

    // PII-SHAPE: JSON data files — classify FIELD NAMES, count rows, report
    // no values. Untagged hits are presumed real until the owner says
    // otherwise (the scan sees shape, not provenance).
    if (ext === ".json") {
      let doc; try { doc = JSON.parse(text); } catch { continue; }
      const rows = Array.isArray(doc) ? doc : [doc];
      const classes = new Map();
      for (const row of rows.slice(0, 200)) collectPII(row, classes, 0);
      const hit = [...classes.entries()].filter(([, n]) => n > 0);
      const strong = hit.filter(([c]) => c !== "contact");
      if (strong.length >= 2 || (strong.length === 1 && hit.length >= 2))
        add("PII-SHAPE", "high", rel,
          hit.map(([c, n]) => `${c}×${n}`).join(", ") +
          " — presumed real until owner confirms synthetic");
    }
  }

  // SCAN-INCOMPLETE fires on any of three independent causes — the no-git
  // walk's file cap, a directory it could not read, or a FILE it could not
  // read (permission revoked after listing, race with a delete) — reported
  // together so a reader sees every reason coverage is partial, not just
  // whichever one a message ternary happened to pick.
  if (capHit || dirUnreadable > 0 || fileUnreadable > 0) {
    const reasons = [];
    if (dirUnreadable > 0) reasons.push(`${dirUnreadable} directory(ies) unreadable`);
    if (fileUnreadable > 0) reasons.push(`${fileUnreadable} file(s) unreadable`);
    if (capHit) reasons.push(`hit its ${WALK_CAP}-file cap with directories still unexplored`);
    add("SCAN-INCOMPLETE", "med", ".",
      `scan did not cover the whole tree (${reasons.join(", ")}) — ` +
      `${hasGit ? "re-scan after fixing permissions for full coverage" : "git init and re-scan for full coverage"}`);
  }

  // DEP-UNUSED: declared dependencies with zero import/require hits.
  const pkgPath = path.join(root, "package.json");
  if (fs.existsSync(pkgPath)) {
    let pkg; try { pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8")); } catch { pkg = null; }
    const deps = pkg ? Object.keys(pkg.dependencies || {}) : [];
    if (deps.length) {
      // Corpus includes config files (.eslintrc.json, .babelrc, vite.config,
      // etc.), not just source — a dep referenced only from a plugin/extends
      // list in config, never imported from code, is still used. package.json
      // itself is excluded (the dependency's own declaration would trivially
      // "find" it). Extension-LESS build/CI filenames (Makefile, Dockerfile,
      // Jenkinsfile, ...) are matched by basename, not extension — a plain
      // `path.extname` filter drops them entirely (measured: a dep invoked
      // only from a Makefile recipe was missed and false-flagged unused
      // before this line existed). Covers GNU Make's own lowercase
      // `makefile` variant (Make's default search order is GNUmakefile,
      // makefile, Makefile — a plain `Makefile`-only match missed it,
      // measured the same way) and Dockerfile's common suffixed forms
      // (`Dockerfile.dev`, `Dockerfile.prod`).
      const EXTLESS_CONFIG = /^(Makefile|makefile|GNUmakefile|Dockerfile(\.[\w.-]+)?|Jenkinsfile|Rakefile|Procfile|Vagrantfile)$/;
      const srcs = files.filter(f => {
        const base = path.basename(f);
        if (base === "package.json" || base === "package-lock.json") return false;
        if (EXTLESS_CONFIG.test(base)) return true;
        const ext = path.extname(f).toLowerCase();
        return /\.(m?[jt]sx?|cjs)$/.test(f) || (TEXT_EXT.has(ext) && ext !== "" && !/\.(md|txt)$/.test(f));
      });
      const corpus = srcs.map(f => {
        try { return fs.readFileSync(path.join(root, f), "utf8"); } catch { return ""; }
      }).join("\n");
      // A prefix-only check ("`\"${d}`") is wrong in BOTH directions: it
      // misses "plugin:my-plugin/recommended" (the name doesn't immediately
      // follow the quote) and it false-hits "react" inside the unrelated
      // "react-native-paper" (a substring, not a reference). Require a real
      // token boundary on both sides instead — neither neighbor character
      // may be an identifier-ish char (letter/digit/./-/_), which still lets
      // ':' and '/' stand as valid boundaries (covers "plugin:x/y" and
      // scoped "@org/x" forms) without matching inside a longer name.
      const escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      for (const d of deps) {
        const re = new RegExp(`(^|[^A-Za-z0-9_.-])${escapeRe(d)}($|[^A-Za-z0-9_.-])`);
        if (!re.test(corpus))
          add("DEP-UNUSED", "low", "package.json",
            `"${d}" declared, zero hits across ${srcs.length} source+config files ` +
            `(confirm before removing — CLI-only or dynamic-import use can still miss this scan)`);
      }
    }
  }

  // DRIFT
  if (hasGit) {
    const st = sh(root, "git", ["status", "--porcelain"]);
    const n = st ? st.split("\n").filter(Boolean).length : 0;
    if (n > 0) add("DRIFT", "info", ".", `${n} uncommitted change(s)`);
  }
  return findings;
}

function collectPII(obj, classes, depth) {
  if (depth > 3 || typeof obj !== "object" || obj === null) return;
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v === "string" && v.trim() && !PLACEHOLDER.test(v)) {
      for (const [cls, re] of Object.entries(PII_FIELDS))
        if (re.test(k)) classes.set(cls, (classes.get(cls) || 0) + 1);
    } else if (typeof v === "object") collectPII(v, classes, depth + 1);
  }
}

// Returns { out, truncated }. `truncated` means coverage is NOT complete —
// either the cap cut the walk short (unexplored directories remain on the
// stack when the loop exits — NOT "out.length happens to equal cap", which
// a tree with exactly `cap` files, fully covered, would also satisfy: `cap`
// is a coverage bound, not a strict output-size bound, since the cap check
// runs only between directories and one very large directory can push `out`
// well past `cap` in a single atomic step while still completing full
// coverage) — OR a directory could not be read at all (permission denied,
// race with a delete). A silently-skipped unreadable directory is coverage
// loss exactly like a cap cutoff: measured directly — a `chmod 000` subtree
// was dropped with zero signal before this counter existed, so the scan
// reported "complete" while having read nothing under it. Both causes fold
// into the same `truncated` flag; the report line does not need to
// distinguish cap-cutoff from read-error to tell the caller "not complete".
function walk(root, cap) {
  const out = [];
  const stack = ["."];
  let unreadable = 0;
  while (stack.length && out.length < cap) {
    const d = stack.pop();
    let entries;
    try { entries = fs.readdirSync(path.join(root, d), { withFileTypes: true }); }
    catch { unreadable++; continue; }
    for (const e of entries) {
      if (e.name === "node_modules" || e.name === ".git" || e.name.startsWith(".DS_")) continue;
      const rel = d === "." ? e.name : path.join(d, e.name);
      if (e.isDirectory()) stack.push(rel);
      else out.push(rel);
    }
  }
  const capHit = stack.length > 0;
  return { out, truncated: capHit || unreadable > 0, unreadable, capHit };
}

function report(findings) {
  const order = { high: 0, med: 1, low: 2, info: 3 };
  findings.sort((a, b) => order[a.sev] - order[b.sev] || a.cls.localeCompare(b.cls));
  for (const f of findings)
    console.log(`${f.cls.padEnd(14)} ${f.sev.padEnd(4)} ${f.loc} — ${f.note}`);
  const actionable = findings.filter(f => f.sev !== "info").length;
  console.log(`debt-scan: ${actionable} actionable finding(s), ${findings.length} total ` +
    `(bounds: verbatim patterns, tracked files, no history scan)`);
  return actionable ? 1 : 0;
}

// ---------------- self-test: two-sided proof ----------------
function selfTest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "debt-scan-"));
  const mk = (dir, rel, content) => {
    const p = path.join(dir, rel);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, content);
  };
  const git = (dir, ...a) => execFileSync("git", ["-C", dir, ...a],
    { stdio: ["ignore", "pipe", "pipe"], env: { ...process.env,
      GIT_AUTHOR_NAME: "t", GIT_AUTHOR_EMAIL: "t@t", GIT_COMMITTER_NAME: "t",
      GIT_COMMITTER_EMAIL: "t@t" } });

  // CLEAN tree: git repo, env.example with placeholders, synthetic-tagged
  // fixture, two "used" dependencies — one imported from source, one
  // referenced ONLY from an extension-less Makefile recipe (regression
  // fixture: a real repro found this dep false-flagged DEP-UNUSED before
  // extension-less basenames were added to the corpus) — plus committed
  // state.
  const clean = path.join(tmp, "clean");
  fs.mkdirSync(clean); git(clean, "init", "-q");
  mk(clean, ".env.example", "API_KEY=your-key-here\n");
  mk(clean, "src/index.js", "const dayjs = require('dayjs');\nmodule.exports = dayjs;\n");
  // Regression fixtures for two naming-convention gaps round-3 review found
  // in the extension-less corpus match: GNU Make's own lowercase `makefile`
  // variant (used here instead of `Makefile` — the two names collide on a
  // case-insensitive filesystem like the default macOS one, so only one can
  // exist in this fixture tree; the regex covers both spellings, this just
  // exercises the lowercase one directly), and Dockerfile's suffixed forms.
  mk(clean, "makefile", "build:\n\tesbuild src/index.js --bundle\n\nlint:\n\twrangler lint\n");
  mk(clean, "Dockerfile.dev", "RUN npx nodemon --version\n");
  mk(clean, "package.json", JSON.stringify({ name: "clean", dependencies: {
    dayjs: "^1", esbuild: "^1", wrangler: "^1", nodemon: "^1" } }));
  mk(clean, "fixtures/case.json", JSON.stringify([{ name: "SNTL7Q-Jordan Lee", note: "synthetic" }]));
  git(clean, "add", "-A"); git(clean, "commit", "-qm", "init");
  const cleanFindings = scanRepo(clean).filter(f => f.sev !== "info");

  // PLANTED tree: every class armed.
  const planted = path.join(tmp, "planted");
  fs.mkdirSync(planted); git(planted, "init", "-q");
  mk(planted, "credentials.json", JSON.stringify({ user: "agent", password: "SNTL7Q-realpass99" }));
  mk(planted, "src/app.js", 'const key = "AKIA' + "ABCDEFGHIJKLMNOP" + '";\nconst x = require("left-pad");\n');
  mk(planted, "package.json", JSON.stringify({ name: "p", dependencies: { "left-pad": "^1", "never-used-dep": "^2" } }));
  mk(planted, "examples/joint.json", JSON.stringify([{ fullName: "SNTL7Q-A", hkid: "Z123456", dob: "1990-01-01" }]));
  mk(planted, "assets/blob.bin", Buffer.alloc(SIZE_LIMIT + 1024).toString("base64"));
  git(planted, "add", "-A"); git(planted, "commit", "-qm", "init");
  mk(planted, "scratch.txt", "uncommitted\n"); // DRIFT
  const noGit = path.join(tmp, "nogit");
  fs.mkdirSync(noGit);
  mk(noGit, ".gitignore", "credentials.json\n");
  mk(noGit, "credentials.json", "{}");
  const plantedFindings = scanRepo(planted);
  const noGitFindings = scanRepo(noGit);

  // UNREADABLE-DIR regression fixture: a no-git tree with a directory
  // chmod'd unreadable. Real repro found this silently swallowed by
  // walk()'s `catch { continue }` — the scan reported clean coverage while
  // having read nothing under that subtree. Root ignores permission bits,
  // so this check is skipped (not failed) when running as root — that is
  // an environment limit of the check, not evidence the fix works there.
  let unreadableOK = "skipped (running as root — permission bits are not enforced)";
  if (typeof process.getuid !== "function" || process.getuid() !== 0) {
    const permTree = path.join(tmp, "permtree");
    mk(permTree, "open/a.txt", "hi\n");
    mk(permTree, "locked/b.txt", "blocked\n");
    fs.chmodSync(path.join(permTree, "locked"), 0o000);
    const permFindings = scanRepo(permTree);
    fs.chmodSync(path.join(permTree, "locked"), 0o755); // restorable before cleanup
    const fired = permFindings.some(f => f.cls === "SCAN-INCOMPLETE" && /unreadable/.test(f.note));
    unreadableOK = fired ? "PASS (SCAN-INCOMPLETE fired on the unreadable dir)"
      : "FAIL — unreadable directory was silently swallowed: " + JSON.stringify(permFindings);
  }

  // UNREADABLE-FILE regression fixture: same silent-swallow shape as the
  // directory case, but on a file's own statSync/readFileSync — round-3
  // review found this still unfixed after the directory case was closed.
  let unreadableFileOK = "skipped (running as root — permission bits are not enforced)";
  if (typeof process.getuid !== "function" || process.getuid() !== 0) {
    const fileTree = path.join(tmp, "filetree");
    mk(fileTree, "open.txt", "hi\n");
    mk(fileTree, "locked.txt", "password = 'SNTL7Q-shouldnotmatter'\n");
    fs.chmodSync(path.join(fileTree, "locked.txt"), 0o000);
    const fileFindings = scanRepo(fileTree);
    fs.chmodSync(path.join(fileTree, "locked.txt"), 0o644); // restorable before cleanup
    const fired = fileFindings.some(f => f.cls === "SCAN-INCOMPLETE" && /file\(s\) unreadable/.test(f.note));
    unreadableFileOK = fired ? "PASS (SCAN-INCOMPLETE fired on the unreadable file)"
      : "FAIL — unreadable file was silently swallowed: " + JSON.stringify(fileFindings);
  }

  const got = new Set(plantedFindings.map(f => f.cls));
  const expect = ["SECRET-NAME", "SECRET-CONTENT", "PII-SHAPE", "BIG-BINARY", "DEP-UNUSED", "DRIFT"];
  const missed = expect.filter(c => !got.has(c));
  const cleanOK = cleanFindings.length === 0;
  const noGitOK = noGitFindings.some(f => f.cls === "VCS-MISSING");

  // Containment must be checked against the secret this suite actually
  // CONTENT-SCANS (the AKIA key in src/app.js) — credentials.json's password
  // is structurally unreachable by the content-scan path (CRED_NAME files are
  // flagged whole, never opened), so testing only that value proves nothing
  // about mask(). Check every run of 6+ chars from BOTH planted secrets, not
  // just full-string containment, so a partial leak (a slice, not the whole
  // value) still fails the assertion.
  const report = JSON.stringify(plantedFindings);
  const secrets = ["AKIA" + "ABCDEFGHIJKLMNOP", "SNTL7Q-realpass99"];
  const leakedRun = secrets.flatMap(sec => {
    const hits = [];
    for (let i = 0; i + 6 <= sec.length; i++) {
      const run = sec.slice(i, i + 6);
      if (report.includes(run)) hits.push(run);
    }
    return hits;
  });
  const leak = leakedRun.length > 0;

  console.log(`clean tree: ${cleanOK ? "PASS (0 actionable)" : "FAIL — " + JSON.stringify(cleanFindings)}`);
  console.log(`planted tree: ${missed.length === 0 ? "all 6 classes fired" : "MISSED " + missed.join(",")}`);
  console.log(`no-git tree: ${noGitOK ? "VCS-MISSING fired" : "FAIL"}`);
  console.log(`extension-less config dep (Makefile/makefile/Dockerfile.dev): ${cleanOK ? "PASS (esbuild/wrangler/nodemon not false-flagged unused)" : "see clean-tree FAIL above"}`);
  console.log(`unreadable directory: ${unreadableOK}`);
  console.log(`unreadable file: ${unreadableFileOK}`);
  console.log(`value containment: ${leak
    ? "FAIL — leaked runs " + JSON.stringify([...new Set(leakedRun)])
    : "PASS (no 6+ char run of either planted secret appears in output)"}`);
  fs.rmSync(tmp, { recursive: true, force: true });
  const unreadableFailed = typeof unreadableOK === "string" && unreadableOK.startsWith("FAIL");
  const unreadableFileFailed = typeof unreadableFileOK === "string" && unreadableFileOK.startsWith("FAIL");
  const ok = cleanOK && missed.length === 0 && noGitOK && !leak && !unreadableFailed && !unreadableFileFailed;
  console.log(`self-test: ${ok ? "PASS (two-sided + containment)" : "FAIL"}`);
  return ok ? 0 : 1;
}

const arg = process.argv[2];
if (!arg) { console.error("usage: debt-scan.mjs <repo-dir> | --self-test"); process.exit(2); }
process.exit(arg === "--self-test" ? selfTest() : report(scanRepo(path.resolve(arg))));
