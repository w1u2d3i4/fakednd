#!/usr/bin/env python3
"""Dice roller for the TRPG DM Agent framework."""

from __future__ import annotations

import argparse
import random
import re
import sys
from dataclasses import dataclass


TERM_RE = re.compile(r"([+-]?)(\d*d\d+(?:k[hl]\d+)?|\d+)", re.IGNORECASE)
DICE_RE = re.compile(r"(?:(\d*)d(\d+))(?:k([hl])(\d+))?$", re.IGNORECASE)


@dataclass
class RollTerm:
    sign: int
    raw: str
    total: int
    text: str


def normalize_expression(expr: str, adv: bool, dis: bool) -> str:
    expr = expr.replace(" ", "")
    if adv and dis:
        adv = dis = False
    if adv:
        return re.sub(r"(?<!\d)1?d20(?!\d)", "2d20kh1", expr, count=1, flags=re.IGNORECASE)
    if dis:
        return re.sub(r"(?<!\d)1?d20(?!\d)", "2d20kl1", expr, count=1, flags=re.IGNORECASE)
    return expr


def parse_terms(expr: str) -> list[tuple[int, str]]:
    expr = expr.replace(" ", "")
    if not expr:
        raise ValueError("empty expression")
    pos = 0
    terms: list[tuple[int, str]] = []
    for match in TERM_RE.finditer(expr):
        if match.start() != pos:
            raise ValueError(f"cannot parse near: {expr[pos:]}")
        sign_text, raw = match.groups()
        sign = -1 if sign_text == "-" else 1
        terms.append((sign, raw))
        pos = match.end()
    if pos != len(expr):
        raise ValueError(f"cannot parse near: {expr[pos:]}")
    return terms


def roll_term(sign: int, raw: str, rng: random.Random) -> RollTerm:
    dice_match = DICE_RE.match(raw)
    if not dice_match:
        value = int(raw)
        total = sign * value
        return RollTerm(sign, raw, total, str(value))

    count_text, sides_text, keep_kind, keep_count_text = dice_match.groups()
    count = int(count_text) if count_text else 1
    sides = int(sides_text)
    if count <= 0 or sides <= 0:
        raise ValueError(f"invalid dice term: {raw}")
    rolls = [rng.randint(1, sides) for _ in range(count)]
    kept = rolls
    keep_suffix = ""
    if keep_kind:
        keep_count = int(keep_count_text)
        if keep_count <= 0 or keep_count > count:
            raise ValueError(f"invalid keep count in term: {raw}")
        kept = sorted(rolls, reverse=(keep_kind.lower() == "h"))[:keep_count]
        keep_suffix = f"->{','.join(str(x) for x in kept)}"
    subtotal = sum(kept)
    total = sign * subtotal
    text = f"{raw}({','.join(str(x) for x in rolls)}{keep_suffix})"
    return RollTerm(sign, raw, total, text)


def roll_expression(expr: str, rng: random.Random) -> tuple[int, str]:
    rolled = [roll_term(sign, raw, rng) for sign, raw in parse_terms(expr)]
    total = sum(term.total for term in rolled)
    parts: list[str] = []
    for index, term in enumerate(rolled):
        prefix = ""
        if index > 0:
            prefix = "+" if term.sign > 0 else "-"
        elif term.sign < 0:
            prefix = "-"
        parts.append(prefix + term.text)
    return total, "".join(parts)


def result_text(total: int, dc: int | None, ac: int | None) -> str:
    target = dc if dc is not None else ac
    if target is None:
        return ""
    return "成功" if total >= target else "失败"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Roll dice with full TRPG display output.")
    parser.add_argument("expression", help="Dice expression, such as 1d20+5, 2d20kh1+4, or 1d10")
    parser.add_argument("--kind", default="检定", help="Display kind: 检定, 攻击, 豁免, 伤害, 事件")
    parser.add_argument("--label", default="", help="Display label")
    parser.add_argument("--dc", type=int, help="Difficulty Class target")
    parser.add_argument("--ac", type=int, help="Armor Class target")
    parser.add_argument("--adv", action="store_true", help="Roll first d20 with advantage")
    parser.add_argument("--dis", action="store_true", help="Roll first d20 with disadvantage")
    parser.add_argument("--seed", help="Deterministic random seed")
    args = parser.parse_args(argv)

    rng = random.Random(args.seed)
    expr = normalize_expression(args.expression, args.adv, args.dis)
    total, detail = roll_expression(expr, rng)

    tags = [args.kind]
    if args.adv and not args.dis:
        tags.append("优势")
    elif args.dis and not args.adv:
        tags.append("劣势")
    tag = "|".join(tags)

    label = f" {args.label}" if args.label else ""
    target_text = ""
    if args.dc is not None:
        target_text = f" vs DC{args.dc}"
    elif args.ac is not None:
        target_text = f" vs AC{args.ac}"

    outcome = result_text(total, args.dc, args.ac)
    outcome_text = f" -> {outcome}" if outcome else ""
    print(f"[{tag}]{label}: {detail}={total}{target_text}{outcome_text}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        print(f"roll.py error: {exc}", file=sys.stderr)
        raise SystemExit(2)
