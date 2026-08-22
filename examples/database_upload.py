"""数据库管理接口完整示例：上传当天 Archery 与慢 SQL 数量。"""

import os
import sys
from datetime import datetime

import requests


API_BASE_URL = os.getenv("OPS_API_BASE_URL", "http://127.0.0.1:10010/api/v1")
API_KEY = os.getenv("OPS_API_KEY", "")


def auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}


def main() -> None:
    now = datetime.now().astimezone()
    report_date = now.date().isoformat()
    payload = {
        "report_date": report_date,
        "source": "Archery + 慢 SQL 平台",
        "source_updated_at": now.isoformat(timespec="seconds"),
        "data": {
            # 均填写 report_date 当天新增或发现的数量。
            "archery_tickets": 6,
            "slow_sql_production": 24,
            "slow_sql_non_production": 11,
        },
    }
    write_response = requests.post(
        f"{API_BASE_URL}/database",
        json=payload,
        headers=auth_headers(),
        timeout=(5, 30),
    )
    write_response.raise_for_status()
    write_result = write_response.json()
    print(f"写入结果：{write_result['data']['action']} - {write_result['message']}")

    query_response = requests.get(
        f"{API_BASE_URL}/database",
        params={"start_date": report_date, "end_date": report_date},
        timeout=(5, 30),
    )
    query_response.raise_for_status()
    result = query_response.json()
    print(f"Archery 工单：{result['data']['archery_tickets']}")
    print(f"慢 SQL 总数：{result['data']['slow_sql_total']}")
    print(f"数据来源：{', '.join(result['meta']['sources'])}")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"接口返回错误：HTTP {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as exc:
        print(f"无法连接后端服务：{exc}", file=sys.stderr)
        raise SystemExit(2)
