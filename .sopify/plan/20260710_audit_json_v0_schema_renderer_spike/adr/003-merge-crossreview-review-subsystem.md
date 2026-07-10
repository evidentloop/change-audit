# ADR-003：将 CrossReview 合并为内部 review 子系统

## 状态

已采纳，迁移后复核 consequences

## 日期

2026-07-10

## 上下文

CrossReview 已实现 ReviewPack、prompt、host-integrated ingest、ReviewResult、normalizer、adjudicator、测试和 eval harness；change-audit 负责 Audit Graph、HTML 与用户反馈。两个项目都处于 alpha 且 CrossReview 没有真实用户。

保持两个包会要求用户安装两次、发现两个 Skill，并维护两套发布和兼容策略。把 CrossReview 作为运行时依赖又会保留这些产品边界。

## 决策

- CrossReview 核心等价迁入 `change_audit.review`。
- ReviewPack 与 ReviewResult 继续作为内部审查契约。
- change-audit 是唯一产品名；CrossReview 是内部能力名。
- 旧 `crossreview` CLI 不进入新 distribution。
- 原测试、eval harness、canonical prompt 和可选 reviewer 行为必须保留。
- 真实 eval fixtures 继续隔离；main 只放 harness 与 synthetic fixtures。
- 迁移先记录基线，再改 import；adapter 在等价迁移完成后实现。
- 旧仓库和 PyPI 包不立即删除、不 yank。

## 理由

现在合并的兼容成本最低，可以把已有审查工程资产直接转化为一个完整用户产品，同时保留内部模块边界和可验证迁移。

## 替代方案

- 两个产品独立发展：拒绝，因为没有用户证明双产品边界有价值。
- change-audit 依赖 `crossreview` 包：拒绝，因为用户仍需承担两包版本协调。
- 复制少量代码、放弃测试与 eval：拒绝，因为会损失现有质量资产。

## 影响

- Wave 0 必须证明 ReviewResult 行为等价。
- import、测试、CI、prompt 资源和可选 extra 都需要迁移。
- 合并 dogfood 成功后才能重新评估旧仓库归档。
- 本 ADR 的实际迁移差异在 Wave 0B 后补充。
