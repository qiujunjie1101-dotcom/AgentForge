"""验证 Demo 数据初始化结果。"""

from app.core.store import store
from app.seed import seed_demo_data


def main():
    """清空内存数据并重新执行 Demo 初始化。"""

    store.clear()
    result = seed_demo_data()

    print(result)
    print("agents:", list(store.agents.keys()))
    print("models:", list(store.models.keys()))
    print("tools:", list(store.tools.keys()))
    print("mcp_servers:", list(store.mcp_servers.keys()))


if __name__ == "__main__":
    main()
