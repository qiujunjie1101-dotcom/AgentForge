# AgentForge Chat 调试页设计

更新日期：2026-10-02

## 1. 页面目标

Chat 调试页用于选择 Agent、输入问题，并同时观察一次运行中的用户问题、AI 回答、RAG、Tool、MCP、Trace、Token 和 Cost。

核心教学链路：

```text
用户输入
   ↓
Agent Runtime
   ├── Retriever → Knowledge
   ├── Tool      → Business System
   ├── MCP       → External Capability
   └── LLM
   ↓
最终回答
```

第一版只做页面结构、视觉、Mock 数据和运行过程模拟，不连接真实后端。

## 2. 路由与布局

路由：

```text
/chat
```

页面采用左右双栏：

- 左侧 Chat 约 65%。
- 右侧 Debug Panel 约 35%。
- Chat 消息区和 Debug Panel 独立滚动。
- 页面高度接近浏览器可视区域。

顶部展示页面标题、副标题、Agent Selector 和“新建会话”。

## 3. Agent Selector 与信息栏

Agent Selector Mock：

```text
电商客服 Agent  RAG + Tool + MCP
销售 Agent      RAG + Tool
HR Agent        Simple Chat
```

展示当前 Agent 的发布状态。

轻量信息栏展示模型、知识库数量、Tool 数量和 MCP 数量，帮助开发者确认当前调试对象。

## 4. Chat 空状态

初次进入不展示伪造聊天记录，显示“开始调试你的 Agent”和说明文字。

示例问题：

- 订单 10001 还没发货，可以退款吗？
- 物流超过 7 天没更新怎么办？
- 我想申请售后应该怎么处理？

点击示例只填入输入框，不自动发送。

## 5. 消息与输入区

用户消息右侧对齐，AI Agent 消息左侧对齐。

AI 消息底部弱化展示引用数量、Token、Cost、耗时和“重新运行”。

输入区采用 ChatGPT 风格多行输入框：

- Enter 发送。
- Shift + Enter 换行。
- 显示当前 Agent。
- 发送按钮在空内容或运行中不可用。

## 6. Demo Runtime

发送后按步骤模拟：

```text
加载 Agent 配置
   ↓
RAG 检索
   ↓
Tool 调用
   ↓
MCP 调用
   ↓
LLM 生成
   ↓
Cost 记录
   ↓
完成
```

每一步间隔约 300～700ms，只用于视觉演示。用户消息立即出现，Agent 显示 Thinking，Debug Panel 自动切换到 Trace，完成后生成 Mock AI 回答。

模拟器位置：

```text
src/mock/runtime-simulator.ts
```

入口建议为 `simulateAgentRun()`，通过回调或 Store action 逐步更新状态。

## 7. Debug Panel

顶部 Tab：

```text
[Sources] [Tools] [MCP] [Trace] [Run]
```

Sources 对应 RAG，Tools 对应 Tool Calling，MCP 对应 MCP 调用，Trace 对应执行链路，Run 对应本次运行概要。

Debug Panel 顶部提供教学提示，解释 Agent 回答还会受到 RAG、Tool、MCP 和 Prompt 的影响。

## 8. Sources

顶部展示 Retriever 信息：Mode、Top K、返回 Chunk 数量，并明确标记 `Demo Retriever`。

每个 Chunk Card 展示：

- Rank。
- Score。
- Content。
- Source。
- Chunk ID。

长内容支持展开和收起。

## 9. Tools

Tool Call Card 展示：

- Tool 名称。
- 状态。
- 耗时。
- 输入 JSON。
- 输出 JSON。
- 风险等级。
- 是否需要审批。

预留高风险 `refund_order` 场景，状态为 `Waiting Approval`，但不实现真实审批。

## 10. MCP

MCP Call Card 展示：

- MCP Server。
- Tool 名称。
- 状态。
- Input。
- Result。
- Transport。
- Latency。

## 11. Trace

Trace 使用树形结构展示：

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

节点可展开查看 Input 和 Output。`llm.call` 额外展示 Provider、Model、输入 Token、输出 Token 和耗时。

Span 状态：

```text
pending
running
success
failed
waiting_approval
```

状态颜色保持克制。

## 12. Run

Run Overview 展示：

- Run ID。
- Trace ID。
- Agent。
- Status。
- Duration。
- Input Tokens。
- Output Tokens。
- Total Tokens。
- Cost。

Run Pipeline 展示 Agent Config、RAG、Tool、MCP、LLM、Response 的 Pending、Running 和完成状态。

## 13. 成功、失败和降级

成功时顶部显示 `Run completed`。

失败 Mock 使用 `MCP_CONNECTION_FAILED`：

- `mcp.call` Span 显示 Failed。
- 展示“无法连接订单 MCP Server”。
- Chat 不崩溃。
- AI 回答降级为只根据知识库给出建议。

该场景用于展示 Runtime 容错概念。

## 14. 会话交互

- “重新运行”使用同一问题重新播放 Mock 执行动画。
- “新建会话”清空 Chat 和 Debug Panel，并生成新的 Mock conversationId。
- “最近会话”使用简单 Sheet 展示 Mock 会话，不实现完整历史管理。

## 15. 类型与状态

类型文件：

```text
src/types/chat.ts
```

至少定义：

```text
ChatMessage
AgentRun
KnowledgeChunk
ToolCall
MCPCall
TraceSpan
RunStatus
```

状态至少包含 Agent ID、Conversation ID、Messages、Run、Sources、Tool Calls、MCP Calls、Spans 和 `idle | running | success | failed`。

建议由 Pinia Store 统一管理页面状态，避免把运行逻辑集中在 `ChatDebug.vue`。

## 16. Mock 数据

统一放在：

```text
src/mock/chat.ts
```

包括：

```text
mockChatResponse
mockSources
mockToolCalls
mockMcpCalls
mockTraceSpans
mockRun
```

Mock 数据不得散落在 Vue 组件中。

## 17. 组件建议

```text
src/views/chat/
└── ChatDebug.vue

src/components/chat/
├── AgentSelector.vue
├── ChatHeader.vue
├── ChatMessageList.vue
├── ChatMessage.vue
├── ChatComposer.vue
├── EmptyChatState.vue
├── DebugPanel.vue
├── SourcePanel.vue
├── SourceChunkCard.vue
├── ToolCallPanel.vue
├── ToolCallCard.vue
├── MCPCallPanel.vue
├── MCPCallCard.vue
├── TracePanel.vue
├── TraceTree.vue
├── TraceSpanNode.vue
├── RunOverview.vue
└── RunPipeline.vue
```

## 18. 当前禁止事项

第一版不开发真实 LLM、DeepSeek、SSE、Milvus、Embedding、Retriever、Tool Executor、MCP Client、Trace 后端、Cost API 和 Conversation 数据库。全部使用 Mock。

## 19. 验收

- 能选择 Agent。
- 能输入问题。
- 能模拟 Agent Run。
- 能展示 AI 回答。
- 能查看 Sources、Tool、MCP、Trace、Token 和 Cost。
- 能模拟成功和失败状态。
- 页面保持 AgentForge 全局视觉一致。
