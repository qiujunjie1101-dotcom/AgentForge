# AgentForge 信息架构与路由

更新日期：2026-10-02

## 1. 六个核心一级页面

```text
AgentForge
│
├── ① 工作台 Dashboard
│
├── ② Agent 管理
│   ├── Agent 列表
│   └── Agent 配置 / 编辑
│
├── ③ 知识库
│
├── ④ 能力中心
│   ├── Tool
│   └── MCP
│
├── ⑤ Chat 调试
│
└── ⑥ Trace / 运行记录
```

## 2. Cost 位置

Cost 暂不设置独立一级页面：

- 工作台展示总体 Token、总成本和趋势概览。
- Trace 详情展示单次运行的输入 Token、输出 Token、总 Token 和调用成本。

这样可以避免页面过散，并让成本数据与运行上下文绑定。

## 3. 已明确路由

```text
/dashboard               工作台
/agents                   Agent 列表
/agents/:id               Agent 配置 / 详情
/knowledge-bases          知识库列表
/knowledge-bases/:id      知识库详情
/capabilities             Tool / MCP 能力中心
/capabilities/tools/:id   Tool 详情
/capabilities/mcp/:id     MCP Server 详情
/chat                     Chat 调试
/runs                     Trace / 运行记录
/runs/:traceId            Trace 详情
```

根路径 `/` 可重定向到 `/dashboard`。

## 4. 页面开发策略

- 后续由用户指定页面开发顺序。
- 当前页面需要的全局框架可以实现，但其他业务页只保留占位路由。
- 页面之间的跳转应预留稳定路由，例如 Tool 或 MCP 绑定的 Agent 可跳转到 `/agents/:id`。
- 不因为实现一个页面而提前开发其他页面业务。

## 5. 统一侧边栏

产品导航统一为：

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

只保留当前教学版真正有价值的入口，不增加登录、组织、租户、权限、Billing、Marketplace、Workflow Canvas 或复杂设置中心。

## 6. 页面关系

```text
Dashboard
   ↓
创建 Agent
   ↓
绑定 Knowledge Base
   ↓
绑定 Tool / MCP
   ↓
Chat 调试
   ↓
Agent Runtime
   ↓
Trace / Run
```

具体跳转约定：

```text
Agent → /chat?agentId=:id
Chat 完成 Run → /runs/:traceId
Trace 重新调试 → /chat?agentId=:id
知识库绑定 Agent → /agents/:id
Tool / MCP 使用 Agent → /agents/:id
```

## 7. 页面命名

一级页面统一使用：

```text
工作台
Agent 管理
知识库
能力中心
Chat 调试
运行记录
```

`Trace`、`Run`、`Span` 等英文专业术语只在详情和技术信息中使用。
