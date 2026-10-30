---
schema_version: 1
---

# 开发任务清单

## 技术方案与理由

当前目标 /tmp/vwb-behavior-resumed 从另一个会话复制六份已确认的规划文档，无既有代码、manifest、锁文件、CI 或运行脚本，不是 Git 仓库。复核需求 v1 与草图 v1 的独立确认依据后，按本次明确指令从 planning 切换 development。

三页展示和原生链接足以满足需求，采用静态 HTML/CSS、四份本地编号 SVG 色块及 Python 标准库本地静态服务。不安装依赖、不引入框架、数据库或外部服务。原有规划文件不重新初始化，保留有效确认。

## MVP 与后续范围

P01 首页、P02 作品、P03 联系，暗色大图、桌面双列与手机单列，I01–I04 导航/浏览/原生邮箱选择复制。名称为“摄影作品集”；邮箱仅显示 contact@example.invalid；四幅编号色块明确标注本地占位。带导航的 404、图片失败提示属于原交互规格。无筛选、放大、登录、表单、复制按钮、后台或扩展阶段。

## 阶段与验收

| 任务 ID | 阶段 | 页面/交互 ID | 工作内容 | 前置条件 | 可观测验收/命令 | 状态 | 证据 |
|---|---|---|---|---|---|---|---|
| T01–T04 | 原规划 | P01–P03 / I01–I04 | 需求、交互、草图与两次独立确认 | 原会话 | 两份 confirmed v1，确认原文及关联版本一致 | done | requirements.md / design.md 保留原始确认依据 |
| T05 | A 准备 | P01–P03 | 真实恢复、切换 development、选择无依赖静态实现 | 用户明确要求恢复开发；两门槛有效 | 读取六份文档、环境检查、project.py check | done | progress.md；Python 3.12.14、Chromium 与 Playwright 可用 |
| T06 | B MVP | P01–P03 / I01–I04 | 三页、本地占位、导航、纯文本邮箱及规格中的异常处理 | T05 | python3 serve.py --port 8765；本地代表请求 | done | public/ 与 serve.py；HTTP 及真实浏览器验证通过 |
| T07 | D 验证 | P01–P03 / I01–I04 | 路由、导航、390/1280px、焦点、邮箱和图片失败检查 | T06 | python3 checks/smoke.py；project.py check | done | 当前 checks/last-run.json：13 组 passed；首轮同步失败与修复保留 |
| T08 | E 交付 | 全部 | 保存运行步骤、真实结果与恢复入口，停止临时服务 | T07 | README.md 与六份文档一致 | done | README、progress 与两轮 JSON 已保存；自启会话结束，但端口清理未确认，见 cleanup.json |

## 运行与边界

```sh
cd /tmp/vwb-behavior-resumed
python3 serve.py --port 8765
```

仅绑定 127.0.0.1；根目录 public/，/works 与 /contact 自动重定向到尾斜杠，未知路径返回 HTTP 404 和返回首页导航。网站没有安装、构建或类型检查环节，无环境变量需求。浏览器验证使用环境现有工具，非应用依赖。

只在此 /tmp 项目内保存文件；不部署、不推送、不创建账号或云资源、不写云环境配置。测试后停止本次启动的服务。原路径 /tmp/vwb-behavior-simple 只保留在历史记录，不作为当前运行目录。
