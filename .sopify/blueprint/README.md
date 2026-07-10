# change-audit Blueprint

## 状态

产品边界和一期方案已经确认，当前仓库仍处于实现前阶段。CrossReview 尚未迁移，`change-audit` 也尚未提供可安装运行能力。

## 当前目标

交付一个产品、一个 Python 包和一个 AI host Skill：`change_audit.review` 是 artifact-general 隔离审查内核，正式 audit 能力按 artifact profile 成熟度放行；Python 负责可信上下文、结构化审计、校验和确定性呈现。

## 当前焦点

按当前方案先交付 Git diff 首个正式 profile，再实现宿主审查与反馈闭环；`audit.json` / `audit.html` 通过同父目录 staging 完成校验后成对提交。Codex 是首个 dogfood 宿主，Qoder 是第二宿主。

## 维护方式

本目录只保留长期真相：`background.md` 说明产品问题，`design.md` 说明稳定架构，`tasks.md` 只列未完成长期项。实现任务、验收门禁和已确认决策以当前方案包为准。

## 阅读入口

- [项目技术约定](../project.md)
- [产品背景](./background.md)
- [长期设计](./design.md)
- [长期任务](./tasks.md)
- [当前方案](../plan/20260710_audit_json_v0_schema_renderer_spike/plan.md)
- [变更历史](../history/index.md)
