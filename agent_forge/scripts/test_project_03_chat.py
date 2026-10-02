"""验证 Demo Agent 的完整 Chat 执行链路。"""

from dataclasses import asdict

from app.core.store import store
from app.runtime.agent_runtime import agent_runtime
from app.runtime.schemas import ChatRequest
from app.seed import seed_demo_data


def main():
    """执行退款场景 Chat 并输出完整运行结果。"""

    store.clear()
    seed_demo_data()

    result = agent_runtime.run_chat(
        ChatRequest(
            tenant_id="tenant_demo",
            user_id="user_demo",
            agent_id="agent_customer_service",
            message="订单 10001 还没发货，可以退款吗？",
        )
    )

    print(asdict(result))


if __name__ == "__main__":
    main()
