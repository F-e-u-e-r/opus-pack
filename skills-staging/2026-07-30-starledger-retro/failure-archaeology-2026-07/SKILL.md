---
name: failure-archaeology-2026-07
description: 在 starledger 診斷「executor 報告可疑」「set check 異常」「快照與 main 不一致」這類問題、或想理解 #205/#212–#219 這串 PR 為什麼存在時載入。2026-07-26→30 紀元的死因檔案——含兩個被推翻的錯誤診斷與一串工具陷阱。
---

# starledger：failure archaeology（2026-07-26 → 07-30 紀元）

（驗證日 2026-07-30。每段：發生了什麼→為什麼錯→留下的規則。時間軸皆可由 starledger git
歷史重建；executor run 的原始 log 屬 owner 可見的 routine 通知，repo 端不留痕。）

## 1. Zero-job 假完成（→ PR #205）

executor 對「當下新鮮的 668/668」下了三個常設結論（fully drained／disable／P3 完成）；34
分鐘後 daily sync +17 全數否證。**第一層錯**在 executor 契約（快照→常設的升格通道存在）。
規則落點：`ai-executor-zero-job-contract`。

## 2. 被推翻的診斷：「stale snapshot / sync race」（助理自己的錯）

前一段分析把事故定性為「executor 跑在過期 668 快照上」。git 時間軸否證：dataset `c07cf0f3`
在 run 當下**就是**當前 main（2026-07-25T07:33Z→07-26T07:51Z 窗口）；所謂 stale 是「拿快照
跟**更晚的** main 比」的觀察偏差。owner 的方法要求（先比 BASE_SHA/sync 時刻/run 時刻再定性）
是抓錯的關鍵。留下的規則：**定性 race/stale 前先釘時間軸**；「A 觀察 ≠ B 觀察」的最常見成因
是「觀察時刻不同」，不是「A 的輸入壞了」。連帶教訓：freshness gate 對這次事故其實不會觸發
（run 在 sync 前就報告完）——**權威邊界才是主修**，freshness 只關相鄰情境。

## 3. Spec 有寫、實作沒有：removed-star prune（→ #212/#213/#214）

「a removed star prunes its annotation」在 spec 裡存在多時，assembler 的**型別簽名**就證明
不可能履行（無 canonical 輸入）；首次 production unstar 才暴露。留下的規則：spec 句子要對到
**可執行證據**（測試或型別）；「從未走過的路徑」的宣稱一律存疑（annotation_count 單調遞增
＝prune 從未發生的歷史證據）。修復驗收＝生命週期自己產出修復 PR（#214），不是手改資料。

## 4. Owner 兩度更正的審查參數：sol effort

記憶與本機設定檔都寫 ultra；owner 明令 sol＝字面 `max`、永不 ultra。規則：模型/effort 這類
**易變外部事實**永遠現場 discovery＋以 owner 最新指示為準，不從舊筆記回憶（`review-and-
merge-workflow` 已收）。

## 5. 工具陷阱（全部本會話實踩）

| 陷阱 | 症狀 | 解法 |
|---|---|---|
| zsh 把 `$c:stars.json` 當歷史修飾詞 | `bad substitution` | 寫 `${c}:stars.json` |
| `rg` 無命中 exit 1；zsh 無匹配 glob 直接 abort | `&&` 鏈整條斷、或 `no matches found` | 預期可能零命中的 grep 後接 `|| true`／分開跑；glob 先確認存在 |
| vitest include 是 repo-root 相對 | 套件目錄下跑 `vitest run tests/x` → No test files found | 從 root 用完整路徑跑 |
| `gh pr checks --watch \| tail` | 輸出重複/截斷、merge 結果被吃掉 | 大輸出落檔再讀尾段；或分開查 `gh pr view --json state` |
| 片語 grep 抓不到跨行折行 | `rg "reviewed merge"` 零命中但句子存在 | 見 `doc-status-sweep-method` |
| 驗證檔用 `cp` 自製 expected | 循環比對，什麼都沒證明 | 驗證鏈必含**獨立來源**（server 讀回的轉錄 vs 機械抽取的 canonical） |

## 6. 已封存的裁決（別重開）

- 一次性手動 prune 解鎖 closeout：owner 駁回（「暫時 PASS ≠ lifecycle 已實作」）。
- 3c stdout 遺失時原地重跑 plan：owner 駁回（第二份 live 觀察、覆寫 manifest）。
- 「stale base / race」二選一的事故定性：**兩者皆非**——時間軸已裁定（第 2 段）。
- 後續 hardening（machine-readable `empty_reason`、pre-budget eligible counts、閘在
  retry/refresh=0 下的健全性驗證）→ starledger issue #207；#213 的 6 條 test nits → 該 PR
  的 deferred-ledger comment。皆非 blocker，也**不要**在無新證據時折進別的 PR。

## 再驗證

```bash
# 時間軸重建範式（第 2 段的證據形狀）：dataset 演進逐 commit 列印
for c in $(git log --format=%h -8 origin/main -- dataset-meta.json); do
  printf '%s %s %s\n' "$c" "$(git show -s --format=%cI "$c")" "$(git show "${c}:dataset-meta.json" | jq -c '{repo_count}')"; done
```
