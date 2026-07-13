# EvidentLoop 外部 Alpha 试跑清单

本轮只验证 macOS arm64、Python 3.11、Codex CLI `0.144.1` 的首次安装与一句话审计。维护者提供精确 commit 对应的本地 wheel、源码目录和 SHA-256；不创建 tag，不使用 PyPI、移动分支或远程 Skill 安装。

## 试用者执行

1. 记录环境版本，不修改维护者提供的文件：

```bash
sw_vers
uname -m
python3.11 --version
uv --version
codex --version
node --version
npx skills@1.5.16 --version
```

2. 核对维护者给出的 commit 与 wheel SHA-256，再安装 CLI 和 Skill：

```bash
git -C <SOURCE_DIR> rev-parse HEAD
shasum -a 256 <WHEEL_PATH>
uv tool install --force <WHEEL_PATH>
npx skills@1.5.16 add <SOURCE_DIR> \
  --skill evidentloop --agent codex -g --copy -y
evidentloop doctor --json
```

3. 在不含敏感代码的本地 Git 仓库准备一个非空 staged diff，然后只发一句请求：

```text
请使用 EvidentLoop 审计 staged changes。
```

4. 只有以下条件全部满足才记为走通：

- package 为 `0.1.0a0`、schema 为 `0.3`、prompt 为 `v0.4`；
- orchestrator 与 reviewer 的 `thread.started` ID 非空且不同；
- reviewer JSONL 恰有一个最终 `agent_message` 和 `turn.completed`，没有工具、命令、文件修改或协作事件；
- reviewer 的空工作目录没有产生文件；
- 临时 HOME、`CODEX_HOME` 和工作目录已在 `finalize` 前删除；
- `audit.json` 与 `audit.html` 位于同一正式目录，JSON 为 schema `0.3`、`review_status=complete`，状态与计数完整；
- 成功运行后 `.run/` 未保留。若任一隔离信号不可见或不满足，应停在 `finalize` 前并记录阻塞。

## 脱敏反馈模板

请只返回以下信息，不发送仓库路径、源码、diff、prompt、raw analysis、报告文件、凭据或代理配置。

```text
候选 commit：
wheel SHA-256：
环境：macOS / arm64 / Python / uv / Codex / skills CLI
首次安装耗时：
一句话到报告耗时：
结果：通过 / 阻塞 / 失败
review_status / verdict：
隔离证据：thread ID 是否不同；禁止事件数；空目录是否不变
阻塞位置：安装 / discovery / compatibility / prepare / reviewer / finalize / report
最容易误解的一步：
其他脱敏反馈：
```

维护者不代为操作。功能建议只记录为后续任务；本轮只修安装阻塞、错误行为和文档误导。
