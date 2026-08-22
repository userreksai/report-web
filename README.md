# 运维报告中心前端

基于 Vue 3 + Vite 的六页面运维数据平台。后端已经拆分为独立仓库 [`report-service`](https://github.com/userreksai/report-service)，前端服务使用 8888 端口，后端 API 统一使用 10010 端口。

## 服务关系

```text
浏览器
  └─ https://前端域名/api          report-web 同域入口
               └─ http://127.0.0.1:10010/api   report-service 后端
```

生产环境默认请求同域地址，由 `server.mjs` 转发到本机后端：

```text
/api/v1
```

这样即使页面通过 HTTPS 访问，浏览器也不需要连接没有 TLS 证书的 10010 端口。后端不在本机时，在 `report-web.service` 中设置代理目标：

```ini
Environment=REPORT_API_ORIGIN=http://后端服务器:10010
```

修改后执行 `sudo systemctl daemon-reload && sudo systemctl restart report-web`。如确实需要让浏览器直连另一个已配置 HTTPS 的公开 API，仍可在构建前设置 `VITE_API_BASE_URL`。

## 已实现

- 首页、项目、数据库、安全审批、资源、月报全部通过后端接口查询。
- 全站共享近 7/30/90 天、本月和自定义时间范围。
- 快捷时间自动查询，详情和“查看全部”继续使用当前范围。
- 加载、空数据、错误、重新查询状态。
- 展示后台更新时间、源系统时间、数据来源和统计口径。
- 登录页面保留，业务页面当前可直接进入。

## 本地开发

先启动后端，确认健康检查正常：

```bash
curl http://127.0.0.1:10010/api/v1/health
```

然后启动前端：

```bash
pnpm install
pnpm run dev
```

Vite 监听 `0.0.0.0:8888`，开发和生产服务都会把 `/api` 转发至 `127.0.0.1:10010`。

## 前端服务器部署

```bash
bash deploy/install-report-web.sh
```

常用命令：

```bash
sudo systemctl status report-web
sudo systemctl restart report-web
sudo journalctl -u report-web -f
```

后端安装与 systemd 使用方法请查看 [`report-service` 部署说明](https://github.com/userreksai/report-service#服务器一键部署)。

## Python 接口示例

`examples/` 中的六份脚本默认请求：

```text
http://127.0.0.1:10010/api/v1
```

完整字段、表结构和统计口径见 [接口使用手册](docs/API.md)。
