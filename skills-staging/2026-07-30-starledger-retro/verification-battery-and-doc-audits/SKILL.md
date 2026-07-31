---
name: verification-battery-and-doc-audits
description: 在 starledger 改了任何程式碼或 docs、要在 push 前跑本地驗證、或改動 canonical prompt / runbook 這類「prettier 管不到的 fenced 區塊」時載入。這是本地驗證管線與文件機械稽核的實測配方。
---

# starledger：本地驗證管線與文件機械稽核

（驗證日 2026-07-30，HEAD `55ae7b2`。CI 的 `verify` job 跑同一套＋smokes＋schema drift＋
deploy verify；本地先綠＝CI 大機率綠。）

## 程式碼／全域管線（依序）

```bash
pnpm install --frozen-lockfile   # 分支剛切、或 lockfile 動過時必跑
pnpm typecheck && pnpm lint
pnpm exec prettier --check <你動過的檔案們>   # 見下方「範圍化」陷阱
pnpm test:coverage               # vitest 全套含 coverage 門檻（2026-07-30 為 750 tests）
pnpm build
```

- **prettier 範圍化陷阱**：`pnpm format:check` 是 `prettier --check .`——**未追蹤**的本地目錄
  也會被掃（實例：untracked `skills-staging/` 讓 repo-wide check 紅，但 CI 只 checkout 追蹤
  檔所以綠）。判斷自己的變更時用範圍化的 `pnpm exec prettier --check <files>`；repo-wide 紅
  先看紅的是不是 untracked。
- prettier 對 `.md` 生效（printWidth 100、proseWrap 預設 preserve＝不重排你手動換行的散文）。
  fence 的邊界要分清：**受支援語言的 fence（json/ts/js…）會被重排**（實測：json fence 的
  `{"a":1}` 會被展開）；`text`／未知語言的 fence 才是盲區——canonical prompt 正是 ` ```text `
  fence，所以整塊 prettier 管不到，必須機械稽核（下節）。
- **vitest 路徑陷阱**：include pattern 是 repo-root 相對（`packages/**/tests/**`）；從套件目
  錄跑 `vitest run tests/x.test.ts` 會「No test files found」。永遠從 repo root 用完整路徑：
  `pnpm exec vitest run packages/classifier/tests/<file>`。

## 文件機械稽核（改 runbook/prompt 必跑）

```bash
# 1. 新增行長（既有檔已有 >100 的合法長行——只稽核你「新增」的行）
git diff -U0 origin/main -- docs/ | grep '^+' | grep -v '^+++' | sed 's/^+//' | awk 'length($0)>100 {print "LONG: "$0}'
# 2. fence 奇偶（fenced block 被切壞是 prettier 抓不到的）
grep -c '^```' docs/routines/starledger-ai-classification.md docs/P3.2-executor-runbook.md
# 3. canonical prompt 的 1.–14. 步全數在場
for n in $(seq 1 14); do grep -qE "^${n}\. " docs/routines/starledger-ai-classification.md || echo "MISSING step $n"; done
```

## 指令實測（dogfooding）模式

文件裡寫的指令，**從已套用的文件逐字抽出來跑**（防手滑改壞），斷言**不變量**而非當下數字
（語單天天長）：

```bash
# 例：抽 3c 的 node 一行式並執行（fence slice；'node -e "' 到 '"' 的唯一區段）
sed -n '/^       node -e "$/,/^       "$/p' docs/routines/starledger-ai-classification.md | sed 's/^       //' | bash
# 斷言：extra=0、duplicates=0、且 stars−missing == annotations−duplicates−extra
```

負例（真實）：驗證腳本硬編 `685/673/12`——同日兩個 PR 合併後數字全變；owner 明示「不要在
script 中硬編數字，只斷言不變量」。

**完成定義**：管線五步綠＋（動了 docs 時）三項機械稽核過＋dogfooding 斷言成立——然後才
commit/push。

## 再驗證

```bash
rg -n '"format:check"|"test:coverage"' package.json      # scripts 仍如上
cat .prettierrc.json                                     # printWidth 100（proseWrap 未設＝preserve）
```
