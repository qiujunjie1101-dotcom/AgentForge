"""按演示顺序验证 Agent 平台的完整运行闭环。"""

from app.core.store import store
from app.runtime.agent_runtime import agent_runtime
from app.runtime.schemas import ChatRequest
from app.runtime.trace_recorder import trace_recorder
from app.seed import seed_demo_data


def main():
    """依次输出初始化、Chat、Trace 和 Cost 等演示结果。"""

    store.clear()

    print("1. 初始化数据")
    print(seed_demo_data())

    print("=" * 100)
    print("2. 查看 Agent")
    for agent in store.agents.values():
        print(agent.agent_id, agent.name, agent.status)

    print("=" * 100)
    print("3. 执行 Chat")
    result = agent_runtime.run_chat(
        ChatRequest(
            tenant_id="tenant_demo",
            user_id="user_demo",
            agent_id="agent_customer_service",
            message="订单 10001 还没发货，可以退款吗？",
        )
    )
    print("answer:")
    print(result.answer)

    print("=" * 100)
    print("4. 来源")
    for source in result.sources:
        print(source.chunk_id, source.source, source.score)

    print("=" * 100)
    print("5. Tool")
    print(result.tool_results)

    print("=" * 100)
    print("6. MCP")
    print(result.mcp_results)

    print("=" * 100)
    print("7. Trace")
    print(trace_recorder.render_tree(result.trace_id))

    print("=" * 100)
    print("8. Cost")
    for cost in store.costs.values():
        print(cost)


if __name__ == "__main__":
    main()
