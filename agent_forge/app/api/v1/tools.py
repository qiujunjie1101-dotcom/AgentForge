"""Tool 的创建、查询和测试接口。"""

from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.store import store
from app.runtime.schemas import ToolDefinition
from app.shared.response import ApiResponse


router = APIRouter()


class CreateToolRequest(BaseModel):
    """创建 Tool 时提交的配置。"""

    tool_id: str
    name: str
    description: str = ""
    risk_level: str = "low"
    requires_approval: bool = False


@router.get(
    "/tools",
    response_model=ApiResponse[list[dict]],
)
async def list_tools() -> ApiResponse[list[dict]]:
    """返回当前 Store 中的全部 Tool。"""

    return ApiResponse(
        data=[
            asdict(tool)
            for tool in store.tools.values()
        ]
    )


@router.post(
    "/tools",
    response_model=ApiResponse[dict],
)
async def create_tool(
    request: CreateToolRequest,
) -> ApiResponse[dict]:
    """创建 Tool 及其风险和审批配置。"""

    tool = ToolDefinition(
        tool_id=request.tool_id,
        name=request.name,
        description=request.description,
        risk_level=request.risk_level,
        requires_approval=request.requires_approval,
    )

    store.tools[tool.tool_id] = tool

    return ApiResponse(data=asdict(tool))


@router.post(
    "/tools/{tool_id}/test",
    response_model=ApiResponse[dict],
)
async def test_tool(
    tool_id: str,
) -> ApiResponse[dict]:
    """执行一次固定结果的 Demo Tool 测试。"""

    tool = store.tools.get(tool_id)

    if not tool:
        return ApiResponse(code=404, message="tool not found", data=None)

    return ApiResponse(
        data={
            "tool_id": tool.tool_id,
            "tool_name": tool.name,
            "success": True,
            "result": {
                "order_id": "10001",
                "status": "未发货",
            },
        }
    )
