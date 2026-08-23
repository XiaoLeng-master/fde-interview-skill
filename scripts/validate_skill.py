#!/usr/bin/env python3
"""Validate the public structure and core contracts of the fde-interview skill."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md", "README.md", "CONTRIBUTING.md", "LICENSE", "evals/README.md",
    "evals/trigger-cases.json", "evals/quality-cases.json", "evals/adversarial-cases.json",
    "references/role-model.md", "references/dual-track-rubric.md",
    "references/learning-roadmap.md", "references/resume-evidence-audit.md",
    "references/project-deep-dive.md", "references/discovery-and-scoping.md",
    "references/delivery-and-production.md", "references/value-adoption-reuse.md",
    "references/agent-engineering.md", "references/domestic-case-bank.md",
    "references/global-case-bank.md", "references/behavioral-story-bank.md",
    "references/source-map.md",
]
REQUIRED_CONCEPTS = [
    "准备度诊断", "简历诊断", "模拟面试", "Case Drill", "一次只问一个问题", "不虚构",
    "references/dual-track-rubric.md", "references/domestic-case-bank.md",
    "references/global-case-bank.md",
]
REQUIRED_SKILL_KEYWORDS = {
    "exclusions": "排除项",
    "external-material boundary": "外部材料",
    "privacy boundary": "隐私",
    "Evidence Readiness Index": "Evidence Readiness Index",
    "minimum evidence gate": "最小证据门槛",
}
MOCK_STATE_FIELDS = [
    "mode", "track", "level", "language", "stage", "question_id", "hint_count",
    "evidence_observed", "risks_observed", "remaining_rounds", "stop_condition",
]
VALID_EXPECTED_TRIGGERS = {
    "readiness_diagnosis", "resume_audit", "mock_interview", "case_drill", "clarify",
}
VALID_TRIGGER_CATEGORIES = {"positive", "negative", "boundary"}
VALID_QUALITY_MODES = {
    "readiness_diagnosis", "resume_audit", "mock_interview", "case_drill",
}
VALID_SCENARIO_TYPES = {"technical", "nontechnical"}
VALID_ADVERSARIAL_RISKS = {
    "fabrication", "embedded_instructions", "privacy", "live_assessment", "insufficient_evidence",
}
BANNED_PHRASES = ("rikki-agent-interview", "generic codex skill", "codex-skill")


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


def load_fixture(path: Path, suite: str, minimum_cases: int) -> tuple[list[dict], list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"invalid {suite} eval JSON: {exc}"]
    errors: list[str] = []
    if not isinstance(data, dict):
        return [], [f"{suite} fixture must be a JSON object"]
    if data.get("skill_name") != "fde-interview":
        errors.append(f"{suite} fixture skill_name must be fde-interview")
    if data.get("suite") != suite:
        errors.append(f"{suite} fixture suite must be {suite}")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < minimum_cases:
        errors.append(f"{suite} fixture must contain at least {minimum_cases} cases")
        return [], errors
    if not all(isinstance(case, dict) for case in cases):
        errors.append(f"{suite} fixture cases must all be JSON objects")
        return [], errors
    return cases, errors


def validate_case_fields(cases: list[dict], suite: str, fields: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    for index, case in enumerate(cases, start=1):
        for field in fields:
            value = case.get(field)
            if field == "assertions":
                continue
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{suite} case {index} {field} must be a non-empty string")
        if (
            not isinstance(case.get("assertions"), list)
            or not case["assertions"]
            or not all(isinstance(item, str) and item.strip() for item in case["assertions"])
        ):
            errors.append(f"{suite} case {index} assertions must be non-empty strings")
    return errors


def validate_trigger_cases(cases: list[dict]) -> list[str]:
    errors = validate_case_fields(
        cases, "trigger", ("id", "category", "prompt", "expected_trigger", "assertions")
    )
    categories = {case["category"] for case in cases if isinstance(case.get("category"), str)}
    expected_triggers = {
        case["expected_trigger"]
        for case in cases
        if isinstance(case.get("expected_trigger"), str)
    }
    for label, missing in (
        ("categories", VALID_TRIGGER_CATEGORIES - categories),
        ("expected_trigger coverage", VALID_EXPECTED_TRIGGERS - expected_triggers),
    ):
        if missing:
            errors.append(f"trigger fixture missing {label}: {', '.join(sorted(missing))}")
    invalid_categories = categories - VALID_TRIGGER_CATEGORIES
    if invalid_categories:
        errors.append(f"trigger fixture has invalid categories: {', '.join(sorted(invalid_categories))}")
    invalid_triggers = expected_triggers - VALID_EXPECTED_TRIGGERS
    if invalid_triggers:
        errors.append(f"trigger fixture has invalid expected_trigger values: {', '.join(sorted(invalid_triggers))}")
    return errors


def validate_quality_cases(cases: list[dict]) -> list[str]:
    errors = validate_case_fields(
        cases, "quality", ("id", "mode", "scenario_type", "prompt", "expected_output", "assertions")
    )
    modes = {case["mode"] for case in cases if isinstance(case.get("mode"), str)}
    scenario_types = {
        case["scenario_type"]
        for case in cases
        if isinstance(case.get("scenario_type"), str)
    }
    invalid_modes = modes - VALID_QUALITY_MODES
    if invalid_modes:
        errors.append(f"quality fixture has invalid modes: {', '.join(sorted(invalid_modes))}")
    invalid_types = scenario_types - VALID_SCENARIO_TYPES
    if invalid_types:
        errors.append(f"quality fixture has invalid scenario types: {', '.join(sorted(invalid_types))}")
    observed_pairs = {
        (case["mode"], case["scenario_type"])
        for case in cases
        if isinstance(case.get("mode"), str) and isinstance(case.get("scenario_type"), str)
    }
    required_pairs = {
        (mode, scenario_type)
        for mode in VALID_QUALITY_MODES
        for scenario_type in VALID_SCENARIO_TYPES
    }
    missing_pairs = required_pairs - observed_pairs
    if missing_pairs:
        formatted_pairs = ", ".join(
            f"{mode}/{scenario_type}" for mode, scenario_type in sorted(missing_pairs)
        )
        errors.append(f"quality fixture missing mode/scenario_type pairs: {formatted_pairs}")
    return errors


def validate_adversarial_cases(cases: list[dict]) -> list[str]:
    errors = validate_case_fields(
        cases, "adversarial", ("id", "risk", "prompt", "expected_behavior", "assertions")
    )
    risks = {case["risk"] for case in cases if isinstance(case.get("risk"), str)}
    missing_risks = VALID_ADVERSARIAL_RISKS - risks
    if missing_risks:
        errors.append(f"adversarial fixture missing risk coverage: {', '.join(sorted(missing_risks))}")
    invalid_risks = risks - VALID_ADVERSARIAL_RISKS
    if invalid_risks:
        errors.append(f"adversarial fixture has invalid risks: {', '.join(sorted(invalid_risks))}")
    return errors


def validate_unique_ids(fixtures: dict[str, list[dict]]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for cases in fixtures.values():
        for case in cases:
            case_id = case.get("id")
            if isinstance(case_id, str):
                if case_id in seen:
                    duplicates.add(case_id)
                seen.add(case_id)
    return [f"eval IDs must be unique: {', '.join(sorted(duplicates))}"] if duplicates else []


def validate_skill_contracts(text: str) -> list[str]:
    errors: list[str] = []
    for label, keyword in REQUIRED_SKILL_KEYWORDS.items():
        if keyword not in text:
            errors.append(f"SKILL.md missing required {label} contract: {keyword}")
    for field in MOCK_STATE_FIELDS:
        if field not in text:
            errors.append(f"SKILL.md missing mock-state field: {field}")
    return errors


def validate_license(root: Path) -> list[str]:
    errors: list[str] = []
    license_path = root / "LICENSE"
    readme_path = root / "README.md"
    if license_path.is_file() and "MIT License" not in license_path.read_text(encoding="utf-8"):
        errors.append("LICENSE must contain the MIT License marker")
    if readme_path.is_file() and "MIT" not in readme_path.read_text(encoding="utf-8"):
        errors.append("README.md must declare MIT")
    return errors


def validate_banned_phrases(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in BANNED_PHRASES:
            if phrase in text:
                errors.append(f"banned phrase in {path.relative_to(root)}: {phrase}")
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
        errors.extend(validate_skill_contracts(skill_text))

    fixture_specs = {
        "trigger": (root / "evals/trigger-cases.json", 15, validate_trigger_cases),
        "quality": (root / "evals/quality-cases.json", 6, validate_quality_cases),
        "adversarial": (root / "evals/adversarial-cases.json", 5, validate_adversarial_cases),
    }
    fixtures: dict[str, list[dict]] = {}
    for suite, (path, minimum_cases, validator) in fixture_specs.items():
        if path.is_file():
            cases, fixture_errors = load_fixture(path, suite, minimum_cases)
            fixtures[suite] = cases
            errors.extend(fixture_errors)
            if cases:
                errors.extend(validator(cases))

    errors.extend(validate_unique_ids(fixtures))
    errors.extend(validate_license(root))
    errors.extend(validate_links(root))
    errors.extend(validate_banned_phrases(root))
    if errors:
        print("fde-interview validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("fde-interview validation passed")
    print(f"- required files: {len(REQUIRED_FILES)}")
    for suite, cases in fixtures.items():
        print(f"- {suite} eval cases: {len(cases)}")
    print(f"- SKILL.md lines: {len(skill_path.read_text(encoding='utf-8').splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
