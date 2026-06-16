# 状态模板

## PC 人物表

```yaml
id: pc
name:
difficulty: standard
species:
class:
subclass:
background:
level: 1
xp: 0
abilities:
  str:
  dex:
  con:
  int:
  wis:
  cha:
proficiency_bonus: 2
saves:
skills:
ac:
hp:
max_hp:
speed:
initiative:
passive_perception:
resources:
  spell_slots:
  class_features:
  inspiration:
  legendary_feat:
spells:
equipment:
conditions:
personality:
  goal:
  flaw:
  bond:
  secret:
growth_log:
```

## 法术表条目

```yaml
- name:
  level:
  school:
  casting_time:
  range:
  target:
  attack_or_save:
  dc:
  damage_or_healing:
  duration:
  concentration:
  resource:
  description:
  upcast:
```

## NPC 演变状态

```yaml
npc_id:
  trust: 0
  suspicion: 0
  debt: 0
  stage: 初识
  personality_axes:
    loyalty: 0
    fear: 0
    ambition: 0
    mercy: 0
    obsession: 0
  growth_flags: []
  scars: []
  memory_log:
    - session:
      event:
      player_choice:
      npc_feeling:
      mechanical_change:
  current_tactical_goal:
  faction_shift:
```

## 战役状态

```yaml
campaign:
  title:
  tone:
  current_session:
  current_map:
  current_scene:
  date:
  clocks:
    faction_clock_name:
      value: 0
      max: 6
      trigger:
  discovered_secrets: []
  active_quests: []
  failed_quests: []
  unresolved_threads: []
party:
  members:
  camp:
  supplies:
```

## Session 日志

每次游玩后追加：

```markdown
## Session N

地点：
在场角色：
玩家目标：
关键骰子：
重要选择：
战斗/探索结果：
NPC 关系变化：
获得线索：
消耗资源：
敌方时钟：
下次开场：
```
