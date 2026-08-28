#!/usr/bin/env bash
# Installs the sepia skill at USER scope for Claude Code, Codex, Grok Build,
# and Antigravity. Claude Code / Codex / Grok follow symlinks; Antigravity
# gets a copy. For project-scope installs, see README.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILL="$ROOT/skills/sepia"

link() {
  mkdir -p "$(dirname "$2")"
  ln -sfn "$1" "$2"
  echo "linked  $2"
}

link "$SKILL" "$HOME/.claude/skills/sepia"   # Claude Code (Grok Build auto-discovers this too)
link "$SKILL" "$HOME/.agents/skills/sepia"   # Codex (user scope)

# Antigravity global skills dir (copy: keep in sync by re-running install.sh)
AG="$HOME/.gemini/config/skills/sepia"
mkdir -p "$(dirname "$AG")"
rm -rf "$AG"
cp -R "$SKILL" "$AG"
echo "copied  $AG"

# Antigravity global workflow: adds the /sepia slash command (skills alone have no slash there)
WF="$HOME/.gemini/antigravity/global_workflows/sepia.md"
mkdir -p "$(dirname "$WF")"
cp "$ROOT/.agents/workflows/sepia.md" "$WF"
echo "copied  $WF"

echo ""
echo "Installed at user scope:"
echo "  Claude Code + Grok Build : ~/.claude/skills/sepia (symlink)"
echo "  Codex                    : ~/.agents/skills/sepia (symlink)"
echo "  Antigravity              : ~/.gemini/config/skills/sepia (copy) + /sepia workflow"
echo ""
echo "Keep this clone: the symlinks point into it. 'git pull' updates the"
echo "symlinked installs; re-run install.sh after pulling to refresh the"
echo "Antigravity copy."
