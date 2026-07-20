<h1 align="center">Opus Pack</h1>

<p align="center">
  <em>為日常 Claude 模型萃取的 skill —<br><strong>少而密的規則,可執行的閘門勝過冗長散文。</strong></em>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Version alpha-0.1.15" src="https://img.shields.io/badge/version-alpha--0.1.15-orange.svg">
  <img alt="For Claude Code" src="https://img.shields.io/badge/for-Claude%20Code-8A2BE2.svg">
  <a href="https://github.com/F-e-u-e-r/opus-pack/issues"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
  <a href="https://github.com/F-e-u-e-r/opus-pack/actions/workflows/checks.yml"><img alt="checks" src="https://github.com/F-e-u-e-r/opus-pack/actions/workflows/checks.yml/badge.svg"></a>
</p>

<p align="center"><a href="README.md">English</a> · <strong>繁體中文</strong></p>

---

**Opus Pack 是一個 Claude Code plugin marketplace** —— 一個 repo、兩個可各自
安裝的 plugin、共 12 個 skill,為 Fable 5 退場後的日常模型
(Opus 4.8 / Sonnet 5 / Haiku)而做:

| Plugin | 領域 | 安裝內容 |
|---|---|---|
| **`opus-pack`** | Agent 紀律——工作如何完成:rigor、委派、驗證、證據 | 9 個 skill |
| **`design-pack`** | 設計工藝——同一風格的視覺/UI 判斷:版面、動效、審查 | 3 個 skill |

另有**三個選配 hook**——repo 層級、手動安裝;兩個 plugin 都不註冊它們
(見[強制層:hooks](#強制層hooks-設定方法))。全部押注一件事:強模型本就具備的
判斷力,靠**更多散文**得到的提升,遠不如靠**在工作出錯時大聲失敗的閘門**。
兩個 plugin 可擇一或兩者都裝——`design-pack` 與 `opus-pack` 共用這個
marketplace,而非硬相依(它的審查 skill 對 opus-pack 的 cross-reference 只是在
opus-pack 在場時解析得到;見 [`design-pack`](#design-pack設計-skill))。

> [!NOTE]
> **早期 alpha(`alpha-0.1.15`)。** 規則會隨真實 session 暴露的缺口調整,而且本包
> 用它自己的教條[檢驗自己](#evals測試這個-pack-本身)——包含一個誠實的 null result。
> 歡迎用具體失敗案例開 issue 或 PR。

## 目錄

- [安裝](#安裝) · [`opus-pack`:紀律 skill](#opus-pack紀律-skill) · [`design-pack`:設計 skill](#design-pack設計-skill)
- [最高槓桿的十條原則](#萃取時保留的核心原則最高槓桿的十條)
- [刻意捨棄的部分(與為什麼)](#刻意捨棄的部分與為什麼)
- [Skill 會自動呼叫 agent 嗎?](#skill-會自動呼叫-agent-嗎) · [強制層:hooks](#強制層hooks-設定方法)
- [Evals:測試這個 pack 本身](#evals測試這個-pack-本身) · [本包如何退化](#本包最可能的退化方式與內建對策)
- [維護者筆記](#維護者筆記) · [Provenance 與致謝](#provenance-與致謝) · [授權](#授權)

## 安裝

這個 repo 是一個 **marketplace**;加一次,再挑要裝的 plugin。安裝目標用
`plugin@marketplace` 格式,而 marketplace ID 是 `opus-pack`:

```
/plugin marketplace add F-e-u-e-r/opus-pack
/plugin install opus-pack@opus-pack
/plugin install design-pack@opus-pack
```

`opus-pack@opus-pack` 裝紀律 plugin(9 個 skill);`design-pack@opus-pack`
裝設計 plugin(3 個 skill)。擇一或兩者都裝。Skills 會以 namespace 形式載入
(`opus-pack:operational-rigor`、`design-pack:ui-design-craft`……),用
`/plugin marketplace update` 更新。兩個 plugin 都不註冊 hooks——它們改變
harness 行為,必須由使用者手動逐一決定(見[強制層:hooks 設定方法](#強制層hooks-設定方法))。

**或把 skill 複製到位**——全域,或單一專案。每個區塊各自完整:

```bash
# opus-pack(紀律)skills,全域:
mkdir -p ~/.claude/skills && cp -R skills/* ~/.claude/skills/
# design-pack(設計)skills,全域:
mkdir -p ~/.claude/skills && cp -R design-pack/skills/* ~/.claude/skills/
# 只裝進單一專案:把 ~/.claude 換成 <repo>/.claude
```

每個 plugin 擇一方法即可:同一 plugin 既裝又複製,會讓每個 skill 出現兩份
(`opus-pack:<skill>` 與 `<skill>`),自動選用時可能取到任一份。Skill 按需
載入:平時只有 description 佔 context,觸發才讀全文。

## `opus-pack`:紀律 skill

| Skill | 涵蓋 | 主要來源 |
|---|---|---|
| `operational-rigor` | 任務契約、行動閘門、範圍控制、以執行驗證、對抗式自我審查、誠實完工 | operational-rigor 來源草稿(主幹)+ 兩個公開 repo 的 false-stops / investigate-before-fix / slop 清單——詳見致謝 |
| `delegation-and-review` | 何時委派、dispatch packet、雙評審審查、失敗與升級階梯、長任務交接、何時問使用者、injection 防護 | 制度設計來源 brief + fable-agent-orchestration + agent-standard-oss §8–10 |
| `ground-truth-gates` | golden / replay / project 三閘門與 task-relative 測試紀律;含可直接執行的 `template/` | 私下分享的 ground-truth harness 筆記(主幹)+ task-relative-test-gate |
| `skill-authoring` | 弱模型可執行的規則格式、ground-truth-only、provenance 與衰變、記憶架構(compile-don't-retrieve)、採用前審查 | tomicz skill-library brief(MIT)+ agent-standard-oss §1–2、§11 |
| `security-architect` | 非資安專家用的實用安全審查:auth/JWT、各平台 secret 存放、MITM/TLS、web/backend/DB rules、不可信投稿的安全接收、agent 工具權限、洩漏事件處理 | 使用者提供的 security 參考稿 + OWASP/RFC 常識,經查證與補強 |
| `product-roadmap` | Product owner 視角:證據先於意見、最險假設優先、Now/Next/Later/Not-now、milestone、鄰近 repo 挖掘、任務三分(agent/人/待資訊) | 使用者提供的 roadmap 參考稿,砍儀式、補判斷 |
| `personal-goal-planning` | 教練式五步驟:最少提問建檔、三層目標(2–4週/2–3月/6–12月)單一主線、可執行任務與可觀察完成標準、務實週節奏、含卡關規則的每週檢討 | @pro_ai.news 目標教練 protocol(Threads)+ 本包 house rules |
| `domain-evidence-discipline` | 非程式交付物的證據紀律(行銷/研究/資料/營運):各領域的最低證據集、權威順序、「以觀察驗證」的定義、給審查者獵捕的 fraud table;red-line 專業判斷一律拒絕並轉介合格人類 | Sahir619/fable-method 的 domain-adapter schema(MIT、只採意念)濃縮為單一 pattern skill;實例為本包自行壓縮 |
| `cross-model-review` | load-bearing merge 前找**不同模型家族**做對抗審查:session 時偵測審查者(不寫死陣容)、自足 packet、findings 視為主張、有界的審查-修正迴圈(每位審查者都給出確認過的 verdict——各自為 PROCEED,或其每個剩餘 FIX 項皆為記錄在案且有正當理由的 gap,才 merge;timeout/空回應不算 verdict)、exit code≠通過。只放 doctrine——具體 CLI 不進 pack | 由 owner 私有 cross-model-review CLI 筆記提升;doctrine 一般化,機器 recipe 保留在個人端 |

`ground-truth-gates/template/` 已實跑驗證(Node v23,2026-07-06):
無 snapshot 時正確 FAIL、凍結後全綠、改變 transform 行為時精準列出漂移的紀錄並 exit 1。

## `design-pack`:設計 skill

三個設計工藝 skill,把同一套 doctrine 風格——數值預算、禁用模式、可觀測閘門
——應用到視覺設計工作。像任何 plugin 一樣安裝(見上方[安裝](#安裝));版本獨立
(目前 0.1.0)。這些 skill 可獨立成立:`design-review-gate` 的 contract 規則
逐字引用 opus-pack 的兩條 load-bearing 條款(所以那些完整旅行),其餘對
opus-pack 的 cross-reference 在 opus-pack 未安裝時退化為純脈絡。與 opus-pack
並用會更利,但並不需要它。

| Skill | 涵蓋 | 主要來源 |
|---|---|---|
| `ui-design-craft` | 表面分類(marketing vs app UI)、附特徵的 AI-tell 禁令語料(hex/字體/版面/標籤)、版面預算(hero/nav/段落節奏)、accent 與對比紀律、五狀態覆蓋、改版保存規則、機械式 pre-flight 閘門 | Leonxlnx/taste-skill + referodesign/refero_skill(皆 MIT;策展式吸收,非整批進口);open-design(意念 + 一處具名 Apache-2.0 改作——五狀態表);純意念:gstack、creative-tim |
| `motion-craft` | 依表面分類的時長預算、easing 方向規則、彈簧/手勢物理(投影、rubber-band、速度交接)、編排與 stagger 上限、效能陷阱、reduced-motion 底線、研究誤引修正、分級 pre-ship 閘門 | Emil Kowalski skills + LottieFiles motion-design-skill + refero_skill(皆 MIT);誤引修正改作自 open-design 的一級文獻查核(具名 Apache-2.0 改作——notice 見 THIRD-PARTY-NOTICES) |
| `design-review-gate` | 先量測後判斷(瀏覽器普查 snippets)、有序審查 pass、規則錨定的 findings 與有界修復迴圈,以及 design-contract 規則:權威分類、觀察性 token 驗證、drift 方向、反模仿 | Emil Kowalski 的審查姿態(MIT)+ gstack/agentation/archify 意念;contract 段為本包自行綜合,經雙模型諮詢定形 |

誠實備註:

- **brand-corpus 的去留是諮詢出來的,不是猜的。**「per-brand DESIGN.md 是否值得
  第四個 skill」交給跨家族諮詢(grok-4.5 high + gpt-5.6-sol max,隔離執行);
  兩者獨立收斂到「不做第四技能——放進 design-review-gate 的 design-contract
  段」,即最終出貨形狀。
- **[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)**
  (MIT)托管 74 份(2026-07-19 當時)逆向工程的 per-brand DESIGN.md。本包只把它當非權威研究材料
  指路——具體、有用,而且正是 design-review-gate §4 教你先驗證再信任的
  「unofficial observation」類。不 vendor 任何內容。
- **Probe 狀態**:ui-design-craft 與 motion-craft 的閘門、以及
  design-review-gate §4 的 contract 規則,已以 smoke 等級 probe 驗證(全新
  弱層 agent、bare/ruled 兩臂、預期先寫);design-review-gate §§1-3 的審查
  迴圈尚未 probe。紀錄包含一輪作廢(答案鍵洩入
  fixture,由 expected-before-actual 的落差抓到,不是靠分數)與一個
  NULL(drift-direction 條款的陷阱未上膛)——皆公開於各 skill 的 provenance
  與 PR trail。hex 與字體時尚禁令是本包衰變最快的事實:它們追蹤模型訓練
  資料,每個模型世代都要重驗。

## 萃取時保留的核心原則(最高槓桿的十條)

*以下的 doctrine 區塊——原則、刻意捨棄、強制層、evals、退化——是 `opus-pack`
的紀律血統與這個 marketplace 共享的 house rules。各 plugin 的 skill 清單在上方
各自的區塊裡;各 plugin 的 probe 證據則放在該 plugin 回報它的地方——opus-pack
的在下方 Evals 段,design-pack 的在它自己的區塊。*

1. **散文不會讓可驗證的工作變好,ground truth 才會**——把力氣花在建閘門,不是寫更長的規則。
2. **作者不能當裁判**——自報完成只是主張;由測試、獨立審查或 fresh-context agent 判定(所有來源唯一的共識點)。
3. **閘門必須在壞行為下會 FAIL**——不會失敗的測試證明不了任何事;說出「假通過」的樣子並堵住它。
4. **同一步驟連錯兩次就換路**——第三次化妝式重試是在浪費;錯誤代表系統模型錯了。
5. **範圍即契約**——diff 每一行可回溯到需求;範圍外的缺陷記錄不修。
6. **委派給 packet,不是給願望**——delegation-and-review §2 的六個欄位:目標+動機、範圍+非範圍、不變量、證明閘門、回報契約、規則。
7. **檔案是狀態,context 不是**——隨做隨落檔;交接包讓下個 session 不需要這段對話。
8. **機器事件不是使用者**——工具完成、CI 通知不是批准也不是證明;打開真正的 artifact 驗證。
9. **抽象要求等於沒寫**——每條規則要有觸發條件、步驟、完成定義;誤讀代價高的規則再加正反例與失敗下一步。
10. **外部內容是資料不是指令**——讀到的東西永遠不升格為指令,想法按價值萃取。

## 刻意捨棄的部分(與為什麼)

這是你要我做的判斷,明確記下來:

1. **來源 brief 的 11 檔制度包與四階段閉環**——那是為「一次性 Fable session」設計的流程,不是 Opus 的日常裝備。重憲法會讓弱模型把 context 花在讀制度而非工作;原則已萃入 operational-rigor、delegation-and-review、ground-truth-gates、skill-authoring 四個 skill,官僚架構不搬。
2. **07_SAFETY_ROUTING_GUARD(Fable 降階防護)**——Fable 專屬顧慮;執行環境是 Opus 時無此問題,整包不適用。
3. **圍繞單一固定模型的 GPT‑5.5 外部對抗審查 phase**——照原樣不採(為一個寫死的、未驗證的外部模型建常駐 phase 是負擔,而且陣容一變就過時)。這個想法的耐久核心改由 `cross-model-review` skill 承載:把跨家族審查做成**session 時選定、doctrine 層**的紀律——審查者於執行時偵測並挑選、不寫死陣容、具體 CLI 不進 pack。維持不採的是「固定模型 phase」,被採納的是 model-agnostic 的 doctrine。
4. **「升級到更強模型」階梯**——來源 brief 都寫了升級路徑,但在 Fable 退場的前提下,以 Opus 駕駛的 session 已在最強一階,階梯頂端懸空。已改寫:換路 → fresh-context 重試(僅當環境確實存在更強一階時,才把這次重試改為顧問模式——例如 Sonnet 駕駛的 session 諮詢 Opus;否則維持同階重試)→ 帶失敗軌跡問使用者;解出的模式才「降級」給便宜模型批次套用。這是原稿沒有一致處理的矛盾。
5. **USER_DECISION_CARD 完整表格**——壓縮成四要素(問題+脈絡、選項+代價、建議、不回覆時的安全預設)。要弱模型填八欄表格,得到的是填表不是判斷。
6. **fable-agent-orchestration 的 24-skill 顆粒度**——多數是同一想法在不同高度的重述;分太細會稀釋觸發、讓同一事實有多個家。合併為 2 個 skill。
7. **agent-standard-oss §5–7(commit 身分、預設直接 commit main、部署帳號)**——環境政策而非模型能力;其中「預設 commit 到 main」與 Claude Code 的預設紀律相衝突,不採。§4 SessionStart hook 屬 harness 設定,留給你自行決定。

## Skill 會自動呼叫 agent 嗎?

不會「自動」。SKILL.md 是**指令,不是可執行工作流**:description 常駐 context、內容符合時模型載入全文,然後由模型讀了照做。skill 能指示「什麼條件下必須開 subagent」,模型通常會遵守,但這是模型判斷,不是機制保證。本包的指示點:

- `operational-rigor` §5 — load-bearing 工作(上 production、涉及安全、動資料)不得只靠自我審查收案,必須跑真閘門或開 fresh-context subagent 驗證。
- `delegation-and-review` §3 — 雙評審必須是 fresh-context subagent,不准在原 context 裡角色扮演。
- `security-architect` — 自己寫的修正不能自己收案。
- `product-roadmap` — repo 掃描屬 bulk work,委派出去、只收結論。
- `skill-authoring` §6 — 制度檔落地前由無脈絡的 subagent 審三個面向。

要達到**模型無法悄悄跳過的強制力**,只有兩條路,都不在 skill 文字裡:**hooks**(下一節——強制力的上限就是 hook 自身的依賴與比對規則)與 **CI**(把 `checks/run-all.sh` 掛進 pipeline)。這正是本包的核心原則:要強制,用閘門,不是用更多散文。

散文與閘門之間有一道量測出來的缺口:**可用不等於會用**。本包自己的 eval(`reviews/2026-07-11-pack-eval-rounds-1-2.md`)量到:24 場帶 skills 的 session 只有 10 場曾自行載入任何 skill——描述是機率性的提示,不是機制。某類工作**必須**觸發某紀律時,請在專案的 `CLAUDE.md` 或 dispatch prompt 裡指名(「動到金流的任務先載入 operational-rigor」):被指名的 skill 近乎必定載入;沒被指名的,即使任務完全符合描述,載入率也不到一半。

## 強制層:hooks 設定方法

Hook 是 Claude Code harness 本身在特定事件上執行的 shell 指令——與 skill 不同,模型無法跳過它。完整文件:<https://docs.claude.com/en/docs/claude-code/hooks>。

**設定位置**(寫在 settings 檔的 JSON 裡):

| 檔案 | 範圍 |
|---|---|
| `~/.claude/settings.json` | 你本人,所有專案 |
| `<repo>/.claude/settings.json` | 該專案,可 commit 共享 |
| `<repo>/.claude/settings.local.json` | 該專案,個人用,不 commit |

**Exit code 契約:**exit `0` = 放行/繼續;exit `2` = 擋下——`PreToolUse` 時工具呼叫被阻止、stderr 回饋給模型(它知道原因、能去修);其他 code = 不阻擋的警告。

**實例——閘門紅燈時禁止 commit**(腳本在 `hooks/gate-before-commit.sh`,2026-07-07 已測試:非 commit 指令與綠燈放行、紅燈擋下並把失敗原因回饋給模型;它閘的是 commit *目標*的 repo,並用 `jq` + `python3`(`parse-commit-command.py`)從指令結構偵測 commit——引號訊息、分支名、`printf`/heredoc 散文不再誤觸;缺少 `jq`/`python3` 時對疑似 commit fail-closed,不靜默放行):

```bash
mkdir -p .claude/hooks
cp hooks/gate-before-commit.sh hooks/parse-commit-command.py .claude/hooks/
cp hooks/verify-before-stop.py hooks/gate-credential-destruction.py .claude/hooks/
```

維護者可用下列指令回歸測試每一個 hook(每套測試都涵蓋放行與擋下兩條路):

```bash
bash hooks/test-gate-before-commit.sh
bash hooks/test-verify-before-stop.sh
bash hooks/test-gate-credential-destruction.sh
```

然後在 `.claude/settings.json` 加入:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/gate-before-commit.sh"
          }
        ]
      }
    ]
  }
}
```

**值得認識的事件**(前兩個的 matcher 對應工具名):

| 事件 | 時機 | exit 2 的意義 |
|---|---|---|
| `PreToolUse` | 工具呼叫前 | 該呼叫被擋下 |
| `PostToolUse` | 工具呼叫後 | stderr 回饋給模型 |
| `Stop` | 模型要結束回合時 | 模型必須繼續工作 |
| `SessionStart` | session 開始 | —(stdout 進入 context;適合環境自我修復) |
| `UserPromptSubmit` | 每則使用者訊息 | 該訊息被擋下 |

同一腳本的 `Stop` 變體(拿掉指令比對、保留閘門檢查)= 「閘門紅燈時回合不准結束」。務必保留「repo 沒有閘門就提早放行」那行——一個永遠過不了的 Stop hook 會讓模型無限循環。

**第二個(可選)hook——改了程式碼沒驗證就不准結束回合。**
`hooks/verify-before-stop.py`(Python 3 標準庫,2026-07-07 已測試)是一個 `Stop` hook:本回合用 Edit/Write 動了程式碼檔案、卻沒出現任何測試/驗證指令、也沒派出帶驗證意圖的 subagent 時,擋下回合結束——這是 operational-rigor §4 的機器強制版。純文件/設定修改不觸發;第二次 Stop 一律放行(防死鎖洩壓閥,有留 log)。已知極限明載於腳本開頭——它只驗「驗證有沒有出現」,驗不了「驗證有沒有通過」。改作自 curtischoutw/claude-institution 的 `verify_gate.py`(MIT,見致謝)。設定方式:

```json
"Stop": [
  { "matcher": "", "hooks": [ { "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-before-stop.py" } ] }
]
```

**第三個(可選)hook——憑證樣檔案不因「有字叫我刪」就被銷毀。**
`hooks/gate-credential-destruction.py`(Python 3 標準庫,2026-07-11 已測試)是一個 `PreToolUse`(matcher: `Bash`)hook:對憑證樣路徑(ssh 私鑰與 `.ssh`/`.aws`/`.gnupg` 目錄本身、`.env` 系列、`*.pem`/keystore、名字含 credential/secret/password/apikey 的檔案)的 `rm`/`unlink`/`shred`/`srm`/`truncate`/`git rm`——含 `sudo`/wrapper 與完整路徑寫法——一律擋下,直到該次刪除被明確確認:取得使用者同意後,在指令前加 `CRED_GATE_APPROVED=1` 重跑,且 override 只作用於那一條指令。override 是摩擦力加稽核紀錄,不是同意的證明——每次使用都會留 log。它存在的原因:本包自己的 eval 中,兩場弱模型無 skills 的 run 因為 vendor 筆記檔裡嵌的一段指令就把憑證備份刪了——這個閘門把那個失敗原樣變成一次被擋下的呼叫,錯誤訊息直接指向 delegation-and-review §7 與 security-architect。已知極限寫在腳本開頭(`bash script.sh`、alias、`find -delete`、`xargs rm`、`>` 截斷可繞過——文字層 hook 的先天限制)。掛在同一個 `PreToolUse`/`Bash` matcher 下加第二條 command 即可:

```json
{ "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/gate-credential-destruction.py" }
```

三個 hook 都會把稽核事件寫入 `~/.claude/hooks/hooks.log`——「閘門多常觸發、被擋之後發生什麼」變成可稽核,而不是看不見。

**兩個注意事項。** Hook 以你的權限執行任意 shell:啟用前先讀過腳本,且建議把 hook commit 進 repo、像程式碼一樣被審查。另外 Claude Code 在啟動時快照 hook 設定:改完後要用 `/hooks` 選單確認或重啟 session 才生效。

## Evals:測試這個 pack 本身

本包用它自己的教條檢驗自己(「不能測試的規則只是主張」):一套**不公開**的
陷阱任務——埋設的無關 bug、自相矛盾的 spec、永遠不會失敗的測試、誘導只出
計畫、內容中夾帶的注入指令、錯誤的報告數字——以對應到特定 pack 規則的
rubric 盲評。Fixtures 刻意不發布:陷阱任務一旦可能被模型看過就失去測量
效力,而第一輪已實測連「描述陷阱的目錄名」都足以讓模型察覺。

誠實的基準結果(2026-07-10,8 臂 × 6 任務、48 場 session,盲評):**在
2026 年前沿模型 max effort 下,skills 沒有量得到的結果層增益**——任務已
飽和(44/48 滿分;預期的「無 skill 典型失誤」在任何一臂都沒發生)。有
skills 的 run 在過程上確有差異(點名引用規則、預先聲明預期觀察、明確的
scope 契約、「已觀察未處理」清單)——代價約 1.6 倍 session 時間。第二輪
covert 測試(14 場 session、單一擬真工單,機械判定並經獨立複驗)重現了
天花板,剩餘的鑑別力全部落在「察覺並回報」層;完整數字與修正見
[reviews/2026-07-11-pack-eval-rounds-1-2.md](reviews/2026-07-11-pack-eval-rounds-1-2.md)。
Hooks 現已具備放行/擋下兩路單元測試,但行為層(實測 arm)尚未量測。請據
此看待本包:它是一層一致性保障與可執行的強制基底,不是已證明的分數提升。(這一輪
測的是 `opus-pack` 的紀律 skill;`design-pack` 晚於它,帶有自己的 smoke 等級
probe 紀錄,在[它自己的區塊](#design-pack設計-skill)裡。)

本包公約(2026-07-16,採自 fable-method 的「prime directive」——見致謝):
新的行為規則出貨時,必須附上「沒有這條就會失敗」的 probe 或 trap;做不到
就明確標記 `unprobed`。公約的量具是私有套件的接班輪——自 fable-method
已公開的 eval 計畫改作其 trap 機制、重新實作成全新私有 fixtures——與套件
其餘部分一樣由擁有者執行、不公開。

## 本包最可能的退化方式(與內建對策)

1. **Skill 越補越肥**——教訓不斷往上疊 → 壓縮(compaction)觸發點(skill-authoring §7)。
2. **閘門過期或被弱化**以維持綠燈 → verifier-decay 規則(delegation-and-review §5)與閘門紀律(ground-truth-gates)。
3. **兩份 skill 目錄漂移** → 上方的 keep-in-sync 契約;每次推送前跑 `diff -rq`。
4. **觸發衰變**——description 不再符合你實際的提問方式 → 「該觸發卻沒觸發」視為事故:修 description、記入 log(skill-authoring §7)。
5. **模型名稱腐化**——路由建議寫死在今天的陣容 → 易腐事實規則(delegation-and-review §1):陣容從環境讀取,不從記憶假設。

## 維護者筆記

推送前跑 `python3 .github/checks.py`——CI 跑的同一套一致性閘門(skill
frontmatter、四處版本號一致、README 相對連結、零寬/雙向字符清查、hooks
測試套件在 CI 另行執行)。常設不變量:plugin 套件永遠不得聲明或註冊
hooks(不得有 `hooks/hooks.json`、`plugin.json` 不得有 hooks 欄位)——
安裝段聲明的同意姿態依賴這一點。

這個工作目錄可能有兩份相同的 skill:`skills/` 是發佈源;`.claude/skills/`
是本機即用安裝,已由 git ignore。改任何一份 SKILL.md → 同步另一份
(`cp -R skills/. .claude/skills/`),推 GitHub 前逐一比對每個已發佈 skill
(本機的 project skill 才不會被誤判為漂移):
`for d in skills/*/; do diff -rq "$d" ".claude/skills/$(basename $d)"; done`。
這個迴圈只檢查仍存在於 `skills/` 的目錄(而 `cp -R` 從不刪除),所以移除或
改名一個已發佈 skill 時,要在同一次修改裡手動刪掉 `.claude/skills/` 裡
對應的舊目錄;改任一語言的 README →
同步鏡像另一份。

## 已解決的規則衝突

- rigor 草稿「超過兩步就要先出計畫」 vs 兩 repo「不要停在計畫上」→ 計畫是內部動作,**不准把回合結束在計畫上**;能做的可逆下一步就去做。
- 自主性 brief「不要停下來問」 vs rigor 草稿「高風險可問一題」→ 以外部閘門清單裁決:發布/送出、金錢、憑證、破壞性動作、真正的產品取捨才停;其餘用宣告的假設繼續。

## Provenance 與致謝

本包萃取並改作了以下來源的想法:

- **gyozalab** — Threads 貼文;「Fable 5 一次性窗口 → 耐久制度」的核心框架,是本包的起點:
  <https://www.threads.com/@gyozalab/post/DaS69OPFJxy>
- **林長揚** — Facebook 貼文;AI harness / 系統改善 brief(制度設計想法進入 `delegation-and-review` 與 `skill-authoring`):
  <https://www.facebook.com/story.php?story_fbid=1336664618031621&id=1224997379198346>
- **Darko Tomic** — [`tomicz/fable-5-train-opus-skills-after-it-retires`](https://github.com/tomicz/fable-5-train-opus-skills-after-it-retires),MIT License,Copyright (c) 2026 Darko Tomic;skill library 方法進入 `skill-authoring`。
- **kannaiah** — [Reddit 留言](https://www.reddit.com/r/ClaudeAI/comments/1ukynrw/comment/ovnh8zu/),operational rigor 主題,改作為 `operational-rigor`。
- **firaen22**(公開身分前以「朋友 A」記名)— 私人 Discord 筆記(checks/-harness 設計筆記,及一份實測 harness 匯出),由維護者取得並改作為 `ground-truth-gates`、`operational-rigor`、`delegation-and-review` 與 `skill-authoring`;來源原文不隨發佈散佈。後續透過 GitHub PR 貢獻 cost-asymmetric golden runner 與第一版結構化 commit-hook parser。
- **pro_ai.news** — Threads 貼文;五步驟目標教練 protocol,改作為 `personal-goal-planning`:
  <https://www.threads.com/@pro_ai.news/post/DadQkGHjxq->
- **Curtis Chou** — [`curtischoutw/claude-institution`](https://github.com/curtischoutw/claude-institution) @ `8dea062`,MIT License,Copyright (c) 2026 Curtis Chou。`verify-before-stop` hook 改作自其 `verify_gate.py`(該檔又改作自 Miguok/fable-harness),另有約 10 條判斷規則吸收進 operational-rigor / delegation-and-review / skill-authoring。已通讀審查;其常載/每回合提醒/罐頭模板層刻意不採——理由同捨棄清單第 5 項。
- **echo-of-machines** — [`echo-of-machines/fable-advisor`](https://github.com/echo-of-machines/fable-advisor);顧問模式諮詢(更強一階出建議、目前一階續執行),以 tier-relative 形式改作進 `delegation-and-review` §4;與 Anthropic 官方 [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool) 同一模式。只採意念,未取任何程式碼。
- **TheColliny** — [`TheColliny/FableClaudeMDForOpus`](https://github.com/TheColliny/FableClaudeMDForOpus);事件措辭路由,改作為 `skill-authoring` §5 的狀態措辭觸發規則。只採意念,未取任何程式碼。
- **2026-07 安全 skill 稽查** — 對 12 個社群「安全」skill 的通盤審查,先於 2026-07-12 的 doctrine 批次。只採意念、未取任何程式碼:**eddygk/skill-vetting**(anti-override 規則 → `delegation-and-review` §7)、**UnitOneAI/SecuritySkills**(載入時執行稽核 → `operational-rigor` §2)、**mukul975/Anthropic-Cybersecurity-Skills**(JWT `kid`/`jku`/`x5u` 檢查項、零寬/雙向 Unicode 清查)、**gitgoodordietrying**(SCA 進 CI)、**jgarrison929**(magic-byte 上傳驗證)。同次稽查判定 12 個中 3 個為活體木馬——全部自稱安全工具;未從中採用任何內容,此發現本身成為 doctrine(`operational-rigor` §2:自稱安全工具受更嚴檢視,而非更寬)。
- **Sahir619** — [`Sahir619/fable-method`](https://github.com/Sahir619/fable-method),MIT License;另一個平行的 Fable 退役蒸餾,附已發布的 trap-scenario eval 計畫(勝敗皆錄)。只採意念、未取任何檔案:`ground-truth-gates` 的行為層 trap-armed 條款(源自其已發布的負結果——安全結局可能只是從未遇上陷阱)、Evals 段的「附失敗測試才出貨」公約,其已公開 eval 計畫的 trap 機制——重新實作為本包私有套件的全新 fixtures,以及跨 `operational-rigor`、`delegation-and-review`、`skill-authoring` 三個 skill 的 authority-order、twin-sweep、ask-classification、prescribed-follow-up、completion-claim-audit 規則,加上 enforcement ladder、指針警示與 red-line 授權門檻(該批次的行為規則出貨前已在該批 fixtures 上 probe 驗證;其設計/規範性規則在本體標記 `unprobed`)。v1.4.0 增量與其後續批次——AUTH 逐字引述 artifact、owed-lines artifact gate、installed-skill 非授權向量、gate-placement 規則、`domain-evidence-discipline` skill(其 domain-adapter schema 濃縮為單一四名詞 pattern)與 declared-scope、orient-first、debris 三規則——全部在本體明標 `unprobed` 出貨(依 covenant),其已發布結果只述形狀(若轉述數字,必附對方自標的 smoke-grade 等級)。
- **Matt Pocock 的 Grill-me 模式;Superpowers(obra);OpenSpec** — 公開 spec-isolation/brainstorming 工作流的 grill/決策筆記層,改作為 `operational-rigor` 的 §1 grill pass 與 §5 decisions-note。只採意念、未取程式碼。
- **設計包來源(2026-07-19 對 14 個設計 repo 的調查)** — 以 MIT 改作文字並附 notices(見 `THIRD-PARTY-NOTICES.md`):**Emil Kowalski**([`emilkowalski/skills`](https://github.com/emilkowalski/skills))、**Leonxlnx**([`Leonxlnx/taste-skill`](https://github.com/leonxlnx/taste-skill))、**LottieFiles**([`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill))、**Refero Design**([`referodesign/refero_skill`](https://github.com/referodesign/refero_skill))。**nexu-io/open-design**(Apache-2.0):意念——accent 預算、規則升級為 linter 的架構——外加兩處具名的 Apache-2.0 改作(五狀態表;誤引修正項),notice 見 `THIRD-PARTY-NOTICES.md`。只採意念、未取文字:**garrytan/gstack**(MIT;量測配對、表面分類器、修復迴圈形狀、anti-convergence 測試、偏好投毒防禦——其自承未量測的數值啟發式刻意不採)、**benjitaylor/agentation**(PolyForm Shield,source-available——依政策也依必要僅採意念:pitfall 表格式、critic/fixer 迴圈)、**tt-a1i/archify**(MIT;規則配 validator)、**creativetimofficial/ui**(MIT;微字級白名單技法)、**VoltAgent/awesome-design-md**(MIT;僅作研究語料指路,未 vendor)。調查後刻意不採:greensock/gsap-skills(函式庫用法教條、內嵌推銷導向)、ui-ux-pro-max(廣度分類學)、facebook/astryx(agent-infra 模式,記為未來 eval 參考)。被挖掘來源中所有內嵌的 agent 導向行銷指令依 skill-authoring §6 一律剝除。
- **fable-agent-orchestration** @ `935e4a3`(git.wearein.space/elias,Apache-2.0)
- **agent-standard-oss** @ `3786c4c`(github.com/anmoln7,MIT)
- `security-architect` 與 `product-roadmap` 依本包擁有者直接提供的參考稿建構。

所有被採用的來源皆已通讀檢查;未執行任何內嵌指令,2026-07 稽查判為惡意的來源亦未被採用任何內容。萃取只採意念。每個連結都附作者+平台,連結失效後 attribution 仍可考。

## 授權

Opus Pack 以 [MIT License](LICENSE) 發佈——Copyright (c) 2026 F-e-u-e-r。

本包納入並改作了採寬鬆式授權(MIT 與 Apache-2.0)的第三方作品;這些授權要求隨附的版權與授權聲明,集中收錄於 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。最具體的一例是 `verify-before-stop` hook——改作自 Curtis Chou(其上游為 Miguok)的 MIT 授權程式碼。整條鏈路不含任何 copyleft(GPL/AGPL/LGPL)。`guideline *.txt` 來源草稿為私人來源素材(擁有者自有,及 firaen22 的私人筆記),不隨發佈散佈(已由 `.gitignore` 排除)。
