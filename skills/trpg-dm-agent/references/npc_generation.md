# NPC 与地图生成

## 数量要求

从剧情底子生成完整战役时，默认生成：

- 100+ 主要 NPC。
- 200+ 次要 NPC。
- 5-6 张地图。
- 每张地图至少 8-20 个可登场 NPC、3 个环境机关、1 个野外事件表、1 个怪物/敌对势力表、2 个阵营时钟。

最初生成的 100 个 NPC 默认都是主要 NPC。后续临时生成的店员、路人、守卫、孩子、证人等默认是次要 NPC，除非反复登场或能改变局势。

## 主要 NPC 字段

每个主要 NPC 至少记录：

```yaml
id:
tier: major
name:
short_intro:
public_role:
faction:
location:
first_scene:
primary_goal:
secondary_goal:
current_tactical_goal:
bottom_line:
secret:
pressure_button:
personality_axes:
  loyalty:
  fear:
  ambition:
  mercy:
  obsession:
relationship:
  trust:
  suspicion:
  debt:
stats:
  ac:
  hp:
  speed:
  attack:
  save_dc:
  key_skills:
resources:
speech_style:
combat_style:
subagent_prompt:
growth_triggers:
memory_log:
```

`primary_goal` 是人生目标或阵营使命，不能因为一时恐惧就消失。`secondary_goal` 是当前章节目标，可被交易、说服、失败或环境改变。`current_tactical_goal` 是本场景/本回合目标。

## 次要 NPC 字段

```yaml
id:
tier: minor
name:
scene_function:
location:
fixed_goal:
first_line:
useful_detail:
risk:
upgrade_trigger:
```

次要 NPC 主要服务场景、线索、气氛和选择后果。若玩家持续关注、建立关系、救援、伤害、招募，或该 NPC 有独立欲望并改变局势，升级为主要 NPC。

## 地图字段

每张地图记录：

```yaml
id:
name:
player_intro:
public_conflict:
hidden_conflict:
factions:
major_npcs:
minor_npcs:
landmarks:
environment_buttons:
wilderness_events:
monsters:
clocks:
secrets:
entry_points:
exit_points:
```

地图不是静态背景。每张地图至少同时推进两个阵营目标，让玩家在速度、安全、线索、资源和关系之间取舍。

## 生成配比

主要 NPC 建议：

- 20% 队友候选、盟友、导师、救援对象。
- 20% 反派、敌方代理、猎手、债主。
- 20% 阵营代表、官员、商人、神职、佣兵。
- 20% 中立资源、怪人、证人、研究者、旅行者。
- 20% 秘密持有者、双面间谍、未来章节关键人。

次要 NPC 建议：

- 每张地图 30-40 个。
- 包括路人、巡逻、店员、难民、码头工、学徒、孩子、病人、囚犯、赌徒、传令、动物处理者、尸体身份、野外目击者。

## 野外事件

每张地图至少准备 `1d12` 事件：

- 1-2：怪物/野兽/巡逻遭遇。
- 3-4：环境危险。
- 5-6：阵营行动。
- 7-8：NPC 私事或求助。
- 9-10：线索、遗迹、梦境、尸体或旧战场。
- 11：商机、营地、旅行者或短休机会。
- 12：稀有事件，推进主线或暴露主要秘密。
