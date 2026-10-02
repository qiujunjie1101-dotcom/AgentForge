"""编排一次完整 Agent Chat 执行流程。

当前教学版使用自研 Runtime 模拟执行链路，方便理解 Agent 的核心运行机制。
生产版可将 Graph 执行部分升级为 LangGraph，以支持持久执行、流式输出、
Human-in-the-loop 和 Persistence 等能力。
"""

import uuid
from time import time

from app.core.store import store
from app.runtime.mcp_gateway import mcp_gateway
from app.runtime.model_gateway import model_gateway
from app.runtime.rag_service import rag_service
from app.runtime.schemas import (
    ChatRequest,
    ChatResult,
    Conversation,
    CostRecord,
    Message,
    RunStatus,
)
from app.runtime.tool_gateway import tool_gateway
from app.runtime.trace_recorder import trace_recorder


class AgentRuntime:
    """加载 Agent 配置并协调 RAG、Tool、MCP 和模型调用。"""

    def run_chat(
        self,
        request: ChatRequest,
    ) -> ChatResult:
        """执行一次完整的 Agent Chat 请求。"""

        run_id = f"run_{uuid.uuid4().hex[:12]}"

        agent = store.agents.get(request.agent_id)

        if not agent:
            raise ValueError(f"Agent 不存在：{request.agent_id}")

        if agent.status.value != "published":
            raise ValueError(f"Agent 未发布：{request.agent_id}")

        model = store.models.get(agent.model_id)

        if not model:
            raise ValueError(f"模型不存在：{agent.model_id}")

        # 每次运行创建独立 Trace，统一记录后续执行步骤。
        trace = trace_recorder.start_trace(
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            agent_id=request.agent_id,
            run_id=run_id,
        )

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="agent.config.load",
            kind="runtime",
            input={
                "agent_id": agent.agent_id,
            },
            output={
                "agent_name": agent.name,
                "mode": agent.mode.value,
                "model_id": agent.model_id,
            },
            latency_ms=5,
        )

        conversation_id = self._ensure_conversation(request)
        self._save_user_message(conversation_id, request.message)

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="conversation.message.save",
            kind="conversation",
            input={
                "conversation_id": conversation_id,
            },
            output={
                "message_saved": True,
            },
            latency_ms=3,
        )

        # 检索 Agent 绑定知识库中的相关内容。
        start = time()
        chunks = rag_service.retrieve(agent, request.message)
        rag_context = rag_service.build_context(chunks)
        rag_latency = int((time() - start) * 1000)

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="rag.retrieve",
            kind="rag",
            input={
                "query": request.message,
                "knowledge_base_ids": agent.knowledge_base_ids,
            },
            output={
                "chunk_ids": [chunk.chunk_id for chunk in chunks],
                "sources": [chunk.source for chunk in chunks],
            },
            latency_ms=rag_latency,
        )

        # 调用 Agent 已绑定的本地 Tool。
        start = time()
        tool_results = tool_gateway.call_tools(agent, request.message)
        tool_latency = int((time() - start) * 1000)

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="tool.call",
            kind="tool",
            input={
                "tool_ids": agent.tool_ids,
            },
            output={
                "tool_results": tool_results,
            },
            latency_ms=tool_latency,
        )

        # 通过统一 Gateway 调用 Agent 已绑定的 MCP Server。
        start = time()
        mcp_results = mcp_gateway.call_mcp(agent, request.message)
        mcp_latency = int((time() - start) * 1000)

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="mcp.call",
            kind="mcp",
            input={
                "mcp_server_ids": agent.mcp_server_ids,
            },
            output={
                "mcp_results": mcp_results,
            },
            latency_ms=mcp_latency,
        )

        # 将 Prompt、RAG、Tool 和 MCP 结果交给模型网关生成回答。
        start = time()
        llm_result = model_gateway.chat(
            model=model,
            system_prompt=agent.system_prompt,
            user_message=request.message,
            rag_context=rag_context,
            tool_results=tool_results,
            mcp_results=mcp_results,
        )
        llm_latency = int((time() - start) * 1000)

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="llm.call",
            kind="llm",
            input={
                "provider": model.provider,
                "model": model.model_name,
            },
            output={
                "input_tokens": llm_result["input_tokens"],
                "output_tokens": llm_result["output_tokens"],
                "cost": llm_result["cost"],
            },
            latency_ms=llm_latency,
        )

        answer = llm_result["answer"]
        self._save_assistant_message(conversation_id, answer)

        total_tokens = llm_result["input_tokens"] + llm_result["output_tokens"]
        cost = llm_result["cost"]

        # 单独保存本次模型调用的 Token 与成本记录。
        cost_record = CostRecord(
            cost_id=f"cost_{uuid.uuid4().hex[:12]}",
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            agent_id=request.agent_id,
            run_id=run_id,
            model_id=model.model_id,
            input_tokens=llm_result["input_tokens"],
            output_tokens=llm_result["output_tokens"],
            total_cost=cost,
        )
        store.costs[cost_record.cost_id] = cost_record

        trace_recorder.add_span(
            trace_id=trace.trace_id,
            name="cost.record",
            kind="cost",
            output={
                "total_tokens": total_tokens,
                "total_cost": cost,
            },
            latency_ms=2,
        )

        trace_recorder.finish_trace(
            trace_id=trace.trace_id,
            final_answer=answer,
            total_tokens=total_tokens,
            total_cost=cost,
            status=RunStatus.SUCCESS.value,
        )

        return ChatResult(
            run_id=run_id,
            trace_id=trace.trace_id,
            conversation_id=conversation_id,
            answer=answer,
            sources=chunks,
            tool_results=tool_results,
            mcp_results=mcp_results,
            input_tokens=llm_result["input_tokens"],
            output_tokens=llm_result["output_tokens"],
            cost=cost,
        )

    def _ensure_conversation(
        self,
        request: ChatRequest,
    ) -> str:
        """复用已有会话，或根据当前问题创建新会话。"""

        if request.conversation_id and request.conversation_id in store.conversations:
            return request.conversation_id

        conversation_id = f"conv_{uuid.uuid4().hex[:12]}"

        conversation = Conversation(
            conversation_id=conversation_id,
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            agent_id=request.agent_id,
            title=request.message[:30] or "新会话",
        )

        store.conversations[conversation_id] = conversation

        return conversation_id

    def _save_user_message(
        self,
        conversation_id: str,
        content: str,
    ) -> None:
        """保存用户消息。"""

        message = Message(
            message_id=f"msg_{uuid.uuid4().hex[:12]}",
            conversation_id=conversation_id,
            role="user",
            content=content,
        )
        store.messages[message.message_id] = message

    def _save_assistant_message(
        self,
        conversation_id: str,
        content: str,
    ) -> None:
        """保存 Agent 最终回答。"""

        message = Message(
            message_id=f"msg_{uuid.uuid4().hex[:12]}",
            conversation_id=conversation_id,
            role="assistant",
            content=content,
        )
        store.messages[message.message_id] = message


# API 层通过统一实例执行 Chat 请求。
agent_runtime = AgentRuntime()
