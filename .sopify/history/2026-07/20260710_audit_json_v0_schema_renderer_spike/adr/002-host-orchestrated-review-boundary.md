# ADR-002：宿主编排 review，Python 保持三命令边界

## 状态

已采纳

## 日期

2026-07-10

## 上下文

一期需要使用 AI host 已有的 LLM 能力发现语义问题，又不希望 Python 包绑定模型 SDK、API key 或单一供应商。一个普通 Python 命令也无法反向要求 Codex、Qoder 等宿主开启新的隔离审查上下文。

## 决策

- 用户动作称为 `review`，由 Agent Skill 发现和编排。
- Python 只提供 `prepare`、`finalize`、`render` 三个模块命令。
- `prepare` 与 `finalize` 通过同父目录隐藏 staging workspace 中的 `.run/` 跨进程交接。
- Skill 负责宿主 LLM 调用、安装授权、错误处理和正式产物展示。
- Python 包不包含模型 SDK、provider/API key 配置或 standalone reviewer；宿主 LLM 是唯一模型执行面。
- 后续增加 console-script 时，不移除 `python -m change_audit` 模块入口。

## 理由

该边界让产品复用宿主已有模型能力，同时保持核心包可测试、可离线渲染、无供应商锁定。Skill 拥有编排知识，但不复制 schema、renderer 或 Python 业务逻辑。

## 替代方案

- `python -m change_audit review` 一键调用宿主 LLM：拒绝，因为普通进程没有宿主回调协议。
- Python 内置模型 SDK：拒绝，因为会引入 API key、供应商和额外依赖。
- 让 LLM 直接编辑 `audit.json`：拒绝，因为机械字段和引用容易漂移。

## 影响

- Skill 不再是 30 行命令便条，而是一期正式的宿主编排层。
- `.run/` 必须有清理、失败诊断和 prompt injection 测试；POSIX 权限尽力收紧为目录 `0700`、文件 `0600`，但不作为跨平台硬门禁。
- 用户默认只看到 `audit.json` 与 `audit.html`。
- 完整 review 的正式产物按 ADR-005 在 staging 中验证后成对提交。
- Wave 5 删除迁移期为等价性保留的 standalone CLI/config/reviewer/formatter 与 provider verify 路径；不以 change-audit 新命名复制这些未使用能力。
