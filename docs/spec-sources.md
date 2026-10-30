# 格式依据与兼容范围

核对日期：2026-10-30。官方文档站在本环境返回 HTTP 403，因此未声称读取其页面正文；采用可访问的官方 GitHub 原文和本地 CLI 帮助。未关闭 TLS 或校验。

| 来源 | 用途与限制 |
|---|---|
| [Agent Skills specification 原文](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) | SKILL.md、name/description、按需加载与资源路径规范。 |
| [OpenAI skill-creator](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator) | 使用其 init_skill.py 初始化，generate_openai_yaml.py 生成 UI，quick_validate.py 校验；脚本仅临时下载，不作为本仓库依赖。 |
| [openai/skills README](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) | GitHub URL 的 skill-installer 用法；该仓库已标 deprecated，新的插件结构以 openai/plugins 为准。 |
| [openai/plugins](https://github.com/openai/plugins/tree/0722921d5542fc593105c27bd52630babd8b8c2a) | README 要求 .codex-plugin/plugin.json；采用其 skill-only 插件常用字段与 skills 路径。 |
| [官方 Remotion manifest 示例](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/remotion/.codex-plugin/plugin.json) | name、version、description、author、repository、license、skills 字段形状依据；不复制其服务或资产。 |
| [Codex Skills](https://developers.openai.com/codex/skills) / [Build plugins](https://developers.openai.com/codex/plugins/build) | 用户复核宿主安装与当前插件分发流程的官方入口；本环境页面未读取。 |
| [Codex config schema](https://github.com/openai/codex/blob/main/codex-rs/core/config.schema.json) | 为 CLI 发现探测核对 sqlite_home/log_dir 的受支持配置；未改写平台配置或凭据。 |

`schemas/plugin.schema.json` 是本项目的严格兼容字段 profile，**不是官方完整 schema**。自动校验验证该 profile 和资源位置；官方 quick_validate 只验证 Skill 元数据，不验证插件安装、对话行为或所有 Agent Skills 最新字段。根目录 plugin.json 的可移植格式未验证，暂不宣称支持。

本地安装复制和状态工具已验证；Codex CLI 0.163.0 的真实 skills/list 探测因宿主状态目录只读未完成，不能算发现成功。远端 GitHub 安装、GitHub Actions、插件市场安装仍需对应环境验证。独立代理的恢复与开发演练只证明所记录场景，不代表 UI 的自动发现。
