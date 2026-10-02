"""服务健康检查接口。"""

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.store import store
from app.shared.response import ApiResponse


router = APIRouter()


@router.get(
    "/health",
    response_model=ApiResponse[dict],
)
async def health() -> ApiResponse[dict]:
    """返回应用状态和内存 Store 中的资源数量。"""

    settings = get_settings()

    return ApiResponse(
        data={
            "status": "ok",
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "models": len(store.models),
            "agents": len(store.agents),
            "knowledge_bases": len(store.knowledge_bases),
            "tools": len(store.tools),
            "mcp_servers": len(store.mcp_servers),
            "traces": len(store.traces),
            "costs": len(store.costs),
        }
    )
