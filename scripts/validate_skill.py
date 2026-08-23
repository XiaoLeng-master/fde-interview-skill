#!/usr/bin/env python3
"""Validate the public structure and core contracts of the fde-interview skill."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "evals/evals.json",
    "references/role-model.md",
    "references/dual-track-rubric.md",
    "references/learning-roadmap.md",
    "references/resume-evidence-audit.md",
    "references/project-deep-dive.md",
    "references/discovery-and-scoping.md",
    "references/delivery-and-production.md",
    "references/value-adoption-reuse.md",
    "references/agent-engineering.md",
    "references/domestic-case-bank.md",
    "references/global-case-bank.md",
    "references/behavioral-story-bank.md",
    "references/source-map.md",
]

REQUIRED_CONCEPTS = [
    "准备度诊断",
    "简历诊断",
    "模拟面试",
    "Case Drill",
    "一次只问一个问题",
    "不虚构",
    "references/dual-track-rubric.md",
    "references/domestic-case-bank.md",
    "references/global-case-bank.md",
]


def validate_frontmatter(text: str) -> list[str]:
    errors: list[str] = []
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md is missing YAML frontmatter"]
    frontmatter = match.group(1)
    if not re.search(r"^name:\s*fde-interview\s*$", frontmatter, re.MULTILINE):
        errors.append("frontmatter name must be fde-interview")
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 40:
        errors.append("frontmatter description is missing or too short")
    return errors


def validate_links(root: Path) -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown in root.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean_target = target.split("#", 1)[0]
            if clean_target and not (markdown.parent / clean_target).resolve().exists():
                errors.append(f"broken relative link in {markdown.relative_to(root)}: {target}")
    return errors


def validate_evals(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid eval JSON: {exc}"]
    if data.get("skill_name") != "fde-interview":
        errors.append("eval skill_name must be fde-interview")
    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 5:
        errors.append("evals must contain at least five cases")
        return errors
    for index, case in enumerate(evals, start=1):
        for field in ("id", "prompt", "expected_output", "files", "assertions"):
            if field not in case:
                errors.append(f"eval {index} is missing {field}")
        if not case.get("assertions"):
            errors.append(f"eval {index} has no assertions")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        errors.extend(validate_frontmatter(skill_text))
        line_count = len(skill_text.splitlines())
        if line_count >= 500:
            errors.append(f"SKILL.md has {line_count} lines; expected fewer than 500")
        for concept in REQUIRED_CONCEPTS:
            if concept not in skill_text:
                errors.append(f"SKILL.md missing required concept: {concept}")

    eval_path = root / "evals/evals.json"
    if eval_path.is_file():
        errors.extend(validate_evals(eval_path))

    errors.extend(validate_links(root))

    if errors:
        print("fde-interview validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("fde-interview validation passed")
    print(f"- required files: {len(REQUIRED_FILES)}")
    print(f"- eval cases: {len(json.loads(eval_path.read_text(encoding='utf-8'))['evals'])}")
    print(f"- SKILL.md lines: {len(skill_path.read_text(encoding='utf-8').splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
