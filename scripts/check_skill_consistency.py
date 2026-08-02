#!/usr/bin/env python3
"""Run deterministic integrity checks for the packaged Skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "analyze-romantic-relationships"
SKILL_MD = SKILL / "SKILL.md"


def main() -> int:
    errors: list[str] = []
    if not SKILL_MD.is_file():
        print(f"ERROR: missing {SKILL_MD.relative_to(ROOT)}")
        return 1

    text = SKILL_MD.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3:
        errors.append("SKILL.md must contain YAML frontmatter")
        frontmatter = ""
    else:
        frontmatter = parts[1]

    keys = []
    for line in frontmatter.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.append(match.group(1))
    if keys != ["name", "description"]:
        errors.append(f"SKILL.md frontmatter keys must be name, description; found {keys}")
    if "name: analyze-romantic-relationships" not in frontmatter:
        errors.append("SKILL.md name does not match the installation directory")

    for path in SKILL.rglob("*.md"):
        body = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
            if target.startswith(("http://", "https://", "#")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken link in {path.relative_to(ROOT)}: {target}")

    required_snippets = {
        "不得将有限材料当作读心": "mind-reading boundary",
        "报告命题": "report/event distinction",
        "强迫控制": "coercive-control safety routing",
        "行动检验投入与履约": "action/language evidence distinction",
        "同意分析": "separate analysis/publication consent",
    }
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in SKILL.rglob("*.md"))
    for snippet, label in required_snippets.items():
        if snippet not in corpus:
            errors.append(f"missing required {label}: {snippet}")

    validator = ROOT / "relationship_case_validator.py"
    skill_validator = SKILL / "scripts" / "validate_case.py"
    if not skill_validator.is_file():
        errors.append("Skill validator script is missing")
    elif validator.read_bytes() != skill_validator.read_bytes():
        errors.append("root validator and Skill validator have drifted")

    forbidden = {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"}
    for name in forbidden:
        if (SKILL / name).exists():
            errors.append(f"extraneous file inside Skill: {name}")

    agent_yaml = SKILL / "agents" / "openai.yaml"
    if not agent_yaml.is_file():
        errors.append("agents/openai.yaml is missing")
    else:
        agent_text = agent_yaml.read_text(encoding="utf-8")
        if "$analyze-romantic-relationships" not in agent_text:
            errors.append("default prompt does not explicitly invoke the Skill")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Skill consistency checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
