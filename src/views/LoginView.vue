<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowRight,
  ChartNoAxesCombined,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  ShieldCheck,
  UserRound,
} from '@lucide/vue'

const router = useRouter()
const username = ref('admin')
const password = ref('ops-report')
const remember = ref(true)
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

function submit() {
  error.value = ''
  if (!username.value.trim() || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }
  loading.value = true
  window.setTimeout(() => {
    sessionStorage.setItem('report-auth', username.value.trim())
    router.replace('/')
  }, 420)
}
</script>

<template>
  <main class="login-page">
    <div class="grid-layer" />
    <section class="login-brand">
      <div class="brand-badge"><ChartNoAxesCombined :size="25" /></div>
      <p>OPS REPORTING CENTER</p>
      <h1>
        <span class="headline-line">把复杂的运维数据，</span>
        <span class="headline-line headline-accent">收敛到一个视图。</span>
      </h1>
      <p class="brand-description">
        统一查看项目、数据库、安全审批、资源投入与月报，快速识别需要关注的变化。
      </p>
      <div class="brand-points">
        <span><CheckCircle2 :size="16" /> 统一数据口径</span>
        <span><CheckCircle2 :size="16" /> 实时运行状态</span>
        <span><CheckCircle2 :size="16" /> 安全访问控制</span>
      </div>
    </section>

    <section class="login-card-wrap">
      <form class="login-card" @submit.prevent="submit">
        <div class="login-card-heading">
          <span class="login-icon"><ShieldCheck :size="21" /></span>
          <div>
            <h2>登录运维报告中心</h2>
            <p>使用您的运维平台账号继续</p>
          </div>
        </div>

        <label class="field-label" for="username">用户名</label>
        <div class="input-wrap">
          <UserRound :size="17" />
          <input
            id="username"
            v-model="username"
            autocomplete="username"
            placeholder="请输入用户名"
          />
        </div>

        <label class="field-label" for="password">密码</label>
        <div class="input-wrap">
          <LockKeyhole :size="17" />
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password"
            placeholder="请输入密码"
          />
          <button type="button" :aria-label="showPassword ? '隐藏密码' : '显示密码'" @click="showPassword = !showPassword">
            <EyeOff v-if="showPassword" :size="17" />
            <Eye v-else :size="17" />
          </button>
        </div>

        <div class="form-options">
          <label>
            <input v-model="remember" type="checkbox" />
            保持登录
          </label>
          <span>仅限内部网络访问</span>
        </div>

        <p v-if="error" class="form-error">{{ error }}</p>

        <button class="login-button" :disabled="loading">
          {{ loading ? '正在进入…' : '登录' }}
          <ArrowRight v-if="!loading" :size="17" />
        </button>

        <div class="online-status">
          <span />
          系统在线 · 数据源连接正常
        </div>
      </form>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  position: relative;
  display: grid;
  min-height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(circle at 17% 25%, rgba(22, 213, 217, 0.12), transparent 25rem),
    radial-gradient(circle at 82% 80%, rgba(102, 167, 255, 0.08), transparent 28rem),
    var(--bg-deep);
  grid-template-columns: minmax(0, 1.1fr) minmax(430px, 0.9fr);
}

.grid-layer {
  position: absolute;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(38, 72, 91, 0.14) 1px, transparent 1px),
    linear-gradient(90deg, rgba(38, 72, 91, 0.14) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(to bottom right, black, transparent 72%);
  inset: 0;
}

.login-brand,
.login-card-wrap {
  position: relative;
  z-index: 1;
}

.login-brand {
  display: flex;
  max-width: 780px;
  justify-content: center;
  padding: clamp(48px, 8vw, 112px);
  flex-direction: column;
}

.brand-badge {
  display: grid;
  width: 44px;
  height: 44px;
  margin-bottom: 20px;
  color: #003236;
  background: var(--primary);
  border-radius: 11px;
  box-shadow: 0 0 34px rgba(22, 213, 217, 0.2);
  place-items: center;
}

.login-brand > p:first-of-type {
  margin: 0 0 14px;
  color: var(--primary);
  font: 650 11px/1 var(--font-data);
  letter-spacing: 0.2em;
}

.login-brand h1 {
  max-width: 720px;
  margin: 0;
  font-size: clamp(36px, 4vw, 56px);
  line-height: 1.12;
  letter-spacing: -0.045em;
}

.headline-line {
  display: block;
  white-space: nowrap;
}

.headline-accent {
  color: var(--primary);
}

.brand-description {
  max-width: 580px;
  margin: 24px 0 0;
  color: var(--text-soft);
  font-size: 16px;
  line-height: 1.8;
}

.brand-points {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 22px;
  margin-top: 34px;
}

.brand-points span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: var(--text-soft);
  font-size: 12px;
}

.brand-points svg {
  color: var(--success);
}

.login-card-wrap {
  display: grid;
  padding: 32px;
  background: rgba(7, 19, 31, 0.36);
  border-left: 1px solid rgba(43, 76, 98, 0.35);
  place-items: center;
}

.login-card {
  width: min(100%, 440px);
  padding: 34px;
  background: linear-gradient(145deg, rgba(19, 37, 56, 0.96), rgba(10, 25, 38, 0.98));
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.login-card-heading {
  display: flex;
  align-items: center;
  gap: 13px;
  margin-bottom: 30px;
}

.login-icon {
  display: grid;
  width: 42px;
  height: 42px;
  color: var(--primary);
  background: var(--primary-soft);
  border: 1px solid rgba(22, 213, 217, 0.2);
  border-radius: 10px;
  place-items: center;
}

.login-card h2 {
  margin: 0;
  font-size: 19px;
}

.login-card-heading p {
  margin: 3px 0 0;
  color: var(--text-muted);
  font-size: 11px;
}

.field-label {
  display: block;
  margin: 0 0 8px;
  color: var(--text-soft);
  font-size: 11px;
  font-weight: 650;
}

.input-wrap {
  display: flex;
  height: 46px;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
  padding: 0 12px;
  color: var(--text-muted);
  background: var(--bg-deep);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.input-wrap:focus-within {
  color: var(--primary);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-soft);
}

.input-wrap input {
  min-width: 0;
  flex: 1;
  color: var(--text);
  background: transparent;
  border: 0;
  outline: 0;
}

.input-wrap button {
  display: grid;
  padding: 5px;
  color: var(--text-muted);
  cursor: pointer;
  background: transparent;
  border: 0;
  place-items: center;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: -2px;
  color: var(--text-muted);
  font-size: 10px;
}

.form-options label {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
}

.form-options input {
  accent-color: var(--primary);
}

.form-error {
  margin: 12px 0 0;
  color: var(--danger);
  font-size: 11px;
}

.login-button {
  display: flex;
  width: 100%;
  height: 46px;
  align-items: center;
  justify-content: center;
  gap: 9px;
  margin-top: 22px;
  color: #003034;
  cursor: pointer;
  background: var(--primary);
  border: 0;
  border-radius: var(--radius-sm);
  font-weight: 750;
}

.login-button:hover:not(:disabled) {
  background: #46e5e6;
}

.login-button:disabled {
  cursor: wait;
  opacity: 0.7;
}

.online-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 22px;
  color: var(--text-muted);
  font-size: 10px;
}

.online-status span {
  width: 7px;
  height: 7px;
  background: var(--success);
  border-radius: 999px;
  box-shadow: 0 0 10px rgba(49, 209, 139, 0.65);
}

@media (max-width: 900px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .login-brand {
    display: none;
  }

  .login-card-wrap {
    border-left: 0;
  }
}

@media (max-width: 520px) {
  .login-card-wrap {
    padding: 16px;
  }

  .login-card {
    padding: 26px 22px;
  }
}
</style>
