# 任务清单：EvidentLoop 身份迁移、零摩擦分发与发布证据收口

归档目录：`.sopify/history/2026-07/20260711_identity_and_distribution/`

> Wave 0 至 Wave 5 已完成；`e6f3381` 保留为 Wave 4 验证候选，Wave 5 dogfood 绑定 `81e7b1f`。repository 已改名为 `evidentloop/evidentloop`；用户已确认 Wave 6 checkpoint，Wave 7 只按准确 commit、tag、evidence 与公开验证顺序执行。

## Wave 0：身份与注册风险门禁（最高优先级）

- [x] 0.1 按 USPTO 官方策略检索 `EVIDENTLOOP`、`EVIDENT LOOP`、相近读音/拼写及相关软件/SaaS 服务；精确候选为 0，近似结果未发现直接冲突。
- [x] 0.2 WIPO Global Brand Database 未取得可验证结果；用户明确接受该缺口并要求停止继续审计名称风险，未伪造“未发现”结论。
- [x] 0.3 已核验 PyPI、GitHub、`.com` / `.dev` RDAP 与相邻品牌状态；`Evidence Loop` 面向医疗研究证据，`Evidently` 面向 AI evaluation / monitoring，均记录为相邻品牌。
- [x] 0.4 冻结 `EvidentLoop` 目标矩阵、schema `0.3` canonical URI、prompt `v0.5`、package `0.1.0a0`、精确 allowlist、历史证据策略与外部动作边界，详见 ADR-004 与 `design.md`。
- [x] 0.5 身份 checkpoint：用户明确采用 `EvidentLoop` 并停止继续审计名称风险；ADR-004 已采纳，ADR-002 已废弃，允许进入 Wave 1。本决定不授权外部改名、注册或发布。

## Wave 1：本地身份 clean break

- [x] 1.1 已生成旧身份清单并冻结精确 allowlist：历史 `.sopify`、历史报告及其 provenance、旧架构/时序快照，以及 Wave 7 前仍真实存在的 remote URL。
- [x] 1.2 distribution、source package、Python import、module entry 与版本读取已统一为 `evidentloop`，未保留 `change_audit` import alias。
- [x] 1.3 public audit schema 已升级到 `0.3`，canonical `$id`、title、`extensions.evidentloop` 与 validator 已同步；旧报告只作为历史证据保留。
- [x] 1.4 reviewer prompt 保留 `source="product"`，标题、version `v0.4`、hash、run marker 及解析逻辑已迁移并由 provenance 测试冻结。
- [x] 1.5 staging suffix、CLI/error prefix、HTML title/kicker、JS global 与 feedback localStorage prefix 已统一；未新增 locator 或 feedback event 品牌字段，领域契约未改名。
- [x] 1.6 活动测试、fixture、prompt-lab 与生成入口已迁移；三个 example 的 6 个历史报告 hash 不变。
- [x] 1.7 活动 Skill 已迁到唯一目录 `skills/evidentloop/`，frontmatter、metadata、触发词与命令已同步，旧 Skill 已删除。
- [x] 1.8 活动 README、核心文档、封面与架构 SVG/PNG 已同步；旧封面删除，历史架构/时序快照字节不变，新图只陈述当前 Git diff 能力。
- [x] 1.9 Python `317 passed`、Ruff、JS、clean wheel、module CLI、schema/prompt probe、旧身份扫描、历史 hash、Markdown 链接、SVG 结构与浏览器视觉验证均通过。最终 clean wheel 只包含 `evidentloop/` 与 dist-info，SHA-256 为 `d7e7d39a6d1eec4f085577d9f0a0f3f6ad5ed7fe5779d97f46c53f8d763ae9b4`。

## Wave 2：Python CLI 产品化

- [x] 2.1 `pyproject.toml` 已增加 `evidentloop` console script 与 Homepage / Repository / Issues URLs；clean wheel 中 console script 与 `python -m evidentloop` help 完全一致。
- [x] 2.2 已实现 `doctor [--json]`，检查版本、schema、prompt、package resources 和 Git；`npx` 缺失只产生非阻断 warning，并输出待 Wave 3 隔离验证的标准 Skill 安装候选、手工 fallback 与下一句请求，不扫描宿主私有目录。
- [x] 2.3 已实现离线 `demo [--out DIR]`：wheel 内独立合成 fixture 在临时 Git 仓库中复用 `prepare -> frozen replay -> finalize`；终端、`audit.json` extension 与 HTML 均明确标记未执行实时 AI 审查。
- [x] 2.4 Python `326 passed`、Ruff、JS 语法/行为、CI YAML、旧身份 allowlist 自动门禁、clean wheel build/install、console/module entry、doctor、demo 与 package resources 均通过。
- [x] 2.5 已审计现有反馈能力并确认首个公开 Alpha 延后反馈消费与重新生成；保留浏览器交互、localStorage 与 `audit-feedback.jsonl` 导出，README 明确边界，未来 Pages 继承同一声明，蓝图继续保留完整闭环长期任务。

## Wave 3：Skill 安装与用户入口

- [x] 3.1 已按宿主能力定义集成边界并建立实测矩阵；Skill 在 `prepare` 前精确要求 package `0.1.0a0`、schema `0.3`、prompt `v0.5`，任一不符即停止。未增加旧版本兼容、迁移器或宿主适配层。
- [x] 3.2 已用 skills CLI `1.5.16` 在隔离 HOME 中从本地 checkout 完成用户级 copy 安装；默认递归找到嵌套 Skill，`SKILL.md`、`agents/openai.yaml` 与 `references/codex-cli-isolation.md` 完整一致。Codex CLI `0.144.1` 的 `skills/list` 将其识别为启用的用户级 Skill，且无解析错误。
- [x] 3.3 中英文 README 已收敛为公开发布目标路径与当前本地 Alpha 路径；补齐 uv 主路径、pipx fallback、诊断、更新/卸载和高级人工入口，并明确 PyPI、远程 Skill 与 Pages 当前尚不可用。
- [x] 3.4 主 `SKILL.md` 只保留宿主无关流程；Codex CLI 的已验证路径迁入一层 reference 并按需读取。未增加执行面清单、宿主注册表或 adapter。

## Wave 4：本地集成与外部试跑

- [x] 4.1 已从 `e05db14` 的 clean source archive 构建 sdist/wheel；macOS arm64、Python 3.11.15 下 wheel × uv 0.11.28 与 sdist × pipx 1.15.0 均隔离安装成功。安装后在先证明拒绝网络连接的 macOS sandbox 中完成 CLI、module entry、兼容探针、doctor、demo、6 类 package resources 与 demo provenance 验证；wheel SHA-256 为 `e01b4cda…d650b`，sdist SHA-256 为 `b07a61a7…824a`。
- [x] 4.2 macOS arm64、Python 3.11.15、Codex CLI `0.144.1` 的全新 HOME 已用本地 wheel 与复制安装的 Skill 完成一句话真实审计。独立 reviewer thread 与 orchestrator thread 不同；除 thread/turn 生命周期事件外，JSONL 仅有一个最终 `agent_message`，无工具、命令、文件修改或协作事件。最终报告为 `complete / concerns`，风险分 40，`billing.py:3` 精确锚定 1 条 high finding，`.run/` 已清理。canonical `Where` 与精确 section heading 已冻结在 prompt `v0.4`，未修改 demo fixture；文档收口后的 clean 候选 wheel SHA-256 为 `3c108b40…1370a`，sdist 为 `4623350b…dded8`，其 wheel runtime 文件与 E2E 实测 wheel 完全一致。
- [x] 4.3 外部执行者已在 macOS arm64 / Python `3.11.15` / Trae CLI（GLM-5.2）中，使用固定 `00bfac7a` source archive、`d0bdc57f…8fd1` wheel 与同 archive Skill 完成首次安装和一句话审计。主链生成 schema `0.3` 正式产物，结果为 `complete / inconclusive`；run identity、计数、自包含 HTML、独立重渲染和 `.run/` 清理已复核。Trae 手工读取候选 Skill 编排，原生 Skill discovery 保持未验证，隔离增强为当前不支持或未验证。用户确认该限制不阻塞 4.3 收口。
- [x] 4.4 已以 `e6f3381` 重建 clean candidate。Python `328 passed`、Ruff、feedback JavaScript、Markdown shell 语法、Skill 规范、SVG/XML 与 diff check 通过；wheel 通过 uv `0.11.28`、sdist 通过 pipx `1.15.0` 在仓库外 Python `3.11.15` 环境安装。Codex CLI `0.144.3` 隔离 reviewer 的 thread、JSONL、工具禁用、空工作目录和 pre-finalize 清理断言通过，正式报告为 `complete / concerns`，风险分 `40`，1 条 high finding 精确锚定；独立重渲染与原 HTML 字节一致。未修改 runtime、Skill、prompt 或 schema。

## Wave 5：Pages 与发布证据收口

- [x] 5.1 用户确认 `.sopify` 保留在 main，但普通用户 README 不展开内部维护信息；调整 ADR-003，取消 `audit-evidence` branch、固定 worktree、symlink 和双 commit 发布协议。
- [x] 5.2 已增加单一发布边界检查器，并由 CI 在实际构建 wheel、sdist 和复制安装 Skill 后调用；门禁检查 `.sopify/state`、`.sopify/user`、`raw-analysis.md`、常见私钥文件/标记和用户主目录绝对路径。现有 4 处历史 receipt 本地路径已脱敏。clean build、安装后 doctor/demo 与边界检查通过。
- [x] 5.3 main 的 `docs/` 已提供最小 Pages 入口、双语 README 共用的 PNG 封面和生成架构图，以及绑定 `d6776ca..81e7b1f` 的脱敏自身审计报告。报告项目名为 `EvidentLoop`，结果为 `complete / inconclusive`，0 findings；未声称隔离增强。README 分别展示该自身审计概览和当前 schema `0.3` 离线 demo 的修改行证据与浏览器本地决策；未把安装、demo 或计划中的反馈消费重复画入架构图。
- [x] 5.4 已生成并校验 release evidence bundle 草案；manifest 绑定 `81e7b1f`、package `0.1.0a0`、schema `0.3`、prompt `v0.5`，包含 audit pair、测试摘要和 checksums。bundle SHA-256 为 `f2a1ca6acf1404e58842e86936d4d7c0133c1a2dd1826a238197c070e968f694`，仅保留为待发布的 GitHub Release 资产，不写入 main。

## Wave 6：发布候选与用户 checkpoint

- [x] 6.1 已新增 tag-triggered `publish.yml`：只在目标 repository 运行，tag 必须与 package version 一致；build job 复用测试、构建与发布边界门禁，publish job 只授予 `contents: read` / `id-token: write` 并绑定 `pypi` environment。YAML、权限与 tag/version 本地检查通过；environment 外部配置留在 7.5。
- [x] 6.2 已从 clean candidate 完成 README/PyPI/Pages 收口与预览；Python `329 passed`、Ruff、feedback JavaScript、Markdown 本地目标、SVG/XML 与 diff check 通过。sdist/wheel 构建、仓库/分发包/Skill 边界扫描、仓库外 wheel import、doctor 与离线 demo smoke 通过；package `0.1.0a0`、schema `0.3`、prompt `v0.5` 一致。运行时、Skill 与 prompt 自 `81e7b1f` 的真实宿主 smoke 后未改变；7.2 仍对准确 release commit 重跑真实审计。
- [x] 6.3 用户已审计最终 diff，并授权 PyPI Trusted Publisher、release tag、main push、GitHub Release + evidence bundle 及 GitHub Pages；无域名变更。PyPI pending publisher 已登记 `evidentloop/evidentloop`、`publish.yml`、environment `pypi`，允许进入 7.2。

## Wave 7：经授权发布

- [x] 7.1 GitHub repository 已于发布 checkpoint 前改名为 `evidentloop/evidentloop`；旧地址重定向、新仓库读取、main CI 与本地 canonical remote 已验证。该事实不授权后续 tag、PyPI、Release 或 Pages 操作。
- [x] 7.2 PyPI README 图片已固定到 `v0.1.0a0` tag；main release commit 为 `88134ae`。该准确 commit 的 Python `329 passed`、Ruff、JavaScript、构建边界与真实 EvidentLoop 审计均通过，审计结果为 `complete / inconclusive`、0 findings。
- [x] 7.3 已生成绑定 `88134ae4bba0fa9995a6bb2d46ba17f9e0bcc6b6` 的 release evidence bundle；身份、manifest、audit status、脱敏与内部 checksums 均通过，外层 SHA-256 为 `3be3ee211f6e8247a8586331860e1892ffcc823f002db2e6d0510053126bd57d`。
- [x] 7.4 release commit 已推送并验证，远端 main、tag 解引用与 evidence manifest 的 `source_commit` 一致。
- [x] 7.5 PyPI Trusted Publisher 与受保护的 `pypi` environment 已配置；不可变 tag `v0.1.0a0` 指向 `88134ae`。GitHub pre-release 已发布并附带已回下载校验的 evidence bundle；随后审批 deployment，Actions run `29465092193` 的 build 与 publish jobs 均成功，PyPI 已发布 `0.1.0a0`。
- [x] 7.6 GitHub Pages 已从 main `/docs` 启用，首页与样例报告返回 HTTP 200；公开 PyPI 元数据、`uv tool install`、离线 demo、pipx 与远程 Skill copy 安装均通过，README tag 图片、Release 与 evidence 链路可访问。

## Wave 8：收口

- [x] 8.1 已在 main 的 `.sopify` 同步 blueprint、project、history 与最终 receipt；长期蓝图只保留已生效身份、真实交付状态和未完成长期项，未提交运行态或用户数据。
- [x] 8.2 用户已明确要求整体收口并授权直接操作；当前方案归档至 history。除本次方案归档提交外，未创建额外实现 commit、tag 或 Release。
