"""FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.seed import seed_demo_data


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug,
)


# Demo 阶段允许跨域访问，方便后续 Vue3 前端直接联调。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化内存 Demo 数据。"""

    seed_demo_data()


# 所有业务接口统一使用 /api/v1 前缀。
app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    """返回应用基础信息和 Swagger 文档地址。"""

    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }
