# 任务清单：EvidentLoop 身份迁移、零摩擦分发与审计证据隔离

目录：`.sopify/plan/20260711_identity_and_distribution/`

> 当前只进入方案评审。Wave 0 身份 checkpoint 通过前不得修改源码身份；Wave 6 发布 checkpoint 通过前不得提交或推送身份实现与发布候选，不得改名远端 repository、购买域名、配置 PyPI、push tag、发布或启用 Pages。经用户明确授权的纯方案文档 commit/push 不属于发布操作。

## Wave 0：身份与注册风险门禁（最高优先级）

- [ ] 0.1 按 USPTO 官方策略检索 `EVIDENTLOOP`、`EVIDENT LOOP`、相近读音/拼写及相关软件/SaaS 服务，保存查询式、结果链接、检索日期和判断；交互数据库无法验证时不得用搜索引擎零命中替代。
- [ ] 0.2 在 WIPO Global Brand Database 执行相同精确词与近似词筛查，并记录数据库覆盖限制；基础筛查发现同类软件中的实质混淆风险时再停车决定是否补充 EUIPO/CNIPA 或专业法律意见，不把专业检索设为默认 Alpha 前置条件。
- [ ] 0.3 核验 `evidentloop` PyPI 项目页、GitHub org/repository 目标、`evidentloop.com` WHOIS 与相邻品牌 `Evidently` / `EvidenceLoop`，区分“未发现公开项目”“可注册”“已取得”三种状态。
- [ ] 0.4 按“相邻品牌可接受；精确同名或同类软件中的实质混淆才阻断”形成名称判断，冻结目标身份矩阵、旧标识 allowlist、schema/prompt 版本策略、历史证据策略和所有外部预留动作；不使用 placeholder package 抢占 PyPI。
- [ ] 0.5 身份 checkpoint：向用户提交 0.1-0.4 证据与 ADR-004，获得明确确认后才将 ADR-004 标为已采纳、ADR-002 标为已废弃并进入 Wave 1；未通过则保持 `change-audit` 并停止迁移。

## Wave 1：本地身份 clean break

- [ ] 1.1 生成受版本管理文件的旧身份清单，按 source、tests、schema、prompt、Skill、docs、`.sopify`、历史证据分类；冻结仅允许 ADR-002、迁移说明和历史证据保留旧名的 allowlist。
- [ ] 1.2 将 distribution、source package、Python import、module entry 与版本读取统一为 `evidentloop`；不保留 `change_audit` import alias。
- [ ] 1.3 将 schema `$id`、title、extension namespace 与 validator 统一为 EvidentLoop；按 checkpoint 结论升级 schema 并验证旧报告只作为历史证据读取。
- [ ] 1.4 将 reviewer prompt 标题、source、version、hash、run marker 与 ingest identity 统一为 EvidentLoop；任何 prompt 文本变化都必须重新冻结 provenance 测试。
- [ ] 1.5 将 staging suffix、CLI/error prefix、HTML title/kicker、feedback localStorage prefix、导出 provenance 与默认目录名统一为 EvidentLoop。
- [ ] 1.6 将活动测试、fixture、prompt-lab、dogfood 入口和生成脚本迁移到新 identity；历史已归档输出不重写。
- [ ] 1.7 执行格式、schema、Python、JS 与完整测试；对受版本管理活动文件运行旧标识扫描，只有 allowlist 命中可通过。

## Wave 2：Python CLI 产品化

- [ ] 2.1 在 `pyproject.toml` 增加 `evidentloop` console script 与 Homepage / Repository / Issues URLs，并验证与 `python -m evidentloop` 行为一致。
- [ ] 2.2 实现 `doctor --json`，检查版本、schema、prompt、package resources 和 Git；将 `npx` 缺失作为非阻断提示，不扫描宿主私有目录。
- [ ] 2.3 实现 `demo`：把独立合成 fixture 打进 wheel，在临时 Git 仓库中复用 `prepare -> replay -> finalize`，并在终端、JSON、HTML 标明 provenance。
- [ ] 2.4 增加 console script、doctor、demo、离线运行和 clean wheel package resource 测试。
- [ ] 2.5 在实现 CLI/HTML 改动前审计现有反馈能力，确定首个 Alpha 的反馈消费范围：若纳入完整消费与重新生成，补齐结构化输入输出、状态迁移和回归测试；若延后，保留交互反馈能力并在 README/Pages 明确边界。该选择不回退 EvidentLoop 的长期闭环愿景。

## Wave 3：标准 Skill 与用户文档

- [ ] 3.1 将现有 `integrations/agent-skill/change-audit/` 迁移为唯一活动目录 `skills/evidentloop/`，更新 frontmatter、agent metadata、触发词与命令，不保留双 Skill。
- [ ] 3.2 删除 Codex/Qoder 作为产品前提的表述，改为宿主能力契约和实测支持矩阵；明示 CLI/schema/prompt 兼容范围并在 `prepare` 前 fail closed。
- [ ] 3.3 在隔离临时 HOME 中用标准 skills CLI 从本地 checkout 安装 `evidentloop`，验证嵌套目录、辅助文件、全局安装形态与 discovery。
- [ ] 3.4 重写中英文 README 首屏为“在线看 -> `uvx` demo -> 正式安装 -> 一句话审计”，首版只陈述 Git diff，并补充 uv 主路径、pipx fallback、诊断、更新/卸载和高级人工通道。

## Wave 4：本地集成与外部试跑

- [ ] 4.1 从 clean sdist/wheel 做本地离线安装，验证 CLI、module entry、demo、doctor、package resources、uv tool 本地 wheel 安装与 pipx clean install。
- [ ] 4.2 用本地 wheel 与 `skills/evidentloop/` 至少完成一个宿主的 `Skill discovery -> isolated review -> finalize` 全新环境 smoke；其他宿主不提前宣称已验证。
- [ ] 4.3 用本地 wheel 与 Skill 找至少一名外部试用者走通首次安装与一句话审计，记录阻塞、误解与反馈；不要求 evidence worktree 或公开发布。
- [ ] 4.4 根据 4.2-4.3 修正 CLI、Skill 与文档后重跑 clean wheel、完整测试和真实宿主 smoke。

## Wave 5：evidence worktree 与 Pages

- [ ] 5.1 在本地准备 orphan `audit-evidence` branch 与固定 worktree，写全新机器可复制的 fetch、worktree、symlink、验证、恢复与移除命令，不硬编码绝对路径。
- [ ] 5.2 把整个 `.sopify` 和现有 dogfood/生成证据复制到 evidence worktree；保留旧报告原身份，确认 state/user、raw output、密钥和本地绝对路径不进入分支，再从 main 移除并加入 ignore。
- [ ] 5.3 在 `audit-evidence` 建立 `docs/` Pages 入口和 `evidence/releases/<tag>/<source-sha>/` bundle；manifest 必须记录产品身份与版本，永久证据只含脱敏 audit、测试摘要与 checksums。
- [ ] 5.4 验证 main checkout 在没有 evidence worktree 时仍可完整测试、build、安装和运行；验证维护环境通过 symlink 可恢复 Sopify，main 不再跟踪 `.sopify` 或生成型证据。

## Wave 6：发布候选与用户 checkpoint

- [ ] 6.1 新增并本地检查 tag-triggered Trusted Publishing workflow：只授予 `contents: read` 与 `id-token: write`，绑定目标 repository 与受保护 environment，复用 clean build/test 门禁。
- [ ] 6.2 从 clean candidate 生成 README/PyPI/Pages 预览、构建物摘要、完整测试、真实宿主 smoke、身份扫描、脱敏结果与 evidence manifest 草案。
- [ ] 6.3 发布 checkpoint：向用户提交 main/evidence 双侧 diff、准确版本、目标 GitHub 改名、域名动作、PyPI/Trusted Publisher、tag、push、Pages 与 Release 清单；获得明确授权前停止。

## Wave 7：经授权发布

- [ ] 7.1 经授权将 GitHub repository 从 `evidentloop/change-audit` 改名为 `evidentloop/evidentloop`，验证重定向与权限，并更新本地 remote；失败时停止后续发布。
- [ ] 7.2 创建 main release commit，并针对该准确 commit 重跑确定性测试与真实审计；source 有任何变化则废弃候选并重跑。
- [ ] 7.3 在 evidence worktree 生成绑定 7.2 `source_commit` 的 release bundle，验证身份、manifest、audit status、脱敏与 checksums 后创建 evidence commit。
- [ ] 7.4 推送 main 与 `audit-evidence`，验证远端两个 commit、main 内容边界和 manifest 的 `source_commit` 一致；Release 链接确切 evidence commit/path。
- [ ] 7.5 建立 PyPI `evidentloop` 项目所有权并配置 Trusted Publisher；创建与 package version 相同、指向 7.2 main commit 的不可变 tag，由 workflow 发布 Alpha。
- [ ] 7.6 从 `audit-evidence/docs` 启用或刷新 Pages，并从公开入口验证 PyPI README、`uvx evidentloop demo`、`uv tool install evidentloop`、pipx、远程 Skill 安装和确切 evidence commit 链路。

## Wave 8：收口

- [ ] 8.1 在 `audit-evidence/.sopify` 同步 blueprint、project、preferences、history 与最终 receipt；长期蓝图只保留已生效的 EvidentLoop 身份和真实交付状态。
- [ ] 8.2 显式确认后归档当前方案；除方案归档和已授权的 Wave 7 操作外，不额外创建实现或发布 commit，不创建额外 tag 或发布。
