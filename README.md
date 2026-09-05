<!-- markdownlint-disable MD028 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

![astrbot_plugin_helloworld](https://socialify.git.ci/DBJD-CR/astrbot_plugin_helloworld/image?custom_description=AstrBot+Plugin+%E6%8F%92%E4%BB%B6%E6%A8%A1%E6%9D%BF&description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Brick+Wall&pulls=1&stargazers=1&theme=Auto)

<p align="center">
  <img src="assets/PluginRank.svg" alt="Plugin Rank">
  <img src="assets/StarRank.svg" alt="Star Rank">
  <img src="assets/ShitMountain.svg" alt="ShitMountain">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-AGPL_3.0-blue.svg" alt="License: AGPL-3.0">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/AstrBot-v4.24.2+-orange.svg" alt="AstrBot v4.24.2+">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AstrBot-v4.27.4%20Compatible-brightgreen.svg" alt="Compatible with AstrBot v4.27.4">
  <img src="https://img.shields.io/github/v/release/DBJD-CR/astrbot_plugin_helloworld?label=Release&color=brightgreen" alt="Latest Release">
  <img src="https://img.shields.io/badge/QQ群-1033089808-12B7F3.svg" alt="QQ群">
</p>

[![Moe Counter](https://count.getloli.com/get/@DBJD-CR6?theme=moebooru)](https://github.com/DBJD-CR/astrbot_plugin_helloworld)

---

一个为 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 设计的自定义插件模板，基于官方基础模板扩展而来。当前版本主要补充了更完整的仓库工程化配置、社区协作文件、自动化工作流，以及更完善的插件元数据示例，适合作为个人或团队维护 AstrBot 插件仓库时的起始模板。

使用这个模板，让你的 AI 能产出更多应用了 AstrBot 新特性的插件代码！

## 📑 快速导航

- [✨ 功能特性](#-功能特性)
- [📊 输出示例](#-输出示例)
- [🚀 安装与使用](#-安装与使用)
- [📋 指令说明](#-指令说明)
- [⚙️ 配置项详解](#️-配置项详解)
- [📂 插件目录与结构](#-插件目录与结构)
- [🏗️ 架构说明](#️-架构说明)
- [❓ 常见问题](#-常见问题)
- [🚧 已知限制](#-已知限制)
- [📄 许可证](#-许可证)

---
<!-- 开发者的话 -->
> **开发者的话：**
>
> 大家好，我是 DBJD-CR，这是我为 AstrBot 改的一个插件模板，如果存在做的不好的地方还请理解。
>
> 和我写的其他插件一样，本插件模板也是"Vibe Coding"的产物。
>
> 所以，**本插件的所有文件内容，全部由 AI 编写完成**，我几乎没有为该插件编写任何一行代码，仅进行了架构设计与修改部分文字描述和负责本文档的润色。所以，或许有必要添加下方的声明：

> [!WARNING]  
> 本插件模板和文档由 AI 生成，内容仅供参考，请仔细甄别。
>
> 虽然这只是个插件模板，也还是诚邀各路大佬对本模板提出一些意见，希望大家多多指点。
>
> 如果觉得这个模板比较实用的话，**就为这个模板点个** 🌟 **Star** 🌟 **吧~** ，这是对我们的最大认可与鼓励！

> [!NOTE]
> 虽然本插件模板的开发过程中大量使用了 AI 进行辅助，但我保证所有内容都经过了我的严格审查，所有的 AI 生成声明都是形式上的。你可以放心参观本仓库和使用本插件模板。并且该模板会持续维护。

> [!TIP]
> 本项目的相关开发数据 (持续更新中)：
>
> 开发时长：累计 2 天（主插件部分）
>
> 累计工时：约 5 小时（主插件部分）
>
> Tokens Used：5,371,300

---

## ✨ 功能特性

相较于官方基础模板，本插件模板当前新增或调整了以下内容：

### 🧩 插件能力演示

本模板的 [`main.py`](main.py) 以最小实现演示了 AstrBot 插件常用的核心能力，方便新开发者"开箱即学"：

- **基础指令**：演示配置读取与富媒体消息链（At + Plain）。
- **指令组与带参指令**：演示指令组组织方式与自动参数解析。
- **权限过滤**：演示仅管理员可用的指令。
- **主动消息**：演示通过 `unified_msg_origin` 向任意会话推送消息。
- **KV 存储**：演示插件维度的 `put_kv_data` / `get_kv_data`。
- **大文件存储规范**：演示将大文件存放于 `data/plugin_data/<plugin_name>/` 目录。
- **文转图**：演示 HTML + Jinja2 模板渲染图片。
- **会话控制**：演示多轮交互（`@session_waiter`）。
- **调用 AI**：演示调用当前会话的聊天模型。
- **LLM 工具**：演示通过 `@filter.llm_tool` 注册工具供模型调用。
- **钩子示例**：演示 AstrBot 提供的事件钩子能力。
- **插件 Pages**：演示在 WebUI 内嵌页面并通过 bridge 与后端 API 通信。
- **插件配置**：提供可视化配置，支持 string/int/bool/object/list、滑块（slider）、下拉选项（options）与 `_special` 特殊渲染（模型/TTS/STT 提供商、人格、知识库选取）等类型。
- **插件国际化**：提供中英文翻译资源，覆盖插件名、描述、配置项与 Pages 文案。

### 📦 仓库工程化

- **完整重写的 README 展示结构**：新增 Socialify 封面、状态徽章、访问计数、快速导航、开发者说明、友情链接、推荐阅读、仓库状态与 Star 历史等更完整的仓库首页展示内容。
- **更适合二次分发的文档骨架**：为安装、指令、配置、目录结构、架构说明、常见问题、已知限制等章节预留了更清晰的模板化占位结构，方便后续按真实插件内容补全。
- **补充 [`metadata.yaml`](metadata.yaml) 元数据**：插件标识改为 `astrbot_plugin_helloworld` 前缀形式，并同步调整展示名、短描述、描述、作者、仓库地址、版本信息、AstrBot 版本约束与支持平台列表，作为更贴近实际发布场景的参考写法。
- **改为以 [`metadata.yaml`](metadata.yaml) 作为主要元数据来源**：在 [`main.py`](main.py) 中移除了 [`register()`](main.py) 装饰器写法，仅保留基于插件类的实现方式，使模板结构与当前元数据文件协同。
- **新增贡献指南 [`CONTRIBUTING.md`](CONTRIBUTING.md)**：补充了 Issue 使用说明、代码贡献流程、代码风格要求、提交规范与文档贡献说明。
- **新增更新日志 [`CHANGELOG.md`](CHANGELOG.md)**：提供标准化版本记录文件，便于后续按发布节奏维护变更历史。
- **新增社区协作文件**：补充 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)、[`PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) 与多种 GitHub Issue 模板，覆盖 Bug、功能建议、文档建议、设计建议与开放讨论等协作场景。
- **新增 Dependabot 配置**：通过 [`dependabot.yml`](.github/dependabot.yml) 为 GitHub Actions 与 Python 依赖提供定期更新检查能力。
- **新增 Ruff 质量工作流**：通过 [`ruff-format.yml`](.github/workflows/ruff-format.yml) 增加格式化、自动修复、质量报告与 PR 评论能力，用于改进模板仓库的代码规范体验。固定使用 `0.14.2` 版本。
- **新增长期未活跃 Issue 清理工作流**：通过 [`stale.yml`](.github/workflows/stale.yml) 自动标记和关闭长期无活动 Issue，减少仓库维护负担。
- **新增自动发布工作流**：通过 [`release.yml`](.github/workflows/release.yml) 在 [`metadata.yaml`](metadata.yaml) 的版本号发生变更后自动提取版本信息、检查是否已有同名 Release，并尝试结合 [`CHANGELOG.md`](CHANGELOG.md) 生成发布说明，用于简化插件的版本发布流程。
- **新增“屎山检测”工作流**：通过 [`shit-mountain.yml`](.github/workflows/shit-mountain.yml) 集成额外的趣味化代码质量分析流程，作为仓库 CI 展示和风格化管理的一部分。
- **新增仓库展示资源与脚本**：增加 [`assets/`](assets/) 下的可视化徽图资源，以及 Windows 环境下可直接运行的 [`run_ruff.bat`](run_ruff.bat) 脚本，方便本地维护。

整体上，这个模板已经不再只是官方示例的最小复制，而是一个偏向"可直接拿去改造成个人仓库"、同时覆盖 AstrBot 插件核心能力的增强版起始模板。

## 📊 输出示例

- `/helloworld`：`@你 Hello, 用户名~`
- `/demo echo 你好`：`你说了：你好`
- `/demo todo 吃饭,睡觉,写插件`：渲染并发送一张待办清单图片
- `/demo guess`：进入猜数字多轮会话，机器人提示"大了/小了/猜对啦"
- `/demo ask 你好`：调用当前会话的聊天模型并返回回复
- `/demo data`：`插件数据目录: .../data/plugin_data/astrbot_plugin_helloworld`
- `/demo admin`：仅管理员可用，返回当前平台名

## 🚀 安装与使用

1. **下载插件**: ~~通过 AstrBot 的插件市场下载。~~或从本 GitHub 仓库的 Release 下载 `astrbot_plugin_helloworld` 的 `.zip` 文件，在 AstrBot WebUI 中的插件页面右下角的 `➕` 选择 `从文件安装`。
2. **安装依赖**: 本插件的核心依赖为 `None`，插件下载安装时会自动安装插件所需的依赖，通常无需额外安装。如果你的环境中确实缺少相关依赖，请安装：

   ```bash
   pip install -r requirements.txt
   ```

3. **重启 AstrBot (可选)**: 如果插件没有正常加载或生效，可以尝试重启你的 AstrBot 程序。
4. **配置插件**: 进入 AstrBot WebUI，找到 `AstrBot 插件模板` 插件，选择 `插件配置` 选项，配置相关参数。

## 📋 指令说明

### 顶层指令

| 指令 | 说明 |
| --- | --- |
| `/helloworld` | 演示配置读取与富媒体消息链（At 发送者 + 自定义问候语） |
| `/demo` | 指令组入口，无子指令时渲染指令树 |

### 指令组 `/demo`

| 指令 | 权限 | 演示能力 | 说明 |
| --- | --- | --- | --- |
| `/demo echo <文本>` | 所有人 | 带参指令 | 自动解析参数并复读 |
| `/demo count` | 所有人 | KV 存储 | 计数器，达到上限自动清零 |
| `/demo send` | 所有人 | 主动消息 | 通过 `unified_msg_origin` 推送消息 |
| `/demo todo <事项>` | 所有人 | 文转图 | 用逗号分隔，渲染待办清单图片 |
| `/demo guess` | 所有人 | 会话控制 | 猜数字多轮交互（输入"退出"结束） |
| `/demo ask <问题>` | 所有人 | 调用 AI | 调用当前会话的聊天模型 |
| `/demo admin` | 仅管理员 | 权限过滤 | 返回当前平台名 |
| `/demo data` | 所有人 | 大文件存储 | 显示插件数据目录 |

### LLM 工具（非指令）

| 工具名 | 说明 |
| --- | --- |
| `get_weather` | 注册为 LLM 工具，返回硬编码示例数据（非真实天气） |

---

## 🎣 事件钩子一览

AstrBot 提供的事件钩子用于拦截全局消息 / LLM 请求。**事件钩子不能与指令装饰器（`command`/`command_group` 等）共用**，且部分钩子内部不能使用 `yield` 发送消息，需改用 `event.send()`。

| 钩子 | 触发时机 | 本模板默认行为 | 副作用 |
| --- | --- | --- | --- |
| `on_astrbot_loaded` | AstrBot 初始化完成 | 记录日志 | 无 |
| `on_waiting_llm_request` | 等待 LLM 响应前 | **默认关闭**，开启后发送"🤔 正在思考中..." | ⚠️ 有（发送消息），默认关 |
| `on_llm_request` | LLM 请求发出前 | 记录日志（可修改 `ProviderRequest`） | 无 |
| `on_llm_response` | LLM 请求完成后 | 记录日志 | 无 |
| `on_agent_begin` | Agent 开始运行（>v4.23.1） | 记录日志 | 无 |
| `on_using_llm_tool` | LLM 工具调用前（>v4.23.1） | 记录日志 | 无 |
| `on_llm_tool_respond` | LLM 工具调用后（>v4.23.1） | 记录日志 | 无 |
| `on_agent_done` | Agent 运行完成（>v4.23.1） | 记录日志 | 无 |
| `on_decorating_result` | 发送消息前 | **默认关闭**，开启后回复末尾追加感叹号 | ⚠️ 有（修改消息），默认关 |
| `after_message_sent` | 消息发送后 | 记录日志 | 无 |

> [!TIP]
> 本模板中所有**有用户可见副作用**的钩子（发送/修改消息）均通过配置项默认关闭，仅记录日志的钩子保持开启，确保不影响日常使用。

---

## ⚙️ 配置项详解

本插件在 AstrBot WebUI 中提供了一套结构清晰的可视化配置体系，覆盖基础行为、AI 联动与平台资源选取。
您可以在 AstrBot 管理面板的"插件配置"中直接编辑，无需修改代码。

<details>
<summary>点击查看配置项详解</summary>

### 🧩 1. 基础行为配置

控制插件指令的回复风格与交互行为。

- **默认问候语 (`greeting`)**:
  - 类型：`String`
  - 默认值：`Hello`
  - 说明：用于 `/helloworld` 指令回复时的问候语前缀。
  - 提示：可与富媒体消息链（At 发送者 + 文本）组合展示，是演示"配置读取"的最直观示例。

- **计数器上限 (`count_limit`)**:
  - 类型：`Integer`（滑块）
  - 默认值：`10`
  - 范围：`1 - 20`（步长 `1`）
  - 说明：`/demo count` 指令的计数上限，达到后自动清零重新计数。
  - 提示：滑块组件支持在 WebUI 中直接拖动调整，无需手输数字。

- **运行模式 (`mode`)**:
  - 类型：`String`（下拉选择）
  - 默认值：`fast`
  - 可选项：`fast`（展示文本`快速`）/ `safe`（展示文本`安全`）
  - 说明：插件的运行模式，演示 `options` 下拉框配置项。
  - 提示：下拉框的展示文本通过 `labels` 字段指定，保存值仍为 `options` 中的原始值。

- **标签列表 (`tags`)**:
  - 类型：`List`
  - 默认值：`[]`
  - 说明：自定义标签列表，每个元素为字符串。
  - 提示：演示 `list` 类型配置的可视化编辑。

```json
{
  "greeting": "Hello",        // 默认问候语
  "count_limit": 10,          // 计数器上限（1~20，滑块）
  "mode": "fast",             // 运行模式（快速 / 安全）
  "tags": []                  // 自定义标签列表
}
```

---

### 🎛️ 2. 高级嵌套配置 (`advanced`)

演示 `object` 类型配置的嵌套子项结构。

- **比例 (`ratio`)**:
  - 类型：`Float`（滑块）
  - 默认值：`0.5`
  - 范围：`0 - 1`（步长 `0.1`）
  - 说明：嵌套子配置中的比例参数，演示 object 类型下的滑块控件。

```json
{
  "advanced": {
    "ratio": 0.5             // 比例（0~1，滑块）
  }
}
```

---

### 🤖 3. 平台资源选取（`_special` 特殊渲染）

借助 AstrBot 提供的 `_special` 特殊渲染能力，在 WebUI 中直接下拉/多选已配置好的模型提供商、人格与知识库，无需手填 ID。

- **聊天模型提供商 (`ai_provider`)**:
  - 类型：`String`
  - `_special`：`select_provider`
  - 说明：下拉选择 WebUI 中已配置的聊天模型提供商。
  - 提示：结果返回提供商字符串，可用于 `/demo ask` 等 AI 指令。

- **TTS 提供商 (`tts_provider`)**:
  - 类型：`String`
  - `_special`：`select_provider_tts`
  - 说明：下拉选择 WebUI 中已配置的语音合成（TTS）提供商。

- **STT 提供商 (`stt_provider`)**:
  - 类型：`String`
  - `_special`：`select_provider_stt`
  - 说明：下拉选择 WebUI 中已配置的语音识别（STT）提供商。

- **人格 (`persona`)**:
  - 类型：`String`
  - `_special`：`select_persona`
  - 说明：下拉选择 WebUI 中已配置的人格设定。

- **知识库 (`knowledgebase`)**:
  - 类型：`List`
  - `_special`：`select_knowledgebase`
  - 默认值：`[]`
  - 说明：多选 WebUI 中已配置的知识库。
  - 提示：`select_knowledgebase` 返回 `list` 类型，建议将配置项 `type` 设为 `list`、默认值设为 `[]`。

```json
{
  "ai_provider": "",         // 聊天模型提供商（select_provider）
  "tts_provider": "",        // TTS 提供商（select_provider_tts）
  "stt_provider": "",        // STT 提供商（select_provider_stt）
  "persona": "",             // 人格（select_persona）
  "knowledgebase": []        // 知识库，支持多选（select_knowledgebase）
}
```

---

### 📋 4. 开关与 AI 联动

- **启用 AI 相关指令 (`enable_ai`)**:
  - 类型：`Boolean`
  - 默认值：`true`
  - 说明：控制是否启用 AI 相关能力。
  - 提示：关闭后 `/demo ask` 指令与 `on_waiting_llm_request` 钩子的"正在思考"提示将不再生效。

- **回复追加感叹号 (`enable_decorate`)**:
  - 类型：`Boolean`
  - 默认值：`false`
  - 说明：演示 `on_decorating_result` 发送消息前钩子，开启后所有回复末尾会追加感叹号。
  - 提示：默认关闭，避免影响日常消息。

- **LLM 响应前提示 (`enable_waiting_hint`)**:
  - 类型：`Boolean`
  - 默认值：`false`
  - 说明：演示 `on_waiting_llm_request` 钩子，开启后每次调用 LLM 都会先发送"🤔 正在思考中..."提示。
  - 提示：默认关闭，避免每次对话都出现提示消息，影响日常使用。

```json
{
  "enable_ai": true,             // 是否启用 AI 相关指令
  "enable_decorate": false,      // 是否在回复末尾追加感叹号（演示钩子）
  "enable_waiting_hint": false   // LLM 响应前是否发送提示（演示钩子，默认关）
}
```

> [!NOTE]
> 以上所有配置项的 `description`、`hint` 与下拉展示文本均支持按 WebUI 语言显示，翻译见 [`.astrbot-plugin/i18n/`](.astrbot-plugin/i18n/zh-CN.json)。

</details>

---

## 📂 插件目录与结构

```bash
AstrBot/
└─ data/
   └─ plugins/
      └─ astrbot_plugin_helloworld/
         ├─ .astrbot-plugin/                # 插件国际化资源
         │  └─ i18n/                        # 语言文件（zh-CN / en-US）
         ├─ .gitignore                      # Git 忽略规则
         ├─ _conf_schema.json               # AstrBot WebUI 配置界面 schema 定义
         ├─ CHANGELOG.md                    # 插件更新日志
         ├─ CONTRIBUTING.md                 # 本插件的贡献指南
         ├─ LICENSE                         # 许可证文件
         ├─ main.py                         # 插件主入口文件（能力演示）
         ├─ metadata.yaml                   # 插件元数据信息
         ├─ pages/                          # 插件 Pages（WebUI 内嵌页面）
         │  └─ demo/                        # 演示页：index.html / app.js / style.css
         ├─ README.md                       # 插件说明文档
         ├─ requirements.txt                # 插件依赖声明（本模板无第三方依赖）
         ├─ run_ruff.bat                    # Ruff 一键格式化与自动修复脚本
         │
         └─ assets/                         # README / 仓库展示资源
```

---

## 🏗️ 架构说明

```mermaid

```

示例架构说明。

---

## ❓ 常见问题

### Q1：README 最上面那个头图好好看，怎么弄的？

[Socialify](https://socialify.git.ci/)；[仓库地址](https://github.com/wei/socialify)

### Q2: 那个猫猫访客数又是怎么弄的？

[MoeCounter](https://count.getloli.com)；[仓库地址](https://github.com/journey-ad/Moe-Counter)

### Q3: 仓库状态这个卡片呢？

[Repobeats](https://repobeats.axiom.co/?ref=producthunt)

### Q4：要钱吗？

都是免费的哦。

---

## 🚧 已知限制

要在你自己的仓库使用此模板，请修改以下文件的内容为你的实际情况 (主要是涉及仓库链接、徽章资源、发布流程与文档格式的替换)：

- PULL_REQUEST_TEMPLATE.md
- ShitMountain.svg 等 SVG 徽章资源 (不想要可以都删了)
- CHANGELOG.md
- CODE_OF_CONDUCT.md (替换为你的实际邮箱)
- CONTRIBUTING.md
- metadata.yaml (废话)
- README.md (不然呢)
- .github/workflows/release.yml (如你的版本字段、分支策略或 Changelog 标题格式不同，请一并调整)

> [!TIP]
>
> 要使用本仓库提供的 Issue 模板，您还需要运行该脚本 [Issue & PR 标签自动替换脚本](https://github.com/DBJD-CR/awesome_issue_pr_label) 以适配自定义的标签。
>
> 当前 [`release.yml`](.github/workflows/release.yml) 的整体思路是可复用的，但它默认依赖 [`metadata.yaml`](metadata.yaml) 中存在 `version` 字段，且更适合配合形如 `## [v1.0.0] - 2026-05-08` 的 [`CHANGELOG.md`](CHANGELOG.md) 标题格式使用；如果你的仓库使用不同的分支模型、版本命名或更新日志格式，建议在套用模板时同步修改该工作流。

## 💖 友情链接与致谢

- [AstrBot](https://github.com/AstrBotDevs/AstrBot)：在此感谢其开发团队对该项目的付出。

## 📚 推荐阅读

我的其他插件：

- [主动消息 (Proactive_chat)](https://github.com/Pancakes-Labs/astrbot_plugin_proactive_chat) - 它能让你的 Bot 在特定的会话长时间没有新消息后，用一个随机的时间间隔，主动发起一次拥有上下文感知、符合人设且包含动态情绪的对话。
- [灾害预警 (Disaster_Warning)](https://github.com/Pancakes-Labs/astrbot_plugin_disaster_warning) - 它能让你的 Bot 提供实时的地震、海啸、台风、气象预警信息推送服务。
- [视奸面板 (Live_Dashboard)](https://github.com/Pancakes-Labs/astrbot_plugin_live_dashboard) - 它能让你的 Bot 和群友随时随地视奸你。
- [代码统计 (Count_Loc)](https://github.com/Pancakes-Labs/astrbot_plugin_count_loc) - 它能让你的 Bot 对任意公开的 GitHub 或 GitLab 仓库的代码行数、文件数量、注释行数、物理总行数等指标进行快捷获取和分析。

## 🤝 贡献

欢迎提交 [Issue](https://github.com/DBJD-CR/astrbot_plugin_helloworld/issues) 和 [Pull Request](https://github.com/DBJD-CR/astrbot_plugin_helloworld/pulls) 来改进这个插件！

- 对于新功能的添加，请先通过 Issue 等方式讨论。
- 对于 PR (拉取请求)，请确保你已阅读并同意遵守本项目的 [贡献指南](https://github.com/DBJD-CR/astrbot_plugin_helloworld/blob/main/CONTRIBUTING.md)。

## 📞 联系我们

如果你对这个插件模板有任何疑问、建议或 bug 反馈，欢迎加入我的 QQ 交流群。

- **QQ 群**: 1033089808
- **群二维码**:
  
  <img width="281" alt="QQ Group QR Code" src="https://github.com/user-attachments/assets/53acb3c8-1196-4b9e-b0b3-ad3a62d5c41d" />

## 📄 许可证

GNU Affero General Public License v3.0 - 详见 [LICENSE](LICENSE) 文件。

本插件采用 AGPL v3.0 许可证，这意味着：

- 您可以自由使用、修改和分发本插件。
- 如果您在网络服务中使用本插件，必须公开源代码。
- 任何修改都必须使用相同的许可证。

## 📊 仓库状态

![Alt](https://repobeats.axiom.co/api/embed/2c8d42b135fc9fc4c4bf1b4d88c4490bbc57a919.svg "Repobeats analytics image")

## ⭐️ 星星

<a href="https://www.star-history.com/?repos=dbjd-cr%2Fastrbot_plugin_helloworld&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=dbjd-cr/astrbot_plugin_helloworld&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=dbjd-cr/astrbot_plugin_helloworld&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=dbjd-cr/astrbot_plugin_helloworld&type=date&legend=top-left" />
 </picture>
</a>

---

Made with ❤️ by DBJD-CR
