# AgentForge Trace / 运行记录设计

更新日期：2026-10-02

## 1. 页面目标

运行记录用于将每一次 Agent Run 作为完整的可观测记录展示出来，帮助用户完成以下路径：

```text
查看历史 Agent Run
   ↓
定位某一次运行
   ↓
查看完整 Trace
   ↓
查看每个 Span
   ↓
查看 RAG / Tool / MCP / LLM / Cost
```

核心教学关系：

```text
Run   = 一次 Agent 完整执行
Trace = 这次 Run 的执行链路
Span  = 执行链路中的一个具体步骤
```

即：

```text
Run
 ↓
Trace
 ↓
Span
```

第一版只实现页面结构、视觉、核心交互、Mock 数据、Trace Tree、Run 概览和 Span 详情，不连接真实可观测后端。

## 2. 路由

```text
/runs
/runs/:traceId
```

`/runs` 为运行记录列表，`/runs/:traceId` 为 Trace 详情。

## 3. 运行记录列表页

标题：`运行记录`

副标题：`查看 Agent 每一次执行的状态、链路和资源消耗`

顶部提供：

- 搜索 Run ID / Trace ID。
- Agent 筛选。
- 状态筛选。
- 时间范围筛选。
- “什么是 Trace？”教学提示。

状态筛选包括：

```text
全部
Success
Failed
Running
Waiting Approval
```

时间范围默认“最近 24 小时”。

## 4. 运行记录 Table

运行记录适合使用 Table，字段包括：

- Trace ID。
- Run ID。
- Agent。
- 状态。
- 耗时。
- Token。
- Cost。
- 开始时间。

点击整行进入 Trace 详情。行 Hover 时显示“查看详情”和复制 Trace ID 操作。复制成功显示“Trace ID 已复制” Toast。

状态映射：

```text
RUNNING          → 运行中
SUCCESS          → 成功
FAILED           → 失败
WAITING_APPROVAL → 等待审批
```

Badge 风格保持克制，不使用大面积红色或绿色。

## 5. 列表空状态与 Loading

空状态：

```text
暂无运行记录

完成一次 Agent 调试后，运行记录会显示在这里。

[前往 Chat 调试]
```

列表 Loading 使用 Skeleton Table，不使用全屏白屏或全屏 Spinner。

## 6. Trace 详情顶部

Breadcrumb：

```text
运行记录 / trace_a91e772
```

标题：`Trace Detail`

副标题：`查看本次 Agent Run 的完整执行链路`

右上角操作：

- 复制 Trace ID。
- 重新调试。

重新调试跳转：

```text
/chat?traceId=xxx
```

第一版只完成跳转雏形。

详情 Loading 使用 Skeleton Card 和 Skeleton Tree。

## 7. Run Overview

顶部核心指标 Card：

- Status。
- Duration。
- Total Tokens。
- Cost。

基础运行信息：

- Agent。
- Run ID。
- Trace ID。
- Started At。

Cost 不做独立一级页面，而是在此处结合单次 Run 展示。

## 8. Input / Output

使用独立 Card 展示：

- 用户问题。
- 最终回答。

用户无需返回 Chat 页面即可理解这条 Trace 正在处理什么。

## 9. Trace 详情主体布局

主体采用左右双栏：

```text
┌──────────────────────┬──────────────────────────────┐
│ Trace Tree           │ Span Detail                  │
│                      │                              │
│                      │                              │
└──────────────────────┴──────────────────────────────┘
```

左侧展示执行链路，右侧展示当前选中 Span 的详情。当前选中节点使用明显但克制的高亮。

## 10. Trace Tree

标准成功链路：

```text
Agent Run
├── agent.config.load
├── conversation.message.save
├── rag.retrieve
├── tool.call
├── mcp.call
├── llm.call
└── cost.record
```

每个节点至少展示：

- Span Name。
- Kind。
- Status。
- Latency。

预留 Span Kind：

```text
runtime
conversation
rag
tool
mcp
llm
cost
approval
guard
```

每个 Span 节点可点击。

## 11. Tree 与 Timeline

Trace Tree 顶部提供视图切换：

```text
[Tree] [Timeline]
```

Tree 展示执行逻辑和父子关系。

Timeline 使用简单横条展示耗时关系，不要求精确比例，也不引入复杂图表库。

## 12. Span Detail

右侧基础信息包括：

- Span ID。
- Name。
- Kind。
- Status。
- Latency。

下方使用 Tab：

```text
[Input] [Output]
```

Input 和 Output 使用代码块风格展示 JSON，不实现复杂 JSON 编辑器。

## 13. RAG Span

`rag.retrieve` 除 Input / Output JSON 外，还展示 Retrieved Chunks：

- Chunk ID。
- Rank。
- Score。
- Content 摘要。
- Source。

## 14. Tool Span

`tool.call` 展示：

- Tool 名称。
- Risk。
- Approval 是否需要。
- Input JSON。
- Output JSON。
- Latency。

## 15. MCP Span

`mcp.call` 展示：

- MCP Server。
- MCP Tool。
- Status。
- Input / Output。
- Latency。

## 16. LLM Span

`llm.call` 展示：

- Provider。
- Model。
- Input Tokens。
- Output Tokens。
- Latency。
- Cost。

Prompt 作为默认折叠区域预留。

## 17. Cost Span

`cost.record` 展示：

- Input Tokens。
- Output Tokens。
- Total Tokens。
- Input Cost。
- Output Cost。
- Total Cost。

## 18. 失败与降级 Run

必须准备 MCP 失败 Mock：

```text
mcp.call
✕ Failed
```

错误详情：

```text
Error Code
MCP_CONNECTION_FAILED

Error Message
无法连接订单 MCP Server
```

影响说明：MCP 调用失败，但 Agent 使用 RAG 结果继续生成回答。

整个 Run 第一版优先保持 `Success`，并单独显示 `1 Warning`，避免增加不必要的新状态。

## 19. 等待审批 Run

高风险 Tool 使用 `refund_order`：

```text
tool.call
   ↓
approval.required
   ↓
Waiting Approval
```

详情展示 Tool、High Risk、Approval Required。第一版不实现真实审批系统。

## 20. Latency Breakdown

使用简单 Progress Bar 展示各阶段耗时占比：

- LLM。
- RAG。
- MCP。
- Tool。
- Other。

不要求引入复杂图表库。

## 21. Cost Breakdown

单独 Card 展示：

- LLM Cost。
- Tool Cost。
- MCP Cost。
- Total Cost。

Demo Tool 和 MCP 成本可以为 0，但必须明确它们是 Demo 数据。

## 22. Related Resources

详情页底部展示并支持跳转：

```text
Agent          → /agents/:id
Knowledge Base → /knowledge-bases/:id
Tool           → /capabilities/tools/:id
MCP Server     → /capabilities/mcp/:id
```

## 23. 教学提示

页面顶部提供“什么是 Trace？” Hover 或 Popover：

```text
一次 Agent Run 通常不是一次单独的模型调用。

它可能包含配置加载、RAG 检索、Tool 调用、MCP 调用、
LLM 推理和成本记录。

Trace 用来记录一次完整运行过程中发生的所有关键步骤。
```

## 24. Mock 数据

统一放在：

```text
src/mock/runs.ts
```

至少准备：

- 1 条正常成功 Run。
- 1 条 MCP 失败但降级完成的 Run。
- 1 条 Waiting Approval Run。

每条 Mock 包含：

```text
run
trace
spans
input
output
sources
toolCalls
mcpCalls
cost
```

Mock 数据不得散落在 Vue 组件中。

## 25. TypeScript 类型

类型文件：

```text
src/types/run.ts
```

至少定义：

```text
AgentRun
Trace
TraceSpan
SpanKind
SpanStatus
CostSummary
LatencySummary
```

禁止大量使用 `any`。

## 26. 组件拆分

```text
src/views/runs/
├── RunList.vue
└── RunDetail.vue

src/components/runs/
├── RunTable.vue
├── RunStatusBadge.vue
├── RunOverview.vue
├── TraceTree.vue
├── TraceSpanNode.vue
├── SpanDetail.vue
├── SpanJsonViewer.vue
├── LatencyBreakdown.vue
├── CostBreakdown.vue
├── RunInputOutput.vue
└── RelatedResources.vue
```

## 27. API 接入预留

页面第一版使用 Mock，但真实接入时统一通过 API 模块替换，不允许在 Vue 页面中散落 Axios 调用。

预留接口方向：

```text
getRuns(filters)
getRunDetail(traceId)
getTraceSpans(traceId)
```

后续可映射现有 FastAPI Trace 与 Cost 接口，或替换为生产 Trace Service。

## 28. 当前禁止事项

第一版不开发：

- OpenTelemetry。
- Trace SDK。
- 真实数据库。
- 日志系统。
- 指标平台。
- Grafana。
- Elasticsearch。
- 真实审批系统。
- 真实 Cost Service。

全部使用 Mock。

## 29. 验收

- 能查看运行记录列表。
- 能筛选 Agent 和状态。
- 能进入 Trace 详情。
- 能查看 Run Overview。
- 能查看用户输入和最终回答。
- 能查看 Trace Tree 和 Timeline 雏形。
- 能点击 Span 查看 Input / Output。
- 能展示 RAG、Tool、MCP、LLM 和 Cost。
- 能展示成功、失败降级和等待审批三种情况。
- 能查看 Latency 和 Cost Breakdown。
- 页面与 Chat 调试页视觉保持一致。
