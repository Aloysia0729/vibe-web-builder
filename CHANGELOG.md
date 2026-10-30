# Changelog

采用语义化版本；未发布变更先写 Unreleased。此文件记录版本内容，不表示远端 Release 已发布。

## [Unreleased]

尚无额外变更。

## [0.1.1] - 2026-10-31

### Fixed

- CI 的 pip 缓存显式使用 requirements-dev.txt，修复 setup-python 找不到默认依赖文件而在安装和测试前退出的问题。

### Release

- manifest 与 README 同步为 0.1.1；新标签包含 CI 修复，保留原 v0.1.0 标签。建议以 GitHub Pre-release 分发，宿主安装与插件市场兼容性仍需补充验证。

## [0.1.0] - 2026-10-30

### Added

- 中文双模式网页搭建 Skill，自适应访谈、需求/草图独立确认与分阶段开发。
- 按需加载参考文档、六份持久化模板及安全初始化/一致性检查工具。
- Codex skill-only manifest、中文指南、结构校验、工具测试、行为演练与只读 CI。

### License

- 自定义禁止收费许可：允许免费商业使用，禁止对 Skill 或修改版收费；生成的网站不自动继承限制。并非 MIT 或 OSI 开源许可证。

### Limitations

- 自动校验不能证明模型在所有对话中遵守工作流；行为验收须单独执行并记录。
- 标准 Skill 与 manifest 已本地校验；宿主安装发现、GitHub Actions 和公开发布需在对应环境验证。
