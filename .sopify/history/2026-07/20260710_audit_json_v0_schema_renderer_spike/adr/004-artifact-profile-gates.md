# ADR-004：审查内核 artifact-general，正式 audit 按 profile 门禁

## 状态

已采纳

## 日期

2026-07-10

## 上下文

CrossReview 的长期概念边界包含 code diff、plan、design、analysis、review-result 等可独立审查的 artifact，但当前实现、prompt、locatability 和 eval baseline 只验证 `code_diff`。change-audit 一期也以 change/file/hunk 为核心。

如果把一期约束写成永久产品边界，会丢失合并 CrossReview 的长期价值；如果现在把所有类型塞进 `0.2`，又会产生大量没有 fixture 和消费者的可空字段。

## 决策

- `change_audit.review` 保留 artifact-general 审查内核定位。
- 一期公开能力只承诺 Git diff → `audit.json` + `audit.html`。
- 非 diff 类型可以先产生内部 ReviewResult 或宿主摘要，不因此宣称完整 audit 支持。
- artifact 类型只有具备专属 adapter、可信 anchor、eval baseline 和 renderer profile 后，才进入正式 audit 产品面。
- `audit.json 0.2` 是 code-diff audit profile 契约，不冒充所有 artifact 的最终通用 schema。
- 第二种真实 profile 出现时再用独立 ADR 和 schema 版本设计 review target 与新 anchor，不预先堆 nullable 字段。

## 理由

该分层同时保护一期可验证性和长期扩展方向。ReviewPack → reviewer → ReviewResult 的隔离审查协议可以复用，但数据锚点、质量基线和用户呈现必须按 artifact 类型单独证明。

## 影响

- 长期 blueprint 不再把 Git diff 描述为永久产品边界。
- v0 scope、样张和实现任务仍严格以 code diff 为准。
- Renderer 保持共同外壳，定位模块按 profile 切换；没有成熟 profile 时不生成伪完整 HTML。
- 当前 `artifact` 节点继续表示派生正式产物，不复用为被审查输入。
