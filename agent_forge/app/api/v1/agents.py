"""Agent 的创建、查询和发布接口。"""

from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.store import store
from app.runtime.schemas import AgentDefinition, AgentMode, AgentStatus
from app.shared.response import ApiResponse


router = APIRouter()


class CreateAgentRequest(BaseModel):
    """创建 Agent 时提交的配置。"""

    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str = ""
    system_prompt: str = Field(..., min_length=1)
    model_id: str
    mode: AgentMode = AgentMode.RAG_TOOL_MCP
    knowledge_base_ids: list[str] = []
    tool_ids: list[str] = []
    mcp_server_ids: list[str] = []


@router.get(
    "/agents",
    response_model=ApiResponse[list[dict]],
)
async def list_agents() -> ApiResponse[list[dict]]:
    """返回当前 Store 中的全部 Agent。"""

    return ApiResponse(
        data=[
            asdict(agent)
            for agent in store.agents.values()
        ]
    )


@router.post(
    "/agents",
    response_model=ApiResponse[dict],
)
async def create_agent(
    request: CreateAgentRequest,
) -> ApiResponse[dict]:
    """创建一个默认处于草稿状态的 Agent。"""

    agent = AgentDefinition(
        agent_id=request.agent_id,
        tenant_id="tenant_demo",
        name=request.name,
        description=request.description,
        mode=request.mode,
        system_prompt=request.system_prompt,
        model_id=request.model_id,
        knowledge_base_ids=request.knowledge_base_ids,
        tool_ids=request.tool_ids,
        mcp_server_ids=request.mcp_server_ids,
        status=AgentStatus.DRAFT,
    )

    store.agents[agent.agent_id] = agent

    return ApiResponse(data=asdict(agent))


@router.get(
    "/agents/{agent_id}",
    response_model=ApiResponse[dict],
)
async def get_agent(
    agent_id: str,
) -> ApiResponse[dict]:
    """根据 Agent ID 查询详情。"""

    agent = store.agents.get(agent_id)

    if not agent:
        return ApiResponse(code=404, message="agent not found", data=None)

    return ApiResponse(data=asdict(agent))


@router.post(
    "/agents/{agent_id}/publish",
    response_model=ApiResponse[dict],
)
async def publish_agent(
    agent_id: str,
) -> ApiResponse[dict]:
    """将指定 Agent 状态修改为已发布。"""

    agent = store.agents.get(agent_id)

    if not agent:
        return ApiResponse(code=404, message="agent not found", data=None)

    agent.status = AgentStatus.PUBLISHED

    return ApiResponse(data=asdict(agent))
