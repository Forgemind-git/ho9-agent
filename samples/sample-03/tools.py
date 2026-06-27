"""
Tool implementations for the Page Change Monitor Agent.
fetch_page is mocked with realistic page snapshots.
compare_content performs a real line-level diff.
"""

import difflib
import json
import os
from datetime import datetime

# Simulated page snapshots — first call returns "before", second call returns "after"
MOCK_PAGES = {
    "https://status.example-saas.com": {
        "v1": """System Status — example-saas.com
Last updated: 2025-06-26 08:00 UTC

All Systems Operational

Services:
- API: Operational
- Dashboard: Operational
- Webhooks: Operational
- Database: Operational

Recent incidents: None in the last 30 days.""",
        "v2": """System Status — example-saas.com
Last updated: 2025-06-27 09:15 UTC

Partial Outage

Services:
- API: Operational
- Dashboard: Operational
- Webhooks: DEGRADED — elevated error rates since 09:00 UTC
- Database: Operational

Recent incidents:
[OPEN] 2025-06-27 09:00 UTC — Webhook delivery delays affecting some customers.""",
    },
    "https://changelog.example-tool.io": {
        "v1": """Changelog — example-tool.io

## v2.3.1 — 2025-06-20
- Fixed timezone handling in scheduled reports
- Improved CSV export performance

## v2.3.0 — 2025-06-14
- Added multi-workspace support
- New keyboard shortcuts panel""",
        "v2": """Changelog — example-tool.io

## v2.4.0 — 2025-06-27
- BREAKING: Removed deprecated /v1/export endpoint (use /v2/export)
- Added AI-powered search across all content
- New Slack integration with /commands support
- Performance: 40% faster page loads

## v2.3.1 — 2025-06-20
- Fixed timezone handling in scheduled reports
- Improved CSV export performance""",
    },
    "https://pricing.example-platform.com": {
        "v1": """Pricing — example-platform.com

Starter: $29/month — up to 5 users, 10GB storage
Pro: $99/month — up to 25 users, 100GB storage
Enterprise: Contact sales""",
        "v2": """Pricing — example-platform.com

Starter: $29/month — up to 5 users, 10GB storage
Pro: $129/month — up to 25 users, 100GB storage  [PRICE INCREASED]
Enterprise: Contact sales

* Annual billing saves 20%""",
    },
}

# Tracks how many times each URL has been fetched (to alternate between v1/v2)
_fetch_counts: dict = {}

# Snapshot storage directory
SNAPSHOT_DIR = "snapshots"


def fetch_page(url: str) -> dict:
    """
    Fetch the current text content of a web page.
    Alternates between v1 and v2 content to simulate a real change.

    Args:
        url: The URL to fetch

    Returns:
        dict with 'url', 'content', and 'fetched_at'
    """
    _fetch_counts[url] = _fetch_counts.get(url, 0) + 1
    page_data = MOCK_PAGES.get(url)
    if page_data:
        # First fetch returns v2 (the "current" page, which may differ from stored snapshot)
        content = page_data["v2"]
    else:
        content = f"Content of {url}\nLast updated: {datetime.now().strftime('%Y-%m-%d')}\nNo changes detected."

    return {
        "url": url,
        "content": content.strip(),
        "fetched_at": datetime.now().isoformat(),
        "word_count": len(content.split()),
    }


def load_snapshot(url: str) -> dict:
    """
    Load the previously saved snapshot for a URL.

    Args:
        url: The URL whose snapshot to load

    Returns:
        dict with 'found', 'content', and 'saved_at' (or 'found': False if no snapshot)
    """
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    filename = url.replace("://", "_").replace("/", "_").replace(".", "_") + ".txt"
    path = os.path.join(SNAPSHOT_DIR, filename)

    if not os.path.exists(path):
        # Return simulated "old" version to make the demo show changes
        page_data = MOCK_PAGES.get(url)
        if page_data:
            return {
                "found": True,
                "content": page_data["v1"].strip(),
                "saved_at": "2025-06-26T08:00:00",
                "source": "simulated_previous",
            }
        return {"found": False, "content": None, "saved_at": None}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"found": True, "content": data["content"], "saved_at": data["saved_at"]}


def compare_content(old_content: str, new_content: str) -> dict:
    """
    Compare two strings and return a unified diff summary.

    Args:
        old_content: The previous page content
        new_content: The current page content

    Returns:
        dict with 'changed' bool, 'diff' string, 'lines_added', 'lines_removed'
    """
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff_lines = list(difflib.unified_diff(
        old_lines, new_lines,
        fromfile="previous", tofile="current",
        lineterm=""
    ))

    added = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))

    return {
        "changed": len(diff_lines) > 0,
        "lines_added": added,
        "lines_removed": removed,
        "diff": "".join(diff_lines)[:2000],  # cap at 2000 chars
    }


def send_alert(url: str, summary: str) -> dict:
    """
    Send a change alert. In this implementation, prints to console and logs to a file.

    Args:
        url: The URL where changes were detected
        summary: Human-readable description of what changed

    Returns:
        dict with 'sent' bool and 'timestamp'
    """
    timestamp = datetime.now().isoformat()
    alert_msg = f"\n{'!'*50}\nCHANGE ALERT [{timestamp}]\nURL: {url}\n{summary}\n{'!'*50}\n"
    print(alert_msg)

    os.makedirs("alerts", exist_ok=True)
    with open("alerts/alert_log.txt", "a", encoding="utf-8") as f:
        f.write(alert_msg + "\n")

    return {"sent": True, "timestamp": timestamp, "url": url}


def save_snapshot(url: str, content: str) -> dict:
    """
    Save the current page content as the new snapshot for future comparisons.

    Args:
        url: The URL being monitored
        content: The current page content to save

    Returns:
        dict with 'path' and 'saved_at'
    """
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    filename = url.replace("://", "_").replace("/", "_").replace(".", "_") + ".txt"
    path = os.path.join(SNAPSHOT_DIR, filename)
    saved_at = datetime.now().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"url": url, "content": content, "saved_at": saved_at}, f, indent=2)

    return {"path": path, "saved_at": saved_at, "bytes": len(content.encode())}


MONITORED_URLS = [
    "https://status.example-saas.com",
    "https://changelog.example-tool.io",
    "https://pricing.example-platform.com",
]


def get_url_list() -> dict:
    """Return the list of URLs to monitor."""
    return {"urls": MONITORED_URLS, "count": len(MONITORED_URLS)}


TOOLS = [
    {
        "name": "get_url_list",
        "description": "Get the list of URLs to monitor for changes. Call this first.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "load_snapshot",
        "description": "Load the previously saved snapshot content for a URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to load the snapshot for"}
            },
            "required": ["url"],
        },
    },
    {
        "name": "fetch_page",
        "description": "Fetch the current content of a web page.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch"}
            },
            "required": ["url"],
        },
    },
    {
        "name": "compare_content",
        "description": "Compare old and new page content to detect what changed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "old_content": {"type": "string", "description": "Previous page content"},
                "new_content": {"type": "string", "description": "Current page content"},
            },
            "required": ["old_content", "new_content"],
        },
    },
    {
        "name": "send_alert",
        "description": "Send an alert describing what changed on a page.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL where changes were detected"},
                "summary": {"type": "string", "description": "Clear description of what changed"},
            },
            "required": ["url", "summary"],
        },
    },
    {
        "name": "save_snapshot",
        "description": "Save the current page content as the new snapshot for future runs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL being monitored"},
                "content": {"type": "string", "description": "Current page content to save"},
            },
            "required": ["url", "content"],
        },
    },
]

TOOL_FUNCTIONS = {
    "get_url_list": get_url_list,
    "load_snapshot": load_snapshot,
    "fetch_page": fetch_page,
    "compare_content": compare_content,
    "send_alert": send_alert,
    "save_snapshot": save_snapshot,
}
