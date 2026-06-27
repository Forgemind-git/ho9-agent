"""
Tool implementations for the Inbox Triage Agent.
Email data is mocked with realistic message samples.
"""

import json
import os
from datetime import datetime

SAMPLE_EMAILS = [
    {
        "id": "msg_001",
        "from": "sarah.johnson@enterprise-corp.com",
        "from_name": "Sarah Johnson",
        "subject": "Urgent: Production outage affecting 500 users",
        "body": (
            "Hi team,\n\n"
            "We are experiencing a critical production outage that has been ongoing for 45 minutes. "
            "Our dashboard is completely inaccessible and approximately 500 enterprise users are affected. "
            "This is causing significant revenue impact — we estimate $15,000/hour in losses.\n\n"
            "Please escalate this immediately. We need a status update within 15 minutes.\n\n"
            "Best,\nSarah Johnson\nVP Engineering, Enterprise Corp"
        ),
        "received_at": "2025-06-27T09:02:00Z",
    },
    {
        "id": "msg_002",
        "from": "newsletter@techdigest.io",
        "from_name": "Tech Digest",
        "subject": "This week in AI: 5 papers you should read",
        "body": (
            "Welcome to this week's Tech Digest!\n\n"
            "Top stories this week:\n"
            "1. OpenAI releases new reasoning model\n"
            "2. Meta open-sources LLaMA 4\n"
            "3. Google announces Gemini 2.0\n\n"
            "Click here to read the full digest: https://techdigest.io/weekly/2025-06-27\n\n"
            "Unsubscribe | Manage preferences"
        ),
        "received_at": "2025-06-27T08:45:00Z",
    },
    {
        "id": "msg_003",
        "from": "alex.thompson@startup-xyz.com",
        "from_name": "Alex Thompson",
        "subject": "Question about API rate limits",
        "body": (
            "Hello,\n\n"
            "I've been using your API for about two months now and overall it's been great. "
            "I have a question: what are the rate limits for the /v2/analytics endpoint? "
            "I'm building a dashboard that polls every 30 seconds for 50 concurrent users "
            "and I'm starting to hit 429 errors.\n\n"
            "Is there a way to increase limits or would I need to move to a higher tier?\n\n"
            "Thanks,\nAlex"
        ),
        "received_at": "2025-06-27T08:30:00Z",
    },
    {
        "id": "msg_004",
        "from": "billing@acme-solutions.com",
        "from_name": "ACME Solutions Billing",
        "subject": "Invoice #INV-2025-0892 — Payment Required",
        "body": (
            "Dear Customer,\n\n"
            "This is a reminder that Invoice #INV-2025-0892 for $4,250.00 is due on 2025-07-01. "
            "Please process payment at your earliest convenience to avoid service interruption.\n\n"
            "Payment options: Credit card, ACH, or bank transfer.\n"
            "Pay online: https://billing.acme-solutions.com/pay/INV-2025-0892\n\n"
            "Questions? Reply to this email or call +1-800-555-0100.\n\n"
            "ACME Solutions Billing Team"
        ),
        "received_at": "2025-06-27T08:15:00Z",
    },
    {
        "id": "msg_005",
        "from": "maya.chen@partner-agency.com",
        "from_name": "Maya Chen",
        "subject": "Partnership proposal — joint webinar Q3",
        "body": (
            "Hi,\n\n"
            "I'm Maya Chen from Partner Agency. We run a newsletter with 45,000 SaaS founders "
            "and would love to co-host a webinar with your team in Q3. We have had great results "
            "with similar partnerships — our last co-hosted webinar drove 800 sign-ups for our partner.\n\n"
            "Would you be open to a 20-minute call this week to explore this?\n\n"
            "Best,\nMaya"
        ),
        "received_at": "2025-06-27T07:55:00Z",
    },
    {
        "id": "msg_006",
        "from": "david.kim@long-term-customer.com",
        "from_name": "David Kim",
        "subject": "Feature request: bulk export to PDF",
        "body": (
            "Hey,\n\n"
            "Love the product — been using it for 3 years. One thing that would make my life much "
            "easier: the ability to bulk-export reports to PDF. Right now I have to export one by one "
            "which takes forever when I have 40+ reports each month.\n\n"
            "Is this on the roadmap? Happy to jump on a call to share my use case if helpful.\n\n"
            "Cheers,\nDavid"
        ),
        "received_at": "2025-06-27T07:30:00Z",
    },
]

CATEGORY_DESCRIPTIONS = {
    "critical_support": "Production issue, outage, data loss, or security incident requiring immediate response",
    "billing": "Invoice, payment, subscription, or pricing question",
    "technical_support": "API question, bug report, or technical how-to",
    "partnership": "Business partnership, co-marketing, or collaboration proposal",
    "newsletter": "Marketing email, newsletter, or unsolicited promotional content",
    "feature_request": "Product feedback or feature suggestion from a customer",
}


def read_emails() -> dict:
    """
    Fetch a batch of emails from the inbox.

    Returns:
        dict with 'emails' list and 'count'
    """
    return {
        "emails": SAMPLE_EMAILS,
        "count": len(SAMPLE_EMAILS),
        "fetched_at": datetime.now().isoformat(),
    }


def categorise_email(email_id: str, category: str, priority: str, reason: str) -> dict:
    """
    Categorise a single email and record the triage decision.

    Args:
        email_id: The message ID to categorise
        category: One of: critical_support, billing, technical_support, partnership, newsletter, feature_request
        priority: One of: urgent, high, medium, low
        reason: Brief explanation for this categorisation

    Returns:
        dict confirming the categorisation
    """
    valid_categories = list(CATEGORY_DESCRIPTIONS.keys())
    valid_priorities = ["urgent", "high", "medium", "low"]

    if category not in valid_categories:
        return {"success": False, "error": f"Invalid category. Must be one of: {valid_categories}"}
    if priority not in valid_priorities:
        return {"success": False, "error": f"Invalid priority. Must be one of: {valid_priorities}"}

    return {
        "success": True,
        "email_id": email_id,
        "category": category,
        "priority": priority,
        "reason": reason,
        "categorised_at": datetime.now().isoformat(),
    }


def draft_reply(email_id: str, subject: str, body: str) -> dict:
    """
    Draft a reply to an email.

    Args:
        email_id: The message ID to reply to
        subject: Subject line for the reply
        body: Full body of the draft reply

    Returns:
        dict with draft details
    """
    original = next((e for e in SAMPLE_EMAILS if e["id"] == email_id), None)
    if not original:
        return {"success": False, "error": f"Email {email_id} not found"}

    return {
        "success": True,
        "draft_id": f"draft_{email_id}",
        "email_id": email_id,
        "to": original["from"],
        "subject": subject,
        "body": body,
        "created_at": datetime.now().isoformat(),
    }


def save_drafts(drafts: list) -> dict:
    """
    Save all drafted replies to a JSON file.

    Args:
        drafts: List of draft dicts

    Returns:
        dict with path and count
    """
    os.makedirs("drafts", exist_ok=True)
    path = "drafts/triage_drafts.json"

    output = {
        "generated_at": datetime.now().isoformat(),
        "count": len(drafts),
        "drafts": drafts,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return {
        "success": True,
        "path": path,
        "drafts_saved": len(drafts),
        "bytes": os.path.getsize(path),
    }


TOOLS = [
    {
        "name": "read_emails",
        "description": "Fetch the current batch of inbox emails. Call this first to get the messages to process.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "categorise_email",
        "description": (
            "Categorise a single email with a category and priority. "
            "Categories: critical_support, billing, technical_support, partnership, newsletter, feature_request. "
            "Priorities: urgent, high, medium, low."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "email_id": {"type": "string", "description": "The message ID to categorise"},
                "category": {"type": "string", "description": "Category for this email"},
                "priority": {"type": "string", "description": "Priority: urgent, high, medium, low"},
                "reason": {"type": "string", "description": "Brief explanation for this decision"},
            },
            "required": ["email_id", "category", "priority", "reason"],
        },
    },
    {
        "name": "draft_reply",
        "description": "Draft a reply to an email. Write a complete, professional reply ready to send.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email_id": {"type": "string", "description": "The message ID to reply to"},
                "subject": {"type": "string", "description": "Reply subject line"},
                "body": {"type": "string", "description": "Full body of the reply"},
            },
            "required": ["email_id", "subject", "body"],
        },
    },
    {
        "name": "save_drafts",
        "description": "Save all drafted replies to a file. Call once at the end with the complete list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "drafts": {
                    "type": "array",
                    "description": "List of draft dicts from draft_reply calls",
                    "items": {"type": "object"},
                }
            },
            "required": ["drafts"],
        },
    },
]

TOOL_FUNCTIONS = {
    "read_emails": read_emails,
    "categorise_email": categorise_email,
    "draft_reply": draft_reply,
    "save_drafts": save_drafts,
}
