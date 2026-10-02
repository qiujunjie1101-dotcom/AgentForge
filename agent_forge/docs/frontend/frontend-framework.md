# AgentForge 前端整体框架收口

更新日期：2026-10-02

## 1. 收口目标

本阶段不新增业务能力，统一已经设计好的页面雏形，使 AgentForge 成为一个完整、连贯、可演示的 AI Agent 教学平台。

统一范围：

- App Layout。
- Sidebar。
- Header。
- Breadcrumb。
- Router 关系。
- 页面间跳转。
- Page Header。
- Button、Card、Badge、Empty State、Loading、Error、Toast、Dialog。
- Demo 标记。

不重写已经完成的核心页面，不开发真实后端。

## 2. 产品品牌

附件中的 `Enterprise AI Agent Platform` 仅作为历史描述，不作为品牌名称。产品品牌统一为：

```text
AgentForge
```

中文描述可使用：

```text
企业级 AI Agent 教学平台
```

## 3. App Layout

```text
┌─────────────────────────────────────────────────────────────┐
│ Sidebar │                    Main                           │
│         │ ┌───────────────────────────────────────────────┐ │
│         │ │ Header / Breadcrumb                           │ │
│         │ ├───────────────────────────────────────────────┤ │
│         │ │                                               │ │
│         │ │             Router View                       │ │
│         │ │                                               │ │
│         │ └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

建议目录：

```text
src/layouts/AppLayout.vue
src/components/layout/AppSidebar.vue
src/components/layout/AppHeader.vue
src/components/layout/AppBreadcrumb.vue
src/components/layout/EnvironmentBadge.vue
```

## 4. Sidebar

展开宽度建议 240px～260px，收起宽度 64px～72px。支持展开和收起，收起时只显示图标，Hover 使用 Tooltip。

导航顺序：

```text
AgentForge

工作台

构建
├── Agent 管理
├── 知识库
└── 能力中心

调试与运行
├── Chat 调试
└── 运行记录
```

正式图标使用 Lucide Icons，不使用 Emoji。Emoji 只允许出现在教学说明或 Mock 内容中。

底部展示：

```text
当前环境
● 教学版
```

点击可弹出环境信息：Demo Mode、Demo Model Gateway、Demo RAG、Demo Tool、Demo MCP。

## 5. Header 与 Breadcrumb

Header 结构：

```text
Breadcrumb                                      API 状态  帮助  用户
```

用户区域使用 `Demo User`，不实现真实登录。

所有详情页必须使用统一 Breadcrumb：

```text
Agent 管理 / 电商客服 Agent
知识库 / 售后退款知识库
能力中心 / Tool / query_order
运行记录 / trace_a91e772
```

Breadcrumb 节点可点击返回上一级。

## 6. Router 统一配置

每个路由建议使用：

```ts
meta: {
  title: 'Agent 管理',
  icon: 'Bot',
  breadcrumb: true
}
```

详情页可声明：

```ts
meta: {
  title: 'Agent 详情',
  parent: '/agents'
}
```

统一路由表：

```text
/                         redirect /dashboard
/dashboard                工作台
/agents                   Agent 列表
/agents/create            Agent 创建
/agents/:id               Agent 编辑 / 详情
/knowledge-bases          知识库列表
/knowledge-bases/:id      知识库详情
/capabilities             能力中心
/capabilities/tools/:id   Tool 详情
/capabilities/mcp/:id     MCP 详情
/chat                     Chat 调试
/runs                     运行记录
/runs/:traceId            Trace 详情
```

## 7. 页面宽度与容器

- 大多数后台页面 `max-width: 1600px`。
- 主内容 Padding 24px～32px。
- Chat 调试和 Trace 详情可以使用更宽的可用空间。
- 优先保证 1440px、1280px 和 1024px。

## 8. 视觉规范

整体背景：`#F7F8FA` 或 Tailwind `bg-muted/30`。

Card：

- 白色。
- 轻边框。
- `rounded-xl`。
- `shadow-sm`。
- Hover 时轻微强化边框。

禁止大阴影、强浮层、玻璃拟态、大面积渐变。

统一字体层级：

```text
页面 Title       24px / 600
模块 Title       16px～18px / 600
正文             14px
辅助信息         12px～13px
```

## 9. 公共页面组件

```text
src/components/common/
├── PageHeader.vue
├── EmptyState.vue
├── StatusBadge.vue
├── RiskBadge.vue
├── DemoBadge.vue
├── CodeBlock.vue
├── ConfirmDialog.vue
├── LoadingCard.vue
└── CopyButton.vue
```

`PageHeader` 统一接收 title、description、actions 和 breadcrumb。

`EmptyState` 统一接收 icon、title、description 和 action。

Loading 统一提供 Skeleton Card、Skeleton Table 和 Skeleton Detail，不使用全屏白屏 Loading。

Error State 统一展示“加载失败 / 无法获取当前数据 / 重新加载”，接口失败同时使用 Error Toast，不使用 `alert()`。

## 10. Button / Badge / Dialog

按钮层级统一：

- Primary：创建、上传、发送、运行测试。
- Secondary：取消、查看详情、重新运行。
- Ghost：复制、更多、返回。
- Danger：删除。

Badge 分类：状态、风险、Demo、模型。颜色保持克制。

语义色：

```text
Success → Green
Warning → Amber
Error   → Red
Running → Blue
Neutral → Gray
AI      → Indigo / Violet
```

创建类操作统一使用 Dialog。危险操作使用确认文案：

```text
确认删除？
删除后当前资源将无法恢复。
[取消] [删除]
```

## 11. CodeBlock / JSON

统一使用 `CodeBlock` 展示 JSON、Prompt、Input、Output、Schema 和 Trace，支持：

- 等宽字体。
- 复制按钮。
- 自动换行。
- 最大高度。
- 滚动。

第一版使用 `<pre>` 实现，不引入复杂 JSON Viewer。

## 12. Toast 与 Demo 标记

Toast 类型统一为 Success、Error、Warning、Info，例如：

```text
知识库创建成功
Trace ID 已复制
Tool 测试失败
当前为 Demo 模式
```

所有虚拟能力统一使用 `Demo` Badge：

```text
Demo Model
Demo Retriever
Demo Tool
Demo MCP
Demo Trace
```

用户必须能清楚区分真实 UI 与 Mock 能力。

## 13. 公共类型与目录

公共类型：

```text
src/types/common.ts
```

包括 `ApiStatus`、`ResourceStatus`、`Pagination` 和 `SelectOption`。

推荐整体目录：

```text
src/
├── api/
├── assets/
├── components/
│   ├── common/
│   ├── layout/
│   ├── agents/
│   ├── knowledge-base/
│   ├── capabilities/
│   ├── chat/
│   ├── runs/
│   └── dashboard/
├── layouts/
│   ├── AppLayout.vue
├── mock/
├── router/
├── stores/
├── types/
└── views/
```

不为匹配目录而大规模重构已有代码。

## 14. 页面联动

```text
Dashboard → Agent / Knowledge Base / Capabilities / Chat / Runs
Agent → /chat?agentId=:id
Chat 完成 Demo Run → /runs/:traceId
Trace 重新调试 → /chat?agentId=:id
Knowledge Base → /agents/:id
Tool / MCP → /agents/:id
Run → Agent / Knowledge Base / Tool / MCP
```

全局搜索和 Command-K 本阶段不做。

## 15. 当前禁止事项

不新增登录、注册、组织、租户、权限、Billing、Marketplace、Workflow Canvas、Multi-Agent 画布、模型广场和复杂设置中心。

重点仍然是 Agent 开发学习、Agent Runtime 理解和可视化调试。
