---
name: ai-executor-zero-job-contract
description: 讀或修改 starledger canonical prompt 的 step 3、診斷任何 zero-job run 的報告文字、或有人（含 executor 本身）提議「backlog 排空了／停用 routine／P3 完成」時載入。這是 zero-job 結論的權威邊界與逐字報告契約。
---

# starledger：executor zero-job 契約（3a–3e）

（驗證日 2026-07-30，starledger HEAD `55ae7b2`。權威文本＝
`docs/routines/starledger-ai-classification.md` canonical prompt 的 step 3；本 skill 是導讀與
邊界，不是替代品——兩者衝突時以 repo 文本為準。）

## 事故背景（為什麼這份契約長這樣）

2026-07-26：一次 zero-job run 把「當下正確的 668/668 快照」升格為常設宣稱——「fully
drained」「disable this routine」「P3 完成閘達成」——34 分鐘後 daily sync +17 顆星就全數否證
（PR #205 修正；starledger git 歷史可重建時間軸）。兩個教訓都寫進了契約：

1. **快照結論不得升格為常設結論**。star 語單持續成長，「排空」本質上是暫時狀態。
2. **planner 是 budget-limited 的**（`config/ai.yaml` 的 `max_retry_per_run`／
   `max_refresh_per_run` 現值 0）：zero-job manifest 在邏輯上**無法**證明「所有 annotation 都在
   當前 fingerprint」——refresh/retry 候選被 ceiling 靜默丟棄。所以合法的最強宣稱只有
   「snapshot-local manifest is empty **under this base and config**」。

## 協定地圖（依序、遇第一個失敗即停）

前置條件：step-2 `plan` 指令本身 exit 0 且本輪確實寫出 `.ai-runs/manifest.json`；否則報該失敗
指令、exit 0、no conclusion。

| 步 | 檢查 | 通過 | 失敗（全部 fail-closed、exit 0） |
|---|---|---|---|
| 3a | `git fetch --no-tags origin main` 後 `git diff --quiet "$BASE_SHA" origin/main -- stars.json dataset-meta.json ai-annotations.json ai-annotations-meta.json`（`BASE_SHA`＝run 開始時記錄的 commit；step 11 前 HEAD 不得移動，故可 `git rev-parse HEAD` 重導出） | diff exit 0 → 3b | fetch 失敗→`zero jobs; base freshness unverifiable (fetch failed); no conclusion`；diff exit 1→逐字 `empty manifest on stale base; base advanced during run; re-run` + 兩個 SHA；其他 exit→`… (git diff failed) …` + exit 碼 |
| 3b | `config/ai.yaml`：結構檢查**先**（檔可讀＋`ai.enabled`/`ai.executor_kind`/四個 budget ceiling——`max_new_per_run`/`max_retry_per_run`/`max_refresh_per_run`/`max_total_per_run`——齊且型別對）、值檢查**後**（enabled true、kind `claude-routine`、`max_total_per_run`>0） | → 3c | 結構壞→`zero jobs; config unverifiable; no conclusion`；值壞→報**具體**原因，不得說 backlog/manifest empty |
| 3c | node_id **集合**相等（count 相等不是證據）＋ omitted-unfetchable=0（只認**完整**的 step-2 stdout capture；截斷/不可解析＝unavailable） | 全零 → 3d | 任一非零→報五個數字、永不說 "fully classified"；stdout 不可得→`zero jobs; omitted-unfetchable status unavailable; no conclusion`，**絕不原地重跑 plan**（第二份 live 觀察會覆寫 manifest） |
| 3d | （3a–3c 全過）唯一允許的正向結論 | 逐字 `snapshot-local manifest is empty under this base and config` + 證據塊：BASE_SHA、manifest `dataset_sha256`、五數字、四個 budget ceiling、omitted(0)、jobs(0)。cadence 放寬註記為 **3d 專屬** | — |
| 3e | 3c 的**唯一例外**：missing=0 ∧ duplicates=0 ∧ extra>0 ∧ omitted=0 ∧ jobs=0 → removed-star prune 維護路徑 | 見 `removed-star-prune-lifecycle` skill | 收據不完整/數字不合→fail closed + revert |

## 權威邊界（每個 zero-job 結局都適用）

- executor **永不**建議停用本 routine（最多：3d 情況下註記 operator *可*考慮放寬 cadence）。
- executor 對**任何** milestone 都沒有完成權威；P3 的完成**專屬** operator 手動 dispatch 的
  read-only `p3-completion-check` workflow（見 `p3-completion-and-closeout` skill）。
- 逐字報告字串是**介面**：executor prompt、`scripts/p3-completion-check.mjs` 的
  regex（`/omitted (\d+) probe-ok/`）與 operator 通知都在解析它們。改任何一句＝介面變更，
  必須 sweep 全部消費者（operational-rigor 的 call-site sweep）。

## 修改 step 3 的正確程序

1. 改 `docs/routines/starledger-ai-classification.md` 的 fenced prompt（機械稽核見
   `verification-battery-and-doc-audits` skill）。
2. 走正常 PR + CI + owner 的 review 陣容（見 `review-and-merge-workflow` skill）。
3. **合併後 live prompt 必須 reconcile**——repo 內的 prompt 只是 canonical 文本，live routine
   持有副本；不 reconcile 修正就是 inert（見 `live-routine-reconciliation` skill）。

**完成定義**：三步全做完＋下一輪 scheduled run 的報告文字符合新契約（owner 的 push 通知是
run 報告的觀察通道；repo 端 zero-job run 不留痕跡）。

## 負例（本會話實際發生過的不安全合理化，勿重演）

- ❌「668 annotations == 668 repositories，backlog fully classified——叫 operator 停用
  routine。」（事故原文的等價敘述；count 相等不是集合相等，快照不是常設狀態，executor 沒有
  停用建議權。）
- ❌「這次 full-corpus plan 0 jobs 就是 P3.5 在等的完成閘。」（完成閘是 operator dispatch 的
  workflow＋記錄程序，executor 的 0 jobs 最多是 snapshot-local 證據。）
- ❌「stdout 不見了，重跑一次 plan 讀 omitted 就好。」（owner 駁回：第二次 plan 是另一份 live
  觀察且會覆寫 manifest——fail closed 報 no conclusion。）

## 再驗證

```bash
# 逐字字串逐條驗（合併式 alternation 會遮蔽單一字串消失；逐條才看得到缺哪個）
for s in \
  "snapshot-local manifest is empty under this base and config" \
  "empty manifest on stale base; base advanced during run; re-run" \
  "Never skip 3a" \
  "omitted-unfetchable status unavailable"; do
  rg -q "$s" docs/routines/starledger-ai-classification.md || echo "MISSING: $s"
done   # 無輸出 = 契約在場；任何 MISSING = 契約被動過，先讀 diff 再行動
```
