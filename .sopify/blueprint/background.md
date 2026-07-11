# change-audit 背景

## 产品问题

AI coding 会生成代码变更，也会生成 plan、design、analysis、review-result、final answer 和 agent trace 等产物。审查过程通常散落在聊天、终端和临时 Markdown 中，用户难以确认目标是否可靠、结论依据是什么，也难以把自己的接受、误报或严重度调整带到下一轮。

用户真正需要的是一条可审计链路：把有明确边界的审查目标交给隔离上下文，经 AI 语义审查得到可回链 findings，再由成熟的 artifact profile 形成机器记录、人类报告和可导出的用户决策。

## 产品定位

`change-audit` 是面向 AI 变更与可审查产物的可回链审计工具。

- `change_audit.review` 是 artifact-general 隔离审查内核；AI host 的 LLM 负责目标相关的语义判断。
- `change_audit.audit` 与 renderer 是 profile-specific 正式产品层；只有具备 adapter、可信 anchor、eval baseline 和 renderer profile 的类型，才承诺完整审计产物。
- Python 不内置 LLM SDK 或 provider/API key 配置；它负责构造可信上下文、约束审查输出、生成机械字段、校验引用并确定性呈现。
- `change_audit.review` 直接承载 ReviewPack、prompt、ingest、normalizer 与 adjudicator；迁移来源不形成第二个产品或第二套运行链路。
- 用户只需要安装一个包、发现一个 Skill，并看到最终审计产物。

## 用户入口

一期以 AI host 为主要入口，首个正式 profile 是本地 Git diff。用户在自己的仓库中说“用 change-audit 审计本地改动”，Skill 负责选择 diff 范围、编排宿主 LLM、运行 Python 阶段并展示报告路径。用户项目无需复制集成说明或中间契约。

模块命令仍保留为稳定、可调试的底层入口，但 `review` 是 Skill 表达的用户动作，不是 Python 单命令。

## 目标用户

- 在 Codex、Qoder 等 AI coding 宿主中审计本地改动的开发者。
- 需要查看变更摘要、问题证据和修复建议的维护者。
- 需要结构化审计 checkpoint 的自动化工作流。
- 后续需要消费 `audit.json` 或用户反馈的报告与评估工具。

## 核心产物

- `audit.json`：成熟 artifact profile 的最终机器真相源，包含审查目标、状态、findings、evidence 和 fixes。
- `audit.html`：具备 renderer profile 时的默认人类审计界面；共同外壳保持一致，定位内容按 hunk、section、claim 或其他可信 anchor 呈现。
- `audit-feedback.jsonl`：用户显式导出的决策记录；一期只采集，不自动消费。

实验性非 diff 类型可以先停在内部 ReviewResult 或宿主摘要，不因此宣称完整 audit 支持。正式产物在同父目录隐藏 staging 中完成校验后成对提交；成功时中间物默认清理。

## 非目标

- 一期不提供 provider SDK，也不要求用户配置模型 API key。
- 不由 Python 的文本规则替代 LLM 语义审查；确定性规则未来只能作为增强。
- 不自动修改代码，不把审计结论当作发布阻断策略。
- 一期不做 folder diff、无 diff artifact 正式审计或远程 PR URL；这些是后续 profile 候选，不是永久排除。
- 一期不做 hosted dashboard、反馈消费、SVG 产品 renderer 或 Markdown renderer。
