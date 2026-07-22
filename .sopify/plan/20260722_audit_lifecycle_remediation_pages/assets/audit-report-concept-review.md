# Audit report 成品样例审计说明

样例文件：audit-report-concept.html

定位：这是 Wave 3 的可交互目标样例，不是生产 renderer 输出，也不代表真实代码审计结论。它只冻结产品信息层级与端到端边界，不新增正式协议。

## 样例解决什么

1. 页头只保留当前报告真相：review status、当前 verdict、当前风险，以及存在 remediation 时的修复 claim 状态；它们各自只出现一次。
2. 页头边框色由审查完整性与整体 verdict 决定：不完整/不确定为蓝色或中性色，pass 为绿色，concerns 为红色，人工判断为琥珀色；finding 严重度、风险变化和 remediation claim 不控制页头颜色，文字始终保留。
3. 变更摘要是页头后的第一个业务区块，用现有 change/file/finding 数据直接说明改了什么、文件影响与增删规模，并链接到具体证据。
4. remediation 面板明确显示旧报告来源 finding、用户声明和模型 claim；旧 diff 的 runs 不复制到当前报告，当前完整 diff 的 verdict 继续独立展示。
5. 当前 finding 卡片保留模型原判断、人工裁定、当前状态和自有单栏 unified diff；单栏包含文件头、增删统计、旧/新行号、红绿行和 finding 关键行，但不引入 Diff2Html。
6. 同 diff 发生过正式 feedback revision 时才显示纵向历史卡片；只有初次模型审查时不渲染历史模块。其他无数据的 remediation、finding、fixes 也连标题和空框一起省略。
7. schema、run id 和 hash 集中到页尾默认折叠的“报告身份与校验信息”。代码长行保持原貌，很多行由现有 renderer 生成明确标注的可信节选；diff hunk 在有最大高度的容器内按需上下/左右滚动，页面本身不靠 body overflow-x hidden 掩盖溢出。
8. “评论与严重度”和报告身份使用原生 details/open 状态，summary 始终显示展开箭头并随 open 旋转，不用 JavaScript 维护折叠状态。反馈导出状态移到按钮组下方，通过 live region 和中性/成功/警告语义色反馈结果。
9. 交互控件与 summary 最小 44px，正文基准 16px；补齐 skip link、可见焦点、live region 和 reduced motion。

## 数据到页面的最小链路

### audit.json

- 核心 schema 继续使用 0.4。
- 同 diff feedback revision 继续使用现有 run.revision.events 和 human_adjudication，不改协议。
- 修复复审只在 extensions.evidentloop.remediation 保存 version `1`、一跳来源报告/差异身份，以及逐目标 finding id/fingerprint、用户声明和 `claim_id`。
- remediation 请求、serializer 和语义校验共用单一入口；目标必须唯一，`claim_id` 必须精确指向现有 claim。extension 不重复 claim 状态、当前 verdict/风险或当前 diff 身份。
- 修复结论使用现有 summary_audit.claims 及 supports_claim / challenges_claim 边。
- 当前 audit 的 runs 只包含当前 diff 的模型审查及后续同 diff feedback revision；旧报告保持不可变，只通过来源卡片关联。

样例 HTML 尾部的 view-model-sample 只是 renderer context 摘要，不是假装完整 audit.json。

### renderers/html.py

建议把现有散落字段收敛成五个只读 view：

- report_truth：review_status、verdict、risk、open count、人工裁定 notice。
- change_view：变更标题/摘要、文件数、增删行、逐文件 role/change type 与当前 finding 入口。
- remediation_view：直接来源、选择的 finding、声明、claim 与证据。
- finding_view：model、human、current、counted_in_risk、feedback events。
- run_view：仅当前 diff 的权威 run 顺序、人类动作摘要、前后风险与待处理数、报告身份；没有 feedback revision 时不生成历史 section。

风险、verdict、claim、run 顺序全部在 Python context 中确定。模板只展示，浏览器脚本不得重新计算这些业务真相。

### audit.html.j2

- 用一个 truth grid 替代当前 judgment grid 加 metric grid 的重复首屏。
- 变更摘要紧随页头，文件行按需链接到 finding 的单栏 diff 证据。
- remediation 是独立来源与验证 panel，不进入 feedback history；旧 diff runs 不复制到当前报告。
- feedback history 只在当前 diff 存在 feedback revision 时渲染为 article 列表；其他可选 section 同样按数据整体省略。data table 只保留给确实需要列对齐的技术证据。
- 单栏 unified diff 由现有可信 hunk 渲染：`audit.json` 保留完整 hunk，超过现有阈值时只由 renderer 生成包含全部 finding 关键行与明确省略计数的节选；长行不折断，滚动容器按需双向滚动，文件头和节选说明留在容器外。不接入 Diff2Html、语法高亮、双栏、搜索、筛选、侧边栏、同步滚动或全屏状态。
- hash 使用“报告身份与校验信息” details 下沉，但保留完整值和可复制能力。
- 取消动态章节编号，标题靠语义层级而不是 1/2/3 编号表达顺序。

### audit.js

现有反馈脚本的纯函数边界是合理的，不应因为换布局而重写：

- 保留 identity、localStorage fallback、pending state、null 反转、JSONL、copy/download。
- 只更新 DOM 绑定、状态文案与 aria-live 目标。
- remediation 由 renderer 输出，只读展示；不要再建一份浏览器 remediation 状态。
- 不在 JS 中排序 run，不计算风险，不判断 claim，不根据 finding 消失宣布修复。
- 不在 JS 中决定 section 是否存在、页头颜色或 diff 配对；这些均由 Python context 和模板确定。
- 不用 JS 接管 details 展开/收起；导出脚本只更新既有 live status 的文案与语义 tone。

样例内联脚本仅用于演示按钮、null 事件、复制和下载；生产实现继续复用并测试现有 audit.js。

## 可以删除的冗余

当前代码中可确认的死 context：

- html.py 返回的 revision 当前没有模板消费者。
- html.py 返回的 human_findings 当前没有模板消费者。
- html.py 返回的 next_section_number 当前没有模板消费者。

完成新首屏后可继续删除：

- 仅服务旧 judgment grid 的 human_disposition_count、human_comment_count、human_severity_count、model_verdict_label、model_risk_score_label。
- 模板删除后对应的 judgment-grid / judgment-card CSS。
- 历史区改卡片后，仅为该历史表存在的通用 620px 最小宽度依赖；单栏 diff 自己保留受控横向滚动。
- body overflow-x hidden；改为修复具体子元素的 min-width / overflow。
- 动态 fixes/history/evidence 章节编号及其 context 计算。

删除必须与模板、context 和测试同一任务完成；不得先删数据再靠空值或 CSS 隐藏回退。

## 明确保留

- schema 0.4、风险算法、feedback JSONL、report/diff version。
- Jinja autoescape、StrictUndefined、自包含 CSS/JS、HTML trace validator。
- finding 与 diff evidence 主体、完整 hunk 数据、renderer 单一可信节选、localStorage 失败回退。
- 无 Diff2Html、无前端框架、无主题系统、无图表、无双栏 diff、无搜索/复杂筛选、无常驻侧边栏、无语法高亮依赖、无同步滚动、无全屏模式、无全局导航、无复杂动画。

## 样例验收

- 桌面端无需阅读 hash 即可区分审查完整性、当前 verdict 和修复 claim；页头边框与整体状态一致且文字结论始终存在。
- 变更摘要位于页头后，文件影响与增删规模可读，并能直达 finding 的单栏 unified diff。
- 当前样例没有已应用的同 diff feedback revision，因此不出现历史 section；各类可选模块都没有空标题或占位卡片。
- 评论与严重度、报告身份 summary 的展开箭头在收起和展开状态均可见；导出默认状态位于按钮下方，成功/失败更新可被屏幕阅读器读出。
- remediation extension version、必填字段、目标唯一性和 `claim_id` 关联有语义校验；当前 runs 不包含旧 diff runs。
- 375px 下所有业务卡片单列，页面无整体横向滚动；样例中的长行与多行节选只在 hunk 内按需上下/左右滚动，滚动区可用键盘到达，文件头和节选计数不随内容滚走。
- 键盘可到达 skip link、details、裁定、select、textarea、复制和下载。
- 清空评论生成 comment: null；恢复模型严重度生成 severity: null。
- 状态不只依赖颜色，复制失败明确说明数据未丢失并提供下载路径。
