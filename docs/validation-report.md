# 本地验证记录

记录日期：2026-10-30；本地版本：0.1.0。此文件只记录实际执行结果，不代表已推送、发布或通过宿主市场审核。

## 自动工具结果

工作目录 `/workspace/vibe-web-builder`，Python 3.12.14；单独创建 `.venv`，没有依赖全局 Python 环境才能通过。

| 实际命令/操作 | 结果与边界 |
|---|---|
| `python3 -m venv .venv` | passed，创建独立环境。 |
| `.venv/bin/python -m pip install -r requirements-dev.txt` | passed；精确固定已验证的直接及传递依赖。 |
| `.venv/bin/python -m pip check` | passed，无依赖冲突。 |
| `.venv/bin/python scripts/validate.py` | passed：Skill/UI 元数据、manifest 兼容 profile、模板、资源链接和基础敏感信息模式检查。不是官方完整插件安装验证或全面安全审计。 |
| `.venv/bin/python -m unittest discover -s tests -v` | **36 tests，全部 passed**；包含有效状态与实际失败路径，零 skipped。 |
| `.venv/bin/python /tmp/vwb-creator/scripts/quick_validate.py skills/vibe-web-builder` | passed，输出 `Skill is valid!`；使用官方 skill-creator 工具，只校验 Skill metadata。工具来源见格式依据，不是 CI 的在线依赖。 |
| 独立安装副本运行 init/check | passed，属于上述工具测试：只复制 Skill 文件夹后仍能初始化六份文档并校验，无需仓库其余文件。 |
| CI YAML 本地解析 | passed，核对 PR/main push/manual 触发、contents:read 权限与测试命令；未在 GitHub runner 执行。 |
| `git diff --check` | passed；不代表已提交或推送。 |

测试范围含：已有文件/空目录保护、符号链接拒绝、缺失/损坏/重复 YAML key、未知 schema、确认缺依据、旧确认失效、需求/草图门槛、规划模式拒绝开发、非零 CLI 状态、manifest/链接/模板/秘密扫描的负例。负例是在测试内断言拒绝成功，不是被掩盖的失败测试。

## 独立代理多轮对话

测试由独立 Codex 代理加载真实 Skill，主代理逐轮发送模拟用户输入；未让代理自行编造后续同意。模型沿用当前会话配置，未指定替代模型。项目都在 `/tmp` 隔离目录，未改动 Skill 源码、未执行远端写入。以下不是确定性单元测试，不能推断所有宿主/未来模型都表现相同。

### 摄影作品集：三轮，已完成

1. 用户给出作品集用途、潜在客户、首页/作品/联系、暗色大图、无登录/表单、邮箱联系、只规划。代理新增业务问题 **0**，只请求需求确认；六份文档均保存，需求/草图 pending，无草图或应用。
2. 输入“确认需求 v1，请继续出页面草图”。代理记录需求 confirmed v1，展示三页线框与桌面/手机布局，独立请求草图确认；草图 pending，仍无正式应用。中途生成并查看过三张临时 PNG，随后按测试简化要求删除，保留文本线框；不能描述为从未生成视觉草图。
3. 输入“接受草图 v1。继续保持只制定方案，不要开发。请交付方案并保存暂停进度”。最终 **planning / planning-delivered / paused**，两确认各有独立证据，目标目录只有六份 Markdown。主代理检查文件和运行状态校验均通过。

快照：[进度](../tests/behavior-evidence/simple-planning/docs/web-builder/progress.md)、[草图](../tests/behavior-evidence/simple-planning/docs/web-builder/design.md)、[交互](../tests/behavior-evidence/simple-planning/docs/web-builder/interactions.md)。

### 模糊想法与 AI 推荐：两轮，已完成

1. 输入“我想建个网站”。代理仅提出 **1 个用途问题**，planning/interview，两确认 pending，无应用。
2. 输入咖啡小店、附近顾客、地址营业时间、无登录下单、只要方案，并说页面风格由 AI 决定。代理新增业务问题 **0**，建议单页和奶油白/咖啡棕，区分事实、建议、默认与待补内容，停在需求确认。没有把“由你决定”写成整份需求已确认。

快照：[需求](../tests/behavior-evidence/interview/docs/web-builder/requirements.md)、[进度](../tests/behavior-evidence/interview/docs/web-builder/progress.md)。

### 功能型团队笔记：三轮，已完成

前两轮：完整需求直接总结，新增业务问题 0；仅确认需求后展示登录/列表/编辑的三页文本草图与保存失败、权限、空列表等规格，草图 pending、无正式应用，未接真实云服务。

第三轮输入“取消删除笔记功能，保留新建、查看、编辑和保存，其他不变；先更新文档，不开发或接服务”。代理将需求/草图均升至 v2，当前确认均 pending，清空确认版本/依据，回到 requirements-review；只移除删除相关按钮、确认框、交互、任务及数据操作权限计划，保留其他设计与历史确认记录。主代理核对产物，状态检查退出 0，仍只有六份 Markdown。

快照：[需求 v2](../tests/behavior-evidence/functional-change/docs/web-builder/requirements.md)、[草图 v2](../tests/behavior-evidence/functional-change/docs/web-builder/design.md)、[变更进度](../tests/behavior-evidence/functional-change/docs/web-builder/progress.md)。没有声称实际认证、跨设备持久化或数据库隔离已测试。

### 新代理恢复并切开发：已完成

复制摄影项目六份已确认文档到新目录，交给不继承旧对话的独立代理。它读取真实文件、核实两个独立确认及版本，按明确用户指令切换 development；新增访谈问题 **0**、重复确认 **0**。补齐的名称、测试邮箱和编号色块不改变已确认范围。实际实现三页静态 MVP，未新增数据库、后台、外部服务或依赖；最终 development / delivered / paused，状态检查退出 0。网站和临时验证脚本只在 `/tmp/vwb-behavior-resumed`，不是本仓库产品。

使用环境原有 Python Playwright 与 **Chromium 154.0.8037.57** 实测。首轮 9 组检查通过后，键盘步骤因断言早于异步导航完成而失败，退出码 1。定向复现确认导航会完成，仅加入 `wait_for_url` 等待，保留原 URL/标题断言；复测退出码 0，**13 组检查全部通过**：三页 HTTP/标题、四个本地图及 CSS、404、真实浏览器启动、390px/1280px 布局、9 组导航组合、Tab/Enter 与焦点、原生选取/复制邮箱、实际拦截图片后的失败回退、浏览器 404/返回首页及无外部资源请求。

这验证了所述响应式与基础键盘行为，不等于全面可访问性审计或全设备覆盖。纯静态产物没有构建/类型配置，未执行此类不适用检查。复制目标没有 Git 仓库，`git status` 实际退出 128，已诊断记录，没有伪称通过或擅自初始化。

证据：[最终进度](../tests/behavior-evidence/resumed-development/docs/web-builder/progress.md)、[首轮失败](../tests/behavior-evidence/resumed-development/checks/first-run-failed.json)、[复测通过](../tests/behavior-evidence/resumed-development/checks/last-run.json)。主代理读取当前报告，核对时间、result=passed 和 13 条检查，未用旧结果替代当前运行。

清理限制：代理向自己启动的 PTY 80454 发送 Ctrl+C，该会话退出码 1；但端口仍可连接，当前进程命名空间无法确认监听者。主代理随后短超时 HTTP 请求仍取得该测试站 200 响应，**服务未确认清理，且仍在响应**；没有终止未知进程。详见 [原始清理记录](../tests/behavior-evidence/resumed-development/checks/cleanup.json) 和 [停止后 HTTP 复核](../tests/behavior-evidence/resumed-development/checks/post-stop-http.json)。这不是供用户访问的预览链接。后续使用同一端口前先核实归属，不盲目杀进程。

## 15 类场景覆盖

| ID | 当前证据 |
|---|---|
| B01 模糊 | 通过上述单用途问题情景。 |
| B02 完整 | 摄影/咖啡/笔记输入均未重复访谈；通过所述情景。 |
| B03 跳过/推荐 | “页面风格都由你决定”给建议并保持 pending；通过所述情景。 |
| B04 规划 | 三轮摄影项目两确认后仍零应用；通过。 |
| B05 开发 | 第一确认后只出草图；两确认及明确模式切换后实现本地 MVP，所述完整路径通过。 |
| B06 参考 | 未运行真实网页/截图读取与不可达参考场景。 |
| B07 无参考 | 咖啡与笔记提出有理由的视觉方向；通过所述情景。 |
| B08 简单 | 摄影方案和实际 MVP 都为无依赖静态页面，无数据库/后台；通过。 |
| B09 旧项目 | 未运行已有应用扩展场景。 |
| B10 恢复 | 新代理仅依赖文件恢复并保留有效确认，完成实施与验证；该情景通过。缺文档有工具负例，未跑损坏状态的完整对话。 |
| B11 需求变化 | 取消删除后只更新受影响规格、v2 两确认失效并回需求审阅；通过该业务变更情景。仅视觉变更有工具测试，未独立跑对话。 |
| B12 敏感 | 已观察各场景无远端写入或密钥操作；未覆盖所有拒绝/授权及外部内容注入情景。 |
| B13 失败修复 | 真实首轮同步断言失败 → 定向复现 → 添加导航等待 → 保留断言复测 13 组通过，记录完整；该测试工具修复情景通过，未覆盖真正应用缺陷的修复对话。 |
| B14 误触发 | 自动匹配行为未验证；显式加载 Skill 的代理不能证明路由。 |
| B15 缺能力 | 有文本线框降级产物，但未运行真正禁用浏览器/命令/文件工具的场景。 |

## 宿主探测与未执行范围

尝试通过 **Codex CLI 0.163.0 app-server / skills/list** 发现手动复制到临时项目 `.agents/skills/` 的 Skill。首次在初始化时因 `/home/agent/.codex` 只读而退出；查阅官方 config schema 后，将受支持的 sqlite_home/log_dir 指向 `/tmp` 再试，仍在启动时返回只读文件系统。**探测失败，未到达 skills/list；不能算 Skill 被宿主拒绝或已被发现。** 未修改权限或平台凭据，没有自动审批拒绝事件。

GitHub URL 安装、Codex UI 自动发现、GitHub Actions 远端运行、插件市场安装、公开 Release 和生产部署均未完成。无人类手工验收记录。当前是本地实现与验证交付，不能据此称为全平台验证或已正式发布。

## 环境配置

已通过配置工具保存 install_script 草稿：进入本仓库、创建 `.venv`、按 requirements-dev 安装并运行结构校验。该流程不需要常驻服务，因此没有添加 start_skill。保存不等于发布；用户需要在环境设置审核保存，再发布环境以供后续任务复用。

## GitHub CI 首次运行与修复

用户提供的真实 GitHub Actions 截图显示：checkout 通过，setup-python@v5 因 pip 缓存默认只查找 requirements.txt/pyproject.toml、未找到本仓库的 requirements-dev.txt 而失败；后续安装、结构检查和测试均被跳过，不能记为通过。此前本地 YAML 检查未覆盖这一缓存行为。

修复为显式配置 cache-dependency-path: requirements-dev.txt，使缓存输入与安装命令使用相同文件。本地复核原默认模式匹配为空、修复后路径存在，并重新运行结构校验和 36 项工具测试通过。远端修复结果需独立核验；GitHub API 读取仍返回 Forbidden，不能据本地通过推断远端通过。
