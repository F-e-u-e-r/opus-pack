# Third-Party Notices

Opus Pack is released under the MIT License (see `LICENSE`). It incorporates,
adapts, or draws ideas from the third-party works listed below. This file
preserves the copyright and permission notices those upstream licenses require
to travel with the code. Narrative provenance — including idea-level sources
that impose no license obligation — is in `README.md`
("Provenance and acknowledgements"); this file is the canonical legal notice.

Where upstream license files were available, copyright holders and licenses
were checked against those files on 2026-07-07; otherwise they are credited
from the source material available at review time. Every incorporated code
lineage known to this pack terminates in the MIT License; no known copyleft
(GPL/AGPL/LGPL) obligation exists in the chain.

---

## 1. Works under the MIT License

The MIT License text reproduced in Section 3 applies to each of the following
works. Their original copyright notices are:

### Curtis Chou — `curtischoutw/claude-institution` (@ `8dea062`)

```
Copyright (c) 2026 Curtis Chou
```

- **How used:** `hooks/verify-before-stop.py` is a derivative work of
  that project's `verify_gate.py` (detection logic preserved; messages
  rewritten). Approximately ten judgment rules were also absorbed into the
  `operational-rigor`, `delegation-and-review`, and `skill-authoring` skills.
- This is the strongest obligation in this file: a substantial portion of the
  hook is derived from MIT-licensed code, so this notice must ship with it.

### Miguok — `Miguok/fable-harness`

```
Copyright (c) 2026 Miguok
```

- **How used:** upstream of the above — Curtis Chou's `verify_gate.py` was
  itself adapted from this project. Listed to keep the full code lineage of
  `verify-before-stop.py` intact. Also MIT, so the chain carries no additional
  obligations beyond notice retention.

### Darko Tomic — `tomicz/fable-5-train-opus-skills-after-it-retires`

```
Copyright (c) 2026 Darko Tomic
```

- **How used:** the skill-library method informing the `skill-authoring` skill.

### agent-standard contributors — `anmoln7/agent-standard-oss` (@ `3786c4c`)

```
Copyright (c) 2026 agent-standard contributors
```

- **How used:** ideas from its §1–2, §8–10, and §11 informing the
  `delegation-and-review` and `skill-authoring` skills.

### Emil Kowalski — `emilkowalski/skills`

```
Copyright (c) 2026 Emil Kowalski
```

- **How used:** duration budgets, gesture-physics forms (momentum
  projection, rubber-band, velocity handoff), performance-trap material,
  and the review posture adapted into design-pack's `motion-craft` and
  `design-review-gate`. His in-skill course-marketing directives were
  stripped in adaptation.

### Leonxlnx — `Leonxlnx/taste-skill`

```
Copyright (c) 2026 Leonxlnx
```

- **How used:** layout hard rules (hero/nav/zigzag/bento/eyebrow caps with
  their mechanical counts), the production-test tell corpus (curated, not
  imported wholesale), the em-dash binary and its phrasing lesson,
  preservation rules, and the pre-flight-gate framing adapted into
  design-pack's `ui-design-craft`.

### LottieFiles — `LottieFiles/motion-design-skill`

```
Copyright (c) 2025 LottieFiles
```

- **How used:** timing/easing tables (element durations, distance
  multipliers, exit ratio), stagger and overshoot budgets, and the
  severity-tier gate shape adapted into design-pack's `motion-craft`
  (their damping-units conflation is corrected there, not copied).

### Refero Design — `referodesign/refero_skill`

```
Copyright (c) 2026 Refero
```

- **How used:** the anti-AI-slop tell list and litmus tests, the motion
  purpose triad, easing-direction and duration structure, and the
  reduced-motion mapping adapted into design-pack's `ui-design-craft` and
  `motion-craft`.

---

## 2. Works under the Apache License 2.0

### fable-agent-orchestration — `git.wearein.space/elias` (@ `935e4a3`)

- **License:** Apache License, Version 2.0
  (https://www.apache.org/licenses/LICENSE-2.0).
- **How used:** ideas and structural framing only, informing the
  `delegation-and-review` skill. Its 24-skill granularity was evaluated and
  deliberately **not** adopted.
- **Notice:** No source code or other copyrightable expression from this
  project is included in Opus Pack; only non-copyrightable ideas were
  incorporated. Attribution is provided here in keeping with the Apache-2.0
  attribution requirements (§4) and good practice. Should any portion ever be
  found to reproduce this project's expression, that portion remains licensed
  under the Apache License 2.0, and the corresponding upstream copyright and
  `NOTICE` entries must be reproduced with it.

### open-design — `nexu-io/open-design`

- **License:** Apache License, Version 2.0
  (https://www.apache.org/licenses/LICENSE-2.0).
- **How used:** ideas and facts informing design-pack's `ui-design-craft`
  (accent budget), `motion-craft`, and `design-review-gate` (the
  promote-rules-into-a-linter stance) - AND two passages of **adapted
  expression** carried under Apache-2.0 with this notice:
  `ui-design-craft` §4's five-state table (adapted from
  `craft/state-coverage.md`) and `motion-craft` §7's misquote-correction
  items (adapted from `craft/animation-discipline.md`, with this pack's
  own correction of that file's Doherty citation). Its `craft/` layer
  credits the MIT-licensed refero_skill, which this pack also mined
  directly.
- **Notice:** except for the two adapted passages identified above (which
  remain licensed under the Apache License 2.0, reproduced by pointer
  here), no other expression from this project is included; the remaining
  borrowings are non-copyrightable ideas and factual claims with their
  citations.

---

## 3. MIT License text

The following is the standard MIT License, applicable to every work listed in
Section 1 above, under that work's own copyright notice as reproduced there:

```
MIT License

Copyright (c) 2026 Curtis Chou
Copyright (c) 2026 Miguok
Copyright (c) 2026 Darko Tomic
Copyright (c) 2026 agent-standard contributors
Copyright (c) 2026 Emil Kowalski
Copyright (c) 2026 Leonxlnx
Copyright (c) 2025 LottieFiles
Copyright (c) 2026 Refero

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 4. Idea-level and private-note sources (no license text required)

The following informed Opus Pack at the level of ideas and impose no
notice-retention obligation. They are credited in full in `README.md`;
copyright protects expression, not ideas or methods, and no substantial
verbatim expression from these sources is reproduced:

- **gyozalab** — Threads post (originating framing).
- **林長揚** — Facebook post (institution-design ideas).
- **kannaiah** — Reddit comment (operational-rigor ideas).
- **pro_ai.news** — Threads post (goal-coaching protocol).
- **firaen22** (credited as "Friend A" before going public) — private
  Discord notes shared with the maintainer (a checks/-harness design note
  and a measured Claude Code harness export),
  adapted at idea/rule level into `ground-truth-gates`, `operational-rigor`,
  `delegation-and-review`, and `skill-authoring`; source text is not
  distributed.
- **Private source drafts** — the owner's reference drafts for
  `security-architect` and `product-roadmap`, plus the collected
  `guideline *.txt` source copies (guidelines 5 and 6 are firaen22's
  notes; the rest were supplied by the owner). These source drafts are not
  distributed; they are excluded via `.gitignore`.
- **garrytan/gstack** (MIT) — design-review ideas only (measurement
  pairing, surface classifier, fix-loop shape, anti-convergence test,
  preference-poisoning defense) in design-pack's `design-review-gate` and
  `ui-design-craft`; no text copied.
- **benjitaylor/agentation** (PolyForm Shield 1.0.0 — source-available) —
  ideas only (pitfall-table findings form, critic/fixer loop) in
  design-pack's `design-review-gate`; no text or code copied, so no
  license text travels.
- **tt-a1i/archify** (MIT) — the rule-paired-with-validator idea in
  design-pack's `design-review-gate`; no text copied.
- **creativetimofficial/ui** (MIT) — the enumerated micro-text whitelist
  technique in design-pack's `ui-design-craft`; no text copied.
- **VoltAgent/awesome-design-md** (MIT) — referenced in `README.md` as a
  research corpus for design-review-gate's "unofficial observation" class;
  nothing vendored or copied.
