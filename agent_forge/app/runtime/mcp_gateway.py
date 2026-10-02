"""统一接入和治理外部 MCP Server 的 Demo 网关。"""

from app.core.store import store
from app.runtime.schemas import AgentDefinition


class DemoMCPGateway:
    """根据 Agent 绑定关系发现并调用 MCP Server 能力。"""

    def call_mcp(
        self,
        agent: AgentDefinition,
        user_message: str,
    ) -> list[dict]:
        """调用已绑定 MCP Server 暴露的订单查询 Tool。"""

        results: list[dict] = []

        # 当前 Demo 仅响应订单和退款相关问题。
        if "订单" not in user_message and "退款" not in user_message:
            return results

        for server_id in agent.mcp_server_ids:
            server = store.mcp_servers.get(server_id)

            # 忽略不存在或已经失效的 MCP Server 配置。
            if not server:
                continue

            if "query_order_status" in server.tools:
                results.append(
                    {
                        "server_id": server.server_id,
                        "server_name": server.name,
                        "tool_name": "query_order_status",
                        "result": {
                            "order_id": "10001",
                            "status": "未发货",
                            "can_refund": True,
                        },
                        "success": True,
                    }
                )

        return results


# Agent 通过统一 Gateway 使用 MCP 能力，不直接裸连外部 MCP Server。
mcp_gateway = DemoMCPGateway()
