# AgentForge Tool / MCP 能力中心设计

更新日期：2026-10-02

## 1. 页面目标

能力中心统一管理平台内部 Tool 和外部 MCP Server，让用户理解：

```text
Agent
   ↓
Runtime
   ↓
Tool Gateway / MCP Gateway
   ↓
企业系统 / 外部服务
```

第一版只做完整页面雏形、核心交互和 Mock 展示，不连接真实 Tool 或 MCP。

## 2. 路由

```text
/capabilities
/capabilities/tools/:id
/capabilities/mcp/:id
```

能力中心内部使用 Tool 与 MCP Server 两个 Tab，默认进入 Tool。

## 3. 页面顶部

标题：`能力中心`

副标题：`管理 Agent 可调用的业务工具与外部 MCP 服务`

右侧“新建能力”根据当前 Tab 打开新建 Tool 或新建 MCP Server Dialog。

## 4. Tool 列表

说明：`将企业内部业务能力封装为可被 Agent 调用的工具`

支持搜索和筛选：全部、低风险、中风险、高风险、需要审批。

Tool 使用 Card 展示：

- Tool 名称。
- 显示名称。
- 描述。
- 风险等级。
- 是否需要审批。
- 状态。
- 绑定 Agent 数量。
- 查看详情、测试和更多操作。

风险等级映射：

```text
low    → 低风险
medium → 中风险
high   → 高风险
```

高风险可使用克制的警告标识，不使用大面积红色。

空状态：

```text
还没有 Tool

创建第一个 Tool，让 Agent 可以执行实际业务操作。

[创建 Tool]
```

## 5. Tool 详情

顶部展示 Tool 名称、描述和启用状态。

基础信息 Card 展示 Tool ID、Tool Name、描述、风险等级和是否需要审批。

输入参数 Schema 单独使用 Card 展示 JSON。本阶段不实现 Schema 编辑器，可保留禁用的“编辑 Schema”按钮。

返回示例 Card 展示结构化输出，帮助理解模型生成参数、Tool 执行和 Runtime 消费结果的过程。

## 6. Tool 测试面板

输入参数后点击“运行测试”，不调用真实后端，按 Demo 状态展示 Running、Success、耗时和结果。

必须明确标记 `Demo Result`，避免误认为真实系统已经打通。

## 7. 新建 Tool

Dialog 字段：

- Tool Name，必填。
- 显示名称，必填。
- 描述。
- 风险等级。
- 是否需要审批。

本阶段只写入 Mock Store。

## 8. MCP 列表

MCP Server Card 展示：

- 名称。
- 描述。
- 连接状态。
- Tool 数量。
- Resource 数量。
- Prompt 数量。
- 绑定 Agent 数量。
- 查看详情、连接测试和更多操作。

连接状态映射：

```text
CONNECTED    → 已连接
DISCONNECTED → 未连接
ERROR         → 连接异常
UNKNOWN       → 未检测
```

空状态：

```text
还没有 MCP Server

接入 MCP Server，为 Agent 扩展外部工具与资源能力。

[添加 MCP Server]
```

## 9. MCP 详情

顶部展示名称、副标题、连接状态和连接测试按钮。

基础信息 Card 展示 Server ID、名称、Endpoint、Transport 和状态。Endpoint 在第一版中必须明确为 Mock。

能力 Tab：

```text
[Tools] [Resources] [Prompts]
```

Tools 展示能力名称、描述和 Input Schema。Resources 展示 URI 与说明。Prompts 为空时展示“当前 MCP Server 未暴露 Prompt”。

## 10. MCP 连接测试

连接测试 Dialog 依次模拟：

```text
连接 Server
获取 capabilities
获取 tools
获取 resources
```

完成后展示发现的 Tools、Resources 和 Prompts 数量，并明确标记 `Demo Connection Test`。

## 11. 教学提示

页面包含“Tool 与 MCP 的区别”知识卡：

```text
Tool → 平台内部定义的可调用能力
MCP  → 通过 MCP 协议接入的外部能力
```

核心教学结论：

```text
Agent = LLM + Knowledge + Tool + MCP
```

Knowledge 提供知识，Tool 执行平台内部业务能力，MCP 接入外部标准化能力。

## 12. 类型、Mock 与组件

Mock 统一放在：

```text
src/mock/capabilities.ts
```

Tool Mock 至少包含 `query_order`、`create_ticket`、`refund_order`。其中 `refund_order` 为高风险且需要审批。

MCP Mock 至少包含订单 MCP Server、CRM MCP Server、知识检索 MCP Server。订单 MCP 暴露 `query_order_status`、`query_logistics` 和 `policy://refund`。

建议组件：

```text
src/views/capabilities/
├── CapabilityCenter.vue
├── ToolDetail.vue
└── MCPDetail.vue

src/components/capabilities/
├── ToolCard.vue
├── ToolList.vue
├── CreateToolDialog.vue
├── ToolTestPanel.vue
├── MCPServerCard.vue
├── MCPServerList.vue
├── CreateMCPDialog.vue
├── MCPConnectionTestDialog.vue
├── MCPCapabilityTabs.vue
└── CapabilityGuideCard.vue
```

## 13. 当前禁止事项

第一版不开发真实 HTTP Tool、MCP Client、审批流、API Key、鉴权、权限、Runtime、Trace 和 Cost。全部使用独立 Mock。

## 14. 验收

- Tool 列表与详情完整。
- Tool 测试面板可交互。
- MCP 列表与详情完整。
- MCP Tools、Resources、Prompts 可展示。
- MCP 连接测试有演示效果。
- Mock 数据独立管理。
- 页面不依赖真实后端。
