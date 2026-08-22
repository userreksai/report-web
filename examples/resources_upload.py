"""资源管理接口完整示例：上传费用增量、资产快照和项目费用明细。"""

import os
import sys
from datetime import datetime

import requests


API_BASE_URL = os.getenv("OPS_API_BASE_URL", "http://127.0.0.1:10010/api/v1")
API_KEY = os.getenv("OPS_API_KEY", "")


def main() -> None:
    now = datetime.now().astimezone()
    report_date = now.date().isoformat()
    payload = {
        "report_date": report_date,
        "source": "费用中心 + CMDB",
        "source_updated_at": now.isoformat(timespec="seconds"),
        "data": {
            # 费用和续期数为当天发生量；存量/预算字段填写当天最新快照。
            "renewal_expense": 45200.00,
            "certificate_renewals": 3,
            "expiring_certificates_30d": 2,
            "domain_purchase_expense": 8450.00,
            "managed_domains": 42,
            "annual_budget": 2800000.00,
            "project_expenses": [
                {
                    "name": "核心数据库迁移",
                    "team": "基础设施部",
                    "category": "云资源",
                    "budget_usage": 92.0,
                    "cost": 342000.00,
                },
                {
                    "name": "年度安全审计",
                    "team": "安全合规部",
                    "category": "安全服务",
                    "budget_usage": 15.0,
                    "cost": 45000.00,
                },
            ],
            # 费用构成填写当天发生额，四项相加为当天纳入构成的总支出。
            "expense_breakdown": {
                "cloud_resource": 342000.00,
                "project_investment": 0.00,
                "security_service": 45000.00,
                "other": 0.00,
            },
        },
    }
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    response = requests.post(
        f"{API_BASE_URL}/resources", json=payload, headers=headers, timeout=(5, 30)
    )
    response.raise_for_status()
    result = response.json()
    print(f"写入结果：{result['data']['action']} - {result['message']}")

    response = requests.get(
        f"{API_BASE_URL}/resources",
        params={"start_date": report_date, "end_date": report_date, "view": "all"},
        timeout=(5, 30),
    )
    response.raise_for_status()
    query_result = response.json()
    print(f"总支出（人民币）：{query_result['data']['summary']['total_expense']:.2f} 元")
    print(f"费用明细：{query_result['data']['project_expense_total']} 条")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"接口返回错误：HTTP {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as exc:
        print(f"无法连接后端服务：{exc}", file=sys.stderr)
        raise SystemExit(2)
