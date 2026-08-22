"""安全审批接口完整示例：上传当天已完成的 Lark 安全审批数量。"""

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
        "source": "Lark 审批",
        "source_updated_at": now.isoformat(timespec="seconds"),
        "data": {
            # 只填当天状态已完成的审批数量；处理中、驳回不计入。
            "completed_approvals": 8,
        },
    }
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    response = requests.post(
        f"{API_BASE_URL}/security", json=payload, headers=headers, timeout=(5, 30)
    )
    response.raise_for_status()
    write_result = response.json()
    print(f"写入结果：{write_result['data']['action']} - {write_result['message']}")

    response = requests.get(
        f"{API_BASE_URL}/security",
        params={"start_date": report_date, "end_date": report_date},
        timeout=(5, 30),
    )
    response.raise_for_status()
    result = response.json()
    print(f"当天已完成审批：{result['data']['completed_approvals']} 项")
    print(f"统计口径：{result['meta']['methodology']}")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"接口返回错误：HTTP {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as exc:
        print(f"无法连接后端服务：{exc}", file=sys.stderr)
        raise SystemExit(2)
