---
title: EvidentLoop 审计闭环、修复复审与公开产品页
plan_id: 20260722_audit_lifecycle_remediation_pages
status: planned
lifecycle_state: planned
level: standard
created: 2026-07-22
updated: 2026-07-22
archive_ready: false
knowledge_sync:
  project: required
  background: review
  design: required
  tasks: required
---

# EvidentLoop 审计闭环、修复复审与公开产品页

就绪状态: Ready
依据: focus、同 diff 人工裁定、跨 diff 修复复审、报告信息层级、单栏 diff、动态模块和 Pages 范围均已收敛；剩余事项是实施期证据与外部交付门禁，不再需要产品方向决策。

## Context / Why

EvidentLoop 目前能把本地 Git diff 生成可追溯的 `audit.json` / `audit.html`，也能让用户针对同一份代码做人工裁定并生成新的报告修订。但产品链路仍有三处断点：

1. local-diff 正式入口没有把用户明确给出的审计重点传入已有 `ReviewPack.focus`，导致模型完成结构化审查，却可能没有完整覆盖用户意图。
2. `feedback_revision` 只适合同一 `diff_version` 上的人工裁定。若用户根据 finding 修改了代码，必须重新审查新 diff；当前产品没有一种可靠方式说明“这次新审查是针对上份报告的哪些 finding 做修复验证”。
3. 当前 audit HTML 的证据和 finding 基础清晰，但首屏重复结论，人工裁定、反馈历史与修复复审容易混成一个概念；GitHub Pages 仍是单屏英文入口，无法完整解释产品闭环、边界、安装方式和真实证据。

“代码改动是否由 finding 引起”不能从文件路径、提交信息、相似 diff、时间顺序或 finding 消失自动推断。唯一可靠的产品输入是：用户或宿主显式选择一份旧 audit 和其中具体 finding，并声明本次新 diff 的修复目标；EvidentLoop 再验证来源身份，独立审查新代码，并对修复声明给出 `supported / challenged / partial / unknown`。

目标用户链路：

`显式 focus → 初次模型审查 → finding → 同 diff 人工裁定 → 代码修复 → 显式关联旧 finding → 新 diff 独立复审 → 可理解的结果与一跳来源 → Pages / README 公开证据`

## Scope

- 为 local-diff CLI、Python API 和官方 Skill 补齐显式 `focus` 传递；不推断默认重点，不降低完整度门槛。
- 保持 `feedback_revision` 的定义：同一 `diff_version`、不重新审查代码、旧 audit 不可变、生成新的 `report_version`。
- 增加最小修复复审输入：显式提供来源 audit 和一个或多个 finding；验证旧报告原始字节、`report_version`、非空 `diff_version`、finding id 与 fingerprint 后，对当前新 diff 发起独立审查。
- 复用 schema `0.4` 的 `summary_audit`、claims、`supports_claim` / `challenges_claim` 与 namespaced extensions 表达修复声明和验证结果；为 `extensions.evidentloop.remediation` 建立单一、受验证的小契约，但不增加核心 schema 版本或中心 audit-series 状态。
- 将 prompt 从 `v0.5` 升至 `v0.6`，要求 reviewer 独立判断修复声明，禁止把“旧 finding 没再次出现”直接当作已修复。
- 在新报告中只记录直接前驱及所选 finding，重复一跳关联自然形成链；不自动扫描、匹配或改写旧报告。
- 端到端调整 audit report 的 context、模板、CSS、交互与测试：首屏真相层级、误报语义、同 diff 反馈历史、修复复审结果、移动端与无障碍一起收口。
- 新建双语 GitHub Pages 产品页，参考 Sopify 最新页面的信息架构、可访问性和静态交付方式，但不复制其品牌视觉或工作流内容。
- 局部重写 README 的首屏定位、核心闭环、报告示例和安装入口，并盘点、替换过期或低价值素材；README 与 Pages 复用同一份真实报告和权威链接，不扩写成第二个产品网站。
- 完成定向测试、全量回归、代表性桌面/移动端视觉验收、真实公开仓库两轮 dogfood 和候选构建；当前授权仅覆盖本方案包的提交与 feat 分支推送，开发、业务代码提交、发布和 Pages 上线仍不在本轮授权内。
- 候选版本预期为 package `0.1.0a3`、renderer `0.4`、prompt `v0.6`；schema 保持 `0.4`。

## Approach

### 1. 两类 revision 分开建模

- `feedback_revision`：来源与结果保持同一 `diff_version`；用户 accept、false positive、comment、severity override；不调用 reviewer；每次生成新的 `report_version`。
- remediation re-audit：当前 diff 必须与来源 `diff_version` 不同；用户显式选择旧 audit 和 finding；调用 reviewer 审查完整当前 diff，并额外验证“所选 finding 是否已被当前改动解决”。
- 混合 diff 合法：当前 diff 可以同时包含修复和其他改动，关联只作用于明确选择的 finding，不能宣称整个 diff 都由旧 finding 导致。

### 2. 最小来源契约与一跳链路

1. 读取来源 `audit.json` 原始字节并计算 `report_version`，再执行 schema 与语义校验。
2. 要求来源含合法、非空 `extensions.evidentloop.diff_version`；旧版无版本报告不能成为正式修复来源，不猜测补值。
3. 验证用户所选 finding id 与 fingerprint 同时匹配来源最新正式 run，拒绝过期、冲突、重复或未知选择。
4. 冻结当前新 diff 后确认它与来源 `diff_version` 不同，再把最小修复上下文写入 reviewer prompt。
5. 新 audit 仅在 `extensions.evidentloop.remediation` 保存版本为 `1` 的最小对象：直接前驱 `report_version` / `diff_version`，以及逐目标 finding id、fingerprint、用户声明和对应 `claim_id`；不保存本地绝对路径。
6. remediation 请求对象、序列化和语义校验共用一个正式入口；验证版本、必填字段、目标唯一性以及 `claim_id` 与现有 claim 的一一对应。extension 不重复保存 claim 状态、当前 verdict、风险分或当前 `diff_version`。
7. 使用现有 summary claim 与关系边表达 reviewer 对每个修复目标的 `supported / challenged / partial / unknown` 结论。报告自身 verdict 仍由当前完整审查决定，两者不得混写。
8. 新 audit 的 `runs` 只记录当前 diff 的模型审查和后续同 diff 人工修订；旧报告不复制进当前 runs，只通过 remediation 来源卡片保留一跳关联。

### 3. Audit HTML 不是换肤，而是端到端信息重排

- 保留现有颜色变量、字体、finding、diff evidence、自包含 HTML 与无框架实现；不建立第二套组件系统。
- 页头先展示报告真相，再以变更摘要作为第一个业务区块。页头按“审查是否完整 → 当前 verdict / 风险 → 是否经过人工裁定 → 当前待处理数”组织；`review_status` 与 verdict 分开保留，`partial / failed` 和“基于人工裁定，未重新审查代码”始终可见。
- 页头边框色由 renderer 根据审查完整性和当前整体 verdict 决定：不完整或不确定使用蓝色/中性色，`pass_candidate` 使用绿色，`concerns` 使用红色，`needs_human_triage` 使用琥珀色；颜色不由最高 finding 严重度、风险变化或 remediation claim 决定，并始终配合文字。
- 变更摘要复用现有 change/file/finding 关系，展示“改了什么、为什么、影响什么”、文件数、增删行和文件影响列表；文件可跳到对应 finding/diff，不新增图表或第二套摘要 schema。
- finding 卡片区分“当前裁定、模型原判断、按正式 run 顺序的反馈记录”。误报使用中性语义并写明“不计入风险”；已存在的 severity override 只是暂时停用，不被删除，重新确认有效时可以再次生效。
- diff 证据采用 Diff2Html 风格的单栏 unified diff 阅读语法：文件头、增删统计、旧/新行号、红绿行和 finding 关键行。完整可信 hunk 继续保存在 `audit.json`；超过现有展示阈值时只由 renderer 生成 finding 周边可信节选，保留全部关键行并明确省略行数。代码长行不折行，hunk 在固定边界内按需上下/左右滚动，文件头与节选说明留在滚动区外；不引入第二套截断逻辑、Diff2Html、语法高亮或其他运行时依赖，也不提供双栏切换、搜索、复杂筛选、常驻侧边栏、同步滚动或全屏模式。
- 同 diff 发生过正式人工修订时才展示纵向反馈历史，明确 `comment: null` 为删除评论、`severity: null` 为恢复模型严重度；用户端 `created_at` 只展示，不决定顺序。只有初次模型审查时不渲染历史区块。
- 修复复审存在时才展示独立来源与验证面板，显示来源 finding、用户声明、claim 状态、证据与当前新审查结果；旧 diff 的 runs 不进入当前反馈历史，跨 diff 风险只并列显示“来源 / 当前”，不用箭头暗示因果。
- 没有 remediation、finding、feedback history 或 fixes 时，整个对应 section 连同标题和空框一起不渲染。schema、run id 与 hash 集中到页尾默认折叠的“报告身份与校验信息”。
- “评论与严重度”和“报告身份与校验信息”使用原生 `<details>` / `<summary>`，统一显示随 `open` 状态旋转的展开箭头，不用 JavaScript 维护折叠状态。反馈导出状态位于按钮组下方，通过 `aria-live` 和中性/成功/警告三种语义色反馈结果，不与主操作争抢一行。
- 所有关键交互最小触控区 44×44；关键正文与移动端操作文字不低于 16px；页面本身不得横向溢出，只有 diff hunk 等技术证据可在有最大高度的边界内按需双向滚动，并可通过键盘聚焦；补齐 skip link、可见焦点和必要 aria/live 语义。

### 4. GitHub Pages 从入口页升级为产品说明

- 维持 `/docs` 下纯静态 HTML/CSS/少量原生 JS 和 `.nojekyll`，不引入框架、构建链、外部字体、跟踪脚本或动画库。
- 提供 English 与简体中文等价页面，含正确 `lang`、语言切换、canonical、hreflang/x-default、description、Open Graph/Twitter、favicon 和有意义的图片替代文本。
- 信息顺序固定为：价值主张与产品边界 → 为什么需要 → 审计闭环如何工作 → audit report 与真实证据 → 独立产品/宿主集成边界 → 可复制安装命令 → FAQ → footer。
- 复用现有截图与最终同一份真实 dogfood 报告；不建设案例画廊，不写无法证实的营销数据。JavaScript 仅用于安装命令复制并提供失败回退。
- README 只局部重写读者最先接触的产品定位、审计闭环、报告样例和安装/文档入口；先盘点既有 SVG/PNG/GIF 和链接，只更新与当前产品语义不符、重复或视觉质量不足的素材，避免 README 与 Pages 长文重复。
- 开发时先核验仓库实际 Pages source/config；本方案假设 `/docs` 为候选源，不把本地目录存在误写成线上配置已确认。

## Waves / Priority

- [ ] Wave 1 · P0：补齐显式 focus，并冻结 feedback revision 与 remediation re-audit 的输入、身份和无副作用边界。
- [ ] Wave 2 · P0：实现修复复审来源校验、prompt `v0.6` claim 审查、一跳 provenance 和独立新 audit 生成。
- [ ] Wave 3 · P0/P1：端到端收口 audit report 的页头真相、变更摘要、单栏 diff、动态模块、误报、同 diff 反馈历史、修复复审、移动端和无障碍语义。
- [ ] Wave 4 · P1：收口 EvidentLoop GitHub Pages、README 局部叙事与共享素材，补齐双语产品信息架构、真实证据、安装入口、SEO 与无障碍。
- [ ] Wave 5 · P1：完成定向/全量测试、代表性视觉验收、包与 Skill 兼容门禁和两轮真实 dogfood。
- [ ] Wave 6 · P2：用户审计候选后，另行决定提交、发布、Pages 上线和方案归档；不得随开发自动执行。

## Key Decisions

- 同一个复合方案包覆盖早期产品闭环是合理的，但按 Wave 分离 P0 语义正确性、P1 可理解性与公开说明、P2 外部发布，避免同时开发时失去门禁。
- 修复关系必须显式声明且逐 finding 绑定；路径重合、提交说明、相邻时间或 finding 消失只能作为人类线索，不能成为机器事实。
- 新 reviewer 对当前完整 diff 独立审查；修复 claim 是额外结论，不替代当前 verdict，也不因没有同名 finding 就自动 `supported`。
- 只保留直接前驱引用。新 audit 的 runs 不拼接旧 diff 历史；无需 audit series 数据库、全局 registry、跨仓库状态机或自动 matching 服务。
- schema `0.4` 已足够承载 claim 和 namespaced provenance；remediation extension 使用版本化的小契约、唯一 serializer 和语义校验，不靠 renderer 临时解释任意字典。本轮不升级核心 schema，不改变风险算法和 feedback JSONL 协议。
- prompt 升至 `v0.6` 是必要的正式契约变化；package `0.1.0a3`、renderer `0.4` 随候选同步。
- audit HTML 不整体换肤。报告页头之后先展示变更摘要；可选业务模块无数据时完整省略；diff 使用自有单栏 unified 展示；报告身份默认折叠。上述变化必须连同 renderer context、模板、CSS、JS、fixture 和测试一起修改，不能只调颜色或间距。
- GitHub Pages 需要整体重写信息架构，因为当前单屏英文页无法独立讲清产品；复用 Sopify 的双语、SEO、skip link、安装复制和静态交付经验，不复用其品牌皮肤、超大字体或 `~go` 叙事。
- README 只做局部重写和素材校准，不复制 Pages 全文；两者共享产品事实、真实 dogfood 报告和权威安装入口，但按各自阅读场景组织内容。
- 报告、Pages 与 README 只共享视觉语言和产品事实，不共享运行时 CSS/JS；audit report 继续满足单文件自包含与离线可核验。
- 不引入 Diff2Html 或其他前端框架、设计系统平台、图表、暗色主题、双栏 diff、搜索/复杂筛选、常驻侧边栏、语法高亮依赖、同步滚动、全屏模式、复杂动效、远程字体、分析埋点或大规模截图金丝雀矩阵。
- 旧 `20260720_local_diff_focus` 与 `20260720_audit_focus_feedback_clarity` 的必要范围已被本方案吸收；旧方案保持不变且不再单独合入或实施。

## Acceptance Criteria

- 显式非空 focus 原样进入 ReviewPack 与冻结 prompt；缺省保持 `None`；空白 focus 在读取 diff、创建输出目录或 staging 前失败。
- feedback revision 始终保留来源 `diff_version`、不调用 reviewer、不改旧报告；run 顺序是权威顺序，`created_at` 只作展示，null 反转语义和误报后 severity override 的停用/恢复均有测试。
- remediation 输入只有在来源原始字节、`report_version`、非空 `diff_version`、finding id 与 fingerprint 全部匹配时才接受；不含版本的旧报告、相同 diff、未知/过期 finding 均明确失败且不留下 staging。
- 当前 diff 可含无关改动，但报告只对显式选择的旧 finding 声明修复关联；最终 artifact 不泄露来源绝对路径。
- 每个修复目标都有 `supported / challenged / partial / unknown` claim；“旧 finding 未再出现”单独不能得到 `supported`。新 audit verdict 真实反映当前完整 diff。
- 新 audit 只引用直接前驱；remediation extension 版本、字段和 claim 关联通过统一语义校验；当前 runs 不含旧 diff 的 run。连续复审可沿一跳 provenance 追溯，旧 audit 字节保持不变，`diff_version` 与 `report_version` 均由正式输入/输出字节确定。
- 页头分开保留 `review_status` 与 verdict，并明确人工裁定通知；边框色与整体状态确定对应且不只靠颜色表达。变更摘要紧随页头，用现有数据说明变更目的、文件影响和增删规模，不重复堆叠相同风险信息。
- 单栏 unified diff 同时支持增加、删除、上下文、旧/新行号和 finding 关键行，文件入口可从变更摘要直达证据；长行保持原貌并在 hunk 内横向滚动，很多行继续复用 renderer 的可信节选与明确省略计数，极端节选在限定高度内纵向滚动，完整 hunk 不从 `audit.json` 删除；不加载 Diff2Html 或语法高亮依赖。
- 同 diff 反馈历史与跨 diff 修复来源分开；只有存在相应数据才渲染整个模块。反馈历史可以在不阅读 hash 的情况下回答“用户对哪个 finding 做了什么、当前结果为何变化”，修复来源与验证可以回答“选择了哪个旧 finding、声明是否被验证”；跨 diff 风险不使用因果箭头。
- 误报 finding 使用中性视觉且明确不计入风险；技术 hash 完整、可复制但默认下沉；原生 details 始终有可见展开箭头，导出状态位于操作按钮下方并通过 live region 更新；页面无整体横向溢出，关键控件达到 44×44，375px 移动端可完成阅读和反馈操作。
- Pages 英中两页内容等价，元数据、语言互链、跳转、图片语义、安装复制与无 JS 回退有效；README 首屏定位、闭环、报告样例和安装入口与当前产品一致，过期或重复素材已盘点并按需替换；三处链接指向同一份可核验真实报告和权威文档入口。
- schema `0.4` 与反馈协议/风险算法兼容；prompt `v0.6`、renderer `0.4`、package `0.1.0a3` 的源码、Skill、doctor、构建物与测试一致。
- 定向 pytest、全量 pytest、Ruff、schema/package resource、wheel/sdist、Skill 分发、HTML trace/link/metadata 校验全部通过；视觉验收使用少量代表性页面而非快照矩阵。
- 真实 dogfood 至少包含：初次 finding、显式修复关联后的新 diff 独立复审、修复 claim，以及同 diff 人工裁定路径；候选证据经用户审计前不提交、不推送、不发布、不改线上 Pages。

## Constraints / Not-in-scope

- 本方案包位于基于 `origin/main@fcefb77083d32b034e56b04dcd085dcf5a835550` 的当前 feat 分支；后续实施开始前需重新核验隔离工作树，不 pull、stash、覆盖或暂存其他工作区已有改动。
- 本轮只收口并校验 `plan.md`、`tasks.md` 与两份样例资产；不修改业务代码、测试、旧方案、长期知识、版本、文档站或历史报告。
- Wave 1–5 属于同一个复合实施链，方案获批并明确授权开发后可按优先级连续推进，在每个 Wave 末做验证门禁；只有出现语义决策、证据失败或范围漂移才停车。实施产物的 commit、push、release、PyPI 与 GitHub Pages 发布始终需要独立授权。
- 不回写既有 audit 文件。旧报告只作为不可变来源，新功能只影响新生成或用户主动重新渲染的报告。
- 不承诺跨任意大规模重构自动匹配旧 finding，不建立 remediation backlog、工单系统或宿主专属状态。
- Sopify 只是首个 dogfood/参考宿主；EvidentLoop 的 CLI、Python API、Skill、artifact 与 Pages 叙事保持产品中立。

## Status / Progress

- [x] 已在最新 `origin/main` 上创建并切换当前 feat 分支，未覆盖进入本轮前的工作区改动。
- [x] 已批判审计当前 audit HTML 的桌面、移动端、触控、信息层级和反馈语义。
- [x] 已审计当前 EvidentLoop Pages，并对照最新 Sopify Pages 提炼可复用结构与明确不复用项。
- [x] 已生成独立可交互 audit report 成品样例，并记录数据、context、模板、脚本和冗余删除边界；未修改生产 renderer。
- [x] 已确认 schema `0.4` 现有 claims、关系边和 namespaced extensions 可承载最小修复复审，无需架构级方案。
- [x] 已按用户确认收口单栏 diff、动态模块、整体结论色、跨 diff 来源卡片、remediation 小契约和“报告身份与校验信息”。
- [x] 方案已 Ready，并获准仅提交、推送本方案包；尚未授权开发、业务代码提交或发布。

## Next

提交并推送本方案包后停车；明确授权开发后再从 Wave 1 连续推进至候选审计点，任何实施产物提交、推送或发布另行确认。
