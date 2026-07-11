# ADR-005：finalize 成对发布正式审计产物

## 状态

已采纳

## 日期

2026-07-10

## 上下文

`audit.json` 是机器真相源，`audit.html` 是一期默认人类入口。若 finalize 先把 JSON 发布到正式路径，再执行 render，render 或 HTML trace 失败会留下半套报告；宿主可能误把孤立文件当作成功。

## 决策

- prepare 在最终目录的同一父目录以 exclusive create 创建隐藏 sibling staging workspace，例如 `audit/.<slug>.change-audit-staging/`；最终目标 leaf 此时必须不存在。
- staging workspace 内的 `.run/` 保存审查交接材料，workspace 根目录生成候选 `audit.json` 和 `audit.html`。
- 候选 JSON 先通过 schema、引用、锚点、状态和计数校验；候选 HTML 再通过回链、XSS、完整性与 run/graph identity 校验。
- 两个候选都通过后，先按 keep 策略处理 `.run/`，再次检查最终目标 leaf 不存在，再用一次同文件系统目录 rename 把 staging workspace 提交为最终目录。
- 对 prepare 已接受的新目标，任一提交前硬失败均返回非零，最终目录保持不存在；staging 保留诊断，不得把旧报告宣称为本轮成功。
- 目标 leaf 已存在（包括悬空符号链接）或 rename 失败时停止，不主动覆盖，原目标不得作为本轮成功证据。
- 一期采用本地 single-writer：保留 `run_id`、staging/目标 leaf 检查和失败诊断，不承诺原生 no-replace、对抗性竞态或递归符号链接防御。POSIX 权限 `0700/0600` 为 best-effort，不是跨平台硬门禁。

## 理由

同一文件系统上的单次目录 rename 可以把完整 workspace 一次提交为最终目录，使本轮正式路径从不存在直接变成同时包含已校验的 JSON/HTML。结合 single-writer、提交前 leaf 检查和 `run_id` 一致性，宿主可以用完整产物对作为确定验收条件，而不需要一期实现平台专用并发原语。

## 影响

- `prepare_local_diff()` 必须创建 staging workspace，并返回包含 `run_id`、`final_dir` 和 `staging_dir` 的结构化 locator；CLI stdout 只输出 locator JSON，诊断写 stderr。`finalize_review()` 的成功返回值必须同时包含两个正式路径。
- Host Skill 必须验证两个文件及其对应关系，不能只检查其中一个。
- 测试需要覆盖 render、trace、`run_id` 不一致、已有目标/目标 leaf 符号链接和 rename 失败；POSIX 权限只做能力允许时的 best-effort 验证。
- 独立 `render --out` 仍可原子替换指定 HTML；显式输出路径即替换授权，失败时旧 HTML 原样保留且不修改输入 JSON。成对发布约束只适用于完整 review finalize 成功语义。
