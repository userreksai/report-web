# 运维报告中心接口使用手册

本文按“第一次接接口也能照着做”的方式说明。所有接口使用 JSON，路径前缀为 `/api/v1`。

## 一、先理解两个时间

- `report_date`：业务数据归属日期，格式固定为 `YYYY-MM-DD`。它是每张表的唯一键。
- `source_updated_at`：源系统生成这份数据的实际时间，必须是带时区的 RFC3339，例如 `2026-08-22T09:30:00+07:00`。

同一个接口、同一个 `report_date`：

- 第一次 POST：数据库执行新增，HTTP 201，`action` 为 `created`。
- 再次 POST：整份 `data` 覆盖该日旧数据，HTTP 200，`action` 为 `updated`。

因此脚本失败后可以安全重跑，不会出现同一天两行。请注意：覆盖是整份日数据替换，不是字段累加；重跑时应发送完整 `data`。

## 二、接口清单

| 页面/数据表 | 查询 | 上报 | Python 完整示例 |
|---|---|---|---|
| 首页 | `GET /dashboard` | 首页由四张业务表汇总，不单独上报 | `examples/dashboard_query.py` |
| 项目概览 | `GET /projects` | `POST /projects` | `examples/projects_upload.py` |
| 数据库管理 | `GET /database` | `POST /database` | `examples/database_upload.py` |
| 安全审批 | `GET /security` | `POST /security` | `examples/security_upload.py` |
| 资源管理 | `GET /resources` | `POST /resources` | `examples/resources_upload.py` |
| 杂项·月报 | `GET /monthly` | `POST /monthly` | `examples/monthly_upload.py` |

健康检查：`GET /api/v1/health`。

## 三、统一上报格式

```json
{
  "report_date": "2026-08-22",
  "source": "源系统或负责部门名称",
  "source_updated_at": "2026-08-22T09:30:00+07:00",
  "data": {
    "这里是各接口自己的字段": 1
  }
}
```

如果服务器设置了 `OPS_API_KEY`，POST 还必须带请求头：

```text
Authorization: Bearer 服务器分配的密钥
```

密钥不要写死在脚本中。Python 示例从同名环境变量读取。

## 四、统一查询格式

```text
GET /api/v1/projects?start_date=2026-08-01&end_date=2026-08-22
```

开始和结束日期都包含。最多查询 366 天。项目、资源、月报默认只返回部分详情；要查看当前范围全部详情时追加 `view=all`，服务端最多返回 500 条：

```text
GET /api/v1/projects?start_date=2026-08-01&end_date=2026-08-22&view=all
```

返回中的 `meta` 统一解释数据：

```json
{
  "meta": {
    "start_date": "2026-08-01",
    "end_date": "2026-08-22",
    "record_count": 12,
    "updated_at": "后端最后入库时间",
    "source_updated_at": "源系统最新数据时间",
    "sources": ["Jira", "Prometheus"],
    "methodology": "当前页面的统计口径",
    "timezone": "Asia/Bangkok"
  }
}
```

## 五、各表字段与统计口径

### 项目表

数量字段填写 `report_date` 当天发生量：Jira 新增/纳入项、完成项、告警、发布、变更和各环境部署数。`incidents` 与 `tasks` 为当天详情数组。区间查询将数量求和，详情按日期倒序；完成率为 `jira_completed / jira_total`，发布成功率为 `release_success / release_total`。

字段以 [projects_upload.py](../examples/projects_upload.py) 为准。完成数不能大于对应总数，所有数量不能为负数。

### 数据库表

- `archery_tickets`：当天新增 Archery 工单。
- `slow_sql_production`：当天生产环境新发现慢 SQL。
- `slow_sql_non_production`：当天非生产环境新发现慢 SQL。

区间查询按日求和，慢 SQL 总数为生产与非生产之和。

### 安全表

`completed_approvals` 只统计当天状态已完成的 Lark 安全审批；处理中和驳回不纳入。

### 资源表

- 区间发生量并求和：`renewal_expense`、`certificate_renewals`、`domain_purchase_expense`、项目费用和四类费用构成。
- 资产快照取范围内最新一日：`expiring_certificates_30d`、`managed_domains`、`annual_budget`。
- `budget_usage` 为 0–100 的百分数，不要传 0–1 小数。

### 月报表

`report_date` 是月报生成/发布日期；`report_month` 是月报归属月（`YYYY-MM`）。查询是否纳入时间范围以 `report_date` 为准。累计工作项为范围内月报 `work_items` 之和，编制进度与步骤取范围内最新一条。

### 首页

首页不接收 POST，避免同一指标重复上报产生冲突。它实时汇总项目、数据库、安全和资源表，沿用各自统计口径。

## 六、常见错误

| HTTP 状态 | 原因 | 处理方法 |
|---|---|---|
| 400 | JSON 拼写错误、多余内容或未知字段 | 对照 Python 示例检查字段名和逗号 |
| 401 | API Key 缺失或错误 | 设置正确的 `OPS_API_KEY` 环境变量 |
| 422 | 日期/时间格式错误、负数或完成数大于总数 | 阅读返回的 `error.message` 并修正数据 |
| 500 | 后端保存或解析失败 | 保存请求 ID 和服务日志交给运维排查 |
| 503 | 数据库不可用 | 检查数据库目录权限和磁盘空间 |

Python 示例已经区分“服务无法连接”和“接口拒绝数据”，并会打印服务器的中文错误信息。

## 七、生产部署

后端已经拆分到 `https://github.com/userreksai/report-service`。Linux 服务器需安装 Git 和 Go 1.25+，在后端仓库执行：

```bash
bash deploy/install-report-service.sh
```

脚本会构建 Go 二进制，SQLite 保存到 `/var/lib/report-service/report-service.db`，接口监听 10010。建议创建 `/etc/report-service.env`：

```bash
sudo sh -c 'printf "%s\n" "OPS_API_KEY=替换为长随机密钥" > /etc/report-service.env'
sudo chmod 600 /etc/report-service.env
sudo systemctl restart report-service
```

日常检查：

```bash
sudo systemctl status report-service
sudo journalctl -u report-service -f
curl http://127.0.0.1:10010/api/v1/health
```

备份时先复制 `/var/lib/report-service/report-service.db` 及同目录的 `-wal`、`-shm` 文件，或停服务后复制主数据库文件。
