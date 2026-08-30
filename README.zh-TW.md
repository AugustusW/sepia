# sepia

[English](README.md) | **繁體中文**

> 從真正會讓 AI 洩底的層次下手。小說先修敘事架構，再碰字句；專業文件（發版說明、PR 回覆、事故檢討、工單、技術文章）則按 venue 各用一套規則。

這是一套可攜的 [Agent Skill](https://agentskills.io/specification)，支援 Claude Code、Codex、Grok Build 與 Antigravity。全平台共用唯一一份正典 `SKILL.md`，不另開平台分支。四種操作：**write**、**review**（只診斷）、**refactor**（最小修改）、**recreate**（整篇重寫）。

## 操作入口

完整 plugin package 會在 Claude Code、Codex 與 Grok Build 提供一個通用 router，以及四個可直接呼叫的操作入口：

| 操作 | Claude Code | Codex | Grok Build | 用途 |
|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | 撰寫新內容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | 只診斷，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | 依原始事實與意圖重新撰寫 |

通用 router 仍可透過 `/sepia`（Claude Code、Grok Build）或 `$sepia`（Codex）使用。操作 wrapper 依賴同一套 package 裡的正典 skill，不支援單獨安裝；請安裝完整 plugin package。這張表只記錄 package 語法；`v0.3.0` 尚未實測安裝後的 UI 與 runtime 行為。

Antigravity 的 `v0.3.0` 手動安裝流程仍使用 `/sepia <operation>`，不提供獨立操作入口。

## Star 趨勢

<a href="https://www.star-history.com/?repos=Nanako0129%2Fsepia&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Nanako0129%2Fsepia&type=date&theme=dark&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
  </picture>
</a>

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

Claude Code、Codex 與 Grok Build 使用各自的原生 plugin installer；Antigravity 依照下方的手動流程。全部預設採用 **user scope**：安裝一次，每個專案都能用。

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

Antigravity 沒有 marketplace。以下全新安裝固定使用目前的 `v0.3.0` release；任一目的地已存在就會中止：

```bash
(
  set -e

  skill="$HOME/.gemini/config/skills/sepia"
  workflow="$HOME/.gemini/antigravity/global_workflows/sepia.md"

  if [ -e "$skill" ] || [ -L "$skill" ] || [ -e "$workflow" ] || [ -L "$workflow" ]; then
    echo "Antigravity install aborted: move the existing skill and workflow aside first." >&2
    exit 1
  fi

  git clone --branch v0.3.0 --depth 1 https://github.com/Nanako0129/sepia.git "$HOME/.sepia"
  mkdir -p "$HOME/.gemini/config/skills" "$HOME/.gemini/antigravity/global_workflows"
  cp -R "$HOME/.sepia/skills/sepia" "$skill"
  cp "$HOME/.sepia/.agents/workflows/sepia.md" "$workflow"
)
```

Antigravity 沒有自動更新程式。要更新或回復舊版，先檢查想使用的 release，把目前的 clone、skill 與 workflow 移到自行命名的備份路徑，再用該 release tag 重做全新安裝。

### Skills CLI（替代方案，77+ 個 agent）

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update -g                   # update
```

### Project scope（替代方案）

某個 repo 要固定自己的版本時，把 `skills/sepia/` commit 到該 repo，放在 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 解除安裝

Claude Code、Codex 與 Grok Build 各自使用原生指令：

```bash
# Claude Code
claude plugin uninstall sepia@sepia --scope user

# Codex
codex plugin remove sepia@sepia

# Grok Build
grok plugin uninstall sepia
```

Antigravity 透過重新命名停用 skill 與 workflow，之後仍可復原。如果來源缺少，或任一 `.disabled` 目的地已存在，預先檢查會在移動前中止：

```bash
(
  set -e

  skill="$HOME/.gemini/config/skills/sepia"
  workflow="$HOME/.gemini/antigravity/global_workflows/sepia.md"

  if [ ! -e "$skill" ] && [ ! -L "$skill" ]; then
    echo "Antigravity disable aborted: skill not found." >&2
    exit 1
  fi
  if [ ! -e "$workflow" ] && [ ! -L "$workflow" ]; then
    echo "Antigravity disable aborted: workflow not found." >&2
    exit 1
  fi
  if [ -e "$skill.disabled" ] || [ -L "$skill.disabled" ] || [ -e "$workflow.disabled" ] || [ -L "$workflow.disabled" ]; then
    echo "Antigravity disable aborted: a .disabled target already exists." >&2
    exit 1
  fi

  mv "$skill" "$skill.disabled"
  mv "$workflow" "$workflow.disabled"
)
```

這些指令會保留 `~/.sepia` 供檢查。是否刪除該 clone，請另行手動決定。

## 目錄結構

```text
sepia/
├── skills/
│   ├── sepia/                # 正典 skill（Agent Skills standard）
│   │   ├── SKILL.md          # routing、operations、calibration rules、guardrails
│   │   └── references/       # passes、rubric、fingerprints 與 domain rules
│   ├── sepia-write/SKILL.md  # 固定單一操作的薄 wrapper
│   ├── sepia-review/SKILL.md
│   ├── sepia-refactor/SKILL.md
│   └── sepia-recreate/SKILL.md
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
└── research/                # digested evidence base with sources
```

## 資料來源

完整摘要與連結見 [`research/`](research/)。主要來源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 授權

MIT
