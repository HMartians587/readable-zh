# Readable ZH

**保住意思，把话说顺。**

Readable ZH 是一个中文写作 Agent Skill，适用于日常沟通、技术说明和科研交流。它帮助整理绕句、指代不清、重复和模板化表达，同时保留事实、条件、作者立场与证据强度。

当前版本：**0.7.0**。

## 能做什么

- **润色**：把话说得自然、好懂，保留独立信息与原有分寸。
- **审阅**：指出具体问题及修改方向，按请求决定是否改稿。
- **重写**：围绕读者需要重排正文，保留主张、数值、引用和必要限定。
- **根据材料写作**：依据提供的材料组织解释，按用途保持正式文体或作者声音。

编辑时会核对数值、时间、条件、否定、因果、归因和完成状态。例如，“计划测试”应保留为计划，“有人报告”应保留报告者的归属。

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 安装，需要 Node.js 22.20 或以上版本。在项目目录运行：

```sh
npx skills add HMartians587/readable-zh --skill readable-zh
```

按提示选择 Codex 或 Claude Code。默认安装到当前项目，添加 `-g` 可安装为全局技能。

也可手动复制整个 [`skills/readable-zh`](skills/readable-zh) 目录，包含入口、参考文件、界面元数据和许可：

| 宿主 | 安装位置 |
| --- | --- |
| Codex | 用户级 `~/.agents/skills/readable-zh`，或项目内 `.agents/skills/readable-zh` |
| Claude Code | 用户级 `~/.claude/skills/readable-zh` |

Codex 手动安装细节见 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)。Readable ZH 是纯文本技能，由宿主执行写作指导，无需为技能单独搭建服务器。

安装后，Codex 使用 `$readable-zh`，Claude Code 使用 `/readable-zh`。以下示例采用 Codex 写法；在 Claude Code 中，把 `$readable-zh` 换为 `/readable-zh`。也可直接阅读 [`SKILL.md`](skills/readable-zh/SKILL.md)。

### Claude Code 插件安装

也可在 Claude Code 会话中按插件安装：

```text
/plugin marketplace add HMartians587/readable-zh
/plugin install readable-zh@readable-zh
```

以插件方式安装时，使用 `/readable-zh:readable-zh` 调用。插件与上面的独立技能包含相同写作指导。

## 三个可直接复制的用法

### 日常沟通：说清安排与进度

```text
使用 $readable-zh 润色下面的团队消息，语气自然。
保留时间、条件和计划状态，只交付成稿。

原文：这次更新充分彰显了我们对协作效率的重视。工具新增按日期筛选。
批量导出计划下月测试，目前还没有性能数据。
```

### 技术说明：保留条件与操作

```text
使用 $readable-zh 编辑下面的技术说明，面向第一次使用工具的人。
保留阈值、单位和操作顺序，不补充未知参数，只交付成稿。

原文：对于大小超过 10 MB 的文件，需要先压缩，再上传。
未超过 10 MB 的文件可以直接上传。上传完成后，请确认页面是否显示文件名。
```

### 科研交流：保留记录中的证据强度

```text
使用 $readable-zh 把下面的模拟记录整理成一段组会汇报。
先说当前观察，再交代条件和下一步。保留全部数值、设置及不确定性，
不要补充原因，也不要把下一步写成已完成。

模拟记录（仅作用法示例，并非真实实验结果）：
同一数据划分，单个随机种子。基线准确率 81%，方案 A 为 82%。
两组都训练 10 轮。尚未做独立重复，不能据此判断差异是否稳定。
下一步计划增加随机种子，再检查差异。
```

更多用法见 [使用指南](docs/usage.md)。

## 贡献与许可

欢迎提交具体案例、文档修正和规则改进，见 [贡献指南](CONTRIBUTING.md)。

本项目采用 [MIT 许可](LICENSE)。参考项目与固定来源见 [来源说明](docs/source-map.md)，第三方许可见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。
