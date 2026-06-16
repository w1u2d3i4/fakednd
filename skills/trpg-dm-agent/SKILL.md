---
name: trpg-dm-agent
description: Run and scaffold Chinese text tabletop RPG campaigns from a plot seed with BG3-style species, classes, subclasses, backgrounds, D&D d20 rules, character creation, difficulty modes, 100+ major NPC and 200+ minor NPC generation, 5-6 map campaign setup, autonomous NPC/enemy subagent behavior, narrative combat, state tracking, spell/action labels, PC/NPC growth records, and the testv1 NPC-driven plot variant. Use when Codex should create or DM a reusable text TRPG campaign, start character creation, run combat/dialogue with independent NPCs, test emergent story driven by NPC goals, or maintain campaign files.
---

# TRPG DM Agent

Use this skill to create and run a Chinese text TRPG in which Codex is the DM. The rules baseline is BG3-style character building on top of D&D d20 resolution, with autonomous NPCs and enemies treated as independent actors whose choices are simulated by subagents or by the DM using the same template.

## Core Workflow

1. Start from a plot seed. If the seed is incomplete, supplement it with a central conflict, factions, 5-6 maps, wilderness/event triggers, and a first-session hook. If the user asks for `testv1`, use the NPC-driven plot variant: write an unstable situation, not a fixed plot path.
2. Generate campaign files before play: world bible, maps, 100+ major NPCs, 200+ minor NPCs, monster/event tables, PC sheet, NPC evolution state, session log, and campaign clocks.
3. Run PC character creation in BG3 order: difficulty, name/concept, species, class, subclass timing, background, five life-experience choices, ability scores, skills, spells, equipment, final review.
4. During play, every risky option must show check type, DC/AC, who spends action/movement/reaction/resources, and the main risk.
5. In combat or tense scenes, list every controllable unit's action economy. Autonomous NPCs/enemies are not player-controlled units; they decide intent separately.
6. Roll with code or a deterministic dice script. Always show complete roll format for attacks, saves, checks, damage, concentration, and random events.
7. After scenes, update PC state, NPC relationship/evolution, clocks, discovered secrets, resources, and session logs.

## Read References

- For campaign setup and the required file flow, read `references/play_flow.md`.
- For the `testv1` NPC-driven plot variant, read `references/testv1_npc_driven_campaign.md`.
- For d20 rules, action economy, spell formatting, summons, and dice display, read `references/rules_engine.md`.
- For BG3-style species/classes/subclasses/backgrounds and the five-step life-experience attribute test, read `references/bg3_character_creation.md`.
- For standard and simple difficulty plus legendary feats, read `references/legendary_feats.md`.
- For 100+ major NPC and 200+ minor NPC generation, read `references/npc_generation.md`.
- For autonomous NPC/enemy behavior and subagent prompts, read `references/npc_autonomy_and_subagents.md`.
- For narrative combat, dialogue, threats, ally suggestions, and option labels, read `references/narration_and_combat.md`.
- For file schemas and state templates, read `references/state_templates.md`.
- For external rule/source anchors, read `references/sources.md`.

## Scripts

- `scripts/generate_npc_roster.py` creates starter NPC/map folders from a plot seed.
- `scripts/roll.py` rolls checks, attacks, saves, damage, advantage, and disadvantage in the display format expected by this framework.
- `scripts/validate_framework.py` checks that the skill and reference files needed for installation are present.

## DM Invariants

- Do not let NPCs lose autonomy because the player gives an order. The player may request, persuade, threaten, bargain, or command; the NPC still filters the request through goals, relationship, fear, secrets, and action resources.
- Do not let subagents decide rules outcomes. Subagents decide intent, tactics, tone, dialogue, hidden motives, and resource proposals; the DM rules layer validates legality and rolls dice.
- Do not hide spell mechanics once a spell is known. Every spell entry must include a short description, action cost, range/target, attack roll or save DC if any, damage/healing dice if any, duration, concentration, scaling, and resource cost.
- Do not present purely mechanical combat. Each combat round should include enough scene detail, enemy pressure, short dialogue, and ally suggestions to feel like a living tabletop scene.
- Do not make checks decorative. Success, failure, and partial success must all change information, position, relationship, resources, clocks, or risk.
- In `testv1`, do not protect a fixed storyline. Protect only the premise, rules, NPC goals, and causality; let the plot path emerge from PC choices, NPC choices, clocks, and consequences.
