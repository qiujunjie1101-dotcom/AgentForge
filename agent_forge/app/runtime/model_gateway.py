"""Demo 模型网关，用于模拟模型回答、Token 统计和成本计算。"""

from app.runtime.schemas import ModelConfig


class DemoModelGateway:
    """不依赖外部模型服务的本地 Demo 实现。"""

    def estimate_tokens(
        self,
        text: str,
    ) -> int:
        """按中文字符和其他字符粗略估算 Token 数量。"""

        if not text:
            return 0

        chinese_chars = sum(
            1 for char in text
            if "\u4e00" <= char <= "\u9fff"
        )
        other_chars = len(text) - chinese_chars

        return chinese_chars + max(1, other_chars // 4)

    def chat(
        self,
        model: ModelConfig,
        system_prompt: str,
        user_message: str,
        rag_context: str,
        tool_results: list[dict],
        mcp_results: list[dict],
    ) -> dict:
        """组合运行时上下文，生成固定规则的 Demo 回答。"""

        input_text = "\n".join([
            system_prompt,
            user_message,
            rag_context,
            str(tool_results),
            str(mcp_results),
        ])

        input_tokens = self.estimate_tokens(input_text)

        answer_parts = [
            "根据当前信息，我给你一个简洁结论：",
        ]

        if rag_context:
            answer_parts.append("知识库显示：未发货订单可以申请退款，已发货订单需要走售后流程。")

        if tool_results:
            status = tool_results[0].get("status", "未知")
            answer_parts.append(f"订单工具查询结果显示：当前订单状态为「{status}」。")

        if mcp_results:
            answer_parts.append("MCP 订单服务也返回了订单状态，可作为辅助依据。")

        answer_parts.append("所以，如果订单还未发货，可以直接申请退款；如果已发货，建议创建售后工单或转人工处理。")

        answer = "\n".join(answer_parts)
        output_tokens = self.estimate_tokens(answer)

        # 根据模型配置中的千 Token 单价计算本次调用成本。
        cost = (
            input_tokens / 1000 * model.input_price_per_1k
            + output_tokens / 1000 * model.output_price_per_1k
        )

        return {
            "answer": answer,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": round(cost, 6),
        }


# 后续可替换为 OpenAI、DeepSeek、Qwen 或本地模型适配器。
model_gateway = DemoModelGateway()
