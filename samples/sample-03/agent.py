"""
Page Change Monitor Agent
=========================
Checks a set of URLs for content changes and reports what changed.
Compares current content against saved snapshots, fires alerts for changes,
and saves new snapshots for the next run.

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

SYSTEM_PROMPT = """You are a website change monitoring agent. Your job:
1. Get the list of URLs to monitor using get_url_list
2. For each URL:
   a. Load the previous snapshot with load_snapshot
   b. Fetch the current page content with fetch_page
   c. Compare old vs new content with compare_content
   d. If changed: call send_alert with a clear human-readable summary of what changed
   e. Always save the new snapshot with save_snapshot (whether or not it changed)
3. After processing all URLs, print a final report: how many pages changed, how many stayed the same

Be thorough. Process every URL. Write clear, specific alert summaries that explain exactly what changed and why it matters."""


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
    print(f"Page Change Monitor Agent")
    print(f"Model: {MODEL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    messages = [
        {"role": "user", "content": "Run the page change check now and report all changes."}
    ]

    step = 0
    max_steps = 40

    while step < max_steps:
        step += 1
        print(f"[Step {step}] Calling Claude...")

        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        print(f"         Stop reason: {response.stop_reason}")

        tool_calls = []
        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"\n[Claude]: {block.text[:500]}{'...' if len(block.text) > 500 else ''}\n")
            elif block.type == "tool_use":
                tool_calls.append(block)
                args_preview = json.dumps(block.input)[:120]
                print(f"[Tool call]: {block.name}({args_preview})")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn" or not tool_calls:
            print("\n[Agent] Monitoring run complete.")
            break

        tool_results = []
        for tc in tool_calls:
            print(f"\n[Executing] {tc.name}...")
            result_str = run_tool(tc.name, tc.input)
            result_data = json.loads(result_str)

            if tc.name == "get_url_list":
                count = result_data.get("count", 0)
                print(f"  -> {count} URLs to monitor")
            elif tc.name == "load_snapshot":
                found = result_data.get("found", False)
                print(f"  -> Snapshot {'found' if found else 'not found (first run)'}")
            elif tc.name == "fetch_page":
                wc = result_data.get("word_count", 0)
                print(f"  -> Fetched {wc} words from {tc.input.get('url', '')[:50]}")
            elif tc.name == "compare_content":
                changed = result_data.get("changed", False)
                added = result_data.get("lines_added", 0)
                removed = result_data.get("lines_removed", 0)
                status = f"CHANGED (+{added}/-{removed} lines)" if changed else "no change"
                print(f"  -> {status}")
            elif tc.name == "send_alert":
                print(f"  -> Alert sent for {tc.input.get('url', '')[:50]}")
            elif tc.name == "save_snapshot":
                print(f"  -> Snapshot saved to {result_data.get('path', '')}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result_str,
            })

        messages.append({"role": "user", "content": tool_results})

    if step >= max_steps:
        print(f"\n[Warning] Reached maximum step limit ({max_steps})")

    print(f"\n{'='*60}")
    print(f"Run completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Alerts saved to: alerts/alert_log.txt")
    print(f"Snapshots saved to: snapshots/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)
    run_agent()
