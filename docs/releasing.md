# 版本与发布

采用 SemVer：修正规则/文档且不改变契约用 PATCH；向后兼容的新能力用 MINOR；破坏状态文件、模式或恢复契约用 MAJOR，并给旧版迁移及回退步骤。版本与公开发布状态以 GitHub Release 页面为准。

## 发布前检查

- manifest version、CHANGELOG 版本与 README 一致，CHANGELOG 标明 Added/Changed/Fixed/Breaking 与已知限制。
- README 的安装/调用在目标 Codex 版本实际验证，记录版本与宿主。
- `python scripts/validate.py` 和 `python -m unittest discover -s tests -v` 通过。
- 行为场景按验收标准执行，关键双门槛、规划停止与恢复不得只凭静态检查宣称通过。
- GitHub PR CI 实际成功，不把本地通过当作远端通过。
- `git diff --check`、变更审阅及敏感信息检查通过；确认自定义禁止收费许可适用，分发包包含完整 LICENSE。
- 确认发布范围及远端推送、标签、公开 Release 的明确授权。

## 本地到 GitHub

先 `git status`、`git diff` 审阅；只 stage 此次预期文件，不打包 `.venv`、目标网站文档或秘密。用户授权后由维护者提交并推送到已有的 Aloysia0729/vibe-web-builder 仓库，推荐通过分支/PR 合并 main。没有授权时停在本地，不创建远端资源。

以下是维护者**获得推送授权后**可执行的示例：

```bash
git switch -c feat/vibe-web-builder-skill
git add README.md .codex-plugin .env.example .github .gitignore CHANGELOG.md CONTRIBUTING.md LICENSE docs requirements-dev.txt schemas scripts skills tests
git diff --cached --check
git diff --cached
git commit -m 'feat: add vibe web builder skill'
git push -u origin feat/vibe-web-builder-skill
```

在已有仓库的 GitHub 页面从该分支创建指向 main 的 PR，检查 Validate skill 工作流并完成审阅后合并。若已有同名本地分支，先检查其用途再选择新名称，不覆盖旧分支。推送前仍需在实际宿主验证 README 安装方式。

选择与 manifest、README、CHANGELOG 一致且包含所需修复的版本标签；不移动已经公开的旧标签。当前修复版为 `v0.1.1`，发布说明见 [v0.1.1](releases/v0.1.1.md)。主分支 CI 通过后，已获授权的测试版可标记为 GitHub Pre-release，并明确未验证范围；正式稳定版还应完成真实宿主安装验证。可在 GitHub UI 发布，无需额外脚本或自动发布 workflow。创建 Release 前应核对当前远端状态。

## Release Notes 模板

```text
vX.Y.Z — 标题
适用 Codex/宿主版本：实测版本
新增/修复：用户可观察变化
安装：Skill 目录 URL 和已验证方法
验证：自动检查、行为演练与真实宿主记录
兼容性：状态 schema、破坏性变化、迁移和回退
已知限制：未验证或未支持能力
许可证：LicenseRef-Vibe-Web-Builder-No-Charge-1.0（自定义禁止收费许可）
```

发布后保留历史版本，避免未经授权迁移用户状态。若需 marketplace 分发，另按官方当前格式登记并验证；本仓库不假装已进入市场。
