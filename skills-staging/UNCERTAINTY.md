# UNCERTAINTY — 未定案與驗證缺口（starledger library, 2026-07-30）

每條：主張/風險 → 對話中的出處（最小化描述）→ 倉庫證據 → 狀態 → 為何未定 → 何以解 → 是否開
issue。

## 1. 前代 skills-staging 庫（2026-07-12）滯留未交付，部分主張已被本紀元推翻

- 主張/風險：starledger 本地工作樹存在一份 **untracked** 的 11-skill 前代庫（建檔
  2026-07-12，含三輪審查記錄），從未交付到 opus-pack；其中「到 main 的路＝admin-merge」
  「沒有 auto-merge」兩主張與現行 repo 文本相反。（第三條舊教條「empty manifest→停用
  routine」經事實審查核實**不在前代庫內**——它存在於該紀元的 repo 文本（舊 runbook 文字與
  `program.ts` 註解，後者仍由 starledger #207 追蹤清理）；本檔初稿曾誤歸給前代庫，已更正。）
- 出處：本會話開頭的 `git status` 即見 `?? skills-staging/`；authoring 前直接讀取其 MANIFEST
  與樣本。
- 倉庫證據：starledger 現行 docs 已是 gated auto-merge＋steady-state 教條（PR #217–#219）；
  #205 起 normal merge、無 --admin。
- 狀態：前代庫本體＝historically-valid（其紀元內三輪審查過）；上述三主張＝**contradicted**
  （已在本庫對應 skill 明文取代）。
- 為何未定：前代庫是否要（更新後）交付、還是廢棄，是 maintainer 取捨；它不在任何 repo 裡，
  本次交付範圍（僅 `./skills-staging/`、僅本會話證據）也不含代它背書。
- 何以解：maintainer 決定三選一——按本庫勘誤後合併交付／原樣封存為歷史／捨棄。
- Issue：本條未單獨開（owner 本機狀態）；其上位政策決定由 opus-pack issue #98（staging 追蹤
  政策，見 §7）承載——同一裁決自然涵蓋本條的交付去向。已在 PR 描述中明示。

## 2. 完成閘在 `max_retry_per_run=0` / `max_refresh_per_run=0` 下的健全性

- 主張/風險：`p3-completion-check` 的「0 jobs」是否可能遮蔽 refresh-eligible（fingerprint 已
  變）的工作——與 zero-job 契約同款的 budget-bucket 疑慮，方向是「PASS 可能弱於 spec 語句」。
- 出處：owner 在 #205 的 MUST-FIX 論證中明確點出並要求列入後續 hardening。
- 倉庫證據：`planner.ts` 的 bucket/ceiling 註解支持疑慮成立的可能；閘與 executor 共用同一
  `plan --current` 路徑；starledger issue #207 已載明驗證任務（含 uncapped diagnosis mode 選
  項）。
- 狀態：unverified（需要 code-level 驗證 planner 在 ceiling=0 時對 refresh 候選的確切行為）。
- 為何未定：本會話未讀到能一錘定音的那段選擇邏輯；貿然斷言兩個方向都可能誤導。
- 何以解：starledger #207 的驗證項落地（或一個針對性測試：ceiling=0＋已變 fingerprint 語料
  → plan 是否 0 jobs）。
- Issue：不另開——**已由 starledger #207 承載**；本庫 `p3-completion-and-closeout` 已把 PASS
  措辭鎖在 budget-scoped 語義內。

## 3. Anthropic routine 平台 API 行為（RemoteTrigger 語義）

- 主張/風險：partial-update「未送欄位不變」、`uuid` 沿用、content-only 換文、`run` 即時觸發
  ——全部為 2026-07-26/29 兩次實測；平台屬外部服務、無版本契約可引。
- 倉庫證據：無（starledger 只 version-control prompt 文本與 Identity 表）。
- 狀態：user-must-provide（重用前小步重驗；`live-routine-reconciliation` 已內建重驗指引與
  fail-closed 停損）。
- 何以解：每次使用時的現場 get/update 迴圈本身即驗證；若平台改語義，程序第 4–5 步會當場暴露。
- Issue：未開（外部服務，非兩個 repo 的缺陷）。

## 4. 跨模型審查的工具面細節（模型 slug、effort 值、wrapper 路徑）

- 主張/風險：`gpt-5.6-sol`/`gpt-5.6-luna`/`grok-4.5` 與 effort 字面值屬 owner 本機
  ＋供應商當期狀態；換機器或供應商改版即失效（sol 的 effort 曾記錄為 ultra、owner 二度更正為
  max——同一類漂移的實證）。
- 狀態：陣容**規則**＝verified 的 owner 決策（2026-07-26）；工具**細節**＝user-must-provide。
- 何以解：每次會話現場 discovery＋以 owner 最新指示為準（`review-and-merge-workflow` 已載）。
- Issue：未開。

## 5. Executor run 的原始報告不可從 repo 稽核

- 主張/風險：zero-job run 不留 git 痕跡；其報告文字只存在於 owner 可見的 routine 通知與平台
  session。本庫關於「run 報告符合新契約」的完成定義因此依賴 owner 觀察通道。
- 出處：本會話多次以「請對照你的 push 通知」交棒驗證；事故原始 log 亦是 owner 轉貼（參與者
  引述，經 repo 時間軸旁證）。
- 狀態：partially-verified（契約文本與 PR 產物可稽核；run 報告本身 user-must-provide）。
- 何以解：starledger #207 的 machine-readable 診斷落地後，report 內容可部分落 repo 稽核面。
- Issue：不另開（同樣由 #207 承載）。

## 6. 本會話早段證據的可及性邊界

- 說明：事故 run 原文與「前一段分析」皆以 owner 在本會話首則訊息中的引述為據（參與者引述），
  已用 starledger git 時間軸独立旁證其可證部分（dataset 窗口、PR/commit 時刻）；未被旁證的
  細節（如該 run 的內部步驟敘述）僅作背景、未轉為權威規則。無「重建不可及上下文」之情事。

## 7. 本交付與 opus-pack `.gitignore` 的政策衝突（force-add 揭露）

- 主張/風險：opus-pack 的 `.gitignore` 刻意忽略 `skills-staging/`（與 `evals/`、`internal/`
  同組的本地素材政策）；本次交付被授權要求把庫**提交**在 `./skills-staging/` 之下。
- 處置：以 `git add -f` 入庫，`.gitignore` **未動**（其變更在本交付允許路徑之外）；
  `python3 .github/checks.py` 於檔案入 index 後全過（隱字元掃蕩涵蓋新檔；skill discovery 與
  plugin reachability 不受影響——`skills-staging/` 不是 marketplace skills root）。
- 狀態：追蹤政策＝maintainer 決策待定。
- 何以解／Issue：https://github.com/F-e-u-e-r/opus-pack/issues/98（三選一驗收準則已列）。

## 審查記錄（交付前三審，2026-07-30 執行完畢）

事實審查 1 BLOCKING／3 IMPORTANT／2 MINOR；教義審查 0／4／5；可用性審查 0／5／8。
BLOCKING（真空測試指令）與全部 IMPORTANT 已修入本版——含本檔 §1 的歸屬更正（事實審查
發現「empty manifest→停用」誤歸前代庫）與各技能的執行者/權限補句；MINOR 僅在不影響正確性
/安全/可用性時保留。逐項清單見交付 PR 描述的「Review findings」段。
