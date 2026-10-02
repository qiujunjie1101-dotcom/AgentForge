"""根据 Agent 配置模拟执行本地 Tool。"""

from app.core.store import store
from app.runtime.schemas import AgentDefinition


class DemoToolGateway:
    """基础版本的订单查询 Tool 调用入口。"""

    def call_tools(
        self,
        agent: AgentDefinition,
        user_message: str,
    ) -> list[dict]:
        """在满足绑定关系和关键词条件时调用订单查询 Tool。"""

        results: list[dict] = []

        # Agent 未绑定订单查询 Tool 时不执行任何调用。
        if "tool_query_order" not in agent.tool_ids:
            return results

        # 当前 Demo 仅处理订单和退款相关问题。
        if "订单" not in user_message and "退款" not in user_message:
            return results

        tool = store.tools["tool_query_order"]

        results.append(
            {
                "tool_id": tool.tool_id,
                "tool_name": tool.name,
                "status": "未发货",
                "order_id": "10001",
                "risk_level": tool.risk_level,
                "requires_approval": tool.requires_approval,
                "success": True,
            }
        )

        return results


# 后续演进为 ToolRegistry -> PermissionGuard -> ApprovalGuard -> ToolExecutor -> Trace。
tool_gateway = DemoToolGateway()
