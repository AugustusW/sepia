# 四平台 plugin 格式研究（2026-08）

核心結論：四平台已收斂到 Agent Skills 開放標準（agentskills.io）。同一份 SKILL.md 可直接共用；只需打包層 adapter。

## 共通規格（canonical 要守住的）
- `skill-name/SKILL.md`；name ≤64 字元、小寫+hyphen、＝資料夾名
- description 1–1024 字元（what + when，關鍵字前置）
- frontmatter 只用 spec 六欄位：name, description, license, compatibility, metadata, allowed-tools（claude.ai 上傳會對其他欄位報錯）
- SKILL.md 本體 <500 行 / <5000 tokens；細節放 references/（相對路徑、一層深）
- progressive disclosure：啟動只載 name+description（~100 tokens）
- 驗證：`skills-ref validate ./my-skill`

## 各平台接入
| 平台 | 位置 | 觸發 | 轉換 |
|---|---|---|---|
| Claude Code | `~/.claude/skills/` / `.claude/skills/` / plugin `skills/`；plugin.json 在 `.claude-plugin/`；marketplace.json | 自動 + `/name` | 不用 |
| Codex | `.agents/skills/`（cwd→repo root→`~`）；`.codex-plugin/plugin.json`；custom prompts 已 deprecated | 自動 + `$name` | 不用 |
| Grok Build | 自動吃 Claude Code 的 skills/plugins/marketplaces；也有 `.grok/skills/` | 自動 + `/name` | 不用（零設定相容 Claude Code） |
| Antigravity | `.agents/skills/`（與 Codex 同目錄）或 `~/.gemini/config/skills/`；rules/workflows 每檔 12k 字元上限（skills 不受限） | 純 description 觸發，無 slash；要 slash 需 workflow 包裝檔 | 內容不用 |

## 建議 repo 佈局
```
repo/
├── skills/<name>/SKILL.md + references/   # canonical 唯一真相
├── .claude-plugin/plugin.json + marketplace.json
├── .codex-plugin/plugin.json              # "skills": "./skills/"
├── .agents/workflows/<name>.md            # （可選）Antigravity slash 包裝
├── install.sh                             # symlink 到各平台目錄
└── README.md
```
- Claude Code plugin 的 skills 預設路徑就是 `./skills/` → 零設定
- Grok 免安裝（自動發現 Claude 的安裝結果）
- Codex 與 Antigravity 共用 `.agents/skills/` checkout

官方文件：
- https://agentskills.io/specification
- https://code.claude.com/docs/en/skills / plugins-reference / plugin-marketplaces
- https://developers.openai.com/codex/skills / plugins/build/plugins
- https://docs.x.ai/build/features/skills-plugins-marketplaces
- https://antigravity.google/docs/skills / rules-workflows
