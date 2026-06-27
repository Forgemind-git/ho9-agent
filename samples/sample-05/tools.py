"""
Tool implementations for the Recurring Report Generator.
fetch_data returns mock SaaS product metrics.
build_report and save_report handle formatting and persistence.
"""

import json
import os
import random
from datetime import datetime, timedelta

MOCK_METRICS = {
    "daily": {
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "new_signups": 47,
        "active_users": 1284,
        "churned_users": 3,
        "revenue_usd": 8920.50,
        "api_calls": 284_500,
        "error_rate_pct": 0.12,
        "p95_latency_ms": 143,
        "support_tickets_opened": 12,
        "support_tickets_closed": 15,
        "top_features_used": [
            {"feature": "Dashboard", "sessions": 6420},
            {"feature": "API Explorer", "sessions": 3210},
            {"feature": "Reports", "sessions": 2890},
            {"feature": "Webhooks", "sessions": 1540},
        ],
        "new_signups_by_plan": {
            "starter": 31,
            "pro": 13,
            "enterprise": 3,
        },
        "previous_day": {
            "new_signups": 39,
            "active_users": 1251,
            "revenue_usd": 7650.00,
            "api_calls": 271_000,
        },
    },
    "weekly": {
        "week": "2025-W26",
        "new_signups": 312,
        "active_users_avg": 1190,
        "churned_users": 18,
        "revenue_usd": 61_450.00,
        "api_calls": 1_987_600,
        "error_rate_pct": 0.15,
        "new_mrr_usd": 4_890,
        "churned_mrr_usd": 720,
        "net_new_mrr_usd": 4_170,
    },
}


def fetch_data(report_type: str = "daily", date: str = None) -> dict:
    """
    Fetch product metrics for a given report type and date.

    Args:
        report_type: 'daily' or 'weekly'
        date: ISO date string (YYYY-MM-DD). Defaults to yesterday for daily.

    Returns:
        dict with metrics data
    """
    if report_type not in MOCK_METRICS:
        return {"error": f"Unknown report_type '{report_type}'. Must be 'daily' or 'weekly'."}

    data = dict(MOCK_METRICS[report_type])
    data["fetched_at"] = datetime.now().isoformat()
    data["report_type"] = report_type

    # Slightly randomise values to simulate real data variability
    data["new_signups"] = data.get("new_signups", 0) + random.randint(-3, 3)
    data["active_users"] = data.get("active_users", 0) + random.randint(-20, 20)

    return data


def compute_kpis(data: dict) -> dict:
    """
    Compute derived KPIs from raw metric data.

    Args:
        data: Raw metrics dict from fetch_data

    Returns:
        dict with computed KPI values
    """
    kpis = {}

    if "new_signups" in data and "active_users" in data:
        kpis["signup_to_active_rate_pct"] = round(
            (data["new_signups"] / data["active_users"]) * 100, 2
        )

    if "churned_users" in data and "active_users" in data:
        kpis["daily_churn_rate_pct"] = round(
            (data["churned_users"] / data["active_users"]) * 100, 3
        )

    if "previous_day" in data:
        prev = data["previous_day"]
        if "new_signups" in prev and prev["new_signups"] > 0:
            kpis["signup_change_pct"] = round(
                ((data["new_signups"] - prev["new_signups"]) / prev["new_signups"]) * 100, 1
            )
        if "revenue_usd" in prev and prev["revenue_usd"] > 0:
            kpis["revenue_change_pct"] = round(
                ((data["revenue_usd"] - prev["revenue_usd"]) / prev["revenue_usd"]) * 100, 1
            )
        if "api_calls" in prev and prev["api_calls"] > 0:
            kpis["api_calls_change_pct"] = round(
                ((data["api_calls"] - prev["api_calls"]) / prev["api_calls"]) * 100, 1
            )

    if "revenue_usd" in data and "new_signups" in data and data["new_signups"] > 0:
        kpis["arpu_usd"] = round(data["revenue_usd"] / data["active_users"], 2)

    return kpis


def build_report(data: dict, kpis: dict, report_type: str) -> dict:
    """
    Build a structured markdown report from metrics and KPIs.

    Args:
        data: Raw metrics dict
        kpis: Computed KPIs dict
        report_type: 'daily' or 'weekly'

    Returns:
        dict with 'markdown' content and 'title'
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M UTC")

    def pct_arrow(val):
        if val is None:
            return ""
        arrow = "+" if val >= 0 else ""
        return f" ({arrow}{val}%)"

    if report_type == "daily":
        period = data.get("date", date_str)
        signup_change = pct_arrow(kpis.get("signup_change_pct"))
        rev_change = pct_arrow(kpis.get("revenue_change_pct"))
        api_change = pct_arrow(kpis.get("api_calls_change_pct"))

        feature_rows = ""
        for f in data.get("top_features_used", []):
            feature_rows += f"| {f['feature']} | {f['sessions']:,} |\n"

        plan_rows = ""
        for plan, count in data.get("new_signups_by_plan", {}).items():
            plan_rows += f"| {plan.capitalize()} | {count} |\n"

        markdown = f"""# Daily Product Report — {period}
Generated: {date_str} at {time_str}

---

## Executive Summary

Yesterday's metrics show **{data.get('new_signups', 0)} new sign-ups**{signup_change} and
**${data.get('revenue_usd', 0):,.2f} in revenue**{rev_change}.
The platform processed **{data.get('api_calls', 0):,} API calls**{api_change} with an
error rate of **{data.get('error_rate_pct', 0)}%** — within healthy thresholds.

---

## Key Metrics

| Metric | Value | vs Yesterday |
|--------|-------|-------------|
| New Sign-ups | {data.get('new_signups', 0)} | {signup_change.strip()} |
| Active Users | {data.get('active_users', 0):,} | — |
| Churned Users | {data.get('churned_users', 0)} | — |
| Revenue (USD) | ${data.get('revenue_usd', 0):,.2f} | {rev_change.strip()} |
| API Calls | {data.get('api_calls', 0):,} | {api_change.strip()} |
| Error Rate | {data.get('error_rate_pct', 0)}% | — |
| p95 Latency | {data.get('p95_latency_ms', 0)}ms | — |

---

## Derived KPIs

| KPI | Value |
|-----|-------|
| Signup-to-Active Rate | {kpis.get('signup_to_active_rate_pct', 'N/A')}% |
| Daily Churn Rate | {kpis.get('daily_churn_rate_pct', 'N/A')}% |
| ARPU | ${kpis.get('arpu_usd', 'N/A')} |

---

## Support

| Metric | Count |
|--------|-------|
| Tickets Opened | {data.get('support_tickets_opened', 0)} |
| Tickets Closed | {data.get('support_tickets_closed', 0)} |

---

## Top Features (by sessions)

| Feature | Sessions |
|---------|---------|
{feature_rows}
---

## New Sign-ups by Plan

| Plan | Sign-ups |
|------|---------|
{plan_rows}
---

*Report auto-generated by the Recurring Report Generator agent.*
"""
    else:
        markdown = f"""# Weekly Product Report — {data.get('week', 'W??')}
Generated: {date_str} at {time_str}

---

## Executive Summary

This week saw **{data.get('new_signups', 0)} new sign-ups** and
**${data.get('revenue_usd', 0):,.2f} in revenue**.
Net new MRR was **${data.get('net_new_mrr_usd', 0):,}** (new ${data.get('new_mrr_usd', 0):,} - churned ${data.get('churned_mrr_usd', 0):,}).

---

## Weekly KPIs

| Metric | Value |
|--------|-------|
| New Sign-ups | {data.get('new_signups', 0)} |
| Avg Daily Active Users | {data.get('active_users_avg', 0):,} |
| Churned Users | {data.get('churned_users', 0)} |
| Revenue (USD) | ${data.get('revenue_usd', 0):,.2f} |
| API Calls | {data.get('api_calls', 0):,} |
| Error Rate | {data.get('error_rate_pct', 0)}% |
| New MRR | ${data.get('new_mrr_usd', 0):,} |
| Churned MRR | ${data.get('churned_mrr_usd', 0):,} |
| Net New MRR | ${data.get('net_new_mrr_usd', 0):,} |

---

*Report auto-generated by the Recurring Report Generator agent.*
"""

    title = f"{report_type.capitalize()} Report — {data.get('date', data.get('week', date_str))}"
    return {"markdown": markdown, "title": title, "word_count": len(markdown.split())}


def save_report(filename: str, content: str) -> dict:
    """
    Save the finished report to the reports/ directory.

    Args:
        filename: Filename for the report (e.g. 'daily-2025-06-27.md')
        content: Markdown content of the report

    Returns:
        dict with path, size, and success flag
    """
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {
            "success": True,
            "path": path,
            "bytes_written": len(content.encode("utf-8")),
            "saved_at": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"success": False, "path": path, "error": str(e)}


TOOLS = [
    {
        "name": "fetch_data",
        "description": "Fetch product metrics for a report period. Use report_type='daily' or 'weekly'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "report_type": {
                    "type": "string",
                    "description": "Type of report: 'daily' or 'weekly'",
                    "enum": ["daily", "weekly"],
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format (optional, defaults to yesterday)",
                },
            },
            "required": ["report_type"],
        },
    },
    {
        "name": "compute_kpis",
        "description": "Compute derived KPIs (churn rate, ARPU, growth %) from raw metrics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "description": "Raw metrics dict returned by fetch_data",
                }
            },
            "required": ["data"],
        },
    },
    {
        "name": "build_report",
        "description": "Build a formatted markdown report from metrics and KPIs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {"type": "object", "description": "Raw metrics dict from fetch_data"},
                "kpis": {"type": "object", "description": "Computed KPIs from compute_kpis"},
                "report_type": {"type": "string", "description": "'daily' or 'weekly'"},
            },
            "required": ["data", "kpis", "report_type"],
        },
    },
    {
        "name": "save_report",
        "description": "Save the finished report markdown to the reports/ folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Filename (e.g. 'daily-2025-06-27.md')",
                },
                "content": {
                    "type": "string",
                    "description": "Full markdown content of the report",
                },
            },
            "required": ["filename", "content"],
        },
    },
]

TOOL_FUNCTIONS = {
    "fetch_data": fetch_data,
    "compute_kpis": compute_kpis,
    "build_report": build_report,
    "save_report": save_report,
}
