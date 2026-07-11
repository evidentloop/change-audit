# change-audit Blueprint

## 状态

change-audit v0 code-diff 一期与 Wave 5 单产品收口已经完成并归档。当前已进入零摩擦分发设计阶段：保留 316 项测试和真实 dogfood 所验证的审计内核，把现有 Python CLI 产品化，并补齐标准 Skill 与在线预览。

## 当前目标

公开交付物收敛为 PyPI CLI、同仓库标准薄 Skill 和 GitHub Pages。用户可以先在线看报告、再用 `uvx` 运行 replay demo，正式使用时安装 CLI 与 Skill 后用一句自然语言生成 `audit.json + audit.html`。Schema `0.2` 当前只支持 Git diff；机械审计契约不因分发方式变化而弱化。

## 当前焦点

当前焦点是评审并实施[零摩擦分发方案](../plan/20260711_zero_friction_distribution/background.md)：以 PyPI CLI 作为唯一 runtime 真相源，以标准 Skill 作为发现与编排层，并补齐 replay demo、doctor、GitHub Pages 和真实宿主验证。未经授权不创建 commit、tag 或 release。

## 维护方式

本目录只保留长期真相：`background.md` 说明产品问题，`design.md` 说明稳定架构，`tasks.md` 只列未完成长期项。已完成任务、验收门禁和决策证据保存在归档方案中。

## 阅读入口

- [项目技术约定](../project.md)
- [产品背景](./background.md)
- [长期设计](./design.md)
- [长期任务](./tasks.md)
- [零摩擦分发方案](../plan/20260711_zero_friction_distribution/background.md)
- [已归档的一期方案](../history/2026-07/20260710_audit_json_v0_schema_renderer_spike/plan.md)
- [变更历史](../history/index.md)
