# 任务清单: change-audit 正式改名

目录: `.sopify/plan/20260710_change_audit_rename/`

## 0. 执行前基线

- [x] 0.1 将现有产品设计变更独立提交为 `3bd104a`，验证 JSON、SVG 与 staged diff。
- [x] 0.2 确认删除 `.qoder/` 为有意修改，修复 EOF 空行并独立提交为 `fac854f`。

## 1. 命名契约

- [ ] 1.1 在 `.sopify/project.md` 写入正式命名契约：产品/仓库/CLI/distribution 为 `change-audit`，Python import 为 `change_audit`，内部模型为 Audit Graph。
- [ ] 1.2 在 `README.md` 与 `README.zh-CN.md` 投影新产品名、定位、命令和架构资产链接，不复制内部契约全文。
- [ ] 1.3 在 `.sopify/user/preferences.md` 记录用户确认的长期命名偏好。

## 2. 仓库内语义化迁移

- [ ] 2.1 将 `auditgraph/` 源码占位目录迁移为 `change_audit/`，并将 blueprint/data model 中的 `auditgraph.*` 引用迁移为 `change_audit.*`。
- [ ] 2.2 更新 `.sopify/blueprint/README.md`、`background.md`、`design.md`、`tasks.md` 中的当前产品身份：将 tasks 标题改为 `# change-audit 长期任务`，迁移正文中的产品名和 CLI 示例，同时保留 Audit Graph 模型术语与未来 renderer 产物 `audit-graph.svg`。
- [ ] 2.3 更新 `docs/v0-scope.md`、`docs/data-model.md` 和示例说明中的当前产品名、CLI、package 与产品 namespace。
- [ ] 2.4 将 `docs/assets/audit-graph-architecture.svg/png` 迁移为 `change-audit-architecture.svg/png`；SVG 只替换可见 `<text>` 中的产品名，不修改非可见属性；保留 Typed Audit Graph 标签并完成浏览器视觉验证。保持 `audit-html-preview.png` 文件名不变，仅更新 README 引用上下文。
- [ ] 2.5 更新 `docs/examples/*/audit.html` 中的产品级文本和 localStorage namespace；不改变 `audit.json` schema 与产物文件名。

## 3. 历史保真

- [ ] 3.1 保留 `.sopify/plan/20260707_audit_graph_init/` 的目录与原有正文，新建 `20260710_rename_note.md` 记录后续更名与新方案路径。
- [ ] 3.2 确认旧产品名只出现在历史方案、rename note、Audit Graph 模型和未来 renderer 产物 `audit-graph.svg` 中，不再作为当前产品身份出现。

## 4. 确定性验证

- [ ] 4.1 使用 `rg` 生成旧名称剩余引用清单，并逐项归类为允许保留或迁移遗漏。
- [ ] 4.2 运行 `git diff --check`，确认改名 staged diff 只包含方案内文件。
- [ ] 4.3 使用 `jq empty` 验证全部 JSON 样张，使用 XML 校验验证架构 SVG。
- [ ] 4.4 验证 README/HTML 的相对资源链接、CLI 示例、localStorage namespace 和中英文口径一致，并在浏览器中确认架构 SVG 与 `audit-html-preview.png` 渲染正常。
- [ ] 4.5 确认不存在 `auditgraph` 目录、import 或当前模块引用，统一为 `change_audit`。

## 5. 外部身份迁移 checkpoint

- [ ] 5.1 在用户显式确认后，将 GitHub 仓库改名为 `change-audit`，更新并验证 `origin` URL 与旧链接重定向。
- [ ] 5.2 在所有仓库内工作完成后，将本地目录最后迁移为 `change-audit/`，重新打开 workspace 并复核 Git 状态。

## 6. 收口

- [ ] 6.1 同步 `.sopify/project.md`、blueprint 与长期任务，移除已经完成且不再需要保留的长期改名项。
- [ ] 6.2 准备 finalize 时归档本方案，并确保历史索引同时保留旧名与新名的可追溯关系。
