"""Agent Runtime 使用的核心领域模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Any


class AgentStatus(str, Enum):
    """Agent 生命周期状态。"""

    DRAFT = "draft"
    PUBLISHED = "published"
    OFFLINE = "offline"


class AgentMode(str, Enum):
    """Agent 支持的运行模式。"""

    SIMPLE_CHAT = "simple_chat"
    RAG = "rag"
    TOOL_CALLING = "tool_calling"
    MCP = "mcp"
    RAG_TOOL_MCP = "rag_tool_mcp"


class RunStatus(str, Enum):
    """单次运行的执行状态。"""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class ModelConfig:
    """模型及其计费配置。"""

    model_id: str
    provider: str
    model_name: str
    display_name: str
    input_price_per_1k: float = 0.0
    output_price_per_1k: float = 0.0
    supports_streaming: bool = True
    supports_tool_calling: bool = True


@dataclass
class KnowledgeBase:
    """知识库定义，第一版直接保存内存文档。"""

    kb_id: str
    name: str
    description: str
    tenant_id: str
    documents: list[str] = field(default_factory=list)


@dataclass
class KnowledgeChunk:
    """RAG 检索返回的知识片段。"""

    chunk_id: str
    kb_id: str
    content: str
    source: str
    score: float = 0.0


@dataclass
class ToolDefinition:
    """可供 Agent 调用的 Tool 定义。"""

    tool_id: str
    name: str
    description: str
    risk_level: str = "low"
    requires_approval: bool = False


@dataclass
class MCPServerDefinition:
    """Agent 可连接的 MCP Server 定义。"""

    server_id: str
    name: str
    description: str
    tools: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)


@dataclass
class AgentDefinition:
    """Agent 配置快照。"""

    agent_id: str
    tenant_id: str
    name: str
    description: str
    mode: AgentMode
    system_prompt: str
    model_id: str
    knowledge_base_ids: list[str] = field(default_factory=list)
    tool_ids: list[str] = field(default_factory=list)
    mcp_server_ids: list[str] = field(default_factory=list)
    status: AgentStatus = AgentStatus.DRAFT
    version: str = "v1"


@dataclass
class Conversation:
    """用户与 Agent 的会话。"""

    conversation_id: str
    tenant_id: str
    user_id: str
    agent_id: str
    title: str
    created_at: float = field(default_factory=time)


@dataclass
class Message:
    """会话中的单条消息。"""

    message_id: str
    conversation_id: str
    role: str
    content: str
    created_at: float = field(default_factory=time)


@dataclass
class TraceSpan:
    """Trace Tree 中的单个执行节点。"""

    span_id: str
    trace_id: str
    name: str
    kind: str
    parent_span_id: str | None = None
    input: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    status: str = "success"
    latency_ms: int = 0


@dataclass
class Trace:
    """一次 Agent 运行对应的完整链路记录。"""

    trace_id: str
    run_id: str
    tenant_id: str
    user_id: str
    agent_id: str
    status: str = "running"
    spans: list[TraceSpan] = field(default_factory=list)
    final_answer: str | None = None
    total_tokens: int = 0
    total_cost: float = 0.0
    created_at: float = field(default_factory=time)


@dataclass
class CostRecord:
    """单次模型调用的 Token 与成本记录。"""

    cost_id: str
    tenant_id: str
    user_id: str
    agent_id: str
    run_id: str
    model_id: str
    input_tokens: int
    output_tokens: int
    total_cost: float
    created_at: float = field(default_factory=time)


@dataclass
class ChatRequest:
    """Agent Runtime 的聊天请求。"""

    tenant_id: str
    user_id: str
    agent_id: str
    message: str
    conversation_id: str | None = None


@dataclass
class ChatResult:
    """Agent Runtime 返回的完整聊天结果。"""

    run_id: str
    trace_id: str
    conversation_id: str
    answer: str
    sources: list[KnowledgeChunk]
    tool_results: list[dict[str, Any]]
    mcp_results: list[dict[str, Any]]
    input_tokens: int
    output_tokens: int
    cost: float
