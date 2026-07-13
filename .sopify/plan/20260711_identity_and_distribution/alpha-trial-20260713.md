# Wave 4.3 外部 Alpha 试跑证据

日期：2026-07-13

状态：首次试跑的核心审计链路通过，但候选 commit 与 wheel provenance 不一致；4.3 未关闭，最小复跑候选已准备。

## 脱敏反馈

- 候选 commit：`e05db143e4f3ee540b7d788f40b99f316369c991`
- wheel SHA-256：`3c108b4081393e8b30e8acd6e4dd5da855e6164942c21e63548d1939e411370a`
- 环境：macOS `15.6.1`（`24G90`）/ arm64 / Python `3.11.15` / uv `0.11.28` / Codex CLI `0.144.3` / Node.js `20.20.2` / skills CLI `1.5.16`
- 首次安装耗时：未使用独立计时器；CLI 与 Skill 的落盘完成时间相差约 13 秒，该值不代表完整安装耗时。
- 一句话到报告耗时：未记录端到端起始时间；隔离 reviewer JSONL 完成到正式报告落盘约 21 秒。
- 结果：核心链路通过；Codex CLI `0.144.3` 的隔离能力已接受，4.3 只因候选产物 provenance 与精确耗时缺口保持未关闭。
- `review_status / verdict`：`complete / inconclusive`
- 报告计数：风险分未评分，finding `0`，open finding `0`，unscored finding `0`
- 隔离证据：orchestrator 与 reviewer thread ID 非空且不同；禁止事件 `0`；最终 `agent_message` `1`；`turn.completed` `1`；reviewer 空工作目录未变化；临时 HOME、`CODEX_HOME` 与工作目录在 `finalize` 前删除。
- 正式产物：`audit.json` 与 `audit.html` 同目录；schema `0.3`；run ID 与 locator 一致；最终目录不含 `.run/`，隐藏 staging 已删除。
- 阻塞位置：产品审计链路无阻塞。当前受限宿主默认 npm cache 不可写，复查 skills CLI 时改用临时 cache 后成功；该问题未影响已安装 Skill 的审计。
- 最容易误解的一步：隔离验证示例把检查条件写成注释但没有执行断言；同时 Codex JSONL 的最终文本位于 `item.text`，不是顶层 `text`，原提取命令会失败。
- 其他脱敏反馈：`codex 0.144.3` 在关闭全部工具、插件、MCP、浏览器、计算机使用、图像生成与多智能体后可完成独立 reviewer；运行中出现模型列表刷新超时日志，但 reviewer 和正式报告仍成功完成。

## 4.4 输入

1. 将隔离事件检查实现为失败即停止的脚本，不再只保留注释。
2. 按 `item.completed.item.type == "agent_message"` 提取 `item.text`，并强制校验只有一个最终消息和一个 `turn.completed`。
3. 在试跑脚本中自动记录首次安装及一句话到正式报告的端到端耗时。
4. Codex CLI `0.144.3` 已纳入支持范围；`0.144.1` 只保留为历史实测证据。Skill 和集成文档改为 capability gate，不精确要求某个 Codex CLI 版本，也不把两个离散实测版本包装成连续版本区间。
5. 区分受限宿主的 npm cache 权限问题与产品安装问题；需要时允许为版本探针指定临时 cache。

## 最小复跑候选

- source commit：`74c7d16887a69de5c5f1f6e8ada6ac3ff9427088`
- source archive：`source-74c7d168.tar`
- source archive SHA-256：`ad3cc339da7d15281143518513790d84e13910dc43caa7695447a2c9222116dc`
- wheel：`evidentloop-0.1.0a0-py3-none-any.whl`
- wheel SHA-256：`a12e26fb311513901fb8c56dbc4a12ce6f02c977d37a41248baff1fe75112c18`
- 本地预检：archive commit ID、Skill、prompt、wheel 完整性、隔离安装、兼容探针、doctor、module CLI 与 demo 均通过。
- 外部状态：未执行；4.3 保持待办。

## 隐私边界

本记录不包含试用仓库路径、源码、diff、prompt、raw analysis、报告文件、凭据、代理配置或完整 thread ID。
