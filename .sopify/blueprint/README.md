# change-audit Blueprint

## 状态

change-audit v0 code-diff 一期与 Wave 5 单产品收口已经完成并归档。当前进入产品身份与分发方案评审：保留 316 项测试和真实 dogfood 所验证的审计内核，先完成 EvidentLoop 身份门禁，再推进 Python CLI、标准 Skill、在线预览与证据隔离。

## 当前目标

公开交付物收敛为 PyPI CLI、同仓库标准薄 Skill 和 GitHub Pages。用户可以先在线看报告、再用 `uvx` 运行 replay demo，正式使用时安装 CLI 与 Skill 后用一句自然语言生成 `audit.json + audit.html`。Schema `0.2` 当前只支持 Git diff；机械审计契约不因分发方式变化而弱化。

## 当前焦点

当前焦点是评审[产品身份与分发方案](../plan/20260711_identity_and_distribution/background.md)：EvidentLoop 仅是待门禁激活的目标身份；通过身份 checkpoint 后执行本地 clean break，再推进 CLI、Skill、真实宿主试跑、证据隔离与公开发布。未经对应 checkpoint 授权，不修改或提交源码身份，也不创建 tag 或 release；纯方案文档可在明确授权后独立提交。

## 维护方式

本目录只保留长期真相：`background.md` 说明产品问题，`design.md` 说明稳定架构，`tasks.md` 只列未完成长期项。已完成任务、验收门禁和决策证据保存在归档方案中。

## 阅读入口

- [项目技术约定](../project.md)
- [产品背景](./background.md)
- [长期设计](./design.md)
- [长期任务](./tasks.md)
- [产品身份与分发方案](../plan/20260711_identity_and_distribution/background.md)
- [已归档的一期方案](../history/2026-07/20260710_audit_json_v0_schema_renderer_spike/plan.md)
- [变更历史](../history/index.md)
