"""记录一次 Agent Run 中产生的 Trace 和 Span。"""

import uuid
from time import time

from app.core.store import store
from app.runtime.schemas import Trace, TraceSpan


class TraceRecorder:
    """管理 Trace 的创建、Span 写入和运行结束。"""

    def start_trace(
        self,
        tenant_id: str,
        user_id: str,
        agent_id: str,
        run_id: str,
    ) -> Trace:
        """为一次 Agent Run 创建 Trace。"""

        trace = Trace(
            trace_id=f"trace_{uuid.uuid4().hex[:12]}",
            run_id=run_id,
            tenant_id=tenant_id,
            user_id=user_id,
            agent_id=agent_id,
        )
        store.traces[trace.trace_id] = trace

        return trace

    def add_span(
        self,
        trace_id: str,
        name: str,
        kind: str,
        input: dict | None = None,
        output: dict | None = None,
        parent_span_id: str | None = None,
        status: str = "success",
        latency_ms: int = 0,
    ) -> TraceSpan:
        """向指定 Trace 追加一个执行 Span。"""

        trace = store.traces[trace_id]

        span = TraceSpan(
            span_id=f"span_{uuid.uuid4().hex[:12]}",
            trace_id=trace_id,
            name=name,
            kind=kind,
            parent_span_id=parent_span_id,
            input=input or {},
            output=output or {},
            status=status,
            latency_ms=latency_ms,
        )

        trace.spans.append(span)

        return span

    def finish_trace(
        self,
        trace_id: str,
        final_answer: str,
        total_tokens: int,
        total_cost: float,
        status: str = "success",
    ) -> Trace:
        """写入最终结果并结束 Trace。"""

        trace = store.traces[trace_id]
        trace.status = status
        trace.final_answer = final_answer
        trace.total_tokens = total_tokens
        trace.total_cost = total_cost

        return trace

    def render_tree(
        self,
        trace_id: str,
    ) -> str:
        """按 Span 写入顺序渲染简单的 Trace Tree 文本。"""

        trace = store.traces[trace_id]

        lines = [
            f"Trace {trace.trace_id}｜run_id={trace.run_id}｜status={trace.status}",
            "",
        ]

        for span in trace.spans:
            lines.append(
                f"├── {span.name} [{span.kind}] {span.status} {span.latency_ms}ms"
            )

        return "\n".join(lines)


# 后续可替换为兼容 OpenTelemetry 的 Trace 导出实现。
trace_recorder = TraceRecorder()
