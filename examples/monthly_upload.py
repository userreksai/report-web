"""杂项·月报接口完整示例：上传一份月报及当前编制进度。"""

import os
import sys
from datetime import datetime

import requests


API_BASE_URL = os.getenv("OPS_API_BASE_URL", "http://127.0.0.1:10010/api/v1")
API_KEY = os.getenv("OPS_API_KEY", "")


def main() -> None:
    now = datetime.now().astimezone()
    report_date = now.date().isoformat()  # 月报生成/发布日期，也是幂等键
    payload = {
        "report_date": report_date,
        "source": "运维月报编制平台",
        "source_updated_at": now.isoformat(timespec="seconds"),
        "data": {
            "report_month": now.strftime("%Y-%m"),
            "status": "进行中",
            "work_items": 486,
            "summary": "核心系统稳定运行，完成海外 CDN 扩容和年度证书集中续期。",
            "compilation_progress": 74,
            "compilation_steps": [
                {"name": "项目数据汇总", "completed": True},
                {"name": "数据库质量统计", "completed": True},
                {"name": "安全审批统计", "completed": True},
                {"name": "资源费用核对", "completed": False},
                {"name": "管理摘要确认", "completed": False},
            ],
        },
    }
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    response = requests.post(
        f"{API_BASE_URL}/monthly", json=payload, headers=headers, timeout=(5, 30)
    )
    response.raise_for_status()
    result = response.json()
    print(f"写入结果：{result['data']['action']} - {result['message']}")

    response = requests.get(
        f"{API_BASE_URL}/monthly",
        params={"start_date": report_date, "end_date": report_date, "view": "all"},
        timeout=(5, 30),
    )
    response.raise_for_status()
    query_result = response.json()
    print(f"月报数量：{query_result['data']['summary']['report_count']}")
    print(f"当前编制进度：{query_result['data']['latest_compilation']['progress']}%")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"接口返回错误：HTTP {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as exc:
        print(f"无法连接后端服务：{exc}", file=sys.stderr)
        raise SystemExit(2)
