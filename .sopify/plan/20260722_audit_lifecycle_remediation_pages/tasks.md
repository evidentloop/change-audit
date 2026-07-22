# 任务清单: EvidentLoop 审计闭环、修复复审与公开产品页

目录: `.sopify/plan/20260722_audit_lifecycle_remediation_pages/`

## Wave 1 · P0 输入与身份边界

- [ ] 1.1 为 `evidentloop prepare`、local-diff Python API 与官方 Skill 增加单个可选 `focus`，只传递用户明确提供的原文。
  - 验收：缺省为 `None`；显式空白值在读取 Git diff、分配输出目录和创建 staging 前失败；不从 diff、路径、历史报告或宿主状态推断 focus。
- [ ] 1.2 将两类 revision 的公开契约写入 API/CLI/Skill 文档：同 diff 人工裁定继续走 `feedback_revision`，代码修改后必须走独立 remediation re-audit。
  - 验收：没有“自动判断是否因 finding 改码”的分支；示例明确用户需选择来源 audit、finding id/fingerprint 和当前新 diff。
- [ ] 1.3 定义并实现最小 remediation 请求对象与前置校验顺序。
  - 验收：先校验来源 audit 原始字节、计算 `report_version`、确认非空 `diff_version`、匹配最新 run 的 finding id/fingerprint，再读取/冻结当前 diff；相同 diff、legacy null 版本、未知/过期/重复 finding 在输出目录或 staging 副作用前失败。

## Wave 2 · P0 独立修复复审

- [ ] 2.1 将已验证的来源 finding 摘要与用户修复声明作为受限上下文加入当前完整 diff 的 reviewer 输入，并把正式 prompt 升至 `v0.6`。
  - 验收：reviewer 同时审查完整当前 diff 和逐 finding 修复声明；prompt 明确禁止用路径相似、提交信息、时间顺序或 finding 未重现单独证明修复。
- [ ] 2.2 复用 schema `0.4` 的 `summary_audit.claims` 与 `supports_claim` / `challenges_claim`，让 adapter 输出逐目标 `supported / challenged / partial / unknown`。
  - 验收：每个显式修复目标有稳定 claim id 和证据关系；adapter 不再对 remediation 场景统一写 `not_audited`；当前 audit verdict 仍由当前完整审查独立计算。
- [ ] 2.3 在 `extensions.evidentloop.remediation` 写入最小一跳 provenance，并保持版本与不可变性契约。
  - 验收：正式对象固定为 version `1`、直接前驱 `report_version` / `diff_version` 和逐目标 finding id/fingerprint、用户声明、`claim_id`；请求、serializer 与语义校验共用单一入口；校验目标唯一且 `claim_id` 精确指向现有 claim；extension 不重复 claim 状态、当前 verdict/风险或当前 `diff_version`，不记录绝对路径；旧 audit 原始字节不变。
- [ ] 2.4 覆盖混合 diff 与连续复审，不增加中央状态。
  - 验收：当前 diff 可同时含修复和其他改动，关联只适用于所选 finding；新 audit 的 runs 只含当前 diff 的模型审查及后续同 diff 人工修订，不复制旧报告 runs；下一轮只引用本轮作为直接前驱即可形成可追溯链，不扫描历史目录、不建 registry、不跨报告自动匹配。

## Wave 3 · P0/P1 Audit report 端到端收口

- [ ] 3.1 重排 renderer context 与页头信息，并把变更摘要提升为第一个业务区块。
  - 验收：`review_status` 和 verdict 独立；`partial / failed` 与“基于人工裁定，未重新审查代码”始终在页头可见；页头边框色由审查完整性与整体 verdict 确定，不受 finding 严重度、风险变化或 remediation claim 影响且不只靠颜色表达；变更摘要复用现有 change/file/finding 数据说明变更目的、文件影响、增删规模和证据入口；相同风险信息不重复三遍。
- [ ] 3.2 将 finding 展示拆成当前裁定、模型原判断和正式 run 顺序的反馈记录。
  - 验收：误报使用中性状态并写明不计入风险；severity override 在误报时停用但不删除，重新确认有效时恢复生效；`severity: null` 是恢复模型严重度，`comment: null` 是删除评论；`created_at` 只作标签；可信代码证据使用自有单栏 unified diff，含文件头、增删统计、旧/新行号、红绿行和 finding 关键行；完整 hunk 保留在 `audit.json`，超过现有阈值时只由 renderer 生成保留全部关键行、带明确省略计数的可信节选，不在 adapter、模板或 JS 再做截断。
- [ ] 3.3 用纵向反馈轮次卡代替移动端宽表格，将人类动作与风险/待处理数变化置前，完整技术身份放入可复制折叠区。
  - 验收：只展示当前 diff 的正式 runs；只有存在 `feedback_revision` 时才渲染整个历史模块；不展开 hash 也能说明“对哪个 finding 做了什么、当前结果为何变化”；正式 run 链决定顺序；移动端不依赖横向阅读历史。
- [ ] 3.4 新增独立 remediation 面板，展示来源 finding、用户声明、claim 状态、关键证据与当前新审查结果。
  - 验收：旧报告只作为独立来源卡片，不进入当前 runs 或反馈历史；来源和当前风险并列展示而不用箭头暗示因果；`supported / challenged / partial / unknown` 不能被误读成当前整体 verdict；无 remediation 时整个模块不渲染。
- [ ] 3.5 端到端调整模板、CSS、原生 JS、fixture 与 trace 校验，保留自包含和现有主体风格。
  - 实现参考：assets/audit-report-concept.html 的信息层级与 assets/audit-report-concept-review.md 的端到端边界；样例不是生产 fixture 或截图金丝雀。
  - 验收：remediation、finding、feedback history、fixes 无数据时对应 section 连标题和空框一起省略；schema、run id、hash 集中到默认折叠的“报告身份与校验信息”；“评论与严重度”和报告身份使用原生 details/open 状态及始终可见的展开箭头，不增加 JS 折叠状态；导出状态位于按钮组下方，通过 aria-live 与中性/成功/警告语义色更新；关键交互至少 44×44；关键正文/移动端操作文字至少 16px；有 skip link、可见焦点、reduced-motion 和必要 aria/live；页面无整体横向溢出，代码长行保持 `pre` 且不折断，diff/hunk 在有最大高度的容器内按需上下/左右滚动，滚动区可键盘聚焦且文件头与节选说明保持在外部可见；不引入 Diff2Html、框架、主题、图表、双栏切换、搜索、复杂筛选、常驻侧边栏、语法高亮依赖、同步滚动或全屏模式。

## Wave 4 · P1 GitHub Pages、README 与共享素材

- [ ] 4.1 先核验实际 GitHub Pages source/config，再在 `/docs` 候选源内建立英文与简体中文等价页面和共享静态资产。
  - 验收：`index.html` / `zh-CN.html`、站点 CSS、最小复制 JS 与 `.nojekyll` 边界清楚；不把目录约定当成线上配置证据，不引入构建链、远程字体或跟踪脚本。
- [ ] 4.2 按产品心智重写页面结构：价值与边界、问题、审计闭环、报告/真实证据、宿主集成边界、安装、FAQ、footer。
  - 验收：页面独立说明 EvidentLoop，不要求读者先理解 Sopify；真实报告只保留一个权威入口；不复制 Sopify 品牌皮肤、超大字体或工作流命令。
- [ ] 4.3 补齐双语互链、SEO/社交元数据、图片语义、安装复制回退和无障碍响应式细节。
  - 验收：正确 `lang`、canonical、hreflang/x-default、description、OG/Twitter、favicon、skip link、alt 与尺寸；复制控件有状态反馈和无 Clipboard API 回退；375/768/1024/1440 下无页面横向溢出，触控区不小于 44×44。
- [ ] 4.4 局部重写 README 的首屏定位、核心闭环、报告示例和安装/文档入口，并盘点既有素材。
  - 验收：README 不复制 Pages 全文，不要求读者先理解 Sopify；过期、重复、与当前产品语义不符或视觉质量不足的 SVG/PNG/GIF 明确替换或删除，仍有效的素材复用；文案、alt、尺寸、相对链接和移动端宽度有效。
- [ ] 4.5 将最终真实 dogfood 报告与经筛选的高价值素材接入 Pages、README 和文档的同一产品事实，不复制报告运行时资源。
  - 验收：入口指向同一可核验 artifact 和权威安装/文档地址，不保留互相冲突的截图或旧结论；图片经过尺寸、格式、加载和敏感信息检查；audit HTML 继续单文件自包含，Pages、README 与报告只共享视觉语言和内容事实。

## Wave 5 · P1 验证、候选与 dogfood

- [ ] 5.1 更新 focus、remediation、adapter、feedback revision、renderer、Pages、Skill 和版本门禁的定向测试。
  - 验收：覆盖所有前置失败无副作用、remediation version/必填字段/目标唯一性/claim 关联、legacy/null、相同/混合 diff、跨 diff runs 不拼接、四类 claim、未重现不等于修复、null 反转、severity 停用/恢复、页头色映射、变更摘要、单栏 diff、100+ 行 hunk 的完整 JSON 与 renderer 可信节选、相距较远的多个关键行、超长代码行不折行且局部双向滚动、空模块不渲染、原生 details 展开标识、导出状态 live region、报告身份折叠、44px/移动端结构、双语 metadata/link 与绝对路径泄露。
- [ ] 5.2 运行全量 pytest、Ruff、schema/package resource、wheel/sdist、doctor、Skill 分发、HTML trace 和静态链接/元数据校验。
  - 验收：schema `0.4`、feedback JSONL 和风险算法兼容；prompt `v0.6`、renderer `0.4`、package `0.1.0a3` 在源码、构建物、Skill 与 doctor 中一致。
- [ ] 5.3 做小而有代表性的视觉验收，不建立截图矩阵。
  - 验收：桌面与 375px 移动端分别检查普通模型报告、同 diff 多轮反馈、修复复审，以及 Pages 英中页面；用一个同时含超长行与大 hunk 的 finding 确认状态不是仅靠颜色表达、滚动区键盘焦点可见、横向阅读不撑宽页面、纵向阅读不把整页无限拉长，且滚动到边界后仍可继续浏览报告。
- [ ] 5.4 使用候选版本完成一个公开仓库两轮 dogfood：先产出 finding，再由用户显式选择 finding 关联新 diff 进行独立复审；另验证同 diff 人工裁定路径。
  - 验收：来源/新版本、修复 claim、当前 verdict 与一跳 lineage 可核验；报告无本地绝对路径或敏感信息；候选与证据冻结后停车等待用户审计。

## Wave 6 · P2 外部交付停车点

- [ ] 6.1 用户明确批准候选后，才按独立授权提交精确文件、推送分支，并决定 PR、tag、PyPI/GitHub prerelease 与 Pages 上线顺序。
  - 验收：开发完成不自动触发外部动作；Release 与 GitHub Pages 分别核验并分别留证，线上公开物通过安装、doctor、Skill discovery、链接和报告 smoke 后才宣称完成。
- [ ] 6.2 按 `knowledge_sync` 更新长期约定、验证 receipt 和方案状态；只有显式 `~go finalize` 才归档。
  - 验收：旧两份 focus/feedback 方案保持不变且不单独实施；原工作区用户改动和既有历史报告均未被覆盖。
