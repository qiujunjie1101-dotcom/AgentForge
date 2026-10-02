"""集中注册所有 v1 API 路由。"""

from fastapi import APIRouter

from app.api.v1.agents import router as agents_router
from app.api.v1.chat import router as chat_router
from app.api.v1.costs import router as costs_router
from app.api.v1.health import router as health_router
from app.api.v1.knowledge_bases import router as knowledge_bases_router
from app.api.v1.mcp_servers import router as mcp_servers_router
from app.api.v1.models import router as models_router
from app.api.v1.tools import router as tools_router
from app.api.v1.traces import router as traces_router


api_router = APIRouter()

# 按平台功能模块注册路由，并在 Swagger 中进行分组展示。
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(models_router, tags=["Models"])
api_router.include_router(agents_router, tags=["Agents"])
api_router.include_router(knowledge_bases_router, tags=["Knowledge Bases"])
api_router.include_router(tools_router, tags=["Tools"])
api_router.include_router(mcp_servers_router, tags=["MCP Servers"])
api_router.include_router(chat_router, tags=["Chat"])
api_router.include_router(traces_router, tags=["Traces"])
api_router.include_router(costs_router, tags=["Costs"])
