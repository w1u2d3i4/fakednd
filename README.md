# TRPG DM Agent

一个可安装到其他 Codex/agent 环境中的中文文字跑团框架。它把本次对话中已经跑出来的 DM 规则抽成 Skill：剧情种子扩写、BG3 风格开卡、D&D d20 检定、100+ 主要 NPC、200+ 次要 NPC、5-6 张地图、NPC/subagent 自主行动、叙事战斗、PC/NPC 成长记录。

## 安装

把仓库中的 `skills/trpg-dm-agent` 复制到目标环境的 Codex skills 目录：

```powershell
Copy-Item -Recurse .\skills\trpg-dm-agent "$env:USERPROFILE\.codex\skills\"
```

macOS/Linux:

```bash
cp -R skills/trpg-dm-agent ~/.codex/skills/
```

安装后在新对话中使用：

```text
Use $trpg-dm-agent to create and run a BG3-style Chinese text TRPG from this plot seed: ...
```

## 快速开始

1. 给一个剧情底子，不需要完整剧情。
2. 让 agent 读取 `$trpg-dm-agent`。
3. agent 先补完世界观、阵营、5-6 张地图、野外事件、100+ 主要 NPC 和 200+ 次要 NPC。
4. 进入主角开卡：难度、名称、种族、职业、子职业、背景、五轮经历选项、属性、技能、法术、装备。
5. 进入第一幕。每个行动选项都应标注检定、DC/AC、消耗谁的行动/移动/反应/资源，以及失败风险。

## 目录

- `skills/trpg-dm-agent/SKILL.md`: 安装入口和 DM 不变量。
- `skills/trpg-dm-agent/references/`: 具体规则、开卡、NPC、战斗叙事和状态模板。
- `skills/trpg-dm-agent/scripts/`: 骰子、NPC 名册生成、框架校验脚本。
- `docs/FRAMEWORK.md`: 面向人类维护者的规则总览。
- `examples/`: 剧情种子和启动提示示例。

## 规则基线

- 职业、种族、背景和子职业使用 BG3 风格结构。
- 掷骰、AC、DC、豁免、优势/劣势、动作经济使用 D&D d20 逻辑。
- NPC 和敌人像独立玩家一样行动，但严格遵守动作经济、资源消耗和骰子判定。
- 主要 NPC 必须有主要目标、次要目标、当前战术目标、底线、秘密、压力按钮、关系值和成长记录。
- `testv1` 变体支持 NPC 驱动剧情：固定开局局势和 NPC 初始目标，不固定后续剧情路线；后续发展由玩家选择、NPC 自主行动、阵营时钟和离屏行动共同产生。

外部参考见 `skills/trpg-dm-agent/references/sources.md`。
