---
name: p3-completion-and-closeout
description: 要判斷 starledger 的 AI classification backlog 是否排空、要 dispatch p3-completion-check、閘 FAIL 需要診斷、或要把類似「milestone 完成」的宣稱寫進 spec 時載入。這是完成閘的條件合取、假完成清單與記錄程序。
---

# starledger：P3 完成閘與 closeout 程序

（驗證日 2026-07-30。P3 已於 2026-07-29 正式 closeout——run `30500689860`、base `b5afa9d`、
697/697——本 skill 保留給：閘的再次 dispatch（例如未來稽核）、其他 milestone 想沿用同款
closeout 模式、以及診斷 FAIL。權威文本＝`docs/P3-completion-runbook.md`＋
`scripts/p3-completion-check.mjs`。）

## 完成閘＝條件**合取**（缺一即 FAIL，而且 FAIL 是對的）

`p3-completion-check.yml`（**只有** `workflow_dispatch`，刻意 dormant）checkout 當前
default branch，跑 `scripts/p3-completion-check.mjs`（需 `STAR_SYNC_TOKEN`——credentialed
live README discovery）：

1. node_id 集合相等：missing=0 ∧ extra=0 ∧ duplicates=0（count 相等**不是**證據——缺一顆與
   多一顆會互相抵銷）；
2. live `classifier plan --current ai-annotations.json` 規劃 **0 jobs**；
3. omitted-unfetchable ＝ 0（「0 jobs」不得遮蔽未排空的工作）；
4. credentialed（真 token）；
5. 證據塊列印：base commit SHA、dataset SHA、五數字、jobs、omitted——PASS 是**釘在快照上的**
   （語單持續成長；PASS 只對那個 base 成立）。

拒收的五類假完成（runbook 原文有表）：scoped-subset replay、無 token 的本地模擬、backlog 未
排空時的 zero-**new**、非 credentialed 驗證、「routine 今天沒開 PR」式推論。

## 操作程序（2026-07-29 實走全鏈）

先跑**零成本的本地前置檢查**（set check，見 `removed-star-prune-lifecycle` 的再驗證指令）——
missing/extra/duplicates 任一非零就不必浪費一次 credentialed dispatch，先排空。dispatch 屬
operator 動作：executor 永不 dispatch；互動式 agent 只在 owner 明示時代跑。

```bash
gh workflow run p3-completion-check.yml
RUN_ID=$(gh run list --workflow=p3-completion-check.yml -L1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status
gh run view "$RUN_ID" --log | grep -E "base commit|dataset SHA|missing=|planned jobs|omitted|PASS|FAIL"
```

前置整備（如語單剛動過）：`gh workflow run sync-stars.yml`（有 workflow_dispatch；daily cron
`23 5 * * *` UTC，GitHub scheduler 有延遲常態）把新星拉進 canonical → 讓 routine（scheduled
或 `RemoteTrigger run` 手動）把 missing 排掉 → set 全零後再 dispatch 閘。

## PASS 之後的記錄（closeout 才算完成）

依 `docs/P3-completion-runbook.md` 的 spec-update template：**只動** `docs/P3-ai-spec.md`
的 docs-only PR，模板填五值（日期、N of N、run URL、base SHA、dataset SHA）——記錄 PR 本身
**維持模板窄幅**（這正是它得以豁免跨模型審查的前提）。實務教訓（PR #216→#219 四輪）：模板
只換一顆 bullet **不夠**——同檔還有多處 present-tense 舊狀態句會與新記錄直接矛盾；因此記錄
PR 之後**另開後續 PR**（走正常審查陣容）執行 `doc-status-sweep-method` 的全類掃蕩，兩者不可
混入同一個 PR：混入＝把「機械填空豁免」硬撐到含判斷的掃蕩編輯上。

歷史警示（gate run 史實，`gh api` 可查）：2026-07-26T17:21Z 曾有一次 685/685 的 **PASS 從未
被記錄**，隨語單成長自然作廢——PASS 是釘在快照上的，**不記錄＝沒發生**；PASS 到手就立刻走
記錄程序。

**完成定義**：閘 PASS（證據塊齊）＋記錄 PR 合併＋狀態掃蕩零殘留＋（若動過 canonical prompt）
live reconcile 完成。

## 負例（本會話真實出現）

- ❌「missing=2 但那是我剛 star 的，先 dispatch 沒關係」——會 FAIL 而且該 FAIL；先排空再
  dispatch（合取沒有豁免項）。
- ❌「gate PASS 了，spec 換掉 PENDING 那顆 bullet 就是記錄完成」——#216 之後 owner 連抓三輪
  殘句；記錄=模板+全檔一致性，缺一不可。

## 未定案（勿當作已證）

閘在 `max_retry_per_run=0`／`max_refresh_per_run=0` 下的健全性——zero jobs 是否可能遮蔽
refresh-eligible 工作——由 starledger issue #207（machine-readable 診斷）追蹤，**尚未**在
程式碼層驗證；在該項落地前，把 PASS 敘述為「在此 config 下的完成」是本 repo 已接受的語義
（3d 的同款 budget-scoped 措辭）。

## 再驗證

```bash
sed -n '1,10p' scripts/p3-completion-check.mjs        # 條件合取仍如上
rg -n "workflow_dispatch" .github/workflows/p3-completion-check.yml .github/workflows/sync-stars.yml
```
