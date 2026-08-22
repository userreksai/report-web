<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Bell,
  ChartNoAxesCombined,
  ChevronDown,
  CircleUserRound,
  Database,
  FileChartColumn,
  FolderKanban,
  House,
  LogOut,
  Menu,
  PackageOpen,
  PanelLeftClose,
  PanelLeftOpen,
  ShieldCheck,
  X,
} from '@lucide/vue'

const props = defineProps({
  title: { type: String, required: true },
})

const route = useRoute()
const router = useRouter()
const collapsed = ref(false)
const mobileOpen = ref(false)
const userOpen = ref(false)

const navItems = [
  { label: '首页', to: '/', icon: House },
  { label: '项目概览', to: '/projects', icon: FolderKanban },
  { label: '数据库管理', to: '/database', icon: Database },
  { label: '安全审批', to: '/security', icon: ShieldCheck },
  { label: '资源管理', to: '/resources', icon: PackageOpen },
  { label: '杂项 · 月报', to: '/monthly', icon: FileChartColumn },
]

const shellClasses = computed(() => ({ 'is-collapsed': collapsed.value }))

function navigate(to) {
  mobileOpen.value = false
  router.push(to)
}

function logout() {
  sessionStorage.removeItem('report-auth')
  router.replace('/login')
}
</script>

<template>
  <div class="app-shell" :class="shellClasses">
    <button
      v-if="mobileOpen"
      class="sidebar-scrim"
      aria-label="关闭菜单"
      @click="mobileOpen = false"
    />

    <aside class="sidebar" :class="{ 'mobile-open': mobileOpen }">
      <div class="brand">
        <span class="brand-mark"><ChartNoAxesCombined :size="22" /></span>
        <span class="brand-copy">
          <strong>运维报告中心</strong>
          <small>OPS REPORTING</small>
        </span>
        <button class="mobile-close" aria-label="关闭菜单" @click="mobileOpen = false">
          <X :size="18" />
        </button>
      </div>

      <nav class="main-nav" aria-label="主导航">
        <button
          v-for="item in navItems"
          :key="item.to"
          class="nav-item"
          :class="{ active: route.path === item.to }"
          :title="collapsed ? item.label : undefined"
          @click="navigate(item.to)"
        >
          <component :is="item.icon" :size="19" />
          <span>{{ item.label }}</span>
        </button>
      </nav>

      <div class="system-status">
        <span class="status-light" />
        <span>
          <strong>系统运行正常</strong>
          <small>5 张业务表已接入</small>
        </span>
      </div>

      <button class="collapse-button" @click="collapsed = !collapsed">
        <PanelLeftOpen v-if="collapsed" :size="18" />
        <PanelLeftClose v-else :size="18" />
        <span>收起侧栏</span>
      </button>
    </aside>

    <section class="workspace">
      <header class="topbar">
        <div class="topbar-title">
          <button class="menu-button" aria-label="打开菜单" @click="mobileOpen = true">
            <Menu :size="20" />
          </button>
          <div>
            <span>运维工作台</span>
            <strong>{{ props.title }}</strong>
          </div>
        </div>

        <div class="topbar-actions">
          <button class="notification-button" aria-label="通知">
            <Bell :size="18" />
            <span />
          </button>
          <div class="user-menu-wrap">
            <button class="user-button" @click="userOpen = !userOpen">
              <span class="avatar"><CircleUserRound :size="19" /></span>
              <span class="user-copy">
                <strong>运维管理员</strong>
                <small>系统管理员</small>
              </span>
              <ChevronDown :size="15" />
            </button>
            <div v-if="userOpen" class="user-popover">
              <button @click="logout">
                <LogOut :size="16" />
                退出登录
              </button>
            </div>
          </div>
        </div>
      </header>

      <main class="content-area">
        <slot />
      </main>
    </section>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.sidebar {
  position: fixed;
  z-index: 30;
  inset: 0 auto 0 0;
  display: flex;
  width: var(--sidebar-width);
  flex-direction: column;
  background: rgba(5, 15, 25, 0.96);
  border-right: 1px solid var(--border);
  backdrop-filter: blur(18px);
  transition: width 180ms ease, transform 180ms ease;
}

.brand {
  display: flex;
  min-height: var(--header-height);
  align-items: center;
  gap: 12px;
  padding: 0 20px;
  border-bottom: 1px solid var(--border);
}

.brand-mark {
  display: grid;
  width: 36px;
  height: 36px;
  flex: 0 0 auto;
  color: #022e32;
  background: var(--primary);
  border-radius: 9px;
  place-items: center;
}

.brand-copy,
.system-status span,
.user-copy {
  display: grid;
}

.brand-copy {
  overflow: hidden;
  white-space: nowrap;
}

.brand-copy strong {
  font-size: 15px;
}

.brand-copy small {
  margin-top: 2px;
  color: var(--text-muted);
  font: 600 9px/1 var(--font-data);
  letter-spacing: 0.17em;
}

.main-nav {
  display: grid;
  gap: 5px;
  padding: 20px 12px;
}

.nav-item {
  position: relative;
  display: flex;
  width: 100%;
  height: 44px;
  align-items: center;
  gap: 12px;
  padding: 0 13px;
  color: var(--text-soft);
  cursor: pointer;
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  text-align: left;
  transition: 140ms ease;
}

.nav-item:hover {
  color: var(--text);
  background: var(--surface-soft);
}

.nav-item.active {
  color: var(--primary);
  background: var(--primary-soft);
  border-color: rgba(22, 213, 217, 0.18);
}

.nav-item.active::before {
  position: absolute;
  width: 3px;
  height: 20px;
  content: '';
  background: var(--primary);
  border-radius: 0 3px 3px 0;
  inset: 11px auto auto -13px;
}

.nav-item span {
  white-space: nowrap;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: auto 14px 12px;
  padding: 13px;
  overflow: hidden;
  background: rgba(49, 209, 139, 0.05);
  border: 1px solid rgba(49, 209, 139, 0.15);
  border-radius: var(--radius);
  white-space: nowrap;
}

.system-status strong {
  color: var(--success);
  font-size: 12px;
}

.system-status small {
  color: var(--text-muted);
  font-size: 10px;
}

.status-light {
  width: 8px;
  height: 8px;
  flex: 0 0 auto;
  background: var(--success);
  border-radius: 99px;
  box-shadow: 0 0 0 5px rgba(49, 209, 139, 0.08);
}

.collapse-button {
  display: flex;
  height: 48px;
  align-items: center;
  gap: 12px;
  padding: 0 25px;
  color: var(--text-muted);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-top: 1px solid var(--border);
  white-space: nowrap;
}

.collapse-button:hover {
  color: var(--text);
}

.workspace {
  min-height: 100vh;
  margin-left: var(--sidebar-width);
  transition: margin-left 180ms ease;
}

.topbar {
  position: sticky;
  z-index: 20;
  top: 0;
  display: flex;
  height: var(--header-height);
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  background: rgba(7, 19, 31, 0.88);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(18px);
}

.topbar-title,
.topbar-title > div {
  display: flex;
  align-items: center;
}

.topbar-title > div {
  gap: 10px;
}

.topbar-title span {
  color: var(--text-muted);
  font-size: 12px;
}

.topbar-title span::after {
  margin-left: 10px;
  color: var(--border-strong);
  content: '/';
}

.topbar-title strong {
  font-size: 14px;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.notification-button,
.menu-button {
  position: relative;
  display: grid;
  width: 38px;
  height: 38px;
  padding: 0;
  color: var(--text-soft);
  cursor: pointer;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  place-items: center;
}

.notification-button > span {
  position: absolute;
  width: 7px;
  height: 7px;
  background: var(--danger);
  border: 2px solid var(--bg);
  border-radius: 99px;
  inset: 8px 8px auto auto;
}

.user-menu-wrap {
  position: relative;
}

.user-button {
  display: flex;
  min-height: 42px;
  align-items: center;
  gap: 10px;
  padding: 4px 8px 4px 5px;
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: var(--radius-sm);
}

.user-button:hover {
  background: var(--surface-soft);
}

.avatar {
  display: grid;
  width: 34px;
  height: 34px;
  color: var(--primary);
  background: var(--primary-soft);
  border: 1px solid rgba(22, 213, 217, 0.2);
  border-radius: 8px;
  place-items: center;
}

.user-copy {
  min-width: 92px;
  text-align: left;
}

.user-copy strong {
  font-size: 12px;
}

.user-copy small {
  color: var(--text-muted);
  font-size: 10px;
}

.user-popover {
  position: absolute;
  z-index: 10;
  width: 150px;
  padding: 6px;
  background: var(--surface-strong);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  inset: calc(100% + 8px) 0 auto auto;
}

.user-popover button {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 9px;
  padding: 9px 10px;
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: var(--radius-sm);
}

.user-popover button:hover {
  background: var(--surface-hover);
}

.content-area {
  padding: 26px 28px 48px;
}

.is-collapsed .sidebar {
  width: 74px;
}

.is-collapsed .workspace {
  margin-left: 74px;
}

.is-collapsed .brand {
  padding: 0 19px;
}

.is-collapsed .brand-copy,
.is-collapsed .nav-item span,
.is-collapsed .system-status span,
.is-collapsed .collapse-button span {
  display: none;
}

.is-collapsed .nav-item {
  justify-content: center;
  padding: 0;
}

.is-collapsed .system-status {
  justify-content: center;
  margin-inline: 13px;
  padding: 13px 0;
}

.is-collapsed .collapse-button {
  justify-content: center;
  padding: 0;
}

.menu-button,
.mobile-close,
.sidebar-scrim {
  display: none;
}

@media (max-width: 840px) {
  .sidebar {
    width: min(84vw, 280px);
    transform: translateX(-100%);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .workspace,
  .is-collapsed .workspace {
    margin-left: 0;
  }

  .menu-button,
  .mobile-close {
    display: grid;
  }

  .mobile-close {
    width: 32px;
    height: 32px;
    margin-left: auto;
    padding: 0;
    color: var(--text-soft);
    cursor: pointer;
    background: transparent;
    border: 0;
    place-items: center;
  }

  .sidebar-scrim {
    position: fixed;
    z-index: 25;
    display: block;
    padding: 0;
    background: rgba(1, 7, 12, 0.72);
    border: 0;
    inset: 0;
  }

  .topbar {
    padding: 0 16px;
  }

  .topbar-title {
    gap: 10px;
  }

  .topbar-title span,
  .user-copy,
  .user-button > svg {
    display: none;
  }

  .content-area {
    padding: 20px 16px 36px;
  }
}
</style>
