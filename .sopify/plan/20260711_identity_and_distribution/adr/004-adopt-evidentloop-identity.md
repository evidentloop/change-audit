# ADR-004：采用 EvidentLoop 单一产品身份

## 状态

待定

## 日期

2026-07-12

## 上下文

`change-audit` 准确描述 v0 Git diff 审计，却不能自然覆盖完整 snapshot、receipt 和其他结构化产物作为正式审查目标的长期方向。产品愿景已经明确为：让具备审查边界、可验证来源和可信锚点的 AI 开发产物形成可回链审计记录，并通过交互式报告完成反馈、修订与复审。

`EvidentLoop` 由两个常见词构成：`Evident` 表达依据可检查，`Loop` 表达审查反馈闭环。它可以统一当前单产品组织的 GitHub、repository、PyPI、CLI、Python import 与 Skill 身份，不绑定 code diff、Audit Graph 或 anchor 等单一实现。

初步公开检索未发现有影响力的精确同名软件，但存在 `Evidently` 与 `EvidenceLoop` 等相邻名称。当前风险偏好接受相邻品牌；只有精确同名，或同类软件中足以造成实质混淆的近似名称，才阻断本次命名。PyPI 无公开项目页和域名 WHOIS `No match` 都不等于已经取得名称。正式迁移前仍需完成 USPTO/WIPO 基础筛查并由用户确认风险；专业法律意见只在基础筛查发现实质风险时另行决定。

## 决策

满足以下激活条件后，采用 `EvidentLoop` 作为唯一产品身份，并取代 ADR-002：

1. 完成 USPTO、WIPO 的精确词、近似拼写/读音及相关软件/SaaS 服务基础筛查，保留可审计证据，并按上述实质混淆标准给出判断。
2. 复核 PyPI、GitHub、域名与相邻品牌状态，明确区分“未发现公开项目”“可注册”“已取得”。
3. 用户在身份 checkpoint 明确接受风险、目标身份矩阵、版本策略与后续外部动作边界；这不等于授权立即执行 repository 改名、域名购买或发布。

激活后的身份为：

| 层面 | 身份 |
|---|---|
| 组织 / 产品 | `EvidentLoop` |
| repository | `evidentloop/evidentloop` |
| PyPI / CLI / Python import | `evidentloop` |
| Skill | `skills/evidentloop/` |
| Pages | `https://evidentloop.github.io/evidentloop/` |
| schema / prompt / runtime namespace | `evidentloop` |

迁移采用 clean break：不保留旧 import、旧 CLI、旧 Skill 或双 namespace alias。历史 `.sopify`、dogfood 与已生成报告保留原始 `change-audit` 身份，通过迁移说明与 release manifest 维持 provenance。

ADR-004 在激活前保持“待定”，`change-audit` 仍是当前代码事实；不得仅凭本 ADR 修改源码或执行外部注册操作。

## 理由

- 覆盖结构化产物审计与反馈闭环，不把长期产品限制在 change/revision。
- 组织与产品统一，用户只需理解一个名字。
- 两个常见词形成长期隐喻，比 Audit/Anchor/Graph 组合更接近使命而非机制。
- 零用户、未发布阶段适合执行 clean break，避免把双身份兼容债务带入首个 Alpha。

## 替代方案

- 保留 `change-audit`：仍是门禁失败时的安全回退；优点是 v0 直观，缺点是长期 snapshot/profile 需要额外解释。
- `AnchorLoop`：拒绝。anchor 只代表一项机制，域名与历史公司使用也更不利。
- `AuditAnchor` / `AnchorProof`：拒绝。易被理解为区块链或密码学证明，且超出产品承诺。
- `audit-graph` / `audit-everything`：拒绝。前者绑定内部实现，后者暗示无法保证的穷尽性。

## 影响

- 本地迁移涉及 package/import、schema、prompt、runtime identity、Skill、tests、docs 与生成入口。
- GitHub repository 改名、域名取得、PyPI ownership、Trusted Publisher、tag 和 Pages 均属于后续需授权的外部操作。
- schema 与 prompt 版本必须随实际契约变化升级，建议目标为 schema `0.3` 与 prompt `v0.4`，最终由身份 checkpoint 确认。
- ADR-004 生效后，ADR-002 标为已废弃；ADR-001 与 ADR-003 的分发和 evidence 决策继续有效。
