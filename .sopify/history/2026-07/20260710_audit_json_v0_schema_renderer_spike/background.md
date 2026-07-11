# 变更提案：change-audit v0 code-diff 一期闭环

## 需求背景

用户希望在 Codex、Qoder 等 AI coding 宿主里直接说“帮我用 change-audit 审计本地改动”，随后得到一份带语义 finding、代码上下文和用户决策控件的 HTML 报告。

当前两个仓库各自只覆盖半条链路：

- `change-audit` 已有数据模型、JSON 样张和 HTML 参考件，但没有实现代码。
- CrossReview 已有 Git diff 打包、规范 prompt、宿主审查结果 ingest、ReviewResult、测试和 eval harness，但没有用户。

将 CrossReview 作为外部依赖会保留两次安装、两套 CLI、两套 Skill 和两份契约。当前没有真实用户依赖旧接口，是合并为一个产品的低成本窗口。

合并不等于把产品永久限制为 Git diff。CrossReview 的长期边界包含 plan、design、analysis、review-result 等可审查 artifact；当前代码、prompt 和 eval 只验证 `code_diff`。一期先完成第一个正式 audit profile，长期 blueprint 保留 artifact-general review 内核与按类型成熟度放行的产品方向。

评分：
- 方案质量：9/10
- 落地就绪：8/10

评分理由：
- 优点：用户主链路、宿主边界、内部传输、状态模型、锚点策略和退出门禁均已明确。
- 扣分：风险评分权重仍需在 Wave 2 dogfood 后校准；CrossReview 迁移等价性尚未实际验证。

## 用户价值

一期完成后，用户只感知一个产品：

```text
自然语言触发
  -> AI host Skill
  -> 本地 Git diff 的隔离语义审查
  -> finalize 在隐藏 staging 中生成并校验 JSON/HTML
  -> 成对提交 audit.json + audit.html
  -> 用户反馈 JSONL
```

用户不需要手写 `audit.json`，不需要知道 ReviewPack、ReviewResult 或 CrossReview，也不需要在每个项目复制集成说明。

## 变更内容

1. 将 CrossReview 的审查核心等价迁入 `change_audit.review`。
2. 建立最小可安装 Python 包、JSON Schema、语义校验和自包含 HTML renderer。
3. 建立 `prepare -> host LLM -> finalize（内部 render 并成对提交）` 的宿主编排链路；独立 `render` 只用于重渲染已有审计数据。
4. 建立 ReviewResult 到 Audit Graph 的 category、hunk、状态、verdict 和风险映射。
5. 建立 localStorage 决策暂存与 `audit-feedback.jsonl` 导出。
6. 建立自包含 Skill，并完成 Codex 与 Qoder 两个宿主的 dogfood。
7. 明确 artifact profile 门禁：非 diff 类型先允许内部 ReviewResult，具备 adapter、anchor、eval 和 renderer 后才承诺正式 audit 产物。
8. finalize 在临时区完成 JSON/HTML 生成与全部校验，再成对发布正式产物。
9. 一期发布协议采用本地 single-writer 模型：保留 `run_id`、leaf 检查和失败诊断，不实现原生 no-replace、对抗性竞态或递归符号链接防御。

## 影响范围

- 代码实施期：迁入 review 子系统和原测试；新增 schema、adapter、renderer、命令与 Skill。
- 文档：README、v0 scope、data model、AI host integration、长期 blueprint 和方案 ADR。
- 设计资产：统一 Flat Icon 风格的 v0 架构图和宿主审查时序图；长期 artifact profile 边界由 blueprint 与 ADR 定义，不额外扩图。
- CrossReview 仓库：本轮不修改；后续只在等价迁移和 dogfood 成功后处理归档。

## 风险评估

| 风险 | 缓解 |
|---|---|
| 迁移改变 CrossReview 行为 | Wave 0A 记录 commit、测试和 eval 基线；Wave 0B 使用固定输入比较 ReviewResult |
| LLM 编造文件或位置 | prepare 生成可信 hunk index；finalize 按 file、line、hunk header 反查 |
| 真实 bug 因位置不完整被丢弃 | 降级为未计分 risk，保留原 category 和原因，交给用户判断 |
| 未锚定风险导致评分误导 | 不计入数字评分；仅有此类风险时 risk score 为 null |
| 源码中的 prompt injection | diff 明确作为不可信数据封装；Skill 禁止执行源码或审查文本中的指令 |
| 临时审查材料泄漏或误提交 | POSIX 上尽力收紧 `.run/` 权限；成功清理、失败明确提示，并验收 Git ignore；权限模式不作为跨平台硬门禁 |
| 包资源在 wheel 中丢失 | 隔离安装 smoke test 覆盖 schema、模板、CSS 和 JavaScript |
| Schema 过早冻结 | 语义 bug、干净 diff、partial review 三类 dogfood 后才冻结 `0.2` |
| 一期 diff 约束被误写成永久产品边界 | 蓝图区分 artifact-general review 内核与 code-diff audit profile；每种新 profile 单独建立 eval 与 renderer 门禁 |
| render 失败留下孤立 `audit.json` | JSON/HTML 先在 staging 中完成全部校验，再发布正式产物对；硬失败保留诊断但不发布半套报告 |
| 两个 writer 同时争抢同一输出目标 | 一期明确采用本地 single-writer；prepare 与提交前检查目标 leaf，已有 entry 或 rename 失败即停止；对抗性竞态留待后续加固 |
| 方案规模过大 | 每个 Wave 有独立退出门禁；Wave 1 可独立交付 JSON 到 HTML 能力 |

## 成功标准

- 任意有效样张可以稳定校验并渲染为自包含 HTML。
- AI host 能从自然语言请求完成本地 diff 审查，不依赖 Python 内的模型 SDK。
- 干净审查、存在 finding、partial、failed、not reviewed 五种状态不会互相混淆。
- 所有 bug finding 可回到真实 diff hunk；未定位语义风险不会被静默丢弃。
- 用户默认只看到 `audit.json` 与 `audit.html`，需要时再导出反馈或保留诊断材料。
- 正式报告要么同时存在且相互回链，要么都不作为成功产物发布。
- 长期可审查 artifact 不受 Git diff 永久限制，但只有完成 profile 四项门禁后才能宣称正式支持。
- 未通过当前 Wave 的退出门禁时，不进入下一 Wave。
