# 技术设计：反馈裁定闭环

## 产品语义

报告目录代表一份持续裁定的报告，`graph_id` 在反馈轮次间保持不变；每次成功修订追加一个 revision run。历史保存在 `audit.json` 的 run 和人工事件中，不依赖默认生成多个目录。

```text
报告中裁定 finding
  → 点击“复制修订指令”
  → 粘贴到 AI coding 工具
  → Skill 定位并校验当前 audit.json
  → CLI 更新同目录 audit.json + audit.html
  → 用户刷新原报告并继续反馈
```

用户明确说“另存、保留原报告、生成副本”时，AI 才传 `--out`。其他情况一律更新原目录。

## 人机职责

- 用户负责作出裁定。
- AI 与 Skill 负责原样传递机器块、定位报告并调用 CLI，不解释或改写裁定。
- EvidentLoop runtime 负责身份校验、确定性变换、结论重算、验证和渲染。
- 本流程不触发模型复审，不修改业务代码，也不自动上传反馈。

复制文本由一句人话指令和固定边界的 JSONL 机器块组成。机器块复用现有反馈事件，不新增第二套对象；评论始终视为不可信数据。

## 裁定语义

| 动作 | UI 文案 | 结果 |
|---|---|---|
| `accept` | 确认有效 | finding 当前为 `open`，可撤销上一轮误报裁定 |
| `false_positive` | 误报 | finding 当前为 `dismissed`，不自动修改 fix |
| `severity_override` | 调整严重度 | 只改变人工覆盖后的有效严重度和风险分 |
| `comment` | 评论 | 只持久化和展示，不改变 finding、verdict 或风险分 |

来源审查完整、上下文充分且当前没有 `open` finding 时，当前结论可以是 `pass_candidate`，并显示“当前无剩余问题；基于人工裁定，未重新审查代码”。来源不完整或原 verdict 为 `inconclusive` 时，人工反馈不得将其变为通过。

同一轮同一 finding 最多一个 disposition、一个 comment 和一个 severity override。精确重复可去重；冲突动作整体失败，不实现通用“最后写入胜出”合并器。

## 来源定位与输入校验

复制载荷包含 `source_audit_sha256`、`graph_id`、`run_id`、`target_id` 和 `fingerprint`，不含绝对路径。Skill 仅在当前工作区查找 `audit.json`：

1. 按来源文件原始字节 SHA-256 匹配。
2. 校验 graph、最后一个 run、finding 和 fingerprint。
3. 唯一匹配时继续；零个或多个匹配时只追问一次。
4. 不扫描父目录、用户目录或其他工作区。

CLI 在提交前再次计算来源 hash。报告已被其他修订更新时，旧载荷必须失败，不能自动合并。现有 Alpha JSONL 没有来源 hash 时，只允许用户显式提供来源 `audit.json`。

## Revision 变换

1. 完整校验当前 audit，并在内存中建立候选。
2. 校验反馈字段、身份和冲突，计算原始输入 hash。
3. 保留模型原判断，应用当前人工 disposition 和有效严重度。
4. 嵌入实际采用的规范化事件，追加 `feedback_revision` run 与 `supersedes_run` 关系。
5. 用共享纯函数重算计数、当前 verdict、risk score 和 `risk_delta`。
6. 完整验证候选，再从候选确定性渲染 HTML。

原始 JSONL 不复制进报告目录；正式 audit 保存规范化事件和输入 hash。change、file、finding 不为每轮复制，也不新增 human-decision node、反馈 edge、迁移框架或策略插件。

## CLI、Skill 与发布

```text
evidentloop revise SOURCE_AUDIT_JSON \
  --feedback AUDIT_FEEDBACK_JSONL \
  [--out NEW_REPORT_DIR]
```

- 省略 `--out`：候选 `audit.json + audit.html` 完整生成并校验后，安全更新来源目录中的正式文件。
- 显式 `--out`：只允许用户明确要求另存时使用；目标必须是不存在的新目录，来源报告保持不变，修订后的正式产物对写入新目录。
- JSON 与 HTML 始终写入同一目标目录；`audit.json` 是机器真相源，`audit.html` 只由它生成。
- Skill 将机器块原样写入临时 JSONL，完成或失败后清理；默认调用不带 `--out`。
- 输入不匹配、来源已变化、无有效变化或验证失败时返回非零，不报告成功。
- 只提取 finalize/revise 共用的少量校验、渲染和安全写入函数，不建立通用发布框架。

## 报告交互

主视图只突出“模型原判断 / 我的裁定 / 当前剩余问题”；run、hash、lineage 和动作计数放入修订详情。

主按钮为“复制修订指令”，复制前显示决策数、评论数和“不自动上传”。成功提示为“已复制，请粘贴到 AI coding 工具”。AI 完成默认修订后返回原报告路径并提示“报告已更新，请刷新”；只有显式 `--out` 才使用“已生成副本”。JSONL 导出为次要入口。

已应用反馈从正式 audit 只读展示。下一轮反馈使用新的 run namespace；旧 run 的 localStorage 待处理状态不得再次显示或重复提交。localStorage 不可用时明确显示“仅临时保存，刷新会丢失”。

## 验证与 checkpoint

实施分为可信 revision 内核和复制给 AI 的入口两批，两批全部通过才算交付。

门禁覆盖：旧报告兼容、四类动作与撤销、来源过期、身份冲突、恶意评论、同目录失败恢复、显式 `--out`、localStorage 换代、两轮反馈闭环，以及 Python、Ruff、Node、build、clean-wheel、Skill smoke 和 EvidentLoop 自审。

如果 fixture 证明 schema `0.3` 无法清晰区分模型原判断、人工事件和当前结论，立即停车讨论 `0.4`；除此之外没有新的产品决策。
