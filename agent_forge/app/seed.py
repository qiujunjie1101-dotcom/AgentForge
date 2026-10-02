"""初始化可直接运行和演示的 Demo 数据。"""

from app.core.store import store
from app.runtime.schemas import (
    AgentDefinition,
    AgentMode,
    AgentStatus,
    KnowledgeBase,
    KnowledgeChunk,
    MCPServerDefinition,
    ModelConfig,
    ToolDefinition,
)


def seed_demo_data() -> dict:
    """初始化模型、知识库、Tool、MCP Server 和客服 Agent。"""

    # 避免应用重复启动时多次写入相同数据。
    if store.models:
        return {
            "seeded": False,
            "message": "demo data already exists",
        }

    model = ModelConfig(
        model_id="model_demo_fast",
        provider="demo",
        model_name="demo-fast-model",
        display_name="Demo Fast Model",
        input_price_per_1k=0.001,
        output_price_per_1k=0.002,
    )
    store.models[model.model_id] = model

    kb = KnowledgeBase(
        kb_id="kb_refund_policy",
        name="售后退款知识库",
        description="用于回答退款、退货、售后政策问题。",
        tenant_id="tenant_demo",
        documents=["售后政策.md"],
    )
    store.knowledge_bases[kb.kb_id] = kb

    # Demo 知识片段用于模拟 RAG 检索结果。
    chunks = [
        KnowledgeChunk(
            chunk_id="chunk_refund_001",
            kb_id=kb.kb_id,
            content="未发货订单可以直接申请退款，系统会在 1 到 3 个工作日内原路退回。",
            source="售后政策.md#未发货退款",
            score=0.95,
        ),
        KnowledgeChunk(
            chunk_id="chunk_refund_002",
            kb_id=kb.kb_id,
            content="已发货订单需要等待客户拒收或签收后发起售后申请，由客服审核后处理。",
            source="售后政策.md#已发货售后",
            score=0.88,
        ),
        KnowledgeChunk(
            chunk_id="chunk_logistics_001",
            kb_id=kb.kb_id,
            content="物流超过 7 天未更新时，客服可以创建物流异常工单进行人工排查。",
            source="售后政策.md#物流异常",
            score=0.82,
        ),
    ]

    for chunk in chunks:
        store.chunks[chunk.chunk_id] = chunk

    query_order_tool = ToolDefinition(
        tool_id="tool_query_order",
        name="query_order",
        description="查询订单状态。",
        risk_level="low",
        requires_approval=False,
    )
    store.tools[query_order_tool.tool_id] = query_order_tool

    create_ticket_tool = ToolDefinition(
        tool_id="tool_create_ticket",
        name="create_ticket",
        description="创建售后工单。",
        risk_level="medium",
        requires_approval=False,
    )
    store.tools[create_ticket_tool.tool_id] = create_ticket_tool

    mcp_server = MCPServerDefinition(
        server_id="mcp_order_server",
        name="订单 MCP Server",
        description="模拟订单系统 MCP Server。",
        tools=["query_order_status"],
        resources=["policy://refund"],
    )
    store.mcp_servers[mcp_server.server_id] = mcp_server

    agent = AgentDefinition(
        agent_id="agent_customer_service",
        tenant_id="tenant_demo",
        name="电商客服 Agent",
        description="面向售后、退款、物流问题的企业客服 Agent。",
        mode=AgentMode.RAG_TOOL_MCP,
        system_prompt=(
            "你是企业电商客服 Agent。"
            "回答要简洁、准确。"
            "优先基于知识库和工具结果回答。"
            "不确定时提示转人工。"
        ),
        model_id=model.model_id,
        knowledge_base_ids=[kb.kb_id],
        tool_ids=[query_order_tool.tool_id, create_ticket_tool.tool_id],
        mcp_server_ids=[mcp_server.server_id],
        status=AgentStatus.PUBLISHED,
        version="v1",
    )
    store.agents[agent.agent_id] = agent

    return {
        "seeded": True,
        "models": len(store.models),
        "agents": len(store.agents),
        "knowledge_bases": len(store.knowledge_bases),
        "chunks": len(store.chunks),
        "tools": len(store.tools),
        "mcp_servers": len(store.mcp_servers),
    }
