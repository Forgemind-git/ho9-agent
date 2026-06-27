"""
Recurring Report Generator
==========================
Pulls metrics from a data source, computes KPIs, builds a structured
markdown report, and saves it to the reports/ folder — fully unattended.
Designed to be run on a schedule (cron, etc.).

Usage:
    python agent.py             # generates daily report
    python agent.py weekly      # generates weekly report
"""

import json
import os
import sys
from datetime import datetime

import anthropic
from tools import TOOLS, TOOL_FUNCTIONS

MODEL = "claude-haiku-3-5-20251001"

SYSTEM_PROMPT = """You are a recurring report generator agent. When triggered, you:
1. Fetch the latest metrics using fetch_data for the requested report_type
2. Compute derived KPIs using compute_kpis
3. Build a formatted markdown report using build_report
4. Save the report to a file using save_report
   - Name daily reports: daily-YYYY-MM-DD.md (use today's date)
   - Name weekly reports: weekly-YYYY-WNN.md (use the week identifier from the data)
5. Print a brief confirmation with the key headline numbers

Be precise with numbers. Include all data from fetch_data in the report.
Do the job end-to-end without asking for clarification."""


def run_tool(tool_name: str, tool_input: dict) -> str:
    fn = TOOL_FUNCTIONS.get(tool_name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    try:
        result = fn(**tool_input)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def run_agent(report_type: str = "daily") -> None:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print(f"\n{'='*60}")
    print(f"Recurring Report Generator")
    print(f"Report type: {report_type}")
    print(f"Model: {MODEL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    messages = [
        {
            "role": "user",
            "content": f"Generate the {report_type} report now. Fetch data, compute KPIs, build the report, and save it.",
        }
    ]

    step = 0
    max_steps = 20

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
                args_preview = json.dumps(block.input)[:120]
                print(f"[Tool call]: {block.name}({args_preview})")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn" or not tool_calls:
            print("\n[Agent] Report generation complete.")
            break

        tool_results = []
        for tc in tool_calls:
            print(f"\n[Executing] {tc.name}...")
            result_str = run_tool(tc.name, tc.input)
            result_data = json.loads(result_str)

            if tc.name == "fetch_data":
                signups = result_data.get("new_signups", "N/A")
                rev = result_data.get("revenue_usd", "N/A")
                print(f"  -> Fetched: {signups} sign-ups, ${rev} revenue")
            elif tc.name == "compute_kpis":
                kpis_preview = {k: v for k, v in result_data.items() if k != "error"}
                print(f"  -> KPIs: {json.dumps(kpis_preview)[:200]}")
            elif tc.name == "build_report":
                wc = result_data.get("word_count", 0)
                title = result_data.get("title", "")
                print(f"  -> Built: '{title}' ({wc} words)")
            elif tc.name == "save_report":
                path = result_data.get("path", "")
                size = result_data.get("bytes_written", 0)
                print(f"  -> Saved {size} bytes to {path}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result_str,
            })

        messages.append({"role": "user", "content": tool_results})

    if step >= max_steps:
        print(f"\n[Warning] Reached maximum step limit ({max_steps})")

    print(f"\n{'='*60}")
    print(f"Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Reports saved to: reports/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    report_type = sys.argv[1] if len(sys.argv) > 1 else "daily"
    if report_type not in ("daily", "weekly"):
        print(f"Error: report_type must be 'daily' or 'weekly', got '{report_type}'")
        sys.exit(1)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    run_agent(report_type)
