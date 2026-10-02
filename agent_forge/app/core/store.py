"""基础版本使用的全局内存数据存储。"""

from app.runtime.schemas import (
    AgentDefinition,
    Conversation,
    CostRecord,
    KnowledgeBase,
    KnowledgeChunk,
    MCPServerDefinition,
    Message,
    ModelConfig,
    ToolDefinition,
    Trace,
)


class InMemoryStore:
    """集中保存 Demo 阶段产生的领域对象。"""

    def __init__(self):
        # 按领域类型分别保存对象，主键统一使用字符串 ID。
        self.models: dict[str, ModelConfig] = {}
        self.agents: dict[str, AgentDefinition] = {}
        self.knowledge_bases: dict[str, KnowledgeBase] = {}
        self.chunks: dict[str, KnowledgeChunk] = {}
        self.tools: dict[str, ToolDefinition] = {}
        self.mcp_servers: dict[str, MCPServerDefinition] = {}
        self.conversations: dict[str, Conversation] = {}
        self.messages: dict[str, Message] = {}
        self.traces: dict[str, Trace] = {}
        self.costs: dict[str, CostRecord] = {}

    def clear(self) -> None:
        """清空全部内存数据，主要用于初始化和测试。"""

        self.__init__()


# 基础版本共享同一个 Store 实例，后续替换为 Repository 注入。
store = InMemoryStore()
