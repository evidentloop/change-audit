# 任务清单：change-audit 零摩擦分发与审计证据隔离

目录：`.sopify/plan/20260711_zero_friction_distribution/`

> 架构决策已收口：首次 Alpha 前完成 evidence 隔离，并对 evidence 失败执行 fail closed。任何 branch push、commit、tag、PyPI 发布或 Pages 激活都必须经过 4.4 checkpoint。

## 0. 产品身份门禁

- [ ] 0.1 确认 PyPI `change-audit` 可注册并保存公开查询证据；复核 repo/PyPI/CLI/import/Skill 身份矩阵。若 PyPI 名称无法取得则停车，不自行启用候选品牌。

## 1. Python CLI 产品化

- [ ] 1.1 在 `pyproject.toml` 增加 `change-audit` console script，并验证与 `python -m change_audit` 行为一致。
- [ ] 1.2 实现 `doctor --json`，检查版本、schema、prompt、package resources 和 Git；将 `npx` 缺失作为非阻断提示，输出完整 Skill 目录手工安装 fallback，不扫描宿主私有目录。
- [ ] 1.3 实现 `demo`：把独立合成 fixture 打进 wheel，在临时 Git 仓库中复用 `prepare -> replay -> finalize`，并在终端、JSON、HTML 标明 provenance。
- [ ] 1.4 增加 console script、doctor、demo、离线运行和 clean wheel package resource 测试。

## 2. 标准 Skill 分发

- [ ] 2.1 将现有 `integrations/agent-skill/change-audit/` 迁移为唯一活动目录 `skills/change-audit/`，保留静态薄编排和必要 `agents/` 元数据。
- [ ] 2.2 删除 Codex/Qoder 作为产品前提的表述，改为宿主能力契约和实测支持矩阵。
- [ ] 2.3 明示 CLI/schema/prompt 兼容范围，并在不兼容时于 `prepare` 前 fail closed。
- [ ] 2.4 在隔离临时 HOME 中用 `npx skills@latest add . --skill change-audit -g` 从本地 checkout 验证嵌套目录、辅助文件与全局安装形态。

## 3. 用户文档与 evidence worktree

- [ ] 3.1 重写中英文 README 首屏为“在线看 -> uvx demo -> 正式安装 -> 一句话审计”，首版能力只陈述 Git diff，并链接稳定 Pages 与 `audit-evidence` 分支入口；确切 evidence commit 由 Release 提供。
- [ ] 3.2 补充 uv 主路径、pipx fallback、手工 Skill copy、`npx skills list -g --json` 诊断、更新/卸载和高级人工 `prepare -> external review -> finalize` 文档。
- [ ] 3.3 在本地准备 orphan `audit-evidence` branch 与固定 worktree，写维护者 bootstrap 文档；文档必须给出全新机器从零完成 fetch branch、创建 worktree、建立被忽略的 `.sopify` symlink、验证状态以及故障恢复/移除的可复制命令，且不得硬编码绝对路径。
- [ ] 3.4 把整个 `.sopify` 和现有 dogfood/生成证据复制到 evidence worktree；确认 `.sopify/state`、`.sopify/user`、raw output、密钥和本地绝对路径不进入分支，再从 main 工作树移除并加入 ignore。
- [ ] 3.5 在 `audit-evidence` 建立 `docs/` Pages 入口和 `evidence/releases/<tag>/<source-sha>/` bundle 结构；只永久保存脱敏 audit、测试摘要、manifest 与 checksums。
- [ ] 3.6 验证 main checkout 在没有 evidence worktree 时仍可完整测试、build、安装和运行；验证维护环境通过 symlink 可恢复 Sopify，且 main 不再跟踪 `.sopify` 或生成型证据。

## 4. 发布与验证

### 4A. 本地验证（不触发外部操作）

- [ ] 4.1 从 clean sdist/wheel 做本地离线安装，验证 `change-audit`、`python -m change_audit`、demo、doctor、package resources、uv tool 本地 wheel 安装与 pipx clean install。
- [ ] 4.2 用本地 wheel 与 `skills/change-audit/` 至少完成一个宿主的 `Skill discovery -> isolated review -> finalize` 全新环境 smoke；其他宿主不提前宣称已验证。
- [ ] 4.3 新增并本地检查 tag-triggered publish workflow：只授予 `contents: read` 与 `id-token: write`，绑定受保护 environment，复用 clean build/test 门禁；本地检查不触发外部发布。
- [ ] 4.4 发布 checkpoint：向用户提交 PyPI 名称结果、main/evidence 双侧 diff、准确版本、构建物摘要、测试/宿主 smoke、脱敏结果、README/PyPI 预览和完整外部操作清单；获得明确授权前不 commit/push、不配置 PyPI、不 push tag、不发布、不启用 Pages。

### 4B. 经授权发布（外部操作）

- [ ] 4.5 经授权后创建 main release commit，并针对该 commit 重跑确定性测试与真实审计；source 有任何变化则废弃候选并重跑。
- [ ] 4.6 在 evidence worktree 生成绑定 4.5 `source_commit` 的 release bundle，验证 manifest、audit status 与 checksums 后创建 evidence commit。
- [ ] 4.7 推送 main 与 `audit-evidence`，验证远端两个 commit、main 内容边界和 manifest 的 `source_commit` 一致；Release 链接确切 evidence commit/path，README 保持稳定入口。
- [ ] 4.8 建立 PyPI `change-audit` 项目所有权，并配置绑定准确 repository、workflow 与受保护 environment 的 Trusted Publisher。
- [ ] 4.9 创建并 push 与 package version 相同、指向 4.5 main commit 的不可变 Git tag，由 Trusted Publishing workflow 发布 PyPI Alpha；GitHub Release 页面可选。
- [ ] 4.10 从 `audit-evidence/docs` 启用或刷新 Pages，并从公开入口验证 PyPI README、`uvx change-audit demo`、`uv tool install change-audit`、pipx、远程 Skill 安装和确切 evidence commit 链路。

## 5. 收口

- [ ] 5.1 在 `audit-evidence/.sopify` 同步 blueprint、project、history 与最终 receipt；main 只保留用户所需 README/文档和证据入口。
- [ ] 5.2 显式确认后归档当前方案；除 4.4 已授权的操作外，不额外 commit、创建 tag 或发布。
