# AgentForge Dashboard / 工作台设计

更新日期：2026-10-02

## 1. 页面目标

工作台是 AgentForge 的默认首页，用于让用户在 10 秒内了解：

```text
平台现在有什么
↓
最近发生了什么
↓
当前 Agent 是否正常
↓
接下来可以做什么
```

第一版只实现页面结构、视觉、Mock 数据、关键指标、最近资源、快速入口和真实接口接入预留，不开发真实统计后端。

## 2. 路由

```text
/dashboard
/ → /dashboard
```

## 3. 顶部欢迎区

标题示例：

```text
下午好
欢迎回到 AgentForge
```

副标题：

```text
管理、调试并观察你的 AI Agent
```

右侧快捷操作：

- 创建 Agent → `/agents/create`。
- Chat 调试 → `/chat`。

项目品牌统一使用 `AgentForge`，不使用需求附件中的 `Enterprise AI Agent Platform` 作为产品名。

## 4. 核心指标

第一屏只展示 4 张 Card：

- Agent 数量，并展示已发布数量。
- 知识库数量，并展示文档数量。
- 今日运行次数，并展示成功率。
- Token / Cost，并展示今日 Token 和成本。

桌面布局：

- 1440px：4 列。
- 1024px：2 列。

不在第一屏堆叠十几个 KPI。

## 5. Agent 状态概览

使用轻量 Card 展示：

```text
已发布
草稿
离线
```

使用简单 Progress 或 Badge，不引入复杂饼图。

## 6. 快速开始

展示 4 个入口 Card：

- 创建 Agent → `/agents/create`。
- 创建知识库 → `/knowledge-bases`。
- 添加 Tool → `/capabilities`。
- 调试 Agent → `/chat`。

每个入口包含图标、名称和一句简短说明。卡片需要保持可点击状态和 Hover 反馈。

## 7. 最近 Agent

使用 Card 或简洁列表展示：

- Agent 名称。
- 发布状态。
- 模型。
- 知识库数量。
- Tool 数量。
- MCP 数量。
- 调试入口。

右上角“查看全部”跳转 `/agents`。Agent 项可跳转 `/agents/:id` 或 `/chat` 调试。

## 8. 最近运行

使用 Table 展示：

- Agent。
- 状态。
- 耗时。
- Token。
- 时间。

点击行跳转 `/runs/:traceId`，右上角“查看全部”跳转 `/runs`。

## 9. 最近知识库

轻量展示：

- 知识库名称。
- 文档数量。
- Chunk 数量。

点击跳转 `/knowledge-bases/:id`。

## 10. 运行状态

展示以下服务状态：

```text
API            ● 正常
Model Gateway  ● 正常
RAG Service    ● Demo
Tool Gateway   ● Demo
MCP Gateway    ● Demo
```

教育版必须明确显示 `Demo`，不将教学能力伪装成生产服务。

## 11. 今日使用概览

只展示简单数字和 Progress：

- Runs。
- Successful。
- Failed。
- Average Latency。
- Average Tokens。

不引入复杂 BI 图表。

## 12. Token / Cost 趋势

如需要展示最近 7 天 Token 使用，只使用轻量 CSS Bar 或简单折线视觉，不为 Dashboard 专门引入 ECharts。

Cost 不做独立一级页面；Dashboard 展示总体 Token、总成本和趋势概览。

## 13. 当前环境

页面底部增加教育版说明卡：

```text
当前运行模式  教学版
Model Gateway  Demo
RAG            Demo Retriever
Tool           Demo Tool Gateway
MCP            Demo MCP Gateway
```

下方说明后续可升级：

```text
PostgreSQL / Redis / Milvus / DeepSeek / Real MCP
```

## 14. 学习路径

使用轻量引导展示：

```text
1. 创建 Agent       ✓
2. 添加知识库        ✓
3. 添加 Tool / MCP   ✓
4. Chat 调试         →
5. 查看 Trace        →
6. 分析 Cost         →
```

不设计成课程系统，只作为产品引导。

## 15. 空状态

没有 Agent 时：

```text
开始创建你的第一个 Agent

Agent 可以绑定模型、知识库、Tool 和 MCP，
并通过 Runtime 执行完整 AI 工作流。

[创建 Agent]
```

没有运行记录时：

```text
暂无运行记录

前往 Chat 调试完成第一次 Agent Run。

[开始调试]
```

## 16. Mock 数据

统一放在：

```text
src/mock/dashboard.ts
```

建议包含：

```text
dashboardStats
recentAgents
recentRuns
recentKnowledgeBases
serviceStatus
usageSummary
```

不得把 Mock 数据直接写在页面组件中。

## 17. TypeScript 类型

类型文件：

```text
src/types/dashboard.ts
```

至少定义：

```text
DashboardStats
RecentAgent
RecentRun
ServiceStatus
UsageSummary
```

避免大量使用 `any`。

## 18. 组件拆分

```text
src/views/dashboard/
└── Dashboard.vue

src/components/dashboard/
├── WelcomeHeader.vue
├── StatCard.vue
├── QuickStart.vue
├── RecentAgentList.vue
├── RecentRunTable.vue
├── RecentKnowledgeBases.vue
├── ServiceStatus.vue
├── UsageOverview.vue
└── LearningPath.vue
```

## 19. 联动与 API 预留

工作台是产品导航入口，所有模块需要预留跳转：

```text
Agent         → /agents
知识库         → /knowledge-bases
能力中心       → /capabilities
Chat 调试      → /chat
运行记录       → /runs
具体 Trace     → /runs/:traceId
```

真实数据接入时使用独立 API 模块，不在 Dashboard 组件中散落 Axios 调用。

## 20. 当前禁止事项

第一版不开发真实统计 SQL、Cost Aggregation、监控平台、Grafana、Prometheus、OpenTelemetry Metrics、登录权限、租户数据和复杂图表系统。全部使用 Mock。

## 21. 验收

- 有欢迎区域。
- 有 4 个核心指标。
- 有快速开始。
- 有最近 Agent。
- 有最近 Run。
- 有最近知识库。
- 有服务状态。
- 明确标注 Demo 能力。
- 所有入口可以跳转到对应页面。
- 与 Agent、Chat、Trace 页面视觉一致。
