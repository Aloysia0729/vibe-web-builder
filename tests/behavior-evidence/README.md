# 独立代理对话产物

这里保存真实测试会话生成的 Markdown 快照。所有“用户确认”均来自测试驱动器逐轮发送的**模拟用户输入**，只证明该测试场景，不能作为任何生产项目的授权。没有让代理自行编造后续用户答复。

- [simple-planning](simple-planning/docs/web-builder/progress.md)：完整摄影作品集需求 → 独立需求确认 → 展示草图 → 独立草图确认 → 仅规划交付并暂停。最终只有六份文档。
- [interview](interview/docs/web-builder/progress.md)：模糊想法 → 一个用途问题 → 咖啡店需求与“由你决定” → 推荐单页/视觉并请求需求确认。
- [functional-change](functional-change/docs/web-builder/progress.md)：笔记工具需求确认后展示草图；用户取消删除功能，需求/草图升 v2 并清空当前确认，只更新受影响文档。
- [resumed-development](resumed-development/docs/web-builder/progress.md)：新代理仅依赖已保存文件恢复，明确切开发后实现临时静态 MVP；[首次失败](resumed-development/checks/first-run-failed.json)、[复测 13 组通过](resumed-development/checks/last-run.json) 与[清理限制](resumed-development/checks/cleanup.json)均保留。主代理[停止后 HTTP 复核](resumed-development/checks/post-stop-http.json)仍取得站点响应，不能宣称服务已关闭。

完整测试输入、已观察结果和未运行范围见 [验证记录](../../docs/validation-report.md)。快照内的 /tmp 路径是测试时工作目录，仅作审计记录；重放时使用新的独立目标目录。不要直接把这些已确认文档当成自己的需求。

这些产物不自动证明模型的未来表现。修改 Skill 后应重新逐轮运行对应场景，而不是只验证旧快照。
