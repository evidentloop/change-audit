# change-audit 长期任务

状态：只保留未完成长期项和明确延后项。当前实施顺序、细分任务与验收门禁以[当前方案包](../plan/20260710_audit_json_v0_schema_renderer_spike/tasks.md)为准。

## 一期 code-diff profile

- [ ] 冻结 CrossReview 可验证基线，记录固定 commit、测试、eval 和公开接口事实。
- [ ] 将 CrossReview 审查核心等价迁入 `change_audit.review`，保留测试与 eval 数据隔离，证明行为等价。
- [ ] 建立最小可安装 Python 包、JSON Schema 2020-12、结构校验、引用校验和 wheel 资源验证。
- [ ] 实现纯消费的 HTML renderer、回链校验和 `python -m change_audit render`。
- [ ] 实现 `prepare`：读取本地 Git diff，在最终目录同父目录的隐藏 staging/.run 中生成 `audit-skeleton.json`、ReviewPack、可信 hunk index 和安全 prompt，并返回 `run_id`、final/staging 路径的机器 locator。
- [ ] 实现宿主 LLM 输出的完整性判定、ReviewResult ingest、Audit Graph adapter、锚点降级规则与 `finalize`。
- [ ] 在 staging 中完成 JSON/HTML 全部验证后，复查最终目标 leaf 不存在，再用一次同文件系统目录 rename 成对提交正式产物；目标已存在或 rename 失败时停止并保留 staging 诊断。
- [ ] 对隐藏 bug、干净 diff 和 partial review 完成 dogfood，再冻结 schema、状态语义和暂定风险权重。
- [ ] 实现 HTML finding 决策、localStorage 暂存和 `audit-feedback.jsonl` 显式导出。
- [ ] 交付自包含 change-audit Skill；先在 Codex 完成自然语言到 HTML 的端到端验证，再在 Qoder 验证第二宿主。

## 后续能力

- [ ] 根据一期样本收紧宿主审查 prompt、语言专项提示和 JSON 生成约束。
- [ ] 评估确定性规则作为 LLM 审查增强，但不替代语义 finding 主链路。
- [ ] 评估多审查者、CrossReview adjudication 和语言专项 eval 对幻觉与漏报的改善。
- [ ] 增加正式 `change-audit` console-script 别名并评估 PyPI 发布；永久保留模块入口。
- [ ] 建模多轮审计差异并消费 `audit-feedback.jsonl`。
- [ ] 按真实需求逐类推进 artifact profile：先允许内部 ReviewResult，只有通过 adapter、可信 anchor、eval baseline 和 renderer profile 四项门禁后才公开正式 audit；候选包括 plan/design、analysis/review-result、agent output、folder diff、远程 PR 和 code snapshot。
- [ ] 评估可选 SVG 概览和 Markdown 导出；完整审计仍以 HTML 为主。
- [ ] 补充 Sopify checkpoint 与其他报告工具的 `audit.json` 消费集成。
- [ ] 真实多写者需求出现后，评估原生 race-proof no-replace、平台专用锁、递归 symlink 防御及对应对抗性故障注入；一期只采用本地单写者、非对抗并发模型。

## 明确延后

- [-] 自动修复代码或把审计结果升级为强制策略门禁。
- [-] 默认集成模型 SDK、要求用户配置 provider key，或把 provider-backed 模式作为主链路。
- [-] 在等价迁移和 dogfood 完成前归档、删除 CrossReview 仓库或中断旧包可用性。
