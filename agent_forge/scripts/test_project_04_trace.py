"""验证 Agent Runtime 生成的 Trace Tree。"""

from app.core.store import store
from app.runtime.agent_runtime import agent_runtime
from app.runtime.schemas import ChatRequest
from app.runtime.trace_recorder import trace_recorder
from app.seed import seed_demo_data


def main():
    """执行一次 Chat 并输出对应的 Trace Tree。"""

    store.clear()
    seed_demo_data()

    result = agent_runtime.run_chat(
        ChatRequest(
            tenant_id="tenant_demo",
            user_id="user_demo",
            agent_id="agent_customer_service",
            message="订单可以退款吗？",
        )
    )

    print("trace_id:", result.trace_id)
    print(trace_recorder.render_tree(result.trace_id))


if __name__ == "__main__":
    main()
