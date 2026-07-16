# 任务清单：反馈裁定闭环

目录: `.sopify/plan/20260716_feedback_revision_loop/`

> 一个方案包、两批实施。两批全部通过才算交付；不进入模型复审、自动修复、新 artifact profile 或发布流程。

## Batch A：可信 revision 内核

- [ ] A1 冻结来源 audit、四类反馈、撤销和人机结论分层 fixture；验证 schema `0.3`，不足则停在 schema checkpoint。
- [ ] A2 实现严格 feedback parser 与来源绑定，覆盖字段、时间、重复/冲突、SHA-256、graph/run/finding/fingerprint 和旧 Alpha JSONL。
- [ ] A3 抽取内部 summary 纯函数，保持初次审计结果不变，并统一推导 revision verdict、risk score、计数与 `risk_delta`。
- [ ] A4 实现 revision 变换：保留模型原判断，应用当前裁定，嵌入规范化事件，追加 run 与 `supersedes_run`。
- [ ] A5 扩展语义校验，验证反馈来源、当前 run、人机结论、summary 和旧 schema `0.3` 报告兼容。
- [ ] A6 实现最小安全发布：默认更新同目录正式产物对；显式 `--out` 只写入不存在的新目录；失败不冒充成功。
- [ ] A7 增加 `revise SOURCE --feedback JSONL [--out DIR]` 与公开 API，冻结结构化 stdout 和错误契约。
- [ ] A8 覆盖畸形输入、恶意评论、过期来源、身份冲突、无变化、提交/渲染失败、显式副本和两轮撤销测试。

## Batch B：复制给 AI 的入口

- [ ] B1 更新 renderer：展示模型原判断、我的裁定、当前剩余问题和必要的 revision 详情。
- [ ] B2 更新 feedback JavaScript：主 CTA 复制带来源身份的原样 JSONL 机器块，JSONL 导出降为次要入口。
- [ ] B3 完成隐私与状态提示：默认无绝对路径、复制前计数、更新后刷新、localStorage 失败和旧 run 状态失效。
- [ ] B4 更新薄 Skill：当前工作区唯一定位、原样临时文件、默认同目录更新；只有用户明确要求另存时传 `--out`。
- [ ] B5 更新 README、数据模型、v0 scope、AI host 集成、doctor/兼容探针与 package/Skill 边界测试。
- [ ] B6 运行完整测试、build、clean-wheel 和 Skill smoke，完成两轮“裁定 → 复制 → 粘贴 → 更新 → 刷新”E2E，并验证显式另存副本。
- [ ] B7 使用 EvidentLoop 审计实现 diff，修复已确认问题；同步 project/blueprint，并在用户确认后 finalize，不自动发布版本。
