"""应用基础配置，支持从环境变量和 .env 文件加载。"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """API 与运行时模块共享的统一配置。"""

    # 应用基础信息。
    app_name: str = "Enterprise AI Agent Platform"
    app_env: str = "development"
    app_debug: bool = True
    app_version: str = "0.1.0"

    # 内存 Demo 使用的默认租户和用户。
    default_tenant_id: str = "tenant_demo"
    default_user_id: str = "user_demo"

    # Demo 模型网关使用的默认模型。
    default_llm_provider: str = "demo"
    default_llm_model: str = "demo-fast-model"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """缓存配置实例，避免每次请求重复加载。"""

    return Settings()
