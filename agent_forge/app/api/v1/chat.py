"""业务用户调用 Agent Runtime 的 Chat 接口。"""

from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.runtime.agent_runtime import agent_runtime
from app.runtime.schemas import ChatRequest
from app.shared.response import ApiResponse


router = APIRouter()


class ChatApiRequest(BaseModel):
    """Chat API 接收的用户请求。"""

    agent_id: str = Field(default="agent_customer_service")
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None


@router.post(
    "/chat",
    response_model=ApiResponse[dict],
)
async def chat(
    request: ChatApiRequest,
) -> ApiResponse[dict]:
    """调用 Agent Runtime 并返回完整运行结果。"""

    settings = get_settings()

    # 基础版本使用配置中的默认租户和用户身份。
    result = agent_runtime.run_chat(
        ChatRequest(
            tenant_id=settings.default_tenant_id,
            user_id=settings.default_user_id,
            agent_id=request.agent_id,
            message=request.message,
            conversation_id=request.conversation_id,
        )
    )

    return ApiResponse(data=asdict(result))
