# AgentForge

AgentForge 是一个面向企业级 AI Agent 开发学习的可观测平台 Demo。

当前版本使用 FastAPI、内存 Store 和 Demo Gateway，跑通以下完整链路：

```text
模型配置
  → Agent
  → 知识库 / RAG
  → Tool
  → MCP Server
  → Agent Runtime
  → Trace
  → Token / Cost
```

## 当前能力

- Agent 创建、查询和发布
- Demo 模型配置与模拟计费
- 内存知识库与关键词 RAG
- Demo Tool Gateway
- Demo MCP Gateway
- Agent Chat Runtime
- Conversation、Trace Tree、Cost 记录
- FastAPI Swagger API
- Docker / Docker Compose 启动
- 前端信息架构和页面设计文档

## 后端目录

```text
agent_forge/
├── app/       FastAPI 应用、Runtime、领域模型和 API
├── scripts/   Seed、Agent、Chat、Trace 和全链路演示脚本
├── Dockerfile
├── docker-compose.yml
└── docs/frontend/  前端统一设计文档
```

## 本地运行

```bash
cd agent_forge
uv run uvicorn app.main:app --reload
```

Swagger：<http://127.0.0.1:8000/docs>

健康检查：<http://127.0.0.1:8000/api/v1/health>

## Docker 运行

```bash
cd agent_forge
cp .env.example .env
docker compose up --build
```

## 演示脚本

```bash
cd agent_forge
uv run python -m scripts.test_project_01_seed
uv run python -m scripts.test_project_02_agent
uv run python -m scripts.test_project_03_chat
uv run python -m scripts.test_project_04_trace
uv run python -m scripts.test_project_all
```

## 前端规划

前端计划放在 `agent_forge/frontend/`，技术栈为 Vue 3、TypeScript、Vite、Tailwind CSS、shadcn-vue、Vue Router、Pinia 和 Axios。

已整理的页面设计位于 [agent_forge/docs/frontend](agent_forge/docs/frontend)：

- Dashboard / 工作台
- Agent 管理
- 知识库管理
- Tool / MCP 能力中心
- Chat 调试
- Trace / 运行记录
- 全局 Layout、Sidebar、路由和设计系统

## 后续演进

```text
InMemoryStore → Repository + PostgreSQL
Demo RAG      → pgvector / Embedding / Rerank
Demo LLM      → OpenAI / DeepSeek / Qwen / Local Adapter
Demo MCP      → Real MCP Client / Governance
自研 Runtime   → LangGraph 持久执行与流式能力
```
