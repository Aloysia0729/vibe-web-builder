# 暂停、恢复与变更

先读六份文档及相关代码、Git 改动、验收与最近测试，不依赖隐含会话记忆。schema_version=1；未知版本不猜测迁移。`project.py check` 只查结构、一致性和门槛，不验证用户身份或内容真实性。

| 字段 | 约定 |
|---|---|
| requirements.revision | 正整数；业务/范围变化递增。 |
| confirmation | pending/confirmed；确认时 confirmed_revision=revision，evidence 非空。 |
| design.requirements_revision | 草图依据的需求版本，需求变更须重对齐。 |
| design.revision | 正整数；草图布局或视觉改变递增。 |
| progress.mode | planning/development；明确请求才切 development。 |
| progress.phase | interview / requirements-review / design / design-review / planning-delivered / implementation / validation / delivered。 |
| progress.status | active/paused/blocked；后两者写暂停入口或阻塞原因。 |
| progress.requirements_revision / design_revision | 和对应文档当前 revision 一致。 |

confirmation_evidence 简记用户确认原意与时间/可用会话位置，不含秘密；标签不能自证确认。恢复须审查正文与来源。

## 恢复

1. 简述完成、未完成、已知问题与最近可靠阶段。
2. 意图明确为继续则直接继续；确实不明才问继续还是新建，新建用独立目录。
3. 未确认需求最多到 requirements-review；未确认草图不能实施。planning 不能进入 implementation/validation/delivered。
4. 缺失、冲突或过时：保留现有文件，不重跑 init 覆盖；核对版本、正文、代码，提出保守恢复建议，只重新确认受影响内容。
5. 无可靠确认依据则 pending，不补造用户认可、不重问所有需求。

## 变更与暂停

业务变更：分析受影响页面、交互、任务、设计和实现；递增需求 revision，清空两份 confirmation、confirmed_revision、confirmation_evidence；修订草图后更新其 requirements_revision 并递增草图 revision；同步 progress，回 requirements-review。记录旧决定、原因和影响，重新确认总结及草图，保留有效实现。

仅视觉/模块位置变更：保留需求确认，递增草图 revision、清空草图确认，回 design-review。不改含义的错字修订可保持确认并记原因，不能借此规避业务变更。

planning 切 development 保留有效确认；两门槛均有效可实施，不重访谈。暂停写 status=paused、next_action、剩余任务、能力限制；恢复先核实再 active。
