# 运维报告中心

基于 Vue 3 + Vite 的运维数据可视化前端，包含登录、首页、项目概览、数据库管理、安全审批概览、资源管理和运维月报。

## 本地运行

```bash
npm install
npm run dev
```

开发服务固定监听 `0.0.0.0:8888`。

## 构建与生产运行

```bash
npm run build
npm run start
```

生产静态服务默认监听 `0.0.0.0:8888`，可通过 `PORT` 环境变量调整。

## 服务器部署

服务器源码目录为 `/opt/report-web`。首次部署可执行：

```bash
git clone https://github.com/userreksai/report-web.git /opt/report-web
cd /opt/report-web
npm install --no-audit --no-fund
npm run build
sudo install -m 0644 deploy/report-web.service /etc/systemd/system/report-web.service
sudo systemctl daemon-reload
sudo systemctl enable --now report-web
```

常用维护命令：

```bash
sudo systemctl status report-web
sudo systemctl restart report-web
sudo journalctl -u report-web -f
```

也可以在有 `git`、Node.js 和 npm 的服务器上直接运行：

```bash
bash deploy/install-report-web.sh
```

默认 systemd 服务使用 `www-data` 用户。如服务器没有该用户，请修改 `deploy/report-web.service` 中的 `User` 和 `Group`。
