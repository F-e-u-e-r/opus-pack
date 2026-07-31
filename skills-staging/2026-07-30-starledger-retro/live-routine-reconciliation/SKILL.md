---
name: live-routine-reconciliation
description: starledger 的 canonical prompt fenced block 改動合併進 main 之後、懷疑 live executor 行為與 repo 契約不符、或需要手動觸發一輪 executor 時載入。這是 live Claude Routine 與 version-controlled prompt 的同步程序（含逐位元組驗證）。
---

# starledger：live routine reconciliation

（驗證日 2026-07-29/30——**外部服務行為，易變**：Anthropic routine 平台的 API 形狀與語義以
當日實測為準，再用前先小步重驗。routine 識別資訊來自 starledger 公開文件的 Identity 表。）

## 架構事實（為什麼需要這個程序）

- live routine（trigger `trig_01LGJsFiiqeBtc8rwAstqHVh`，hourly `17 * * * *` UTC，
  `persist_session: false` 每輪全新 checkout）執行的是 canonical prompt 的**副本**
  （`events[0].data.message.content`）。改了
  `docs/routines/starledger-ai-classification.md` 的 fenced block 並合併，**live 行為不變**，
  直到 reconcile——該檔案檔頭本身就要求「live routine must match this file」。
- 相對地，`docs/P3.2-executor-runbook.md`、`prompts/classify-agent-v1.md`、
  `docs/P3-ai-spec.md` 是 executor **每輪開跑時讀**的，repo 修正下一輪即生效。
- 教訓（2026-07-26 實測）：merged 的 runbook 警語**不可靠地**覆蓋未 reconcile 的 live
  prompt——runtime 收口必須換 prompt 本體，不能指望執行器自行擇新棄舊。

## 程序（2026-07-26 與 07-29 兩次實測成功）

1. **抽 canonical**（從合併後的 main，機械抽取勿手抄）：
   `sed -n '/^```text$/,/^```$/p' docs/routines/starledger-ai-classification.md | sed '1d;$d' > canonical.txt`
   ＋`shasum -a 256 canonical.txt`；重抽一次 `cmp` 確認抽取穩定。
2. **更新前記錄**：`RemoteTrigger get` 全文——記下 before `updated_at`、`cron_expression`、
   `enabled`、`events[0].data.uuid` 與整份 `session_context`。
   （`RemoteTrigger` 是 **owner 平台側**的 routine 管理能力，不是 starledger repo 的工具、
   repo 內零蹤跡；若你的會話沒有等效的 routine 管理工具，**就此停下向 owner 要**——不要找
   替代通道。）
3. **更新**：`RemoteTrigger update` **只送 `job_config`**——payload 形狀＝把你在步驟 2 記錄
   的整個 `job_config` 物件原樣鏡射（`ccr.environment_id`、`ccr.events[0].data.*` 含
   `uuid`/`session_id`/`type`/`parent_tool_use_id`、`ccr.session_context`），**只**替換
   `events[0].data.message.content`；`name`/`cron_expression`/`enabled` **一概不送**
   （partial-update 語義：未送欄位不變，2026-07-26/29 兩次實測成立）。
4. **read-back**：fresh `get`，確認 after `updated_at` 已變、schedule/identity 欄位原值。
5. **逐位元組驗證**：把 read-back 的 content 轉錄成檔案，與 canonical.txt 做
   `cmp`＋`shasum -a 256`。API 只回 JSON、無檔案下載——轉錄是唯一位元組化通道；其誠實性靠
   「兩次獨立 server 讀取（update 迴顯＋fresh get）內容一致」＋「與機械抽取的 canonical 檔
   cmp 相等」三角支撐。任一步失敗：立即停、報告、**不得宣稱 reconciliation 完成**。
6. **報告**：before/after `updated_at`、兩側 sha256、schedule 未變證據、一致性結論。

手動觸發一輪：`RemoteTrigger run`（回傳 session id；`last_fired_at` 隨之更新）。下一輪
scheduled 時間看 `next_run_at`。

**完成定義**：cmp IDENTICAL＋兩側同 hash＋schedule/identity 欄位逐一原值＋（可觀察時）下一輪
run 的行為/報告符合新 prompt。

## 負例（本會話真實發生）

- ❌ circular 驗證：「把 canonical.txt `cp` 一份當 expected 再 cmp」——比的是自己跟自己，
  什麼都沒證明（當場自抓移除；驗證鏈必須含 server 側讀回的獨立轉錄）。
- ❌「merged 的 P3.2 每輪必讀，所以 live 舊 prompt 的行為已被收窄」——owner 校正：那只是
  額外的 repo 層警示，**不可靠**；在 reconcile 前，舊 live prompt 仍可能重演舊行為。

## 再驗證

```bash
# canonical 側（hash 與行數隨契約演進變動——記錄當下值供 before/after 對照）
sed -n '/^```text$/,/^```$/p' docs/routines/starledger-ai-classification.md | sed '1d;$d' | shasum -a 256
# live 側：RemoteTrigger get → 目測 updated_at 與 step 3 內容是否為當前契約（API 為外部服務，形狀先小步重驗）
```
