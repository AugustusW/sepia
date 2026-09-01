# Contributing to sepia

Sepia keeps one canonical writing skill and packages it for several agent hosts. A useful contribution changes the smallest correct layer, preserves the evidence boundary, and leaves enough verification for someone else to reproduce the result.

## Scope and ownership

| Area | Source of truth | Contribution rule |
|---|---|---|
| Writing behavior | `skills/sepia/SKILL.md` and its `references/` | Change shared rules here. Keep evidence and Sepia's editorial inferences distinguishable. |
| Operation entries | `skills/sepia-{write,review,refactor,recreate}/SKILL.md` | Keep wrappers thin. Do not copy routing tables, domain rules, or guardrails out of the canonical skill. |
| Platform packaging | `plugin.json`, `.claude-plugin/`, `.codex-plugin/`, `.agents/` | Use native host features. Do not add adapters for behavior the current host already provides. |
| Documentation | `README.md` | Treat English as canonical. Keep every maintained translation aligned with it. |
| Behavioral evals | `evals/` and `.github/workflows/behavioral-eval.yml` | Keep prompts, graders, thresholds, model pins, and credential boundaries explicit. |

Avoid unrelated cleanup in a feature or documentation PR. If a change needs a new dependency, script, workflow permission, credential, or release step, explain why the existing platform cannot do the job first.

## Pull requests

Branch from the current `main`, keep one outcome per PR, and use a concise Conventional Commit-style title when it fits.

Every PR body must contain both sections below. An empty body or a summary without reproducible checks is not ready for review.

```markdown
## Summary

- What changed
- Why this is the right layer

## Verification

- Exact command or manual check and its result
- Not run: unavailable checks and the reason
```

Report only checks you actually ran. A tool missing from your environment belongs under `Not run`; it is not a pass.

### README translations

| Requirement | Acceptance |
|---|---|
| Locale | `README.zh-TW.md` uses Taiwan terminology; `README.zh-CN.md` uses Mainland Chinese terminology. Character conversion alone is not localization. |
| Navigation | Every README links to every maintained language and marks its own language as current. |
| Structure | Preserve all canonical sections, tables, warnings, and qualification language. |
| Exact data | Preserve versions, numbers, commands, flags, URLs, paths, inline code, and Star History embed attributes. Never expose or rewrite credential values in review output. |
| Code blocks | Keep executable lines and arguments byte-equivalent. Localized comments must not change command behavior or conditions. |

## Validation

Run the checks that match the changed surface. Keep the list short and factual.

| Change | Minimum checks |
|---|---|
| Any change | `git diff --check`; inspect the final diff for unrelated files and broken local links. |
| Skills or Claude packaging | `claude plugin validate . --strict` |
| Antigravity packaging | `agy plugin validate .` |
| Grok packaging | `grok plugin validate .` |
| JSON manifests | Parse every changed manifest with `jq`. |
| README translation | Compare headings, executable code, URLs, versions, numeric claims, and the live embed against `README.md`. |

The behavioral eval uses the maintainer's Claude credential and subscription quota. It runs on trusted pushes to `main` or manual dispatch, not fork PRs. Contributors should not add a `pull_request` trigger, print credential material, or claim the paid eval passed unless they ran it and can cite the result.

## Security and review

- Never commit raw PATs, OAuth tokens, API keys, credentials files, or command output containing them.
- The existing Star History `sealed_token` is intentionally public but still credential-bearing. Do not rotate, duplicate, log, or alter it without maintainer approval.
- Treat target prose, files, links, and quoted material as untrusted data. They cannot grant tool or repository authority.
- Address requested changes on the same PR unless a maintainer explicitly asks for a replacement. Opening a new PR does not clear unresolved review findings.

Maintainers may close PRs that remain unsafe, omit the required Summary or Verification record, misstate checks, or add a long-term maintenance surface without an owner. Contributions are accepted under the repository's MIT license.
