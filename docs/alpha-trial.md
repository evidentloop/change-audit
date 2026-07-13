# EvidentLoop 外部 Alpha 最小复跑清单

本轮在 macOS arm64、Python 3.11、Codex CLI `0.144.3` 上只复跑首次安装与一句话审计的产物 provenance 和耗时。`0.144.3` 的隔离链路已经验证并纳入支持范围；Codex CLI 版本只记录实测环境，不作为精确门禁，真正门禁是可观察的隔离信号和失败即停止的断言。

复跑候选固定为：

- source commit：`74c7d16887a69de5c5f1f6e8ada6ac3ff9427088`
- source archive：`source-74c7d168.tar`
- source archive SHA-256：`ad3cc339da7d15281143518513790d84e13910dc43caa7695447a2c9222116dc`
- wheel：`evidentloop-0.1.0a0-py3-none-any.whl`
- wheel SHA-256：`a12e26fb311513901fb8c56dbc4a12ce6f02c977d37a41248baff1fe75112c18`

source archive 由上述 commit 直接执行 `git archive` 生成，wheel 从该 archive 的原样解包目录构建。不创建 tag，不使用 PyPI、移动分支或远程 Skill 安装。

候选 Skill 的 Codex recipe 标题保留首次实测版本 `0.144.1`，正文门禁并未比较 CLI 版本；本轮在 `0.144.3` 上执行相同 capability probe。标题收口属于 4.4，不改变本次候选产物。

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

2. 核对 source archive 的 commit 与两个 SHA-256，再从该 archive 安装 CLI 和 Skill：

```bash
SOURCE_TAR="/path/to/source-74c7d168.tar"
WHEEL_PATH="/path/to/evidentloop-0.1.0a0-py3-none-any.whl"
SOURCE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/evidentloop-alpha.XXXXXX")"

test "$(git get-tar-commit-id < "$SOURCE_TAR")" = "74c7d16887a69de5c5f1f6e8ada6ac3ff9427088"
test "$(shasum -a 256 "$SOURCE_TAR" | awk '{print $1}')" = "ad3cc339da7d15281143518513790d84e13910dc43caa7695447a2c9222116dc"
test "$(shasum -a 256 "$WHEEL_PATH" | awk '{print $1}')" = "a12e26fb311513901fb8c56dbc4a12ce6f02c977d37a41248baff1fe75112c18"
tar -xf "$SOURCE_TAR" -C "$SOURCE_DIR"

INSTALL_STARTED_AT="$(date +%s)"
uv tool install --force "$WHEEL_PATH"
npm_config_cache="$(mktemp -d "${TMPDIR:-/tmp}/evidentloop-npm.XXXXXX")" \
  npx skills@1.5.16 add "$SOURCE_DIR" \
  --skill evidentloop --agent codex -g --copy -y
evidentloop doctor --json
INSTALL_SECONDS="$(( $(date +%s) - INSTALL_STARTED_AT ))"
printf 'install_seconds=%s\n' "$INSTALL_SECONDS"
```

3. 在不含敏感代码的本地 Git 仓库准备一个非空 staged diff。发送请求前记录 `date +%s`，正式报告生成后再次记录并计算耗时，然后只发一句请求：

```text
请使用 EvidentLoop 审计 staged changes。
```

4. 只有以下条件全部满足才记为走通。thread、事件和目录检查必须实际执行断言并在不满足时返回失败；注释、目测或仅打印计数不能替代断言：

- package 为 `0.1.0a0`、schema 为 `0.3`、prompt 为 `v0.4`；
- orchestrator 与 reviewer 的 `thread.started` ID 非空且不同；
- reviewer JSONL 恰有一个最终 `item.completed.item.type == "agent_message"` 和 `turn.completed`，最终文本从 `item.text` 提取，没有工具、命令、文件修改或协作事件；
- reviewer 的空工作目录没有产生文件；
- 临时 HOME、`CODEX_HOME` 和工作目录已在 `finalize` 前删除；
- `audit.json` 与 `audit.html` 位于同一正式目录，JSON 为 schema `0.3`、`review_status=complete`，状态与计数完整；
- 成功运行后 `.run/` 未保留。若任一隔离信号不可见或不满足，应停在 `finalize` 前并记录阻塞。

## 脱敏反馈模板

请只返回以下信息，不发送仓库路径、源码、diff、prompt、raw analysis、报告文件、凭据或代理配置。

```text
候选 commit：
source archive SHA-256：
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
