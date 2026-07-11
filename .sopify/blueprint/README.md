# change-audit Blueprint

## 状态

change-audit v0 code-diff 一期与 Wave 5 单产品收口已经完成并归档。最终 316 项测试、clean wheel、固定 Fireworks range 的 `product/v0.3` dogfood 和两阶段复审均已通过；Qoder 模型级 smoke 由用户明确延后。

## 当前目标

维护一个产品、一个 Python 包和一个 AI host Skill。Schema `0.2` 当前只支持 Git diff；Python 负责可信上下文、结构化审计、校验和确定性呈现。

## 当前焦点

当前焦点是合并已经归档的一期收口变更。tag、Release、PyPI 发布和迁移来源仓库处理均不自动执行。

## 维护方式

本目录只保留长期真相：`background.md` 说明产品问题，`design.md` 说明稳定架构，`tasks.md` 只列未完成长期项。已完成任务、验收门禁和决策证据保存在归档方案中。

## 阅读入口

- [项目技术约定](../project.md)
- [产品背景](./background.md)
- [长期设计](./design.md)
- [长期任务](./tasks.md)
- [已归档的一期方案](../history/2026-07/20260710_audit_json_v0_schema_renderer_spike/plan.md)
- [变更历史](../history/index.md)
