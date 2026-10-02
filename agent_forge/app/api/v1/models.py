"""模型配置的创建与查询接口。"""

from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.store import store
from app.runtime.schemas import ModelConfig
from app.shared.response import ApiResponse


router = APIRouter()


class CreateModelRequest(BaseModel):
    """创建模型配置时提交的参数。"""

    model_id: str
    provider: str
    model_name: str
    display_name: str
    input_price_per_1k: float = 0.0
    output_price_per_1k: float = 0.0


@router.get(
    "/models",
    response_model=ApiResponse[list[dict]],
)
async def list_models() -> ApiResponse[list[dict]]:
    """返回当前 Store 中的全部模型配置。"""

    return ApiResponse(
        data=[
            asdict(model)
            for model in store.models.values()
        ]
    )


@router.post(
    "/models",
    response_model=ApiResponse[dict],
)
async def create_model(
    request: CreateModelRequest,
) -> ApiResponse[dict]:
    """创建模型及其 Token 计费配置。"""

    model = ModelConfig(
        model_id=request.model_id,
        provider=request.provider,
        model_name=request.model_name,
        display_name=request.display_name,
        input_price_per_1k=request.input_price_per_1k,
        output_price_per_1k=request.output_price_per_1k,
    )

    store.models[model.model_id] = model

    return ApiResponse(data=asdict(model))
