---
name: removed-star-prune-lifecycle
description: starledger 的 set check 出現 extra>0（annotation 的 node_id 不在 stars.json）、要修改 packages/classifier 的 assemble/apply/prune-orphans 任一路徑、或有人提議手動編輯 ai-annotations.json 時載入。這是 removed-star（unstar）生命週期的契約與唯一合法修復路徑。
---

# starledger：removed-star prune 生命週期

（驗證日 2026-07-30，HEAD `55ae7b2`。實作於 PR #213（issue #212），production 首證＝PR #214。）

## 背景

spec 的 Merge rule「a removed star prunes its annotation」（`docs/P3-ai-spec.md`）曾是
**未實作**的：`AssembleAiArtifactsInput` 沒有 canonical-identity 輸入——型別簽名層面就不可能
prune；planner 的 PLAN-6 只修剪 classifier **state**，不動發佈 artifact。2026-07-29 第一次
production unstar 留下常設孤兒（extra=1）——偵測者是 routine 自己的 3c set check；
completion-runbook 的 set-check 前置條件因此擋住 closeout（該窗口內完成閘**並未被
dispatch**；若 dispatch 必因 extra=1 FAIL）。修復是 end-to-end
的（owner 指定範圍 A–D），且驗收標準是「**由 deterministic path 自己產出 prune PR**」。

## 契約要點（現行實碼，`packages/classifier/src/`）

- **assemble**（`assemble.ts`）：`canonicalNodeIds: ReadonlySet<string>` 為**必填**；順序＝
  重複 node_id 硬失敗 → 修剪不在 canonical set 的既有 annotation（`prunedNodeIds` 排序回報）
  → **非 canonical 的 validated candidate 硬失敗**（同一輪修剪掉的東西不得由 candidate 重進）
  → 合併 → 排序/序列化/重建 meta。
- **apply**（`program.ts`）：以 `loadCanonicalDataset` 載入並驗證 `--stars/--meta`
  （預設 `stars.json`/`dataset-meta.json`），**硬拒** `manifest.dataset_sha256 ≠` 驗證後
  dataset SHA——絕不用另一份快照的 manifest 執行有破壞性的 prune；canonical set 傳入 assembler。
- **prune-orphans**（`prune-orphans.ts` + CLI）：零 candidate 的專用維護指令。
  收據＝canonical count（含 dataset SHA 前 12 碼）、annotations before、
  `pruned: N (id, …)`、annotations after、changed/no-op；只在 changed 時寫檔；
  「changed 與 prunedNodeIds 不一致」是 invariant violation（拒寫）。
  **stdout 的 `pruned: N` 行是載重介面**——routine 的 3e 逐字解析它
  （測試 `PRUNE-STDOUT-1/2` 釘住格式；改輸出格式＝介面變更）。
- **gate 相容性**：prune-only PR 是 M,M 的完整 artifact pair（結構 gate 只收 A/M pair、拒
  檔案刪除/改名）；provenance `PROV-6`——prune 已離開 canonical 的 node 合法、prune 仍在的
  node 違規；`PROV-8` budget 只計 changed（added+modified），**prune 不佔 budget**；
  meta 蓋驗證後 dataset SHA 滿足 PROV-5；annotations bytes 有實變所以不觸 metadata-only 拒絕。

## Routine 的 3e 維護路徑（唯一合法修復通道）

觸發＝3c 的 exact extra-only case（missing=0 ∧ duplicates=0 ∧ extra>0 ∧ omitted=0 ∧ jobs=0）。
執行（canonical prompt 的逐字兩行式）：
`GENERATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"` 然後
`pnpm classifier prune-orphans --current ai-annotations.json --generated-at "$GENERATED_AT" --out-dir .`，
**只在**「exit 0 ∧ 可讀出 `pruned: N` ∧ N>0 ∧ N==3c 的 extra」時接受；其餘（含截斷/不可解析收據、step-8 verify 失敗）一律 fail closed＋revert。
成功則接 step 9–14 照常出 PR，差異只有：title `chore(ai): prune orphan annotations (<K>
repos, <TS>)`、body 註明 maintenance run＋附完整收據。3e 結局永不是 3d 結論、永不說
"fully classified"、永不宣告完成或建議停用。

**互動式 session 的執行者邊界**：你在互動會話中看到 extra>0 時，先跑下方再驗證的 set check
確認，然後**等下一輪 scheduled run 或依 `live-routine-reconciliation` 手動觸發一輪**——由
executor 走 3e 出 PR；不要在手開分支上自跑 3e（executor 分支前綴規則會擋，見
`gates-and-provenance-map`），除非 owner 另有明示。

**完成定義**：`chore(ai)` PR 由三個 required checks（`verify`、`verify-agent-artifacts`、
`verify-ai-provenance`）放行 auto-merge；合併後 set check 全零（見下方再驗證指令）；全程零
手改 JSON。

## 負例（本會話真實出現、owner 駁回的合理化）

- ❌「一次性手動 prune 技術上可通過現有 provenance gate，先修資料解鎖 closeout。」——owner
  裁決原則：「手動刪掉這一筆只會製造暫時 PASS，並沒有證明 removed-star lifecycle 已實作」；
  修復必須是生命週期本身，且由它自己產出修復 PR 作 production acceptance。
- ❌「assembler 會 prune 就夠了。」——zero-job run 根本不會呼叫 `apply`；沒有 3e＋專用指令，
  修好的 assembler 永遠沒有被呼叫的機會（reachability 是修復範圍的一半）。

## 再驗證

```bash
# 集合狀態（期望全零；數字會隨語單成長變動，斷言不變量而非常數）
git fetch --no-tags origin main -q   # 本地 origin/main 天生落後（daily sync 直推遠端）
jq -n --slurpfile s <(git show origin/main:stars.json) --slurpfile a <(git show origin/main:ai-annotations.json) \
  '($s[0].repos|map(.node_id)) as $S | ($a[0].annotations|map(.node_id)) as $A |
   {missing:(($S-$A)|length), extra:(($A|unique)-$S|length), duplicates:(($A|length)-($A|unique|length))}'
# 契約仍在實碼（0 命中 = 有人動過 prune 契約，先讀 diff）
rg -n "canonicalNodeIds" packages/classifier/src/assemble.ts packages/classifier/src/program.ts | head -5
```
