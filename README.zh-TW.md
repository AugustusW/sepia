# sepia

[English](README.md) | **繁體中文**

> 在真正洩底的那一層去 AI 味。小說先修敘事架構，再碰字句；專業文件（release 公告、PR 回覆、postmortem、工單、技術文章）各自套用貼合 venue 的規則。

可攜的 [Agent Skill](https://agentskills.io/specification)，支援 Claude Code、Codex、Grok Build、Antigravity。一份 canonical `SKILL.md`，不為平台分叉。四種操作：**write**、**review**（只診斷）、**refactor**（最小修改）、**recreate**（整篇重寫）。

## 為什麼還需要另一個 humanizer

市面上的 humanizer 都在改用詞與句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026：61,608 篇故事，人類＋5 個前緣 LLM）證明：只用**敘事結構特徵**的分類器就能以 93.2% macro-F1 偵測 AI 小說，而把表面風格洗掉幾乎不影響偵測率（95.5% → 93.9%）。留下來的破綻全是架構性的：敘事者把主題講明、因果整齊的單線情節、情緒只用身體感官呈現、不引用真實世界、無視讀者、時間全程線性、結局靠主角的成長與釋懷收束。

sepia 把這些量化落差，連同 [`research/`](research/) 裡消化過的十一篇相關研究，整理成小說寫作與改稿的三段 pass：

| Pass | 層次 | 例子 |
|---|---|---|
| 1 | 敘事架構（小說） | 別解釋主題、鬆開因果鏈、把揭露往後放、混用情緒表達模式、稀疏的角色網絡、指名真實事物 |
| 2 | 篇章推進 | 拆掉段落問題序列的模板、修中段鬆垮、變化節奏與位置 |
| 3 | 表面風格 | 經典層：cliché、句法模板、詞彙、語域 |

另附 30 特徵診斷 rubric 與各模型指紋校正表（Claude、GPT、Gemini、DeepSeek、Kimi）。

專業文書壞的方式不一樣。研究指向的是：不帶資訊的填充、該下判斷時的閃躲、chatbot 殘留、無視 venue 的語域、蓋章式的整齊格式。每種文件型態在一份共用 checklist 之上各配一個精簡規則檔：

| 領域 | 要點 |
|---|---|
| Release 公告 | 使用者衝擊優先、每個宣稱附 artifact、不灌行銷詞 |
| PR／issue 回覆 | 第一句就是答案、引 `file:line`、不反射性稱讚、篇幅與 stakes 成比例 |
| Postmortem | 對人 blameless、對機制不留情；時間戳、死路、有主的 action items |
| 工單 | 標題＝結果、驗收條件可測試、能連結就不重複 |
| 技術文章 | 從問題開場、至少一條真實死路、敢下一個判斷、數字附條件 |

貫穿全部的原則：**校準到人類分布，而不是把 AI 特徵反著做。**人類落在中間值；一篇把所有規則用好用滿的故事，只是另一種指紋。skill 每篇挑 3–5 個手法，其餘留白。

## 安裝

預設 **user scope**——裝一次，每個專案都能用。下列 CLI 路徑本身就是 user scope；session 內的 `/plugin install` 對話框會要你選 scope，記得選 **User**。

**Skills CLI（77+ 個 agent，執行時選你的）：**

```bash
npx skills add Nanako0129/sepia -g
```

`-g` 才是 user scope（預設是 project）。之後用 `npx skills update -g` 更新。

**Claude Code plugin（Grok Build 順帶生效）：**

```bash
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user
```

Grok Build 會自動探索 Claude Code 的 plugin，所以同時用 Claude Code 的 Grok 使用者裝這份就夠。

**沒有 Claude Code 的 Grok Build：**跑 `./install.sh`（鏈進 Grok 原生的 `~/.grok/skills/`），或在 Grok 的 Marketplace 分頁直接加 `Nanako0129/sepia`——Grok 可直接使用 Claude Code 格式的 marketplace repo。

**四平台一行裝完：**

```bash
curl -fsSL https://raw.githubusercontent.com/Nanako0129/sepia/main/install.sh | bash
```

這行會把 repo clone 到 `~/.sepia`（可用 `SEPIA_HOME` 覆寫）並以 user scope 安裝；重跑同一行就是更新。想先看內容再跑？自己 clone 下來，從 checkout 執行 `./install.sh`，結果相同。兩種方式裝出來都是：

| 平台 | 位置 | 機制 |
|---|---|---|
| Claude Code | `~/.claude/skills/sepia` | symlink |
| Codex | `~/.agents/skills/sepia` | symlink |
| Grok Build | `~/.grok/skills/sepia`（原生路徑，不需要 Claude Code） | symlink |
| Antigravity | `~/.gemini/config/skills/sepia` ＋ `/sepia` global workflow | copy |

**Project scope（替代方案）：**當某個 repo 需要釘住自己的版本時，把 `skills/sepia/` commit 進該 repo 的 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

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

完整摘要與連結見 [`research/`](research/)。主要文獻：StoryScope（[arXiv:2604.03136](https://arxiv.org/abs/2604.03136)）、LAMP（[CHI 2025](https://arxiv.org/abs/2409.14509)）、Measuring AI Slop（[arXiv:2509.19163](https://arxiv.org/abs/2509.19163)）、Reinhart et al.（[PNAS 2025](https://arxiv.org/abs/2410.16107)）、Russell et al.（[ACL 2025](https://arxiv.org/abs/2501.15654)）、NarraBench（[arXiv:2510.09869](https://arxiv.org/abs/2510.09869)）、Echoes in AI（[PNAS 2025](https://arxiv.org/abs/2501.00273)）、QUDsim（[COLM 2025](https://arxiv.org/abs/2504.09373)）、Beguš（[2024](https://arxiv.org/abs/2310.12902)）、Beyond Checkmate（[EMNLP 2025](https://arxiv.org/abs/2501.19301)）、Nonaka & Perry（[2025](https://arxiv.org/abs/2510.18932)）、Chakrabarty et al.（[2026](https://arxiv.org/abs/2510.13939)）。

## 授權

MIT
