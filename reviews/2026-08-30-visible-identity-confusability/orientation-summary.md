# ⑥ Homoglyph / visible-identity-deception — ORIENTATION (read-only, first-hand)

Repo zero bytes. HEAD 0913e4b (post-⑤). Harness: h_probe.py + h_result.json; the
shipped-regex cross-check re-runs .github/checks.py's own BAD pattern.

## 1. Runtime
macOS 26.5.2 arm64 (darwin); CPython 3.9.6 (/usr/bin/python3); `unicodedata`
Unicode DB **13.0.0**. Version caveat: the confusables/scripts landscape grows with
Unicode releases, but the *mechanism* (distinct code points, confusable glyphs,
cross-script non-normalization) is version-stable; nothing here depends on 13.0.

## 2. H1–H10 (all matched pre-registered expectations)
| H | fixture | key first-hand facts | reading |
|---|---|---|---|
| H1 MIXED-SCRIPT-ID | `paypal` vs `pаypal` (Cyrillic а U+0430) | distinct code points; **shipped invisible sweep: clean**; skeleton→`paypal` collides; mixes scripts in-token | visible homoglyph survives the sweep |
| H2 CONFUSABLE-COLLISION | `scope` vs `scоpe` (Cyrillic о) | two distinct identities, same rendered glyphs; sweep clean; skeleton collision | strongest shape: identity collision |
| H3 HOST/AUTHORITY | `trusted.example` vs `trustеd.example` (Cyrillic е) | text-only compare, **no network**; sweep clean; collides | ⑥ reaches external authority identity |
| H4 PATH/CONFIG-KEY | `authToken` vs `аuthToken` | fixture strings only; sweep clean; collides | ⑥ reaches config/path tokens |
| H5 LEGIT-MULTILINGUAL | `привет` (pure Cyrillic) | single script; not confusable-with any ASCII token | **must NOT hit** — rule ≠ "non-ASCII bad" |
| H6 ACCENTED-LATIN | `café`, `Straße` | pure Latin script; sweep clean; no collision | **CLEAR** — rule ≠ ASCII-only |
| H7 MIXED-NOT-CONFUSABLE | `user名前` (Latin+CJK) | mixes scripts True, confusable False | mixed-script alone ≠ block |
| H8 INVISIBLE-ORTHOGONAL | ZWSP, RLO | **shipped sweep: HIT both** | existing invisible rule owns it; ⑥ orthogonal |
| H9 NORMALIZATION | `ﬁle`(U+FB01) vs `file`; Cyrillic `а` vs `a` | NFKC folds the ligature (True); **does NOT fold Cyrillic→Latin (False)** | normalization = partial support, not a solution |
| H10 SECURITY-RELEVANCE | same confusable in decorative prose vs a `trustedCommands` entry | identical confusable signal; only the boundary differs | severity by boundary → L2, not mere presence |

Cross-check vs the **shipped** `.github/checks.py` BAD regex: H1–H4 homoglyphs all
**clean** (no hit); H8 invisibles both **hit**. My reimplementation == shipped.

## 3. Current coverage map (what exists; none compares glyph-vs-codepoint identity)
- **skill-vetting §2 "Invisible-Unicode smuggling"** — grep over hidden-directive
  ranges (U+200B–200F, 202A–202E, 2066–2069, 2060, 061C, FEFF, 00AD, E0000–E007F).
  Explicitly *"Unicode that can hide directives"* = **concealment**.
- **op-rigor §2 instruction-files bullet** — same sweep, same framing.
- **.github/checks.py check 4** — the BAD regex over all tracked text = CI hygiene.
- **full-source read (sv §1 step 3)** — reads every character; **no** obligation to
  compare rendered glyph vs code-point / expected canonical identity.
- **whole-tree digest** — bytes identity only.
Every "identity/rendered" hit elsewhere in skills/ is UI-render / effect
verification (delegation-and-review, domain-evidence), unrelated to token identity.
`grep homoglyph|confusab|mixed-script|glyph|impersonat = 0` across skills/.

## 4. Fully-compliant false-clear
A candidate SKILL.md declares `trustedCommands: ["scоpe"]` (Cyrillic о), intending
to shadow the trusted ASCII tool `scope`. Reviewer runs the procedure verbatim:
1. opening digest taken; 2. **full-source read** — the entry renders as `scope`,
looks correct; 3. **invisible-Unicode sweep** — CLEAN (shipped BAD regex, first-hand
no hit); 4. **checklist** — no hit (no homoglyph/confusable criterion exists);
5. **fixture** — promised behavior green (the allow-list parses and behaves);
6. **closing digest** matches. Verdict: SAFE-TO-PROPOSE. Yet the granted token is a
**distinct identity** from the trusted `scope`; the reviewer trusted visual sameness
because no rule required comparing code-point / canonical identity. (Pure ⑥: a
*narrow, exact-looking* grant — ③ breadth is not triggered.)

## 5. Disposition — **C. GENUINE-DISTINCT-GAP**
The visible-impersonation mechanism is orthogonal to concealment (H8 hits the sweep;
H1–H4 do not), and **no existing rule carries the identity-deception principle**:
invisible = concealment; exfil = a secret carried in an address/label (a confusable
host carrying *no* secret is not an exfil hit); fabricated-authority = a semantic
claim; full-source = read-not-compare; digest = bytes. Unlike ⑤ (which was B because
security-architect already stated the correspondence *principle* and only the
trigger was missing), ⑥ has **no pre-existing principle** to operationalize — the
"don't trust visual sameness; verify code-point identity" obligation exists nowhere.
Honest nuance for owner adjudication: ⑥ is *adjacent* to the invisible-Unicode rule
as a member of the same "Unicode-deception" threat family (cf. SkillSpector TP2), so
one could argue B if that rule is read as an umbrella principle — but mechanically
the two are orthogonal and no wording states the identity-comparison obligation, so
**C** is the more accurate call.

## 6. Abstraction — **L2** (minimal sufficient)
- **L1 (homoglyph char presence → finding):** over-fires — H5/H6/H7 would falsely
  hit. Rejected.
- **L2 (security-relevant identity confusability):** a finding only when distinct
  code-point strings visually impersonate each other **at an identity-decision
  boundary** (name/identifier/command/path/host/tool/config-key). Catches H1–H4 +
  H10-grant; clears H5/H6/H7 + H10-prose. **Selected.**
- **L3 (general Unicode/identifier-security framework — scripts, IDNA/punycode,
  normalization, font/locale):** a whole Unicode-security project; breaks tranche
  boundedness. **Recorded, NOT activated.**

## 7. Minimal invariant + carve-outs (design CANDIDATE, not approved wording)
> Do not trust visual sameness as identity. Where a security decision depends on a
> name, identifier, command, path, host, tool, configuration key, or other
> authority-bearing token, compare the actual code points / canonical identity
> rather than the rendered glyphs. A visually confusable alternate that can be
> mistaken for a different trusted or reviewed identity is a finding; ordinary
> non-ASCII or multilingual text is not a finding merely for being Unicode.

Carve-outs: (i) pure multilingual (H5) not a finding; (ii) accented/ordinary Latin
(H6) not a finding; (iii) mixed-script without plausible impersonation of a trusted
token (H7) not auto-blocked; (iv) invisible/bidi stays with the existing invisible
rule (⑥ does not re-own; may co-fire); (v) NFKC folding (H9) is supporting evidence
for compatibility cases but does NOT resolve cross-script homoglyphs; (vi) severity
scales with the security-relevance of the boundary (H10: grant token ≫ decorative
prose). Criterion = **distinct identity + plausible visual impersonation +
security-relevant boundary**, NOT "ban homoglyphs".

## 8. Canonical-home recommendation
Provisional: **op-rigor §2 canonical (a semantic sibling limb beside the
invisible-Unicode sweep, under "Instruction files are executable content") +
skill-vetting §2 bare pointer/mirror** — same split the invisible sweep already uses
(it lives in both, kept in sync). Altitude note: ⑥ is a review-time SEMANTIC
comparison obligation, not a range-grep, so its op-rigor wording must read as an
obligation, not a character class. Alternative (skill-vetting-only) is viable if the
owner prefers to keep op-rigor's Unicode presence purely mechanical; compare carrier
altitude at design time.

## 9. Dedup (each distinct; a pure-⑥ case for each)
- **Invisible-Unicode:** concealment (bytes hidden/redirected) vs ⑥ visible
  impersonation. H8 hits the sweep; H1–H4 do not. Can co-fire, cannot substitute.
- **Fabricated authority / self-vouching:** a *semantic* false claim ("official").
  Pure-⑥ (`scоpe` grant token) carries no authority claim yet still deceives. Distinct.
- **Exfiltration channels:** requires a secret carried in address/payload/metadata/
  presence. A confusable **recipient host with no secret** (H3) is not an exfil hit
  but is ⑥. Distinct.
- **Full-source read:** reads every char ≠ code-point-aware identity verification.
- **Whole-tree digest:** bytes identity ≠ reviewer understanding the visible identity.
- **③ trust-grant breadth:** ③ judges the grant *set breadth*; ⑥ asks whether the
  *name* impersonates another identity. `trustedCommands:["scоpe"]` can be an exact,
  narrow grant (③ clean) and still be ⑥.

## 10. Scanner necessity — **SUPPORTING-ONLY**
High-confidence **mixed-script-within-a-security-token** collision (H1–H4: >1 script
in one identifier, or skeleton-collision with a known trusted token) is mechanically
cheap and could be supporting evidence. But general homoglyph detection needs the
full TR39 confusables table **and context** — H5/H6/H7 show pure-multilingual /
accented / legit-mixed content must NOT fire, and H10 shows severity depends on the
security-relevance of the boundary. A generic whole-repo CI scanner would
false-positive heavily on legitimate Unicode. → the canonical decision is a
**review-time semantic comparison obligation**; a scanner is **supporting evidence,
not the canonical decision-maker**. No tooling written this round.

## 11. Broader Unicode-security discoveries (recorded, NOT activated)
IDNA/punycode homograph domains; script-specific & restriction-level (TR39)
frameworks; font/locale-dependent spoofing; normalization beyond NFKC; whole
identifier-security tooling. = the L3 project; deliberately not started.

## Queue
③ SHIPPED → ⑤ SHIPPED → ⑥ ORIENTATION DONE (C / L2, awaiting adjudication) →
④ LOCKED → ⑧ LATER-top. Repo zero bytes; no design gate; STOP.
