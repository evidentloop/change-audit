# 变更提案：EvidentLoop 身份迁移、零摩擦分发与审计证据隔离

## 需求背景

当前审计内核已经通过真实 dogfood，但外部用户仍需 clone、创建 venv、editable install 并手工注册 Skill。产品能力可用，首次成功路径不可用。

分发评审进一步确认：`change-audit` 准确描述 v0 的 Git diff 入口，却不足以承载结构化产物审计与反馈闭环的长期愿景。`EvidentLoop` 将证据可见性与“检查 -> 反馈 -> 修订 -> 复审”闭环合并为同一品牌隐喻，且可以统一 GitHub org、repository、PyPI、CLI、Python import 与 Skill 身份。

本方案因此把产品身份迁移提升为分发前置 Wave。商标与注册风险门禁通过、用户再次确认 ADR-004 之前，只允许完成方案、检索和迁移设计，不修改源码身份，也不执行域名购买、仓库改名、PyPI 注册或公开发布。

评分：

- 方案质量：9/10
- 落地就绪：7/10

评分理由：

- 方案质量扣 1 分：main/evidence 双 commit 无法原子更新，仍需依靠 `source_commit` 校验与 fail-closed 发布门禁。
- 落地就绪扣 3 分：`EvidentLoop` 的 USPTO/WIPO 近似词筛查尚未完成；身份迁移涉及 schema、prompt provenance、Skill、历史证据和远端仓库；CLI、demo、doctor、Pages 与真实宿主 E2E 仍待实现。

## 决策状态

- 分发方式遵循[ADR-001](adr/001-pypi-cli-standard-skill.md)。
- `change-audit` 是当前代码与历史证据基线，遵循[ADR-002](adr/002-change-audit-current-baseline.md)。
- `EvidentLoop` 是待门禁激活的目标身份，遵循[ADR-004](adr/004-adopt-evidentloop-identity.md)；ADR-004 生效后取代 ADR-002。
- main/evidence 边界、首次 Alpha 前隔离和 fail-closed 发布遵循[ADR-003](adr/003-main-and-audit-evidence-placement.md)。

方案包含两个必须停车的 checkpoint：

1. Wave 0 身份 checkpoint：提交官方商标初筛、注册风险、相邻品牌、目标身份矩阵和迁移契约；确认前不改源码身份。
2. Wave 6 发布 checkpoint：提交准确 commit、版本、构建物、测试、真实宿主 smoke、证据与外部操作清单；确认前不提交或推送身份实现与发布候选，不 tag/publish/启用 Pages。经用户明确授权的纯方案文档 commit/push 不属于发布操作。

## 用户成功标准

1. 身份门禁通过后，产品、repository、PyPI、CLI、Python import 与 Skill 统一为 `EvidentLoop` / `evidentloop`，不保留第二套活动 runtime 别名。
2. 无需 clone 或 editable install，即可查看在线报告或运行 replay demo。
3. 正式安装使用 `uv tool install evidentloop` 与标准 skills CLI；pipx 作为 fallback。
4. 用户说“用 EvidentLoop 审计 staged changes”后，得到正式 `audit.json + audit.html`。
5. main checkout 不依赖 `audit-evidence` 即可构建、测试、安装和运行。
6. README/Pages 提供稳定证据入口；每个 PyPI 版本绑定不可变 main tag、`source_commit` 和已发布 evidence bundle。

## 影响范围

- 身份契约：产品、repository、PyPI、CLI、import、Skill、Pages、schema namespace、prompt provenance、运行标识与反馈存储键。
- Python package：console script、demo、doctor、resources 与 PyPI metadata。
- Skill：迁移到 `skills/evidentloop/`，保持静态薄编排。
- 仓库：main 产品面、固定 evidence worktree、Pages 与 evidence bundle。
- 发布：远端 repository 改名、main/evidence 双 commit 校验、Trusted Publishing 与真实宿主 smoke。

## 非目标

- 不在身份 checkpoint 前修改源码、schema、prompt 或活动 Skill。
- 不为旧名保留运行时 alias、双 package、双 CLI 或双 Skill；历史证据保留原名与 provenance。
- 不把非代码 profile 描述为当前能力。
- 反馈闭环是长期核心能力；本方案不把“完整反馈消费并重新生成报告”设为身份迁移的前置门禁。Wave 2 实施前根据现有能力与验证成本确定首个 Alpha 范围，纳入则补齐结构化契约和闭环测试，延后则在公开能力声明中明确边界。
- 不把测试源码、schema 或 release gate 移出 main。
- 不自研 npm 包、独立二进制、本地 LLM 或宿主 adapter registry。
- 不永久保存 raw model output、完整日志、coverage 或未脱敏截图。

## 主要风险

- 名称冲突风险：接受 `Evidently`、`EvidenceLoop` 等非直接冲突的相邻品牌并记录搜索风险；只有精确同名，或同类软件中足以造成实质混淆的近似名称，才阻断 `EvidentLoop`。必须完成官方基础筛查并保留证据，不默认把专业法律意见设为 Alpha 前置条件。
- 身份漂移：迁移必须由单一矩阵驱动，并用旧标识 allowlist 与全仓扫描阻断半迁移状态。
- 历史证据断链：旧 dogfood 不重写；新证据通过 manifest 显式记录旧/新身份与来源 commit。
- 双分支漂移：manifest 绑定准确 `source_commit`；不一致即阻断发布。
- 公开证据泄露本地信息：push 前执行路径、密钥、raw output 与个人信息扫描。
- evidence branch 不减少 Git 对象总量：当前目标是默认树和认知隔离，不宣称解决 clone 体积。
