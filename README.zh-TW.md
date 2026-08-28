# sepia

[English](README.md) | **繁體中文**

> 從真正會讓 AI 洩底的層次下手。小說先修敘事架構，再碰字句；專業文件（發版說明、PR 回覆、事故檢討、工單、技術文章）則按 venue 各用一套規則。

這是一套可攜的 [Agent Skill](https://agentskills.io/specification)，支援 Claude Code、Codex、Grok Build 與 Antigravity。全平台共用唯一一份正典 `SKILL.md`，不另開平台分支。四種操作：**write**、**review**（只診斷）、**refactor**（最小修改）、**recreate**（整篇重寫）。

## 為什麼還需要另一個 humanizer

常見的 humanizer 都在改用詞與句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026：61,608 篇故事，涵蓋人類與 5 個頂尖 LLM）顯示，只靠**敘事結構特徵**的分類器就能以 93.2% macro-F1 偵測 AI 小說；把字句風格修掉，分類表現也只從 95.5% 降到 93.9%。留下的破綻都在架構層：敘事者直接講明主題、單線且因果收得過於工整的情節、情緒只靠身體感受呈現、沒有真實世界的參照、讀者缺席、時間全程線性，以及靠主角成長與接納收束的結局。

sepia 把這些實測差距，連同 [`research/`](research/) 裡整理過的十一篇相關研究，轉成小說寫作與修訂的三個 pass 流程：

| Pass | 層次 | 例子 |
|---|---|---|
| 1 | 敘事架構（小說） | 別再解釋主題、鬆開因果鏈、把揭露往後放、混用情緒呈現模式、稀疏的角色網絡、點名真實事物 |
| 2 | 篇章推進 | 拆掉段落—問題序列的模板、修掉故事中段的鬆垮、變換節奏與位置 |
| 3 | 字句風格 | 所有 humanizer 都在修的那層：陳腔濫調、句法模板、用詞、語域 |

另附 30 項特徵的診斷 rubric，以及各模型的指紋修正（Claude、GPT、Gemini、DeepSeek、Kimi）。

專業文字露餡的方式不同。研究指出，常見問題包括沒有資訊量的填充文字、該下判斷時還在閃躲、chatbot 殘留語氣、無視 venue 的語域，以及像同一個模子印出的排版。每種文件都共用一份檢查表，再各配一份精簡規則檔：

| 領域 | 要點 |
|---|---|
| 發版說明／公告 | 使用者影響擺前面、每項宣稱附佐證、不灌行銷詞 |
| PR／issue 回覆 | 先給答案、引用 `file:line`、不反射性稱讚、篇幅與事情的重要程度相稱 |
| 事故檢討 | 對人不究責，對機制追到底；附時間戳記、記錄走過的死路、每個行動項目都有負責人 |
| 工單 | 標題寫結果、驗收條件能測、能連結就別重複 |
| 技術文章 | 從問題切入、保留一條真實走過的死路、提出一個明確判斷、數字附上適用條件 |

貫穿全篇的原則：**以整個人類分布為校準目標，別把 AI 分布直接倒過來套**。人類的數值多落在中間。每條規則都用上的故事會形成另一種指紋；sepia 每篇只選 3–5 個手法，其餘留白。

## 安裝

每個平台都有原生安裝方式，也各自附上更新指令。全部預設採用 **user scope**：安裝一次，每個專案都能用。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

在 session 裡開啟 `/plugin install` 對話框時，系統會要求選 scope；請選 **User**。

### Codex

```bash
# install
codex plugin marketplace add Nanako0129/sepia
codex plugin add sepia@sepia

# update — refresh the marketplace snapshot, then re-add to pick up the new version
codex plugin marketplace upgrade sepia
codex plugin add sepia@sepia
```

### Grok Build

```bash
# install
grok plugin install Nanako0129/sepia --trust

# update
grok plugin update
```

Grok 也會自動找到既有的 Claude Code sepia 安裝；兩種方式都能用。

### Antigravity

Antigravity 沒有 marketplace；原生安裝方式是放入 Agent Skill 資料夾，再加上 `/sepia` slash workflow：

```bash
# install
git clone https://github.com/Nanako0129/sepia.git ~/.sepia
mkdir -p ~/.gemini/config/skills ~/.gemini/antigravity/global_workflows
cp -R ~/.sepia/skills/sepia ~/.gemini/config/skills/sepia
cp ~/.sepia/.agents/workflows/sepia.md ~/.gemini/antigravity/global_workflows/sepia.md

# update
git -C ~/.sepia pull
rm -rf ~/.gemini/config/skills/sepia && cp -R ~/.sepia/skills/sepia ~/.gemini/config/skills/sepia
cp ~/.sepia/.agents/workflows/sepia.md ~/.gemini/antigravity/global_workflows/sepia.md
```

### 四個平台一次裝完（替代方案）

```bash
curl -fsSL https://raw.githubusercontent.com/Nanako0129/sepia/main/install.sh | bash
```

這會把 repo clone 到 `~/.sepia`（可用 `SEPIA_HOME` 覆寫），並以 user scope 安裝到四個平台；重跑同一行就是更新。想先檢查內容？可自行 clone，從 checkout 執行 `./install.sh`。兩種方式都會安裝到：

| 平台 | 位置 | 機制 |
|---|---|---|
| Claude Code | `~/.claude/skills/sepia` | symlink |
| Codex | `~/.agents/skills/sepia` | symlink |
| Grok Build | `~/.grok/skills/sepia` | symlink |
| Antigravity | `~/.gemini/config/skills/sepia` ＋ `/sepia` global workflow | copy |

### Skills CLI（替代方案，77+ 個 agent）

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update -g                   # update
```

### Project scope（替代方案）

某個 repo 要固定自己的版本時，把 `skills/sepia/` commit 到該 repo，放在 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 目錄結構

```text
sepia/
├── skills/sepia/            # canonical skill (Agent Skills standard)
│   ├── SKILL.md             # routing, operations, calibration rules, guardrails
│   └── references/
│       ├── narrative-pass.md      # fiction pass 1: architecture (the differentiator)
│       ├── discourse-pass.md      # pass 2: paragraph-level flow
│       ├── style-pass.md          # pass 3: surface style
│       ├── rubric.md              # fiction 30-feature diagnosis
│       ├── model-fingerprints.md  # per-model corrections
│       ├── professional-pass.md   # shared non-fiction layer (slop checklist, venue matching)
│       └── domains/               # release-notes, dev-replies, postmortems, tickets, tech-articles
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
├── install.sh
└── research/                # digested evidence base with sources
```

## 資料來源

完整摘要與連結見 [`research/`](research/)。主要來源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 授權

MIT
