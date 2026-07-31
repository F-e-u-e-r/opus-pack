# MANIFEST — starledger retiring-architect library（session 2026-07-26 → 2026-07-30）

專案＝[F-e-u-e-r/starledger](https://github.com/F-e-u-e-r/starledger)（公開）。本庫由該會話
的退休首席架構師萃取；對話證據以最小化改寫記載，倉庫證據於 2026-07-30（starledger HEAD
`55ae7b2`）逐項複核。狀態值：verified / historically-valid / partially-verified /
unverified / user-must-provide——後兩類**不得作為常設權威**：只進 `UNCERTAINTY.md`，或在
技能內以「日期戳觀察＋內建重驗＋fail-closed 停損」的形式出現（例：live 平台 API 行為）。
名詞：「語單」＝canonical starred-repo corpus（`stars.json` 的 repo 集合，每日 sync 持續
成長）。

| Skill | 載入條件（精確） | 對話證據（改寫） | 倉庫證據 | 狀態 |
|---|---|---|---|---|
| `ai-executor-zero-job-contract` | 讀/改 canonical prompt step 3；診斷 zero-job 報告；有人提議 executor 下停用/完成結論 | zero-job 假完成事故＋owner 三個 MUST-FIX（budget-scoped 措辭、stdout 不重跑、Edit-4 不即時生效）；#205 三輪跨模型審查全處置 | `docs/routines/starledger-ai-classification.md` step 3（HEAD 逐字在場；3a–3d 出自 PR #205，3e 出自 PR #213）；dataset-meta git 時間軸 | verified |
| `removed-star-prune-lifecycle` | set check extra>0；動 assemble/apply/prune-orphans；有人想手改 ai-annotations.json | spec-vs-impl 缺口的型別級證明；owner 駁回一次性資料修補、指定 A–D 全範圍；#214 為 production acceptance | `assemble.ts`/`program.ts`/`prune-orphans.ts` 實碼；issue #212、PR #213/#214；PROV-6/PROV-8 於 `provenance.ts` | verified |
| `live-routine-reconciliation` | canonical prompt 合併後；懷疑 live 與 repo 契約不符;需手動觸發一輪 | 兩次實測程序（2026-07-26/29）：content-only update、欄位鏡射、轉錄+cmp+sha256；circular-cp 自誤自糾 | routine spec Identity 表（trigger/env id、cron、persist_session 皆公開文件）；程序本身屬外部平台行為 | repo 側 verified；平台 API 行為＝user-must-provide 級的日期戳觀察（與 UNCERTAINTY §3 同一狀態語彙），技能內附重驗與 fail-closed 停損 |
| `gates-and-provenance-map` | executor/artifact PR 被兩道 AI gate 打紅；預判 artifact 變更能否過 gate；修 gate 實碼 | prune-only PR 過 gate 的推理鏈（M,M、changed=0、PROV-6）於 #214 實證 | `verify-diff.ts`（A/M、pair、NUL）、`provenance.ts`（PROV-5/6/8、metadata-only）、兩個 workflow、ruleset 17928397（gh api 實查 2026-07-26/30） | verified（ruleset 屬易變，已日期戳） |
| `p3-completion-and-closeout` | 判斷 backlog 是否排空；dispatch/診斷 completion 閘；要把 milestone 完成寫進 spec | 2026-07-29 全鏈實走：sync→classify→gate PASS（run 30500689860）→記錄 PR；owner 的六條件合取指令 | `p3-completion-check.mjs` 條件、workflow dispatch-only、completion-runbook 模板、PR #215/#216 | verified；閘在 retry/refresh=0 下的健全性＝unverified（見 UNCERTAINTY） |
| `review-and-merge-workflow` | 開分支/開 PR/跑 owner 審查迴圈/判斷可否合併 | owner 陣容規則（2026-07-26 兩度明示，sol=max 二度更正）；#205×3＋#213×2 輪實證的 packet/處置/合併紀律 | merge 歷史（#205–#219 皆 normal merge）；ruleset 0 approvals/strict:false；deferred-ledger comment 在 #213 | verified（陣容＝owner 決策；工具細節=user-must-provide 換機時） |
| `verification-battery-and-doc-audits` | 改了 code/docs 要在 push 前驗證；動 prettier 盲區的 fenced 區塊 | untracked 目錄污染 repo-wide format:check、vitest root-relative、fence/步數/行長三稽核、dogfooding 斷言不變量 | `package.json` scripts、`.prettierrc.json`、CI `verify` 步驟；本會話 750-test 綠均可重跑 | verified |
| `doc-status-sweep-method` | 宣稱 docs 與新狀態一致之前；政策翻轉後的全庫狀態句清理 | 三輪被 owner 連抓的漏網（#217 關鍵詞/#218 詞形/#219 折行）＋當時的不安全合理化原句 | PR #217/#218/#219 的 diff 與 body；最終 stem sweep 恰 3 keep | verified（方法型；實案可由 PR 重放） |
| `failure-archaeology-2026-07` | 診斷 executor 報告可疑/set 異常/快照 vs main 不一致；理解 #205–#219 何以存在 | 兩個被推翻的診斷（executor 升格；助理的 stale/race 定性）＋六個實踩工具陷阱＋已封存裁決 | git 時間軸可重建；封存項對應 #207/#213-comment | verified（歷史敘述均對得上 repo 記錄） |

備註：
- 本庫**取代**兩類舊主張：（a）前代 2026-07-12 庫內的「到 main＝admin-merge」「沒有
  auto-merge」；（b）該紀元 **repo 文本**中的「empty manifest→停用 routine」教條（存在於舊
  runbook 文字與 classifier 註解，#205/#213 紀元移除；前代**庫本身**未載此條）。詳
  `UNCERTAINTY.md` 第 1 條。
- 環境警示：前代庫至今仍以 **untracked** 形態躺在 starledger 工作樹（`git status` 會看到
  `?? skills-staging/`）——先撞見它的未來會話請以本 MANIFEST 的取代清單為準，勿依其
  admin-merge／no-auto-merge 段落行動。
- 三個 fresh-context 審查（事實／教義／可用性）於 2026-07-30 對本庫執行完畢：合計
  1 BLOCKING＋12 IMPORTANT＋15 MINOR，BLOCKING 與 IMPORTANT 全數已修入本版（含本行所屬的
  MANIFEST 修正）；逐項清單見交付 PR 描述，殘餘不確定見 `UNCERTAINTY.md`。
