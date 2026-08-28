# sepia

> De-AI writing at the layer that actually gives AI away. Fiction gets its narrative architecture repaired before anyone touches word choice; professional documents (release notes, PR replies, postmortems, tickets, technical articles) each get rules matched to their venue.

A portable [Agent Skill](https://agentskills.io/specification) for Claude Code, Codex, Grok Build, and Antigravity. One canonical `SKILL.md`, no per-platform forks. Four operations: **write**, **review** (diagnose only), **refactor** (minimal edits), **recreate** (full rewrite).

## Why another humanizer

Every popular humanizer edits word choice and syntax. [StoryScope](https://arxiv.org/abs/2604.03136) (Russell et al., 2026: 61,608 stories, human + 5 frontier LLMs) showed that a classifier using **narrative-structure features alone** detects AI fiction at 93.2% macro-F1, and that editing the surface style away barely moves it (95.5% → 93.9%). The tells that survive are architectural: themes explained by the narrator, single-track causally-tidy plots, emotions rendered only as bodily sensation, no real-world references, no reader, linear time, endings resolved by protagonist growth and acceptance.

sepia turns those measured gaps, together with the eleven related studies digested in [`research/`](research/), into a three-pass writing and revision protocol for fiction:

| Pass | Layer | Examples |
|---|---|---|
| 1 | Narrative architecture (fiction) | stop explaining the theme, loosen the causal chain, back-load revelations, mix emotion modes, sparse character networks, name real things |
| 2 | Discourse flow | de-template the paragraph-question sequence, fix the mid-story sag, vary rhythm and positions |
| 3 | Surface style | the classic layer: clichés, syntax templates, vocabulary, register |

Plus a 30-feature diagnosis rubric and per-model fingerprint corrections (Claude, GPT, Gemini, DeepSeek, Kimi).

Professional prose fails differently. The studies point at filler that carries no information, hedging where a judgment was needed, chatbot leftovers, register that ignores the venue, and formatting that looks stamped out. Each document type gets a thin rule file on top of one shared checklist:

| Domain | The gist |
|---|---|
| Release notes / announcements | user impact first, artifacts per claim, no marketing inflation |
| PR / issue replies | answer first, cite `file:line`, no reflex praise, length ∝ stakes |
| Postmortems | blameless toward people, merciless toward mechanisms; timestamps, dead ends, owned action items |
| Tickets / work orders | title = outcome, testable acceptance criteria, link don't repeat |
| Technical articles | open at the problem, one real dead end, one committed opinion, numbers with conditions |

The governing principle throughout: **calibrate to the human distribution, don't invert the AI one.** Humans sit at moderate values; a story with every rule applied is a new fingerprint. The skill selects 3–5 moves per story and leaves slack.

## Install

Default is **user scope** — install once, and the skill follows you into every project. The CLI routes below are user-scope out of the box; the in-session `/plugin install` dialog instead asks you to pick a scope, so choose **User** there.

**Skills CLI (77+ agents, pick yours when prompted):**

```bash
npx skills add Nanako0129/sepia -g
```

`-g` is what makes it user scope (the default is project). Update later with `npx skills update -g`.

**Claude Code plugin (Grok Build rides along):**

```bash
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user
```

Grok Build auto-discovers Claude Code's plugins, so this install covers Grok users who also run Claude Code.

**Grok Build without Claude Code:** run `./install.sh` (links into Grok's native `~/.grok/skills/`), or add `Nanako0129/sepia` as a marketplace source in Grok's Marketplace tab — Grok consumes Claude Code marketplace repos directly.

**All four platforms at once:**

```bash
git clone https://github.com/Nanako0129/sepia.git ~/.sepia
~/.sepia/install.sh
```

`install.sh` installs at user scope only:

| Platform | Where | Mechanism |
|---|---|---|
| Claude Code | `~/.claude/skills/sepia` | symlink |
| Codex | `~/.agents/skills/sepia` | symlink |
| Grok Build | `~/.grok/skills/sepia` (native path, no Claude Code needed) | symlink |
| Antigravity | `~/.gemini/config/skills/sepia` + `/sepia` global workflow | copy |

Keep the clone — the symlinks point into it. `git pull` updates Claude Code, Grok, and Codex in place; re-run `install.sh` after pulling to refresh the Antigravity copy.

**Project scope (alternative):** when one repo should pin its own copy, commit `skills/sepia/` into that repo as `.agents/skills/sepia` (Codex + Antigravity) or `.claude/skills/sepia` (Claude Code).

## Layout

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

## 中文說明

sepia 是一個去 AI 味的寫作 skill。小說模式不從詞彙下手：StoryScope 證實真正暴露 AI 身分的是敘事架構——主題講得太白、情節單線到底、情緒全靠身體感官、時間永遠線性、結局收得乾乾淨淨。先修這一層，再輪到篇章與字句；內含 30 特徵診斷 rubric 與各模型指紋表。

專業文書（release 公告、PR/issue 回覆、postmortem、工單、技術文章）各有自己的規則檔，核心是同一件事：對齊 venue 的語域、每個宣稱附上真實 artifact、該下判斷的地方下判斷。支援 write／review（只診斷）／refactor（最小修改）／recreate（重寫）四種操作。校準原則：往人類分布的中間帶靠；把 AI 特徵反轉到極端，只會做出新的指紋。

## Sources

Full digests with links in [`research/`](research/). Primary: StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## License

MIT
