#!/usr/bin/env python3
"""Fail when the files that declare a version disagree about which one it is.

Three files carry sepia's version today: the Claude and Codex plugin manifests
and the canonical SKILL.md's frontmatter. They have never disagreed. This is a
guard for later, not a fix for now.

It matters because the failure would be silent. Nothing breaks at install time
when one manifest is a version behind; the wrong number just gets advertised,
and a version number is exactly the claim a reader uses to judge whether a
project is still maintained.

Discovery rather than a fixed list, so the guard grows with the repository.
The packaging surface has already grown once, with the Antigravity manifest in
Nanako0129/sepia#14, and the root plugin.json and both marketplace.json files
carry no version today. If any of them gains one later, it is checked from that
moment without anyone remembering to add it here. Files with no version are
reported, not failed: absent is a legitimate state, and printing them is how a
maintainer sees what the scan actually looked at.

Standard library only, by design. The repository has no lockfiles and this
should not be the reason it gets one.

    python3 scripts/check_versions.py

Exit status is 0 when every declaration agrees, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Directories that never hold a manifest worth checking.
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache"}

# Any file with one of these names is treated as a packaging manifest, wherever
# it sits. That is the point: a manifest added in a new directory is found.
MANIFEST_NAMES = {"plugin.json", "marketplace.json"}

# A skill declares its version in YAML frontmatter, under `metadata`. Parsed by
# hand rather than with PyYAML to keep the dependency count at zero; the shape
# is fixed and simple enough that a line scan is honest here.
FRONTMATTER_VERSION_RE = re.compile(r"^\s+version:\s*[\"']?([^\"'\s]+)[\"']?\s*$", re.M)


class ManifestError(Exception):
    """A file that should have been readable was not."""


def _iter_files(root):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def _rel(path):
    return str(path.relative_to(ROOT))


def read_json_versions(path):
    """Every version a JSON manifest declares, as (label, version) pairs.

    Both shapes are covered: a top-level `version`, and a `version` on each
    entry of a `plugins` array, which is where a marketplace file would put it.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{_rel(path)}: {exc}") from exc

    found = []
    if isinstance(data, dict):
        if isinstance(data.get("version"), str):
            found.append((_rel(path), data["version"]))
        for index, entry in enumerate(data.get("plugins") or []):
            if isinstance(entry, dict) and isinstance(entry.get("version"), str):
                found.append((f"{_rel(path)} → plugins[{index}]", entry["version"]))
    return found


def read_frontmatter_version(path):
    """The version in a SKILL.md's frontmatter, or None if it declares none."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManifestError(f"{_rel(path)}: {exc}") from exc

    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    match = FRONTMATTER_VERSION_RE.search(text[3:end])
    return match.group(1) if match else None


def scan(root):
    """Walk the repository once. Returns (declared, silent).

    declared: [(label, version)] for everything that states a version.
    silent:   [label] for manifests and skills that state none, which is fine
              and is printed so the scan's reach stays visible.
    """
    declared, silent = [], []

    for path in _iter_files(root):
        if path.name in MANIFEST_NAMES:
            versions = read_json_versions(path)
            if versions:
                declared.extend(versions)
            else:
                silent.append(_rel(path))
        elif path.name == "SKILL.md":
            version = read_frontmatter_version(path)
            if version:
                declared.append((_rel(path), version))
            else:
                silent.append(_rel(path))

    return declared, silent


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv in (["-h"], ["--help"]):
        print(__doc__.strip())
        return 0
    if argv:
        print(f"version check: takes no arguments, got {' '.join(argv)}", file=sys.stderr)
        return 2

    try:
        declared, silent = scan(ROOT)
    except ManifestError as exc:
        print(f"version check: unreadable manifest: {exc}", file=sys.stderr)
        return 1

    width = max((len(label) for label in [l for l, _ in declared] + silent), default=0)
    for label, version in declared:
        print(f"  {label.ljust(width)}  {version}")
    for label in silent:
        print(f"  {label.ljust(width)}  (no version declared)")

    if not declared:
        # Not a pass. Discovery finding nothing means the layout moved and this
        # guard stopped guarding, which is the one failure it cannot report as
        # a mismatch.
        print(
            "\nversion check: FAILED, no file declares a version.\n"
            "Either the manifests moved or this script's discovery is out of date.",
            file=sys.stderr,
        )
        return 1

    versions = {version for _, version in declared}
    if len(versions) > 1:
        print(
            f"\nversion check: FAILED, {len(versions)} different versions declared: "
            f"{', '.join(sorted(versions))}.\n"
            "Every file above that states a version must state the same one.",
            file=sys.stderr,
        )
        return 1

    only = versions.pop()
    print(f"\nversion check: OK, {len(declared)} declarations, all {only}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
