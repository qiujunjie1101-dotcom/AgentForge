"""MCP Server 的创建、查询和连接测试接口。"""

from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.store import store
from app.runtime.schemas import MCPServerDefinition
from app.shared.response import ApiResponse


router = APIRouter()


class CreateMCPServerRequest(BaseModel):
    """创建 MCP Server 时提交的能力配置。"""

    server_id: str
    name: str
    description: str = ""
    tools: list[str] = []
    resources: list[str] = []


@router.get(
    "/mcp-servers",
    response_model=ApiResponse[list[dict]],
)
async def list_mcp_servers() -> ApiResponse[list[dict]]:
    """返回当前 Store 中的全部 MCP Server。"""

    return ApiResponse(
        data=[
            asdict(server)
            for server in store.mcp_servers.values()
        ]
    )


@router.post(
    "/mcp-servers",
    response_model=ApiResponse[dict],
)
async def create_mcp_server(
    request: CreateMCPServerRequest,
) -> ApiResponse[dict]:
    """注册 MCP Server 及其 tools 和 resources。"""

    server = MCPServerDefinition(
        server_id=request.server_id,
        name=request.name,
        description=request.description,
        tools=request.tools,
        resources=request.resources,
    )

    store.mcp_servers[server.server_id] = server

    return ApiResponse(data=asdict(server))


@router.post(
    "/mcp-servers/{server_id}/connect-test",
    response_model=ApiResponse[dict],
)
async def connect_test(
    server_id: str,
) -> ApiResponse[dict]:
    """模拟连接 MCP Server 并返回其已注册能力。"""

    server = store.mcp_servers.get(server_id)

    if not server:
        return ApiResponse(code=404, message="mcp server not found", data=None)

    return ApiResponse(
        data={
            "server_id": server.server_id,
            "connected": True,
            "tools": server.tools,
            "resources": server.resources,
        }
    )
