# ADR-002：Alpha 保留 change-audit 产品身份

## 状态

已采纳

## 日期

2026-07-11

## 上下文

产品曾考虑改名 ClaimBind，以承载未来的非代码审计。但 Alpha 阶段首先需要降低理解和安装成本，而 `change-audit` 已能直接说明当前价值。名称中的 `change` 本身不限定代码，可以覆盖有版本或状态边界的工作流变更。

## 决策

Alpha 保留以下唯一身份：

| 层面 | 身份 |
|---|---|
| 产品、仓库、PyPI、CLI | `change-audit` |
| Python import/source package | `change_audit` |
| Skill | `skills/change-audit/` |
| Pages | `https://evidentloop.github.io/change-audit/` |

v0 只宣称 Git diff 审计。未来的 plan revision、handoff transition 等 profile 可以继续使用 change-audit，只要正式被审对象仍是有版本或状态边界的 change。

本轮不修改 repo/package/import/schema namespace、prompt 文本或 prompt version。PyPI `change-audit` 的实际可注册性是发布前门禁；若不可取得，必须停车重新决策。

## 理由

- 用户一眼知道产品做什么，不需要先理解抽象品牌。
- repo、PyPI、CLI 与 Python import 的连字符/下划线差异是生态惯例，不构成品牌分裂。
- 保留现有身份避免 50 余文件的纯命名迁移，让时间回到 CLI、Skill、demo 和真实审计体验。
- 非代码扩展是否需要改名，取决于被审对象是否脱离 change/revision，而不是输入是否为代码。

## 替代方案

- ClaimBind clean break：拒绝用于当前 Alpha。品牌力更强，但解释成本和迁移面高于当前收益。
- change-audit 品牌 + ClaimBind 技术 alias：拒绝。双身份增加文档和排障分叉。
- 立即寻找其他 Audit/Anchor 名称：拒绝。继续海选不改善当前用户链路。

## 影响

- Phase 0 删除 package/import/repo 改名、prompt 升级与 schema namespace 迁移任务。
- 现有 schema 0.2、`extensions.change_audit`、prompt `v0.3` 和历史证据自然保持一致。
- 若未来正式对象不再是 change/revision，必须新建 ADR 重新评估名称，不能悄悄扩张语义。
