---
name: gates-and-provenance-map
description: starledger 的 executor/artifact PR 被 verify-agent-artifacts 或 verify-ai-provenance 打紅、要預判某個 artifact 變更能否過 gate、或要修改 verify-diff/agent-gate/provenance 任一實碼時載入。這是兩道 AI gate 的裁決語義對照表。
---

# starledger：結構與 provenance gate 語義地圖

（驗證日 2026-07-30，HEAD `55ae7b2`。實碼＝`packages/classifier/src/verify-diff.ts`、
`agent-gate.ts`、`provenance.ts`；workflow＝`.github/workflows/ai-agent-pr.yml`、
`ai-provenance.yml`，皆 `pull_request_target`、只 checkout 受信 base、把 head 當資料讀。）

## 結構 gate（`verify-agent-artifacts`）

- 觸發是 **path-based**：PR 動到 `ai-annotations.json` 或 `ai-annotations-meta.json` 任一
  （含 rename 的舊路徑）才啟用 executor 規則；沒動到＝green no-op。
- 動到時：head branch 必須是核准的 executor 前綴（`claude/`、`codex/`）且同 repo；變更檔案
  **只能**是完整的 artifact pair；狀態只允許 **A 或 M**——刪檔（D）與改名（R）一律拒。
  ⇒ prune-only PR（M,M）可過；「刪 annotation 記錄」與「刪 annotation **檔**」是兩回事。
- diff 解析用 NUL 分隔（`git diff --name-status -z -M`），怪檔名繞不過。

## Provenance gate（`verify-ai-provenance`）

先驗 artifact pair 完整性（schema＋exact hash），再對「受信 base 的 canonical dataset＋live
README discovery」重算並裁決：

| 規則 | 語義 | 對操作的意義 |
|---|---|---|
| PROV-5 | head meta 的 `dataset_sha256` 必須等於**當前 base** 的 canonical SHA | daily sync 讓在途 PR 變紅（born-stale）；用 `meta-rebase`（手動、model-free）重蓋，不重跑模型 |
| changed 集合 | head 對 base「新增＋內容變更」的 annotation，逐筆重算 fingerprint/OID/metadata/config 驗證 | 逐筆錯 → 逐筆違規列出 |
| PROV-8 | `changed.length ≤ max_total_per_run`——**prune 不計入** | prune-only PR 是 changed=0，天然過 budget |
| PROV-6 | prune 只在「該 node 已離開 canonical dataset」時合法；prune 仍在的 node ＝違規 | removed-star 生命週期的 gate 端權威 |
| metadata-only 拒絕 | annotations bytes 沒變、只動 meta ＝拒 | 防 timestamp/metadata churn；真 prune 有 bytes 變化、不受影響 |
| generated_at 規則 | 內容沒變不得只改 generated_at | assembler 的 no-op 保時戳行為與此對偶 |

## 對 PR 作者（人或 agent）的裁決速查

- artifact PR 紅在 PROV-5、其他全綠 → `meta-rebase` 情境（見 P3.2 runbook 的 base/head 取材
  規則），不是重跑分類。
- 紅在「annotation for a repository not in the canonical dataset (invented or removed)」→
  head 想新增/修改一個非 canonical node——若是 removed-star 想「復活」，正解是 prune，不是硬塞。
- 紅在「annotation removed for a repository still in the canonical dataset」→ 有人 prune 了
  仍在語單的 repo——絕不 override，查 stars.json 為準。
- required checks（ruleset 17928397，2026-07-26/30 以 `gh api` 實查）＝`verify`、
  `verify-agent-artifacts`、`verify-ai-provenance`；`strict:false`＋0 approvals——repo 教條
  （P3.2 原文，無條件式）：**merge only when the checks ran against the current `main`
  (otherwise update the branch / meta-rebase so they re-run)**。
  docs-only PR 對兩道 AI gate 是 green no-op，且不觸發 executor 的 STEP-0 throttle
  （head 非 `claude/p3-ai-artifact-*` 且不碰 ai-annotations.json）。

**完成定義**（診斷型載入）：紅檢查已對映到上表某一列＋一個具體修復動作；（修碼型載入）
從 repo root 跑 `pnpm exec vitest run packages/classifier/tests/` 全綠＋PROV 語義表仍與實碼
一致。（陷阱實證：`pnpm --filter @starred/classifier test` 是**真空通過**——該套件沒有 test
script，exit 0、零測試執行；vitest 的 include pattern 是 repo-root 相對。）

## 再驗證

```bash
rg -n "PROV-6|PROV-8|still in the canonical dataset" packages/classifier/src/provenance.ts | head -6
rg -n "may not delete or rename|complete AI artifact pair" packages/classifier/src/verify-diff.ts
gh api repos/F-e-u-e-r/starledger/rulesets --jq '.[].name'   # ruleset 仍在（易變，日期戳重驗）
```
