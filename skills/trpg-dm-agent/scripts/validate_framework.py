#!/usr/bin/env python3
"""Validate the TRPG DM Agent skill layout."""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_REFERENCES = [
    "play_flow.md",
    "rules_engine.md",
    "bg3_character_creation.md",
    "legendary_feats.md",
    "npc_generation.md",
    "npc_autonomy_and_subagents.md",
    "narration_and_combat.md",
    "state_templates.md",
    "sources.md",
]

REQUIRED_SCRIPTS = [
    "roll.py",
    "generate_npc_roster.py",
    "validate_framework.py",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        fail(errors, "Missing SKILL.md")
    else:
        text = skill_md.read_text(encoding="utf-8")
        if "TODO" in text:
            fail(errors, "SKILL.md still contains TODO")
        if "name: trpg-dm-agent" not in text:
            fail(errors, "SKILL.md frontmatter missing name")
        if "description:" not in text:
            fail(errors, "SKILL.md frontmatter missing description")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        fail(errors, "Missing agents/openai.yaml")
    else:
        text = openai_yaml.read_text(encoding="utf-8")
        if "$trpg-dm-agent" not in text:
            fail(errors, "agents/openai.yaml default_prompt must mention $trpg-dm-agent")

    ref_dir = skill_dir / "references"
    for filename in REQUIRED_REFERENCES:
        path = ref_dir / filename
        if not path.exists():
            fail(errors, f"Missing reference: {filename}")
        elif path.stat().st_size < 100:
            fail(errors, f"Reference looks too small: {filename}")

    script_dir = skill_dir / "scripts"
    for filename in REQUIRED_SCRIPTS:
        path = script_dir / filename
        if not path.exists():
            fail(errors, f"Missing script: {filename}")

    if errors:
        print("TRPG DM Agent validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"TRPG DM Agent validation OK: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
