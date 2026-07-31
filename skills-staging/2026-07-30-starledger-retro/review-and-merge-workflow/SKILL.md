---
name: review-and-merge-workflow
description: 要在 starledger 開分支、開 PR、跑 owner 的跨模型審查迴圈、或決定一個 PR 何時可以合併時載入。這是 2026-07-26 之後的現行交付流程——含審查陣容規則與「合併位元組＝受審位元組」紀律。
---

# starledger：審查與合併工作流（2026-07-26+ 現行）

（驗證日 2026-07-30。**取代**前代（2026-07-12 era）文件裡的「admin-merge」與「no
auto-merge」敘述——那是舊紀元；現行如下。）

## 分支與合併機制

- 分支永遠從**剛 fetch 的** `origin/main` 切（daily sync 直推遠端 main，本地 main 天生落後）。
- 人/agent 的 PR：正常 CI（required：`verify`+`verify-agent-artifacts`+`verify-ai-provenance`，
  後兩者對非 artifact PR 是 green no-op）→ 審查收斂 → `gh pr merge <n> --merge`。
  **不用 `--admin`**（owner 明令；亦不得越過紅/pending check。註：routine 文件仍留有
  「admin 僅用於落 meta-rebase 後的 known-good stale PR」殘句——owner 本紀元的更嚴規則
  取代之；strict:false＋meta-rebase 重跑 checks 之下該路徑實質已死）。
  `strict:false` ⇒ 合併前確認 checks 是對 current main 跑的——repo 教條（P3.2 原文）是
  **無條件**的「merge only when the checks ran against the current main（否則 update
  branch／meta-rebase 重跑）」；本會話 #205 曾有一次「僅資料 commit 前進、註明後直接合併」
  的先例，那是**單次、日期戳 2026-07-26 的裁量**，再用需 owner 逐次同意，不是常設許可。
  executor 的 artifact PR 則由 GitHub auto-merge 在三 checks 綠後自動落地。
- **merge 的執行權**：agent 只在 owner 對該類 PR 有明示（或常設書面）授權時執行
  `gh pr merge`；沒有授權就呈報收斂狀態（verdicts＋CI＋freshness）等 owner dispatch。
- `delete_branch_on_merge` 開啟；合併風格＝merge commit。

## Owner 的跨模型審查陣容（owner 決策 2026-07-26，兩次明示）

- **每輪**＝grok-4.5（effort high）＋ luna（`gpt-5.6-luna`，effort **max**）。
- **每第 3 輪、以及最終 commit/merge 前那一輪**＋＝ sol（`gpt-5.6-sol`，effort **max**）。
- sol 的 effort 是字面 `max`，**永不** `ultra`（owner 二度更正；本機 codex 設定檔可能仍寫
  ultra——用參數覆蓋，勿繼承）。
- 工具面（xcheck wrapper、codex/grok CLI 路徑與旗標）是 **owner 本機事實**：換機器＝
  user-must-provide，重新 discovery，勿從本文件回憶 slug/effort。

## 迴圈紀律（本會話 #205 三輪、#213 兩輪實證）

1. Packet 必須 self-contained：reviewer 只看得到你 inline 的內容（diff、必要的未變更事實、
   rubric、owner-accepted deferrals、逐字 verdict 格式——本 repo 慣用：回覆最後一行必須恰為
   `PROCEED` 或 `FIX: <短清單>`）。**每輪從當前 diff 重生 packet**，
   並附上一輪全部 findings 的處置表（reviewer 無記憶，否則重訟）。
2. Reviewer 讀的是 **live workspace**——審查在飛時絕不動被審檔案。
3. Finding 是主張不是判決：先重現再處置（fixed / accepted-with-reason / deferred-to-issue），
   修正文字**自己起草**、不貼 reviewer 的 remedy 原文。
4. **合併位元組＝受審位元組**：最終輪 PROCEED 後不再改 diff；殘餘 nits 以 deferred ledger
   記到 PR comment（#213 先例：6 條 test-hardening nits）。
5. 輪次上限 2–3；不收斂就停下帶軌跡上報，不無限迴圈。
6. 例外（owner 已裁可）：runbook 指定模板的機械填空 PR（如 completion 記錄）可免跨模型審查
   ——內容權威是已受審的 runbook；每次照樣揭露此選擇，CI 照跑。

**完成定義**：最終輪全 reviewer 出**確認的** PROCEED（非空 body、逐字 verdict 行）＋CI 綠
＋（如 main 前進）freshness 判斷已記錄＋merge exit 0＋分支已清。

## 負例（本會話真實張力，已裁決）

- ❌「r3 的 grok nit 一行就能修，順手改掉再合併」——改了就不是受審位元組；正確做法是
  deferred ledger（該 nit 為 fail-closed 方向、不重開任何 overclaim，記錄後合併）。
- ❌「sol 上一輪 PROCEED 過了，最終輪只跑 grok+luna 就好」——陣容規則明定 commit 前那輪
  必含 sol max；最終文字必須被 sol 看過。

## 再驗證

```bash
gh api repos/F-e-u-e-r/starledger/rulesets --jq '.[] | {name, enforcement}'   # 保護仍在（易變）
git log --oneline -5 origin/main    # 合併風格仍為 merge commits
# 陣容規則屬 owner 決策：以 owner 最新指示為準，本檔僅記錄 2026-07-26 版
```
