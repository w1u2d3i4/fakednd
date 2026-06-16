#!/usr/bin/env python3
"""Generate starter campaign roster files from a plot seed."""

from __future__ import annotations

import argparse
import hashlib
import random
from pathlib import Path


SURNAMES = ["林", "吴", "沈", "顾", "周", "秦", "白", "陆", "韩", "苏", "闻", "唐", "谢", "许", "姜", "叶"]
GIVEN = ["微", "烬", "潮", "砚", "岚", "镜", "槐", "珩", "鸦", "眠", "烛", "澈", "棠", "衡", "盐", "曜"]
ROLES = ["债务代理", "失眠医师", "港口巡官", "梦境贩子", "异端学者", "雇佣剑士", "神殿书记", "盐镜商人", "逃亡贵族", "旧塔看守"]
FACTIONS = ["盐镜商会", "夜档馆", "银潮卫队", "失眠者互助会", "黑蜡教团", "旧王密探", "海灯修会", "无名佣兵团"]
PRIMARY_GOALS = [
    "夺回被偷走的名字",
    "让所属阵营掌控梦境贸易",
    "保护一个不能公开的人",
    "找到通往旧塔的真实入口",
    "偿还或抹除一笔古老债务",
    "阻止某个预言在港城实现",
]
SECONDARY_GOALS = [
    "确认主角是否携带关键线索",
    "获得一份账本、证词或地图",
    "拖延敌对阵营的仪式",
    "营救被卷入事件的普通人",
    "把责任转嫁给可替罪的人",
    "换取一次安全通行",
]
TACTICS = ["谈判", "试探", "夺证", "毁证", "救人", "撤退", "跟踪", "设伏", "交易", "呼援"]
PRESSURES = ["秘密曝光", "欠债到期", "人质受威胁", "阵营命令", "旧伤复发", "名字被唤出", "梦境污染", "亲友失踪"]
LOCATIONS = ["银潮港", "盐镜集市", "黑蜡仓库", "旧塔倒影", "玻璃沼", "王冠路"]


def stable_seed(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def pick_name(rng: random.Random, index: int) -> str:
    return rng.choice(SURNAMES) + rng.choice(GIVEN) + f"·{index:03d}"


def major_npc_markdown(rng: random.Random, index: int) -> str:
    name = pick_name(rng, index)
    role = rng.choice(ROLES)
    faction = rng.choice(FACTIONS)
    location = rng.choice(LOCATIONS)
    primary = rng.choice(PRIMARY_GOALS)
    secondary = rng.choice(SECONDARY_GOALS)
    tactic = rng.choice(TACTICS)
    pressure = rng.choice(PRESSURES)
    hp = rng.randint(8, 32)
    ac = rng.randint(11, 16)
    attack_bonus = rng.randint(2, 6)
    return f"""# NPC{index:03d} {name}

## 简短介绍
{name}是{location}的{role}，表面为{faction}办事。第一次登场时，先给一句可见特征和一句未说出口的压力。

## 档案
```yaml
id: NPC{index:03d}
tier: major
name: {name}
public_role: {role}
faction: {faction}
location: {location}
primary_goal: {primary}
secondary_goal: {secondary}
current_tactical_goal: {tactic}
bottom_line: 不会主动牺牲自己的核心秘密，除非主要目标因此得以推进。
secret: 与剧情底子中的核心秘密相连，DM 在生成完整战役时补细节。
pressure_button: {pressure}
personality_axes:
  loyalty: {rng.randint(-2, 2)}
  fear: {rng.randint(-2, 2)}
  ambition: {rng.randint(-2, 2)}
  mercy: {rng.randint(-2, 2)}
  obsession: {rng.randint(-2, 2)}
relationship:
  trust: 0
  suspicion: 0
  debt: 0
stats:
  ac: {ac}
  hp: {hp}
  speed: 9m
  attack: "+{attack_bonus} vs AC, 1d6+2 damage"
  save_dc: {8 + attack_bonus}
  key_skills: ["洞悉", "游说", "欺瞒"]
resources: []
speech_style: 短句，先试探，再给代价。
combat_style: 优先完成当前战术目标，而不是盲目输出伤害。
subagent_prompt: 依据主要目标、次要目标、当前战术目标、压力按钮和关系值决定是否听从玩家。
plot_drive:
  if_player_helps: 推进其当前战术目标，并降低一次相关时钟压力。
  if_player_blocks: 转为交易、设伏、毁证或寻求阵营支援。
  if_ignored: 离屏推进次要目标；在下次登场时改变一个资源或线索位置。
  clocks_influenced: ["local_alarm", "faction_move"]
growth_triggers:
  - 玩家完成或破坏其次要目标
  - 秘密被发现或温柔保管
  - 其压力按钮被敌方利用
memory_log: []
```
"""


def minor_npc_markdown(rng: random.Random, index: int) -> str:
    name = pick_name(rng, index)
    location = rng.choice(LOCATIONS)
    role = rng.choice(["路人", "店员", "守卫", "证人", "搬运工", "学徒", "病人", "赌徒", "难民", "传令"])
    detail = rng.choice(["看见过一枚盐镜", "听见过旧塔钟声", "害怕黑蜡封印", "欠某个主要 NPC 人情", "知道一条小路", "误认主角"])
    return f"""# MINOR{index:03d} {name}

```yaml
id: MINOR{index:03d}
tier: minor
name: {name}
scene_function: {role}
location: {location}
fixed_goal: 活过今天，并避免卷入主要阵营冲突。
first_line: "我只说一句，别把我的名字写进去。"
useful_detail: {detail}
risk: 被威胁、收买或牵连时会提供不完整信息。
upgrade_trigger: 若玩家救援、招募、反复追问，或该角色改变战局，则升级为主要 NPC。
```
"""


def map_markdown(rng: random.Random, index: int) -> str:
    name = LOCATIONS[(index - 1) % len(LOCATIONS)]
    return f"""# Map {index:02d} {name}

```yaml
id: map_{index:02d}
name: {name}
player_intro: 这里有一个公开危险、一个诱惑入口和一个不愿被看见的人。
public_conflict: {rng.choice(FACTIONS)} 与 {rng.choice(FACTIONS)} 正在争夺现场控制权。
hidden_conflict: 地图深处藏着与剧情底子核心秘密相连的证据。
environment_buttons:
  - 易燃物
  - 高处/吊索
  - 可破坏封印
wilderness_events: "roll 1d12 on the local event table"
clocks:
  local_alarm: 0/6
  faction_move: 0/6
```

## 事件表

1. 敌方巡逻靠近。
2. 环境危险爆发。
3. 阵营代理人提出交易。
4. 次要 NPC 求救。
5. 发现一条线索。
6. 怪物或野兽出现。
7. 临时商人或营地资源。
8. 主要 NPC 的秘密被擦到边缘。
9. 天气、梦境或魔法污染改变地形。
10. 旧债追来。
11. 短休机会，但会推进时钟。
12. 主线稀有事件。
"""


def write_roster(args: argparse.Namespace) -> None:
    seed_text = args.seed
    if args.seed_file:
        seed_text += "\n" + Path(args.seed_file).read_text(encoding="utf-8")
    rng = random.Random(stable_seed(seed_text or "trpg-dm-agent"))
    output = Path(args.output)

    if args.dry_run:
        print(f"Would generate {args.major} major NPCs, {args.minor} minor NPCs, {args.maps} maps at {output}")
        return

    major_dir = output / "npcs" / "major"
    minor_dir = output / "npcs" / "minor"
    maps_dir = output / "maps"
    for directory in (major_dir, minor_dir, maps_dir):
        directory.mkdir(parents=True, exist_ok=True)

    for i in range(1, args.major + 1):
        (major_dir / f"NPC{i:03d}.md").write_text(major_npc_markdown(rng, i), encoding="utf-8")
    for i in range(1, args.minor + 1):
        (minor_dir / f"MINOR{i:03d}.md").write_text(minor_npc_markdown(rng, i), encoding="utf-8")
    for i in range(1, args.maps + 1):
        (maps_dir / f"map_{i:02d}.md").write_text(map_markdown(rng, i), encoding="utf-8")

    (output / "README.md").write_text(
        f"# Generated TRPG Campaign\n\nGenerated from seed with {args.major} major NPCs, {args.minor} minor NPCs, and {args.maps} maps.\n",
        encoding="utf-8",
    )
    print(f"Generated roster at {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate NPC and map roster skeletons.")
    parser.add_argument("--seed", default="", help="Plot seed text")
    parser.add_argument("--seed-file", help="Path to a UTF-8 plot seed file")
    parser.add_argument("--output", default="generated/campaign", help="Output campaign directory")
    parser.add_argument("--major", type=int, default=100, help="Number of major NPCs")
    parser.add_argument("--minor", type=int, default=200, help="Number of minor NPCs")
    parser.add_argument("--maps", type=int, default=6, help="Number of maps")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing files")
    args = parser.parse_args()

    if args.major < 1 or args.minor < 1 or args.maps < 1:
        parser.error("major, minor, and maps must be positive")
    write_roster(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
