# AgentForge 前端设计文档

更新日期：2026-10-02

本目录记录 AgentForge 前端已经确认的产品结构、视觉规范和页面需求。后续页面按用户指定的顺序逐个开发，不在单个页面任务中扩展无关模块。

## 文档索引

- [全局视觉与设计系统](./design-system.md)
- [信息架构与路由](./information-architecture.md)
- [知识库管理](./knowledge-base.md)
- [Tool / MCP 能力中心](./capabilities.md)
- [Chat 调试页](./chat-debug.md)
- [Trace / 运行记录](./trace-runs.md)
- [Dashboard / 工作台](./dashboard.md)
- [前端整体框架收口](./frontend-framework.md)
- [待补充页面](./page-backlog.md)

## 已确认原则

- 项目名称统一使用 `AgentForge`。
- 中文产品描述使用“企业级 AI Agent 平台”。
- 不使用附件示例中的 `Enterprise AI Agent Platform` 作为项目名。
- 前端技术栈为 Vue 3、TypeScript、Vite、Tailwind CSS、shadcn-vue、Vue Router、Pinia、Axios。
- 页面采用浅色企业后台风格，强调 AI 平台的运行过程和教学价值。
- Cost 暂不做独立一级页面，放在工作台概览和 Trace 详情中。
- 页面逐个开发；未进入当前任务的页面只保留设计文档或必要路由占位。
- 所有核心页面必须使用统一 App Layout、Sidebar、Header、Breadcrumb 和公共状态组件。

## 当前实现状态

前端工程尚未初始化。计划位置：

```text
agent_forge/frontend/
```

正式初始化和编码前，以用户指定的当前页面为唯一实施范围。
