# AgentForge 知识库管理设计

更新日期：2026-10-02

## 1. 页面目标

实现知识库列表、知识库详情、文档信息和 Chunk 列表，让用户直观看懂：

```text
Document
   ↓
Parser
   ↓
Chunk
   ↓
Retriever
```

第一版暂不实现复杂向量数据库管理、Embedding 配置和高级检索参数。

## 2. 路由

```text
/knowledge-bases
/knowledge-bases/:id
```

## 3. 知识库列表页

标题：`知识库`

副标题：`管理 Agent 使用的企业知识与文档内容`

页面功能：

- 右上角“创建知识库”。
- 搜索框“搜索知识库...”。
- 知识库使用 Card 展示，不使用单纯 Table。
- Card 展示名称、描述、文档数量、Chunk 数量和最近更新时间。
- 支持查看详情、编辑、删除。
- 删除必须经过确认 Dialog。

空状态：

```text
还没有知识库

创建第一个知识库，为 Agent 添加可检索的企业知识。

[创建知识库]
```

## 4. 创建知识库

使用 Dialog，字段包括：

- 知识库名称，必填。
- 知识库描述。

底部操作：取消、创建知识库。

创建期间按钮进入 Loading。创建成功后显示“知识库创建成功” Toast 并刷新列表。

## 5. 知识库详情页

顶部 Breadcrumb：

```text
知识库 / 售后退款知识库
```

顶部展示名称、描述、文档数量和 Chunk 数量，右侧为“上传文档”。

主体包含两个 Tab：

```text
[文档] [Chunks]
```

默认进入文档 Tab。

## 6. 文档 Tab

文档列表至少展示：

- 文档名称。
- 状态。
- 类型。
- Chunk 数量。
- 更新时间。
- 查看和删除操作。

文档状态：

```text
PENDING  → 等待处理
PARSING  → 解析中
PARSED   → 已解析
FAILED   → 解析失败
```

状态使用克制的 Badge。

空状态：

```text
暂无文档

上传 PDF、Word、Markdown 或 TXT 文档开始构建知识库。

[上传文档]
```

## 7. 上传文档

使用 Dialog，支持：

- PDF。
- DOCX。
- Markdown。
- TXT。

上传区域支持拖拽和点击选取。选中文件后展示名称、类型、大小和移除操作。

上传期间展示进度。成功后展示“上传成功，等待文档解析”，然后刷新文档列表。

## 8. Chunk Tab

顶部展示 Chunk 总数和搜索框。每个 Chunk 使用独立 Card，至少展示：

- `chunk_id`。
- `chunk_index`。
- `content`。
- `source`。
- `document_name`。

只有后端返回 metadata 时才展示 `page` 和 `section`，前端不得伪造。

长内容默认限制约 4～6 行，可展开全文和收起。支持复制 Chunk 内容，并显示“Chunk 内容已复制” Toast。

空状态：

```text
暂无 Chunk

文档解析完成后，生成的文本块会显示在这里。
```

## 9. RAG 教学提示

详情页增加轻量流程卡：

```text
Document
   ↓
Parser
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Store
   ↓
Retriever
```

如果教学版尚未接入真实 Embedding 和 Vector Store，必须标记“待接入”，不能模拟为已完成。

## 10. API 设计

统一放在：

```text
src/api/knowledge-base.ts
```

预留方法：

```text
getKnowledgeBases()
createKnowledgeBase()
getKnowledgeBase(id)
deleteKnowledgeBase(id)
getDocuments(knowledgeBaseId)
uploadDocument(knowledgeBaseId, file)
deleteDocument(documentId)
getChunks(knowledgeBaseId)
```

页面不得散落直接 Axios 调用。

## 11. 类型与组件

类型文件：

```text
src/types/knowledge-base.ts
```

至少定义 `KnowledgeBase`、`DocumentItem`、`KnowledgeChunk`、`DocumentStatus`。

建议组件：

```text
src/views/knowledge-base/
├── KnowledgeBaseList.vue
└── KnowledgeBaseDetail.vue

src/components/knowledge-base/
├── KnowledgeBaseCard.vue
├── CreateKnowledgeBaseDialog.vue
├── DocumentList.vue
├── UploadDocumentDialog.vue
├── ChunkList.vue
├── ChunkCard.vue
└── RagPipelineHint.vue
```

## 12. Mock 与验收

如果真实后端接口缺失，允许使用独立 Mock Adapter，例如 `src/mock/knowledge-base.ts`，并明确标记后续替换点。不得把假数据直接写入页面。

必须覆盖列表 Loading、详情 Loading、上传 Loading、删除 Loading、API Error 和空数据。

完成后执行 type-check、build，以及项目存在时的 lint。
