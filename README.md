# Vibe Coding 网页搭建向导

把“我想做个网站”变成明确的需求、页面规格、草图和可执行任务；确认后可继续让 Codex 分阶段实现。适合不了解网页架构的新手，也支持扩展已有网站。默认简体中文，可跟随用户语言。

这是对话工作流程 Skill，不是独立聊天网站，不需要专用 MCP、账号、数据库或 API Key。当前版本 **0.1.1**，许可证为自定义 **禁止收费许可**（见 [LICENSE](LICENSE)）。

## 两种模式

| 模式 | 做什么 | 停在哪里 |
|---|---|---|
| 规划 | 自适应访谈 → 需求确认 → 页面/交互规格 → 草图确认 → 六份文档 | 不创建正式应用；要继续需明确切换开发模式。 |
| 开发 | 同样先经过两次独立确认，再做 MVP、迭代、验证和交付 | 本地代码与运行指导；部署、付费、密钥等单独授权。 |

每轮最多 1–3 个新问题，不重复已回答内容。AI 根据目标与已有项目选择简单技术；静态介绍页不会默认加数据库。没有浏览器时可用文本线框，未运行的检查会明确说明。

## 安装到 Codex

标准 Skill 位于 [skills/vibe-web-builder](skills/vibe-web-builder/)。只安装这个目录即可使用核心能力；Python 工具是可选辅助，缺少 Python 时可手动按模板维护文档。

### 从 GitHub 安装

在已提供 `$skill-installer` 的 Codex 会话中输入：

```text
$skill-installer install https://github.com/Aloysia0729/vibe-web-builder/tree/main/skills/vibe-web-builder
```

此方式依赖该目录已推送到 GitHub；请确认所用分支或标签中存在该目录。`skill-installer` 并非所有宿主都提供；缺失时用手动安装，不需新增远程服务。

### 手动安装本地版本

在你自己的终端，将 Skill 目录复制到目标项目的 `.agents/skills/`。在目标网站项目根目录执行，先把 `VWB_SOURCE` 改为本仓库的实际位置：

```bash
VWB_SOURCE=/absolute/path/to/vibe-web-builder
mkdir -p .agents/skills
if [ -e .agents/skills/vibe-web-builder ] || [ -L .agents/skills/vibe-web-builder ]; then
  echo '已安装，请先查看和备份旧版本，不要直接覆盖。'
else
  cp -R "$VWB_SOURCE/skills/vibe-web-builder" .agents/skills/vibe-web-builder
fi
```

按宿主要求重开 Codex 会话，让其重新发现技能。项目安装只作用于该项目；支持用户级技能的 Codex 版本可使用 `~/.agents/skills/`，具体搜索路径以所用版本的 [Codex Skills 文档](https://developers.openai.com/codex/skills) 为准。手动复制可离线完成；安装/自动发现仍受宿主版本与配置影响。

### skill-only plugin

本仓库附 [.codex-plugin/plugin.json](.codex-plugin/plugin.json)，采用官方 `openai/plugins` 当前示例结构。没有 MCP 或外部服务声明。根目录 `plugin.json` 的跨客户端可移植规范尚未在本环境核实，因此不声称兼容该格式，也没有创建重复 manifest。

插件宿主的市场安装流程请按 [官方构建指南](https://developers.openai.com/codex/plugins/build) 操作；没有为本仓库配置或发布 marketplace，不编造一键 plugin 安装命令。标准 Skill 安装不依赖插件市场。规范来源和验证范围见 [格式依据](docs/spec-sources.md)。

## 如何调用

```text
$vibe-web-builder 我想做一个作品集，只要规划方案。
```

也可以说“帮我从想法开始规划一个网站”。自然语言匹配由 Codex 的技能发现机制决定，并不保证拦截每条消息。仅询问 CSS 属性、HTML 语法或单行修复时不应触发建站访谈。

## 完整初次建站示例

以下是示范对话，并非真实部署或测试记录：

1. 用户：“我想做摄影作品集，给潜在客户看，只做方案。首页、作品、联系三块，暗色大图，无登录，联系只显示邮箱。”
2. 向导直接提取五项基础需求，建议用单页锚点导航和静态技术，将建议与用户事实分开；不重复问用途或要求选择框架。
3. 向导展示需求总结：“目标是让客户看作品并联系；MVP 包含三块内容，作品点击看大图；默认图片由你提供；暂不加入账号/数据库。请确认或修改。”
4. 用户：“确认需求。”向导记录需求 v1 确认，然后输出首页文字线框、移动端排列、配色和导航，细化作品与联系的点击行为。
5. 用户：“草图确认。”向导记录独立的草图 v1 确认，交付六份文档，**在规划模式停止，不创建网站**。
6. 用户：“现在切换到开发模式，按这个方案做出来。”向导复核两份确认与版本，保留访谈，从 MVP 开始实现。没有新业务变化不重问全部需求。
7. 向导按可用能力启动和检查页面，记录实测与未运行项，给出实际运行命令和部署步骤；没有部署授权时不发布。

功能型网站如多人笔记工具，会按需补充数据归属、权限与持久化需求，详细用例见 [行为场景](docs/behavior-scenarios.md)。

## 文档、修改与继续

目标网站项目会生成 `docs/web-builder/`，不是写进 Skill 安装目录：

| 文件 | 用途 |
|---|---|
| requirements.md | 目标、用户、需求、事实状态、假设及需求确认版本。 |
| sitemap.md | 页面、导航、模块、跳转和 MVP 范围。 |
| interactions.md | 按钮、表单、校验、状态及可测试结果。 |
| design.md | 参考证据、视觉规范、草图及独立确认版本。 |
| implementation-plan.md | 技术理由、阶段、任务、验收与依赖。 |
| progress.md | 模式、当前阶段、完成证据、测试、问题及下一步。 |

说“暂停，保存进度”会保存下一步。新会话说“继续这个项目”时先读文档核对真实代码和确认；不能只靠会话记忆。

说“把邮箱改成联系表单”时只修订受影响需求、交互、设计及任务；业务变更使旧需求/草图确认失效，重新确认变化后继续，不推倒有效实现。若只是调整模块位置，只需重确认受影响草图。

可选工具（Python 3.10+、PyYAML 6.x；无工具时按同一规则手动维护）：

```bash
python3 /path/to/skill/scripts/project.py init --project /path/to/website
python3 /path/to/skill/scripts/project.py check --project /path/to/website
```

只有用户已选开发模式才在 init 加 `--mode development`。init 拒绝覆盖已有状态；check 验证元数据与版本，不证明语义完整、用户真实确认或应用可运行。不得把 pending 手动改标签后冒充用户同意。

## 安全与权限

需求确认和草图确认只授权对应内容。外部登录、使用/写入密钥、付费服务、云资源、生产修改、正式部署、远端推送、重要数据删除均需针对动作的明确授权。已有明确授权不重复问。真实秘密通过安全配置渠道提供，不写在聊天、文档或 Git 中；本 Skill 自身无需密钥，[.env.example](.env.example) 只有说明。

## 常见问题

- **只想要方案？** 明确说“只规划”；即使草图确认也不创建应用。
- **不知道选什么技术？** 描述业务目标即可，向导先检查旧项目，再推荐简单方案。
- **没有浏览器或无法读取参考？** 会说明限制并提供文本线框，不伪造已访问/已验证记录。
- **找不到 Skill？** 检查复制路径、目录名、SKILL.md 与宿主搜索路径，重开会话并显式用 `$vibe-web-builder`；本地结构通过不代表宿主已发现。
- **旧状态报错？** 先保留文件，核对版本与确认依据；不要重新初始化覆盖。按 [恢复规则](skills/vibe-web-builder/references/project-resumption.md) 修复受影响部分。
- **Python 工具缺依赖？** 使用已有安全 Python 环境安装 PyYAML 6.x，或手动复制模板；核心对话不依赖脚本。

## 本地验证与贡献

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

CI 使用相同命令，覆盖结构、YAML/UI、manifest 本地兼容 profile、Markdown 资源、模板、工具错误路径和基础秘密检测；不调用远端模型。自动检查无法证明对话遵守约定；人工/独立代理场景与实际结果见 [行为场景](docs/behavior-scenarios.md)、[验证记录](docs/validation-report.md) 和 [验收门槛](docs/acceptance.md)。

维护方式见 [CONTRIBUTING.md](CONTRIBUTING.md)，版本与发布步骤见 [发布指南](docs/releasing.md)。发布状态以 GitHub 标签与 Release 页面为准；发布前复核许可条款和未验证项。

## 许可范围

允许免费使用、修改和分发本 Skill，包括企业内部及其他不收费的商业使用；保留版权声明和完整许可文本，修改版注明修改并遵守相同限制。

禁止销售本 Skill 或修改版、收费访问、收费托管，以及将其捆绑在付费产品、订阅或服务中。例外须另获版权人许可。

使用 Skill 生成的网站和原创代码不因使用了该工具而受此收费限制，可以商业化；不得借生成产物之名将 Skill 本身或其主要内容作为付费产品分发。

这是自定义的源码可用许可，不是 MIT，也不是符合 OSI 定义的开源许可证。完整法律条款以英文 LICENSE 为准。
