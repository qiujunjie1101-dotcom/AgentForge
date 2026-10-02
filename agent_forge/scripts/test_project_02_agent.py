"""验证 Demo Agent 及其资源绑定配置。"""

from app.core.store import store
from app.seed import seed_demo_data


def main():
    """初始化 Demo 数据并输出客服 Agent 配置。"""

    store.clear()
    seed_demo_data()

    agent = store.agents["agent_customer_service"]

    print(agent.name)
    print(agent.mode)
    print(agent.knowledge_base_ids)
    print(agent.tool_ids)
    print(agent.mcp_server_ids)


if __name__ == "__main__":
    main()
