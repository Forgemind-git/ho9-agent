"""
Inbox Triage Agent
==================
Reads a batch of email messages, categorises each one, drafts a reply,
saves all drafts to a file, and prints a summary — fully unattended.

Usage:
    python agent.py
"""

import json
import os
import sys
from datetime import datetime

import anthropic
from tools import TOOLS, TOOL_FUNCTIONS

MODEL = "claude-haiku-3-5-20251001"

SYSTEM_PROMPT = """You are an inbox triage specialist. You process a batch of emails and for each:
1. Assign a category: critical_support, billing, technical_support, partnership, newsletter, feature_request
2. Assign a priority: urgent (respond <1hr), high (<4hr), medium (<24hr), low (this week)
3. Draft a professional reply appropriate to the category and tone

After processing ALL emails:
- Call save_drafts with the complete list of all draft dicts returned by draft_reply
- Print a triage summary table

Rules:
- Newsletter / promotional emails: categorise as 'newsletter', priority 'low', draft a polite unsubscribe acknowledgement
- critical_support emails: mark urgent, draft an empathetic acknowledgement with an ETA
- feature_requests: thank the customer warmly, mention it will be considered for the roadmap
- Write all replies in a professional but warm tone
- Process every single email — do not skip any"""


def run_tool(tool_name: str, tool_input: dict) -> str:
    fn = TOOL_FUNCTIONS.get(tool_name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    try:
        result = fn(**tool_input)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def run_agent() -> None:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print(f"\n{'='*60}")
    print(f"Inbox Triage Agent")
    print(f"Model: {MODEL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    messages = [
        {"role": "user", "content": "Process the current inbox batch: categorise each email, draft a reply, then save all drafts and print a summary."}
    ]

    step = 0
    max_steps = 40
    draft_count = 0

    while step < max_steps:
        step += 1
        print(f"[Step {step}] Calling Claude...")

        response = client.messages.create(
            model=MODEL,
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        print(f"         Stop reason: {response.stop_reason}")

        tool_calls = []
        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"\n[Claude]: {block.text[:600]}{'...' if len(block.text) > 600 else ''}\n")
            elif block.type == "tool_use":
                tool_calls.append(block)
                args_preview = json.dumps(block.input)[:160]
                print(f"[Tool call]: {block.name}({args_preview})")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn" or not tool_calls:
            print("\n[Agent] Inbox triage complete.")
            break

        tool_results = []
        for tc in tool_calls:
            print(f"\n[Executing] {tc.name}...")
            result_str = run_tool(tc.name, tc.input)
            result_data = json.loads(result_str)

            if tc.name == "read_emails":
                count = result_data.get("count", 0)
                print(f"  -> {count} emails fetched")
            elif tc.name == "categorise_email":
                eid = tc.input.get("email_id")
                cat = tc.input.get("category")
                pri = tc.input.get("priority")
                print(f"  -> {eid}: [{pri.upper()}] {cat}")
            elif tc.name == "draft_reply":
                eid = tc.input.get("email_id")
                subj = tc.input.get("subject", "")[:50]
                print(f"  -> Draft for {eid}: {subj}")
                draft_count += 1
            elif tc.name == "save_drafts":
                saved = result_data.get("drafts_saved", 0)
                path = result_data.get("path", "")
                print(f"  -> {saved} drafts saved to {path}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result_str,
            })

        messages.append({"role": "user", "content": tool_results})

    if step >= max_steps:
        print(f"\n[Warning] Reached maximum step limit ({max_steps})")

    print(f"\n{'='*60}")
    print(f"Triage completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Drafts saved to: drafts/triage_drafts.json")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)
    run_agent()
