# AgentForge Frontend Foundation and Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable AgentForge frontend slice with the shared application shell, navigation, routing, design primitives, and a complete Mock-powered Dashboard.

**Architecture:** Create a standalone Vue application in `agent_forge/frontend/`. Route-level views render inside one `AppLayout`; shared layout and common components own navigation, breadcrumbs, status badges, empty/loading states, and code presentation. Dashboard data is strongly typed and isolated in `src/mock/dashboard.ts`, so future API adapters can replace Mock data without rewriting view components.

**Tech Stack:** Vue 3, TypeScript, Vite, Tailwind CSS, shadcn-vue, Vue Router, Pinia, Lucide Vue, Vitest, Vue Test Utils, npm.

## Global Constraints

- Product name is `AgentForge`; never use `Enterprise AI Agent Platform` as the brand.
- Chinese product description is `企业级 AI Agent 教学平台`.
- Use a light gray application background, white cards, restrained indigo/violet accents, light borders, `rounded-xl`, and minimal shadows.
- Formal product icons use Lucide; emoji may appear only in teaching or Mock content.
- The first implementation slice includes the shared shell and Dashboard only. Other business pages are route placeholders.
- All simulated capabilities display a visible `Demo` badge.
- Use Vue 3 Composition API and `<script setup lang="ts">`.
- Do not place Mock data directly inside Vue pages.
- Do not add authentication, organization, tenant, billing, marketplace, workflow canvas, or production APIs.
- Primary desktop targets are 1440px, 1280px, and 1024px.
- Run tests before implementation changes and verify `npm run test`, `npm run type-check`, and `npm run build` before completion.

---

## File Map

```text
agent_forge/frontend/
├── package.json
├── vite.config.ts
├── vitest.config.ts
├── tsconfig.app.json
├── components.json
├── src/
│   ├── App.vue
│   ├── main.ts
│   ├── style.css
│   ├── assets/
│   │   └── agentforge-mark.svg
│   ├── components/
│   │   ├── common/
│   │   │   ├── DemoBadge.vue
│   │   │   ├── EmptyState.vue
│   │   │   ├── PageHeader.vue
│   │   │   └── StatusBadge.vue
│   │   ├── dashboard/
│   │   │   ├── LearningPath.vue
│   │   │   ├── QuickStart.vue
│   │   │   ├── RecentAgentList.vue
│   │   │   ├── RecentKnowledgeBases.vue
│   │   │   ├── RecentRunTable.vue
│   │   │   ├── ServiceStatus.vue
│   │   │   ├── StatCard.vue
│   │   │   ├── UsageOverview.vue
│   │   │   └── WelcomeHeader.vue
│   │   └── layout/
│   │       ├── AppBreadcrumb.vue
│   │       ├── AppHeader.vue
│   │       ├── AppSidebar.vue
│   │       └── EnvironmentBadge.vue
│   ├── layouts/
│   │   └── AppLayout.vue
│   ├── mock/
│   │   └── dashboard.ts
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   └── app.ts
│   ├── types/
│   │   ├── common.ts
│   │   └── dashboard.ts
│   ├── utils/
│   │   └── cn.ts
│   └── views/
│       ├── PlaceholderView.vue
│       └── dashboard/
│           └── Dashboard.vue
└── tests/
    ├── setup.ts
    ├── dashboard-data.spec.ts
    ├── dashboard-view.spec.ts
    ├── layout.spec.ts
    └── router.spec.ts
```

---

### Task 1: Scaffold the Vue Application and Test Harness

**Files:**
- Create: `agent_forge/frontend/package.json`
- Create: `agent_forge/frontend/vite.config.ts`
- Create: `agent_forge/frontend/vitest.config.ts`
- Create: `agent_forge/frontend/tsconfig.app.json`
- Create: `agent_forge/frontend/src/main.ts`
- Create: `agent_forge/frontend/src/App.vue`
- Create: `agent_forge/frontend/src/style.css`
- Create: `agent_forge/frontend/tests/setup.ts`

**Interfaces:**
- Produces: npm scripts `dev`, `build`, `type-check`, and `test`.
- Produces: `@` alias mapped to `src/`.
- Produces: a Vitest jsdom environment with jest-dom matchers.

- [ ] **Step 1: Scaffold Vue + TypeScript**

Run from `agent_forge/`:

```bash
npm create vite@latest frontend -- --template vue-ts
cd frontend
npm install
npm install vue-router pinia axios lucide-vue-next
npm install -D tailwindcss @tailwindcss/vite vitest @vue/test-utils jsdom @testing-library/vue @testing-library/jest-dom @pinia/testing @types/node
npx shadcn-vue@latest init
npx shadcn-vue@latest add button card badge tooltip avatar separator progress skeleton table
```

Expected: `frontend/package.json` exists and `npm run build` succeeds with the default app.

- [ ] **Step 2: Configure Vite, Tailwind, aliases, and Vitest**

Update `vite.config.ts` to include Vue, Tailwind's Vite plugin, and the `@` alias:

```ts
import path from 'node:path'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

Create `vitest.config.ts`:

```ts
import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
})
```

Create `tests/setup.ts`:

```ts
import '@testing-library/jest-dom/vitest'
```

Update `tsconfig.app.json` so application and test imports resolve consistently:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  }
}
```

- [ ] **Step 3: Add npm scripts**

Ensure `package.json` contains:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "type-check": "vue-tsc --noEmit",
    "test": "vitest run"
  }
}
```

- [ ] **Step 4: Add the global Tailwind entry**

Replace `src/style.css` with:

```css
@import "tailwindcss";

:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #111827;
  background: #f7f8fa;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 1024px;
  min-height: 100vh;
  background: #f7f8fa;
}

button,
input,
textarea,
select {
  font: inherit;
}
```

- [ ] **Step 5: Verify the scaffold**

Run:

```bash
npm run type-check
npm run test
npm run build
```

Expected: all commands exit 0. Vitest may report zero tests at this step.

- [ ] **Step 6: Commit**

```bash
git add agent_forge/frontend
git commit -m "chore: scaffold AgentForge frontend"
```

---

### Task 2: Add Typed Dashboard Mock Data

**Files:**
- Create: `agent_forge/frontend/src/types/common.ts`
- Create: `agent_forge/frontend/src/types/dashboard.ts`
- Create: `agent_forge/frontend/src/mock/dashboard.ts`
- Create: `agent_forge/frontend/tests/dashboard-data.spec.ts`

**Interfaces:**
- Produces: `DashboardStats`, `RecentAgent`, `RecentRun`, `RecentKnowledgeBase`, `ServiceStatus`, `UsageSummary`, and `LearningStep`.
- Produces: `dashboardStats`, `recentAgents`, `recentRuns`, `recentKnowledgeBases`, `serviceStatus`, `usageSummary`, and `learningPath`.

- [ ] **Step 1: Write the failing Mock-data test**

Create `tests/dashboard-data.spec.ts`:

```ts
import {
  dashboardStats,
  learningPath,
  recentAgents,
  recentKnowledgeBases,
  recentRuns,
  serviceStatus,
} from '@/mock/dashboard'

describe('dashboard Mock data', () => {
  it('provides the four core metrics', () => {
    expect(dashboardStats).toHaveLength(4)
    expect(dashboardStats.map((item) => item.key)).toEqual([
      'agents',
      'knowledgeBases',
      'runs',
      'tokens',
    ])
  })

  it('keeps dashboard links inside the documented route map', () => {
    expect(recentAgents[0].href).toMatch(/^\/agents\//)
    expect(recentRuns[0].href).toMatch(/^\/runs\//)
    expect(recentKnowledgeBases[0].href).toMatch(/^\/knowledge-bases\//)
  })

  it('marks educational services as Demo', () => {
    expect(serviceStatus.filter((item) => item.mode === 'demo')).toHaveLength(4)
  })

  it('provides the six-step learning path', () => {
    expect(learningPath).toHaveLength(6)
  })
})
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
npm run test -- dashboard-data.spec.ts
```

Expected: FAIL because `@/mock/dashboard` does not exist.

- [ ] **Step 3: Define the types**

Create `src/types/common.ts`:

```ts
export type ResourceStatus = 'published' | 'draft' | 'offline'
export type RunStatus = 'success' | 'failed' | 'running' | 'waiting_approval'
export type ServiceMode = 'healthy' | 'demo'
```

Create `src/types/dashboard.ts` with exact interfaces:

```ts
import type { ResourceStatus, RunStatus, ServiceMode } from './common'

export interface DashboardStat {
  key: 'agents' | 'knowledgeBases' | 'runs' | 'tokens'
  label: string
  value: string
  detail: string
  icon: 'Bot' | 'Database' | 'Activity' | 'Coins'
}

export interface RecentAgent {
  id: string
  name: string
  status: ResourceStatus
  model: string
  knowledgeBaseCount: number
  toolCount: number
  mcpCount: number
  href: string
}

export interface RecentRun {
  traceId: string
  agentName: string
  status: RunStatus
  duration: string
  tokens: number
  startedAt: string
  href: string
}

export interface RecentKnowledgeBase {
  id: string
  name: string
  documentCount: number
  chunkCount: number
  href: string
}

export interface ServiceStatus {
  name: string
  status: string
  mode: ServiceMode
}

export interface UsageSummary {
  runs: number
  successful: number
  failed: number
  averageLatency: string
  averageTokens: number
}

export interface LearningStep {
  label: string
  state: 'complete' | 'next'
  href: string
}
```

- [ ] **Step 4: Create typed Mock data**

Create `src/mock/dashboard.ts` exporting the exact symbols tested above. Use AgentForge demo values from the design specification: 3 Agents, 2 knowledge bases, 28 daily runs, 12.6K tokens, and ¥0.032 total cost. Include at least two recent Agents, three recent Runs, two recent knowledge bases, five service statuses, one usage summary, and six learning steps.

- [ ] **Step 5: Run tests and verify GREEN**

Run:

```bash
npm run test -- dashboard-data.spec.ts
```

Expected: 4 tests pass.

- [ ] **Step 6: Commit**

```bash
git add agent_forge/frontend/src/types agent_forge/frontend/src/mock agent_forge/frontend/tests/dashboard-data.spec.ts
git commit -m "feat: add typed dashboard mock data"
```

---

### Task 3: Implement Router Metadata and Placeholder Routes

**Files:**
- Create: `agent_forge/frontend/src/router/index.ts`
- Create: `agent_forge/frontend/src/views/PlaceholderView.vue`
- Create: `agent_forge/frontend/tests/router.spec.ts`
- Modify: `agent_forge/frontend/src/main.ts`
- Modify: `agent_forge/frontend/src/App.vue`

**Interfaces:**
- Produces: `router` with `/` redirecting to `/dashboard`.
- Produces: route meta fields `title`, `icon`, `breadcrumb`, and optional `parent`.

- [ ] **Step 1: Write the failing router test**

Create `tests/router.spec.ts`:

```ts
import router from '@/router'

describe('AgentForge router', () => {
  it('redirects the root route to dashboard', async () => {
    await router.push('/')
    await router.isReady()
    expect(router.currentRoute.value.fullPath).toBe('/dashboard')
  })

  it('contains all documented top-level routes', () => {
    const paths = router.getRoutes().map((route) => route.path)
    expect(paths).toEqual(expect.arrayContaining([
      '/dashboard',
      '/agents',
      '/knowledge-bases',
      '/capabilities',
      '/chat',
      '/runs',
    ]))
  })

  it('defines route metadata for breadcrumb and navigation state', () => {
    const agentRoute = router.getRoutes().find((route) => route.path === '/agents/:id')
    expect(agentRoute?.meta.parent).toBe('/agents')
    expect(agentRoute?.meta.breadcrumb).toBe(true)
  })
})
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
npm run test -- router.spec.ts
```

Expected: FAIL because the router module does not exist.

- [ ] **Step 3: Implement documented routes**

Create `src/router/index.ts` with `/dashboard`, `/agents`, `/agents/create`, `/agents/:id`, `/knowledge-bases`, `/knowledge-bases/:id`, `/capabilities`, `/capabilities/tools/:id`, `/capabilities/mcp/:id`, `/chat`, `/runs`, and `/runs/:traceId`. Only `/dashboard` loads the real Dashboard view in this phase; all other routes load `PlaceholderView.vue` with route metadata.

- [ ] **Step 4: Mount Router and Pinia**

Update `src/main.ts`:

```ts
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import './style.css'

createApp(App)
  .use(createPinia())
  .use(router)
  .mount('#app')
```

Update `src/App.vue` to render only `<RouterView />`.

- [ ] **Step 5: Run tests and verify GREEN**

Run:

```bash
npm run test -- router.spec.ts
```

Expected: 3 tests pass.

- [ ] **Step 6: Commit**

```bash
git add agent_forge/frontend/src/router agent_forge/frontend/src/views/PlaceholderView.vue agent_forge/frontend/src/main.ts agent_forge/frontend/src/App.vue agent_forge/frontend/tests/router.spec.ts
git commit -m "feat: add frontend route map"
```

---

### Task 4: Build the Shared Application Layout

**Files:**
- Create: `agent_forge/frontend/src/assets/agentforge-mark.svg`
- Create: `agent_forge/frontend/src/stores/app.ts`
- Create: `agent_forge/frontend/src/layouts/AppLayout.vue`
- Create: `agent_forge/frontend/src/components/layout/AppSidebar.vue`
- Create: `agent_forge/frontend/src/components/layout/AppHeader.vue`
- Create: `agent_forge/frontend/src/components/layout/AppBreadcrumb.vue`
- Create: `agent_forge/frontend/src/components/layout/EnvironmentBadge.vue`
- Create: `agent_forge/frontend/tests/layout.spec.ts`
- Modify: `agent_forge/frontend/src/router/index.ts`

**Interfaces:**
- Produces: `useAppStore()` with `sidebarCollapsed` and `toggleSidebar()`.
- Produces: an `AppLayout` that wraps all route views.
- Produces: navigation links for 工作台, Agent 管理, 知识库, 能力中心, Chat 调试, and 运行记录.

- [ ] **Step 1: Write the failing layout test**

Create `tests/layout.spec.ts`:

```ts
import { createTestingPinia } from '@pinia/testing'
import { render, screen } from '@testing-library/vue'
import { createMemoryHistory, createRouter } from 'vue-router'

import AppLayout from '@/layouts/AppLayout.vue'

describe('AppLayout', () => {
  it('renders AgentForge navigation and Demo environment status', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', component: { template: '<div>content</div>' } }],
    })

    await router.push('/')
    await router.isReady()

    render(AppLayout, {
      global: {
        plugins: [router, createTestingPinia({ stubActions: false })],
      },
    })

    expect(screen.getByText('AgentForge')).toBeInTheDocument()
    expect(screen.getByText('工作台')).toBeInTheDocument()
    expect(screen.getByText('Agent 管理')).toBeInTheDocument()
    expect(screen.getByText('知识库')).toBeInTheDocument()
    expect(screen.getByText('能力中心')).toBeInTheDocument()
    expect(screen.getByText('Chat 调试')).toBeInTheDocument()
    expect(screen.getByText('运行记录')).toBeInTheDocument()
    expect(screen.getByText('教学版')).toBeInTheDocument()
  })
})
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
npm run test -- layout.spec.ts
```

Expected: FAIL because `AppLayout.vue` does not exist.

- [ ] **Step 3: Implement the layout store and components**

Create `src/stores/app.ts`:

```ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return { sidebarCollapsed, toggleSidebar }
})
```

Use this exact navigation model in `AppSidebar.vue`:

```ts
const navigation = [
  { label: '工作台', icon: LayoutDashboard, to: '/dashboard' },
  {
    label: '构建',
    children: [
      { label: 'Agent 管理', icon: Bot, to: '/agents' },
      { label: '知识库', icon: Database, to: '/knowledge-bases' },
      { label: '能力中心', icon: Wrench, to: '/capabilities' },
    ],
  },
  {
    label: '调试与运行',
    children: [
      { label: 'Chat 调试', icon: MessageSquare, to: '/chat' },
      { label: '运行记录', icon: Route, to: '/runs' },
    ],
  },
]
```

Implement a collapsible Sidebar using these Lucide icons, a Header with breadcrumbs, `API 正常`, help, and `Demo User`, and an `EnvironmentBadge` that shows `教学版` plus the five Demo subsystem labels. Use the exact Chinese group headings above.

Create a deterministic SVG mark that combines an abstract `A`, connected nodes, a runtime center, and a short trace path. Use the mark only as an AgentForge-owned vector asset; do not copy third-party logos.

- [ ] **Step 4: Nest business routes under AppLayout**

Update the router so `AppLayout` renders child routes through `<RouterView />`. Root still redirects to `/dashboard`.

- [ ] **Step 5: Run tests and verify GREEN**

Run:

```bash
npm run test -- layout.spec.ts router.spec.ts
```

Expected: layout and router tests pass.

- [ ] **Step 6: Commit**

```bash
git add agent_forge/frontend/src/assets agent_forge/frontend/src/stores agent_forge/frontend/src/layouts agent_forge/frontend/src/components/layout agent_forge/frontend/src/router agent_forge/frontend/tests/layout.spec.ts agent_forge/frontend/package.json agent_forge/frontend/package-lock.json
git commit -m "feat: add AgentForge application shell"
```

---

### Task 5: Add Shared Page Components

**Files:**
- Create: `agent_forge/frontend/src/components/common/PageHeader.vue`
- Create: `agent_forge/frontend/src/components/common/EmptyState.vue`
- Create: `agent_forge/frontend/src/components/common/StatusBadge.vue`
- Create: `agent_forge/frontend/src/components/common/DemoBadge.vue`
- Create: `agent_forge/frontend/src/utils/cn.ts`
- Create: `agent_forge/frontend/tests/common-components.spec.ts`

**Interfaces:**
- Produces: `PageHeader` props `title`, `description` with an `actions` slot.
- Produces: `EmptyState` props `title`, `description` with an `action` slot.
- Produces: status and Demo badges reused by Dashboard and later pages.

- [ ] **Step 1: Write failing component tests**

Create `tests/common-components.spec.ts`:

```ts
import { render, screen } from '@testing-library/vue'

import DemoBadge from '@/components/common/DemoBadge.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'

describe('common components', () => {
  it('renders page title, description, and actions', () => {
    render(PageHeader, {
      props: { title: '工作台', description: '管理、调试并观察你的 AI Agent' },
      slots: { actions: '<button>Chat 调试</button>' },
    })
    expect(screen.getByText('工作台')).toBeInTheDocument()
    expect(screen.getByText('管理、调试并观察你的 AI Agent')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Chat 调试' })).toBeInTheDocument()
  })

  it('renders a reusable empty state action', () => {
    render(EmptyState, {
      props: { title: '暂无运行记录', description: '前往 Chat 调试完成第一次 Agent Run。' },
      slots: { action: '<a href="/chat">开始调试</a>' },
    })
    expect(screen.getByText('暂无运行记录')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: '开始调试' })).toHaveAttribute('href', '/chat')
  })

  it('renders status and Demo badges', () => {
    render(StatusBadge, { props: { status: 'success' } })
    render(DemoBadge)
    expect(screen.getByText('成功')).toBeInTheDocument()
    expect(screen.getByText('Demo')).toBeInTheDocument()
  })
})
```

- [ ] **Step 2: Verify RED**

Run:

```bash
npm run test -- common-components.spec.ts
```

Expected: FAIL because the components do not exist.

- [ ] **Step 3: Implement the minimal shared components**

Use Tailwind classes matching the design system. Avoid API logic and page-specific copy.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
npm run test -- common-components.spec.ts
```

Expected: all shared component tests pass.

- [ ] **Step 5: Commit**

```bash
git add agent_forge/frontend/src/components/common agent_forge/frontend/src/utils agent_forge/frontend/tests/common-components.spec.ts
git commit -m "feat: add shared frontend components"
```

---

### Task 6: Implement the Dashboard Components and View

**Files:**
- Create: `agent_forge/frontend/src/components/dashboard/WelcomeHeader.vue`
- Create: `agent_forge/frontend/src/components/dashboard/StatCard.vue`
- Create: `agent_forge/frontend/src/components/dashboard/QuickStart.vue`
- Create: `agent_forge/frontend/src/components/dashboard/RecentAgentList.vue`
- Create: `agent_forge/frontend/src/components/dashboard/RecentRunTable.vue`
- Create: `agent_forge/frontend/src/components/dashboard/RecentKnowledgeBases.vue`
- Create: `agent_forge/frontend/src/components/dashboard/ServiceStatus.vue`
- Create: `agent_forge/frontend/src/components/dashboard/UsageOverview.vue`
- Create: `agent_forge/frontend/src/components/dashboard/LearningPath.vue`
- Create: `agent_forge/frontend/src/views/dashboard/Dashboard.vue`
- Create: `agent_forge/frontend/tests/dashboard-view.spec.ts`

**Interfaces:**
- Consumes: all typed exports from `src/mock/dashboard.ts`.
- Produces: a complete `/dashboard` route with documented navigation links.

- [ ] **Step 1: Write the failing Dashboard view test**

Create `tests/dashboard-view.spec.ts`:

```ts
import { render, screen } from '@testing-library/vue'
import { createMemoryHistory, createRouter } from 'vue-router'

import Dashboard from '@/views/dashboard/Dashboard.vue'

describe('Dashboard', () => {
  it('shows the AgentForge welcome, four metrics, and Demo services', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', component: Dashboard }],
    })

    await router.push('/')
    await router.isReady()

    render(Dashboard, { global: { plugins: [router] } })

    expect(screen.getByText('欢迎回到 AgentForge')).toBeInTheDocument()
    expect(screen.getByText('Agents')).toBeInTheDocument()
    expect(screen.getByText('知识库')).toBeInTheDocument()
    expect(screen.getByText('今日运行')).toBeInTheDocument()
    expect(screen.getByText('Token')).toBeInTheDocument()
    expect(screen.getAllByText('Demo').length).toBeGreaterThanOrEqual(4)
  })

  it('renders links to the core product flow', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/', component: Dashboard },
        { path: '/agents/create', component: { template: '<div />' } },
        { path: '/chat', component: { template: '<div />' } },
      ],
    })

    await router.push('/')
    await router.isReady()

    render(Dashboard, { global: { plugins: [router] } })
    expect(screen.getByRole('link', { name: /创建 Agent/ })).toHaveAttribute('href', '/agents/create')
    expect(screen.getByRole('link', { name: /Chat 调试/ })).toHaveAttribute('href', '/chat')
  })
})
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
npm run test -- dashboard-view.spec.ts
```

Expected: FAIL because Dashboard components do not exist.

- [ ] **Step 3: Implement Dashboard components**

Implement each documented section as a focused component. Use responsive 4-column/2-column metric grids, Card-based quick starts and Agents, a compact Runs table, knowledge-base links, service Demo badges, usage progress, and the six-step learning path.

All copy and links must match `docs/frontend/dashboard.md`. Do not add charts beyond lightweight CSS bars.

- [ ] **Step 4: Run tests and verify GREEN**

Run:

```bash
npm run test -- dashboard-view.spec.ts dashboard-data.spec.ts
```

Expected: all Dashboard tests pass.

- [ ] **Step 5: Commit**

```bash
git add agent_forge/frontend/src/components/dashboard agent_forge/frontend/src/views/dashboard agent_forge/frontend/tests/dashboard-view.spec.ts
git commit -m "feat: implement AgentForge dashboard"
```

---

### Task 7: Verify the First Frontend Slice

**Files:**
- Modify if needed: `agent_forge/frontend/src/style.css`
- Modify if needed: files touched in Tasks 1-6

**Interfaces:**
- Produces: a verified, buildable frontend foundation and Dashboard.

- [ ] **Step 1: Run all automated checks**

Run from `agent_forge/frontend/`:

```bash
npm run test
npm run type-check
npm run build
```

Expected: all tests pass, TypeScript reports no errors, and Vite produces `dist/`.

- [ ] **Step 2: Start the frontend**

Run:

```bash
npm run dev -- --host 127.0.0.1
```

Expected: Vite prints a local URL and `/dashboard` loads.

- [ ] **Step 3: Perform visual QA**

Check 1440px, 1280px, and 1024px widths:

- Sidebar expands and collapses.
- Breadcrumb and Header align correctly.
- Dashboard shows four KPI cards in four columns at 1440px and two columns near 1024px.
- No horizontal overflow appears inside the main content.
- Demo services are visibly marked.
- All Dashboard navigation targets resolve to a real view or intentional placeholder.

- [ ] **Step 4: Re-run automated checks after visual fixes**

```bash
npm run test
npm run type-check
npm run build
```

Expected: all commands exit 0.

- [ ] **Step 5: Commit**

```bash
git add agent_forge/frontend
git commit -m "test: verify frontend foundation and dashboard"
```
