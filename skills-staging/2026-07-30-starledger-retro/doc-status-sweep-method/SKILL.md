---
name: doc-status-sweep-method
description: 要宣稱「docs 與狀態 X 一致」之前載入——特別是 milestone 收官記錄、契約政策翻轉（如 auto-merge 從關到開）之後的全庫狀態句清理。方法論來自同一軸線被 owner 連抓三輪漏網的實案（starledger PR #217→#218→#219）。
---

# 文件狀態掃蕩方法（class → stem → wrap-aware）

（驗證日 2026-07-30。這是**方法 skill**：三輪真實漏網的失敗模式各對應一條規則。）

## 三輪漏網的實案（starledger，2026-07-30 同日）

| 輪 | 掃法 | 漏掉的真實句子 | 為什麼漏 |
|---|---|---|---|
| #217 | 關鍵詞 `pending\|not yet` | 「Continue bounded, **manual backfill**…」「**Auto-merge stays disabled** in v1」 | 矛盾句不含你選的關鍵詞——狀態宣稱是**語意類**，不是詞表 |
| #218 | 語意類，但詞形只列 `human review`、`reviews and merges` | 「…publish through a **reviewed merge**」 | 同類**詞形變化**沒窮舉 |
| #219 | 補 `reviewed merge` 片語 | 同一句 | 片語**跨行折行**（`a reviewed\nmerge`）——單行 regex 連正確片語都抓不到 |

當時的不安全合理化（真實、勿重演）：「掃過 `pending` 都乾淨了，documentation consistency
✅」——關鍵詞零命中被當成類別零殘留，連錯兩輪。

## 方法（宣稱一致性前的必經四步）

1. **定義類，不是詞表**：先用一句話寫下「什麼樣的句子與新狀態矛盾」（例：pre-auto-merge 時代
   的 present-tense 契約句），再從類推導檢索詞。
2. **掃詞幹**：`rg -in "review"` 而不是 `"reviewed merge"`——詞形變化（review/reviews/
   reviewed/reviewer）一網打盡，然後**逐一裁決每個命中**。
3. **keep-ledger**：合法保留的命中（機制語如 retry「pending」、歷史敘述、一次性程序）逐條
   列出＋理由，引進 PR body——「保留」是裁決結果，不是漏掃。
4. **把零命中當可疑訊號**：片語 grep 零命中 ≠ 不存在——markdown 折行會拆散片語；改用單一
   有辨識度的**單詞**重掃一次再下結論。

**完成定義**：PR body 內含（a）可重跑的詞幹掃蕩指令、（b）修正清單 before/after、
（c）keep-ledger 全列附理由；re-run 該指令的命中恰好等於 keep-ledger。

## 正例（#219 最終形）

`rg -in "review" docs/P3-ai-spec.md docs/P3.2-executor-runbook.md` → 恰 3 命中，逐條裁決為
keep（bootstrap PR ×2、meta-rebase operator 覆核）＝掃蕩收斂的可驗證定義。

## 再驗證

方法 skill 無 repo 狀態可驗；每次套用時，「再驗證」＝把你自己的最終掃蕩指令與 keep-ledger
貼進 PR body，讓下一個人能一鍵重跑。
