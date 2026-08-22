"""首页汇总接口完整示例（只查询，不写入）。

使用方法：
1. 安装依赖：python -m pip install -r requirements.txt
2. 确认后端已启动。
3. 直接运行：python dashboard_query.py
"""

import os
import sys
from datetime import date, timedelta

import requests


API_BASE_URL = os.getenv("OPS_API_BASE_URL", "http://127.0.0.1:10010/api/v1")


def query_dashboard(start_date: str, end_date: str) -> dict:
    """查询指定自然日范围内的首页聚合数据，开始日和结束日都包含。"""
    response = requests.get(
        f"{API_BASE_URL}/dashboard",
        params={"start_date": start_date, "end_date": end_date},
        timeout=(5, 30),
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    end = date.today()
    start = end - timedelta(days=29)  # 含今天共 30 个自然日
    result = query_dashboard(start.isoformat(), end.isoformat())

    data = result["data"]
    meta = result["meta"]
    print(f"统计范围：{meta['start_date']} 至 {meta['end_date']}")
    print(f"数据来源：{', '.join(meta['sources']) or '暂无'}")
    print(f"后台更新时间：{meta.get('updated_at') or '暂无'}")
    print(f"项目工作项：{data['projects']['jira_total']}")
    print(f"Archery 工单：{data['database']['archery_tickets']}")
    print(f"已完成安全审批：{data['security']['completed_approvals']}")
    print(f"资源总支出：{data['resources']['total_expense']:.2f}")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"接口返回错误：HTTP {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as exc:
        print(f"无法连接后端服务：{exc}", file=sys.stderr)
        raise SystemExit(2)
