"""模型 Token 与调用成本的明细和汇总接口。"""

from collections import defaultdict
from dataclasses import asdict

from fastapi import APIRouter

from app.core.store import store
from app.shared.response import ApiResponse


router = APIRouter()


@router.get(
    "/costs",
    response_model=ApiResponse[list[dict]],
)
async def list_costs() -> ApiResponse[list[dict]]:
    """返回当前 Store 中的全部成本明细。"""

    return ApiResponse(
        data=[
            asdict(cost)
            for cost in store.costs.values()
        ]
    )


@router.get(
    "/costs/summary",
    response_model=ApiResponse[dict],
)
async def cost_summary() -> ApiResponse[dict]:
    """汇总 Token、总成本和各 Agent 的调用成本。"""

    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    by_agent = defaultdict(float)

    for cost in store.costs.values():
        total_cost += cost.total_cost
        total_input_tokens += cost.input_tokens
        total_output_tokens += cost.output_tokens
        by_agent[cost.agent_id] += cost.total_cost

    return ApiResponse(
        data={
            "total_cost": round(total_cost, 6),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "by_agent": {
                key: round(value, 6)
                for key, value in by_agent.items()
            },
        }
    )
