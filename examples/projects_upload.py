"""项目概览接口完整示例：按 report_date 新增或更新，再查询验证。"""

import os
import sys
from datetime import datetime

import requests


API_BASE_URL = os.getenv("OPS_API_BASE_URL", "http://127.0.0.1:10010/api/v1")
API_KEY = os.getenv("OPS_API_KEY", "")


def headers() -> dict[str, str]:
    result = {"Content-Type": "application/json"}
    if API_KEY:
        result["Authorization"] = f"Bearer {API_KEY}"
    return result


def upload_project_data() -> dict:
    # report_date 是唯一业务键。同一天重复运行会更新，不会新增重复行。
    report_date = datetime.now().astimezone().date().isoformat()
    payload = {
        "report_date": report_date,
        "source": "Jira + Prometheus + 发布平台",
        "source_updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "data": {
            # 以下数量必须是 report_date 当天发生的增量，不是历史累计快照。
            "jira_total": 18,
            "jira_completed": 13,
            "alert_total": 4,
            "alerts_processing": 1,
            "release_total": 5,
            "release_success": 5,
            "change_total": 7,
            "high_risk_changes": 1,
            "prod_deployments": 2,
            "prod_success": 2,
            "prod_rollback": 0,
            "staging_deployments": 4,
            "test_deployments": 9,
            "test_verifying": 2,
            "incidents": [
                {
                    "id": "RCA-4091",
                    "title": "生产数据库集群同步延迟",
                    "owner": "数据库平台组",
                    "status": "分析中",
                    "duration_minutes": 65,
                    "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                }
            ],
            "tasks": [
                {
                    "title": "更新 Q3 安全证书",
                    "owner": "李敏",
                    "count": 4,
                    "due_date": report_date,
                    "status": "进行中",
                }
            ],
        },
    }
    response = requests.post(
        f"{API_BASE_URL}/projects", json=payload, headers=headers(), timeout=(5, 30)
    )
    response.raise_for_status()
    return response.json()


def query_project_data(report_date: str) -> dict:
    response = requests.get(
        f"{API_BASE_URL}/projects",
        params={"start_date": report_date, "end_date": report_date, "view": "all"},
        timeout=(5, 30),
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    write_result = upload_project_data()
    report_date = write_result["data"]["report_date"]
    print(f"写入结果：{write_result['data']['action']} - {write_result['message']}")
    query_result = query_project_data(report_date)
    print(f"查询验证：Jira 工作项 {query_result['data']['summary']['jira_total']} 项")
    print(f"统计口径：{query_result['meta']['methodology']}")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"接口返回错误：HTTP {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as exc:
        print(f"无法连接后端服务：{exc}", file=sys.stderr)
        raise SystemExit(2)
