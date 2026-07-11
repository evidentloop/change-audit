# 变更提案：change-audit 零摩擦分发与审计证据隔离

## 需求背景

当前审计内核已经通过真实 dogfood，但外部用户仍需 clone、创建 venv、editable install 并手工注册 Skill。产品能力可用，首次成功路径不可用。

本方案保留 **change-audit** 作为 Alpha 产品名，通过 PyPI CLI、同仓库标准 Skill 与 GitHub Pages 建立最小分发面。`main` 只承载可独立构建的产品；整个 `.sopify`、公开审计证据和精选生成型测试结果在首次 Alpha 前迁入 `audit-evidence`。evidence bundle 生成、校验或 push 失败时，阻断 tag 与 PyPI 发布。

评分：

- 方案质量：9/10
- 落地就绪：8/10

评分理由：

- 方案质量扣 1 分：main/evidence 双 commit 无法原子更新，必须靠 `source_commit` 校验和 fail-closed 发布门禁维持一致性。
- 落地就绪扣 2 分：固定 worktree 尚未在全新机器验证；console script、demo、doctor、标准 Skill、Pages、PyPI 与真实宿主 E2E 仍待实现。

## 决策状态

架构决策已收口，不再需要产品层拍板：

- 分发方式遵循 [ADR-001](adr/001-pypi-cli-standard-skill.md)。
- 产品身份遵循 [ADR-002](adr/002-keep-change-audit-identity.md)。
- main/evidence 边界、首次 Alpha 前隔离和 fail-closed 发布遵循 [ADR-003](adr/003-main-and-audit-evidence-placement.md)。

后续只有两个执行 gate：0.1 若 PyPI 名称不可取得则停车；4.4 在实际外部操作前确认准确 commit、版本和发布清单。二者不是新的架构选择。

## 用户成功标准

1. 无需 clone 或 editable install，即可查看在线报告或运行 replay demo。
2. 正式安装使用 `uv tool install change-audit` 与 `npx skills@latest add evidentloop/change-audit --skill change-audit -g`；pipx 作为 fallback。
3. 用户说“用 change-audit 审计 staged changes”后，得到正式 `audit.json + audit.html`。
4. main checkout 不依赖 `audit-evidence` 即可构建、测试、安装和运行。
5. README/Pages 提供稳定证据入口；Release 链接对应版本的确切 evidence commit。
6. 每个 PyPI 版本都绑定不可变 main tag、`source_commit` 和已发布 evidence bundle。

## 影响范围

- Python package：console script、demo、doctor、resources 与 PyPI metadata。
- Skill：迁移到 `skills/change-audit/`，保持静态薄编排。
- 仓库：main 产品面、固定 evidence worktree、Pages 与 evidence bundle。
- 发布：main/evidence 双 commit 校验、Trusted Publishing 与真实宿主 smoke。

## 非目标

- 不更改产品名、repo/import/schema namespace 或 prompt version。
- 不把非代码 profile 描述为当前能力。
- 不把测试源码、schema 或 release gate 移出 main。
- 不自研 npm 包、独立二进制、本地 LLM 或宿主 adapter registry。
- 不永久保存 raw model output、完整日志、coverage 或未脱敏截图。

## 主要风险

- 双分支漂移：manifest 绑定准确 `source_commit`；不一致即阻断发布。
- Sopify 恢复依赖 worktree：bootstrap 必须提供全新机器可复制命令和恢复步骤。
- 公开证据泄露本地信息：push 前执行路径、密钥、raw output 与个人信息扫描。
- evidence branch 不减少 Git 对象总量：当前目标是默认树和认知隔离，不宣称解决 clone 体积。
