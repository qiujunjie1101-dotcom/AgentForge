"""基于关键词和内存知识片段的 Demo RAG 服务。"""

from app.core.store import store
from app.runtime.schemas import AgentDefinition, KnowledgeChunk


class DemoRAGService:
    """模拟知识库检索与上下文构建。"""

    def retrieve(
        self,
        agent: AgentDefinition,
        query: str,
        top_k: int = 3,
    ) -> list[KnowledgeChunk]:
        """从 Agent 绑定的知识库中检索相关知识片段。"""

        # 基础版本使用固定业务关键词模拟召回和相关性加权。
        keywords = [
            word
            for word in ["退款", "退货", "售后", "物流", "发货", "订单"]
            if word in query
        ]

        candidates: list[KnowledgeChunk] = []

        for chunk in store.chunks.values():
            if chunk.kb_id not in agent.knowledge_base_ids:
                continue

            hit_score = chunk.score

            for keyword in keywords:
                if keyword in chunk.content:
                    hit_score += 0.1

            # 返回新的知识片段，避免修改 Store 中的原始分数。
            candidates.append(
                KnowledgeChunk(
                    chunk_id=chunk.chunk_id,
                    kb_id=chunk.kb_id,
                    content=chunk.content,
                    source=chunk.source,
                    score=round(hit_score, 4),
                )
            )

        candidates.sort(key=lambda item: item.score, reverse=True)

        return candidates[:top_k]

    def build_context(
        self,
        chunks: list[KnowledgeChunk],
    ) -> str:
        """将知识片段转换为模型可使用的文本上下文。"""

        if not chunks:
            return ""

        lines = []

        for index, chunk in enumerate(chunks, start=1):
            lines.append(
                f"[资料 {index}] {chunk.content}\n来源：{chunk.source}"
            )

        return "\n\n".join(lines)


# 后续可替换为文档解析、Embedding、向量检索、权限过滤、Rerank 和 ContextBuilder。
rag_service = DemoRAGService()
