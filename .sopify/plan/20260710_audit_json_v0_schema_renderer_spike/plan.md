# Plan: change-audit v0 code-diff 一期闭环

Plan Snapshot:
- Goal: 将 CrossReview 合并为 artifact-general 内部审查子系统，并先交付由 AI host Skill 编排的 Git diff 审计 profile、HTML 报告与用户决策闭环。
- Status: D1-D100 已确认；方案文档、长期蓝图与设计图已收口，尚未迁移实现代码。
- Next: 用户审计方案；收到明确开发指令后才从 Wave 0A 开始。

## Context / Why

`change-audit` 已有 `audit.json` 数据模型、一份 `0.2-alpha` 主样张和手工 HTML 参考件，但没有可执行实现。CrossReview 已有可复用的 ReviewPack、ReviewResult、prompt、normalizer、adjudicator、测试和 eval harness，但没有真实用户。

两者本来就是一条链路的上下游。继续分成两个 alpha 包会让用户安装两次、维护两套 Skill，并自行拼接审查结果与报告。合并后以 `change-audit` 作为唯一产品名，CrossReview 作为内部 `change_audit.review` 能力名。

CrossReview 的长期对象本来就包括 plan、design、analysis、review-result 等可审查 artifact；当前实现和 eval 仍硬锁 `code_diff`。因此项目蓝图保留 artifact-general 方向，本方案只实现第一个正式 profile，不把一期范围误写成永久产品边界。

## Scope

- **Wave 0A — Baseline**：冻结 CrossReview 可验证基线，不改行为。
- **Wave 0B — Migration**：建立最小 import 壳并等价迁入 `change_audit.review`。
- **Wave 1 — Schema + Renderer**：完成唯一 JSON Schema、语义校验、HTML renderer 和 `render` 命令。
- **Wave 2 — Host Review Integration**：完成 `prepare`、宿主 LLM 审查、`finalize`、adapter、锚点与状态校验。
- **Wave 3 — Human Decision**：完成 localStorage 与 JSONL 导出。
- **Wave 4 — AI Host Discovery**：完成自包含 Skill、Codex dogfood 和 Qoder 验证。

Schema 在 Wave 2 的语义 bug、干净 diff、partial review 三类 dogfood 全部通过后，才把 code-diff audit profile 从 `0.2-alpha` 冻结为 `0.2`；该版本不承诺已经覆盖所有 artifact 类型。

## Approach

1. **一个产品、一个包、一个 Skill。** CrossReview 代码迁入 `change_audit.review`，不作为外部运行时依赖。
2. **用户动作与 Python 命令分离。** 用户说“用 change-audit 审计本地改动”；Skill 编排流程。Python 只公开 `prepare`、`finalize`、`render`。
3. **宿主 LLM 产生语义 finding。** 默认链路不调用模型 SDK、不读取 API key；provider-backed reviewer 只作为可选兼容能力保留。
4. **隐藏 staging workspace 跨进程交接。** `prepare` 在最终目录同一父目录创建隐藏 sibling workspace，并在其 `.run/` 写入审计骨架、可信 hunk index、ReviewPack 和 prompt；成功时向 Skill 返回包含 `run_id`、最终目录和 staging 目录的机器 locator。Skill 只写 raw analysis；`finalize` 在该 workspace 完成 ingest、adapter、校验和渲染。
5. **LLM 不生成机械字段。** Python 生成 node ID、edge、fingerprint、完整 hunk、summary、review_status、verdict 和风险评分。
6. **结构与语义分层。** JSON Schema 2020-12 是 `audit.json` 唯一结构契约；Python 只补跨对象引用、hunk 锚点与 HTML 回链校验。
7. **渲染器纯消费。** `render` 只读取完整 `audit.json`，不读取 Git、ReviewPack、raw analysis 或宿主状态。
8. **审查内核可泛化，正式审计按 profile 放行。** 非 diff artifact 可以先停在内部 ReviewResult；只有具备 adapter、可信 anchor、eval baseline 和 renderer profile 后，才成为公开的 `audit.json` / `audit.html` 能力。
9. **正式产物成对发布。** finalize 在隐藏 staging workspace 中生成并完成 JSON、HTML、identity 和回链校验，随后在本地 single-writer 前提下，用一次同文件系统目录 rename 提交最终目录。prepare 与提交前都检查目标 leaf，已有目标或 rename 失败时停止且不主动覆盖；提交前硬失败保持正式目录不存在。

## User-facing Contract

用户不需要记命令。典型触发：

```text
用户：帮我用 change-audit 审计最近的本地改动
  -> AI host 匹配 change-audit Skill
  -> 缺包时说明来源并请求安装授权
  -> prepare 生成骨架和隐藏审查上下文
  -> 宿主 LLM 在隔离上下文中审查
  -> finalize 在临时区生成并校验 audit.json + audit.html
  -> 两个正式产物成对发布
  -> Skill 返回摘要和报告路径
```

默认目录：

```text
audit/YYYYMMDD_<slug>/
  audit.json
  audit.html
  .run/                    # 仅 --keep-review-artifacts 后存在
```

运行期内部 workspace：

```text
audit/.YYYYMMDD_<slug>.change-audit-staging/
  .run/
    audit-skeleton.json
    hunk-index.json
    review-pack.json
    prompt.md
    raw-analysis.md
```

用户在 HTML 中导出反馈后，会得到 `audit-feedback.jsonl`；浏览器不保证把下载文件写回原审计目录。

## State and Finding Semantics

- `summary.review_status`：`not_reviewed | complete | partial | failed`，描述审查是否执行完整。
- `summary.verdict`：`pass_candidate | concerns | needs_human_triage | inconclusive`，只描述审查结论。
- ReviewResult 的意图覆盖、文件覆盖和 pack 完整性属于诊断信息，放入 `summary.extensions.change_audit.review_diagnostics`，不新增含糊的核心 coverage 字段。
- 完整审查且无未解决 finding：`complete + pass_candidate + open_finding_count = 0`；可保留 fixed 历史 finding。
- 未执行或失败：分别使用 `not_reviewed` / `failed`，verdict 为 `inconclusive`，risk score 为 `null`。
- 部分审查：`partial + inconclusive + risk_score = null`；已产生的 finding 可以展示，但不能包装成完整结论。
- 无法精确锚定的 bug 降级为 risk，保留原 category 和降级原因。
- 只有当前未解决且通过分类锚点策略的 finding 进入临时 0–100 风险评分；因锚点降级而排除的未解决 finding 计入 `unscored_finding_count`。
- 如果只有未锚定风险：`risk_score = null`、`verdict = needs_human_triage`。
- 评分权重在 Wave 2 dogfood 后冻结；当前方案不提前固化未经验证的公式。

## Security Boundaries

- diff、源码、注释和 raw analysis 都是不可信数据，不得覆盖 Skill 或宿主指令。
- Skill 不执行源码或审查文本建议的命令；prompt 使用明确数据边界包装 diff。
- prepare 以 exclusive create 建立 staging leaf，并在 prepare 与提交前检查最终目标 leaf；任何已有 entry（包括悬空符号链接）都拒绝。POSIX 上尽力将目录设为 `0700`、中间文件设为 `0600`，但权限模式不是跨平台硬门禁；一期不承诺递归符号链接防御或对抗性并发安全。
- 只有 JSON/HTML 全部通过后才执行一次同文件系统目录 rename。已有目标或 rename 失败时停止并保留 staging 诊断，禁止静默覆盖或把旧产物当作本轮成功。
- Jinja2 开启 autoescape；HTML 不引入 CDN、远程脚本或外部资源。

## Key Decisions

- D1-D37：Schema + renderer、模块入口、包资源、完整页面和宿主发现边界。
- D38-D59：宿主 LLM 为主要 finding 生产者；内部传输、finalize、状态、锚点与 prompt injection 边界。
- D60-D90：CrossReview 合并、迁移基线、命名、eval-data 隔离、CI 与发布边界。
- D91：`review` 是 Skill 用户动作，不是 Python 命令。
- D92：`.run/` 作为隐藏跨进程传输目录。
- D93：review status 与 verdict 分离，不新增 `no_findings` verdict。
- D94：bug 必须精确锚定；其他分类允许 file-only；adapter 负责 category 和 risk 映射。
- D95：新增独立 `summary.review_status`。
- D96：无法锚定的语义 bug 降级为 risk，不静默丢弃。
- D97：降级 finding 不进入数字评分；只有降级风险时不输出误导性的 0 分。
- D98：一期只承诺 Git diff 正式审计；长期 blueprint 描述 artifact-general review 内核，非 diff profile 通过 adapter、anchor、eval、renderer 四项门禁后再公开。
- D99：finalize 在同父目录隐藏 staging workspace 生成并验证 JSON/HTML，再用一次同文件系统目录 rename 成对发布；新目标提交前硬失败保持不存在，已有目标不得冒充本轮成功。
- D100：一期采用本地 single-writer 模型；保留 `run_id`、leaf 检查、失败诊断和成对发布，POSIX 权限为 best-effort；原生 no-replace、对抗性竞态与递归符号链接防御延后。

决策与文档收口回执见 `receipts/verify_001.json` 至 `receipts/verify_010.json`。

## Constraints / Not-in-scope

- 本方案只收口文档，不迁移代码、不修改 CrossReview 仓库、不发布、不打 tag。
- 一期不做 folder diff、无 diff artifact 正式审计、远程 PR URL、自动改代码、反馈消费、SVG renderer 或 Markdown renderer；这些是后续 profile 候选，不是永久非目标。
- 方案中的 SVG/PNG 是设计文档资产，不是产品 SVG renderer。
- 一期不启用 publish workflow，不发布 PyPI，不 yank 旧包。
- CrossReview 仓库仅在合并 dogfood 成功且再次获得授权后归档。

## Status

- [x] D1-D100 已确认并写入回执。
- [x] 方案、长期知识库和设计图已按目标架构收口。
- [ ] 实现代码尚未开始。

## Next

等待用户审计。本轮不进入开发实施。
