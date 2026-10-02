"""Agent Runtime Trace 的列表、详情和 Tree 查询接口。"""

from dataclasses import asdict

from fastapi import APIRouter

from app.core.store import store
from app.runtime.trace_recorder import trace_recorder
from app.shared.response import ApiResponse


router = APIRouter()


@router.get(
    "/traces",
    response_model=ApiResponse[list[dict]],
)
async def list_traces() -> ApiResponse[list[dict]]:
    """返回当前 Store 中的全部 Trace。"""

    return ApiResponse(
        data=[
            asdict(trace)
            for trace in store.traces.values()
        ]
    )


@router.get(
    "/traces/{trace_id}",
    response_model=ApiResponse[dict],
)
async def get_trace(
    trace_id: str,
) -> ApiResponse[dict]:
    """根据 Trace ID 查询完整执行记录。"""

    trace = store.traces.get(trace_id)

    if not trace:
        return ApiResponse(code=404, message="trace not found", data=None)

    return ApiResponse(data=asdict(trace))


@router.get(
    "/traces/{trace_id}/tree",
    response_model=ApiResponse[dict],
)
async def get_trace_tree(
    trace_id: str,
) -> ApiResponse[dict]:
    """返回便于调试和展示的 Trace Tree 文本。"""

    if trace_id not in store.traces:
        return ApiResponse(code=404, message="trace not found", data=None)

    return ApiResponse(
        data={
            "tree": trace_recorder.render_tree(trace_id)
        }
    )
