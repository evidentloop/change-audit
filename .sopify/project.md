# change-audit 项目约定

## 命名契约

- 产品、GitHub 仓库、未来 distribution 和 CLI：`change-audit`
- Python import package、源码目录：`change_audit`
- 内部隔离审查子系统：`change_audit.review`
- 内部数据模型：Audit Graph / `AuditGraph`
- 最终机器真相源：`audit.json`
- 默认人类界面：`audit.html`
- 用户反馈：`audit-feedback.jsonl`

中文是主要产品文档与一期正式 HTML 报告语言。英文只保留在项目名、包元数据、命令、字段名、协议标签、代码和通用技术术语中；reviewer 输出的 finding、observation 与 overall 语义正文默认使用简体中文。

## 技术约定

- Python 版本：`>=3.10`。
- 结构契约：JSON Schema 2020-12 是唯一 schema 真相源；Python 只实现校验和语义约束，不建立第二套模型定义。
- 模板：Jinja2；CSS 和 JS 作为 package resources 维护并内联到自包含 HTML。
- 入口：一期保留 `python -m change_audit prepare/finalize/render`；正式 console-script 后续只做别名。
- 宿主边界：AI host LLM 是唯一模型执行面；Python 包不集成模型 SDK，也不读取 provider/API key 配置。
- Prompt provenance：prepare 冻结 product prompt source/version/hash，finalize 校验 prompt 文件及当前契约后再 ingest；跨进程版本漂移或 prompt 篡改不得冒充原版本完成。
- Reviewer payload：Git 文本 diff 不携带 `GIT binary patch`；binary 文件保留路径/change_type 元数据，视觉内容明确不在一期文本审查范围。
- 集成形态：一个 Python 包承载业务，一个用户级/宿主级 Skill 负责发现和编排，用户项目不复制集成文档。
- 一期默认输入：本地 Git diff；长期输入按 artifact profile 管理。
- 默认产物：`audit.json` 和 `audit.html`；`audit-feedback.jsonl` 由用户显式导出。
- 中间产物：prepare 在最终目录同父目录创建隐藏 staging workspace，`.run/` 位于其中；成功时目录整体提交，失败时 staging 留作诊断。
- 并发边界：一期按本地单写者、非对抗并发设计；提交前复查最终目标 leaf 不存在，再执行同文件系统目录 rename。目标已存在或 rename 失败时停止，不主动删除或覆盖目标。
- 隐私权限：POSIX 上尽力将 staging / `.run/` 设为 0700、中间文件设为 0600；精确 mode 不是跨平台退出门禁。

## 一期 code-diff 职责

- `prepare` 选择尚不存在的最终目录，在同父目录 staging 中生成可信 diff 上下文、hunk index 和隐藏审计骨架，并返回 `run_id`、final/staging 路径的结构化 locator。
- Skill 在隔离上下文中调用宿主 LLM，并写入原始审查输出。
- `finalize` ingest 审查结果、生成机械字段、仅在完整性门禁通过时复制转义后的 Overall Assessment 作为语义摘要、执行锚点/引用校验，在 staging 中生成并验证 JSON/HTML；提交前复查目标 leaf 不存在，再用同文件系统目录 rename 成对提交正式产物。目标已存在或 rename 失败时保留 staging 诊断并停止。
- `render` 只消费完整 `audit.json`，不读取 Git 或宿主状态；显式输出路径只授权原子替换该 HTML。
- code-diff 的 `audit.json` 保留完整可信 hunk；HTML finding 只显示命中附近的有界可信片段、真实双行号和明确省略标记。精确 diff range 属于 source 元数据，不作为报告主标题。
- HTML 对有界 hunk 片段优先自动换行并完整展示，横向滚动仅作极端内容兜底；没有 summary claim 时使用顶对齐紧凑提示，不占用与文件列表等高的空白区域。
- ReviewResult 没有独立修复建议时，adapter 不生成 fix；finding 的原因不能冒充修复动作。所有未计分 finding 都必须在 HTML 明示未精确定位。
- 完整 reviewer 输出仍可能因 pack completeness 不足而结论不充分；正式图保留 `complete + inconclusive + risk_score=null`，不得把零 finding 自动包装成候选通过。

## 状态约定

`review_status` 只描述审查过程，`verdict` 只描述结论。`partial` 和 `failed` 均为 `inconclusive` 且不输出数字风险分。覆盖率和解析诊断写入 `summary.extensions.change_audit.review_diagnostics`，不新增核心 `review_coverage`。

数字风险分只计算完成审查且锚点有效的 findings。无法锚定的语义 bug 降级为未计分 risk，保留原分类和原因；只有此类风险时 `risk_score = null` 并要求人工分诊。

## 当前边界

一期主链路（JSON Schema、语义校验、HTML renderer、Git diff adapter、`prepare -> host LLM -> finalize`）已落地。`audit.json 0.2` 冻结时只代表 code-diff audit profile；第二种真实 artifact profile 通过独立 ADR 和 schema 版本扩展，不在一期 schema 中预塞未验证字段。一期不实现原生 race-proof no-replace、平台专用锁或递归 symlink 防御。

实现状态与验证证据见归档方案回执（`.sopify/history/2026-07/20260710_audit_json_v0_schema_renderer_spike/receipts/`）。
