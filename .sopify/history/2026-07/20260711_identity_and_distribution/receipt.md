---
plan_id: 20260711_identity_and_distribution
outcome: completed
---

# completed

## Summary

EvidentLoop 身份迁移、Python CLI 与标准 Skill 分发、准确 release evidence、PyPI Trusted Publishing、GitHub pre-release 和 Pages 已完成并公开验证。

## Release

- Source commit / tag：`88134ae4bba0fa9995a6bb2d46ba17f9e0bcc6b6` / `v0.1.0a0`
- GitHub Release：`https://github.com/evidentloop/evidentloop/releases/tag/v0.1.0a0`
- PyPI：`https://pypi.org/project/evidentloop/0.1.0a0/`
- Pages：`https://evidentloop.github.io/evidentloop/`
- Evidence SHA-256：`3be3ee211f6e8247a8586331860e1892ffcc823f002db2e6d0510053126bd57d`

## Verification

- 准确 release commit：Python `329 passed`、Ruff、JavaScript、build、release boundaries 与真实 EvidentLoop 审计通过。
- Release 资产回下载 SHA-256 与本地 evidence bundle 一致。
- GitHub Actions run `29465092193` 的 build / publish jobs 成功；PyPI wheel 与 sdist 元数据可见。
- 隔离 Python 3.11 环境的 `uv tool install`、demo、pipx 及远程 Skill copy 安装通过。
- Pages build `1097762119` 成功，首页和样例报告返回 HTTP 200。

## Key Decisions

- 首个公开 Alpha 继续只支持本地 Git diff，不扩张到远程 PR、folder review、自动修复或反馈驱动重生成。
- `.sopify` 保留在 main 作为公开开发记录，但继续由发布边界门禁排除出 wheel、sdist 和安装后的 Skill。
- PyPI 发布必须在准确 tag、Release evidence 与 source commit 一致后，通过受保护 environment 审批。
