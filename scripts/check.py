#!/usr/bin/env python3
"""Validate the portable requirements-engineering package using stdlib only."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/requirements-engineering"
REQUIRED = (
    "README.md",
    "SITEMAP.md",
    "LICENSE",
    "skills/requirements-engineering/SKILL.md",
    "skills/requirements-engineering/LICENSE",
    "skills/requirements-engineering/agents/openai.yaml",
    "skills/requirements-engineering/references/sources.md",
    "skills/requirements-engineering/evals/evals.json",
    "scripts/check.py",
    ".github/workflows/check.yml",
)
errors = []

for name in REQUIRED:
    if not (ROOT / name).is_file():
        errors.append(f"Missing required file: {name}")

entry = SKILL / "SKILL.md"
if entry.is_file():
    content = entry.read_text(encoding="utf-8")
    header = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if (
        not header
        or not re.search(r"^name: requirements-engineering$", header[1], re.M)
        or not re.search(r"^description: .+", header[1], re.M)
    ):
        errors.append("SKILL.md needs the expected name and a nonempty description in frontmatter")

# Deliberately narrow heuristics; this is not a secret scanner.
private = re.compile(
    r"/home/[^\s/]+|/Users/[^\s/]+|(?:~|\$HOME)/|"
    r"(?:[a-z0-9-]+\.)*honya\.dev|"
    r"\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b",
    re.I,
)
markdown_link = re.compile(r"!?(?:\[[^\]]*\])\(([^\s)]+)(?:\s+[^)]*)?\)")

for path in sorted(ROOT.rglob("*.md")):
    if ".git" in path.parts:
        continue
    content = path.read_text(encoding="utf-8")
    label = path.relative_to(ROOT).as_posix()
    if private.search(content):
        errors.append(f"Possible private environment reference: {label}")
    for match in markdown_link.finditer(content):
        target = match[1].strip("<>")
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        resolved = (path.parent / unquote(parts.path)).resolve()
        boundary = SKILL.resolve() if path.resolve().is_relative_to(SKILL.resolve()) else ROOT.resolve()
        if not resolved.is_relative_to(boundary):
            errors.append(f"Link escapes package: {label}: {target}")
        elif not resolved.exists():
            errors.append(f"Broken relative link: {label}: {target}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

print("Package check passed: required files, frontmatter, relative links, and environment-reference heuristics.")
