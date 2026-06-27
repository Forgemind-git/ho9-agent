"""
Lead Enrichment Agent
=====================
Takes a list of company names from companies.csv, looks up industry, size,
website, and a contact name for each, and saves the enriched rows to
enriched_leads.csv — all unattended.

Usage:
    python agent.py
    python agent.py companies.csv
"""

import json
import os
import sys
from datetime import datetime

import anthropic
from tools import TOOLS, TOOL_FUNCTIONS

MODEL = "claude-haiku-3-5-20251001"

SYSTEM_PROMPT = """You are a lead enrichment specialist. Your job is:
1. Read the list of companies from the CSV file using read_companies_csv
2. For each company, call lookup_company to get its industry, size, website, and contact name
3. After each lookup, immediately save the enriched row using save_results (output file: enriched_leads.csv)
4. After all companies are processed, print a summary of how many were enriched

Process all companies one by one. Do not skip any. Do not ask for clarification — complete the full job."""


def run_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return its result as a JSON string."""
    fn = TOOL_FUNCTIONS.get(tool_name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    try:
        result = fn(**tool_input)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def run_agent(input_file: str = "companies.csv") -> None:
    """Run the lead enrichment agent."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print(f"\n{'='*60}")
    print(f"Lead Enrichment Agent")
    print(f"Input file: {input_file}")
    print(f"Model: {MODEL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    messages = [
        {
            "role": "user",
            "content": f"Enrich all companies from {input_file} and save results to enriched_leads.csv",
        }
    ]

    step = 0
    max_steps = 30

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
                print(f"\n[Claude]: {block.text[:400]}{'...' if len(block.text) > 400 else ''}\n")
            elif block.type == "tool_use":
                tool_calls.append(block)
                args_preview = json.dumps(block.input)[:150]
                print(f"[Tool call]: {block.name}({args_preview})")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn" or not tool_calls:
            print("\n[Agent] All companies processed.")
            break

        tool_results = []
        for tc in tool_calls:
            print(f"\n[Executing] {tc.name}...")
            result_str = run_tool(tc.name, tc.input)
            result_data = json.loads(result_str)

            if tc.name == "read_companies_csv":
                count = result_data.get("count", 0)
                print(f"  -> Found {count} companies to enrich")
            elif tc.name == "lookup_company":
                name = result_data.get("name", tc.input.get("company_name"))
                industry = result_data.get("industry", "N/A")
                size = result_data.get("size", "N/A")
                print(f"  -> {name}: {industry}, {size}")
            elif tc.name == "save_results":
                total = result_data.get("total_rows", "?")
                print(f"  -> Saved row (total rows: {total})")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result_str,
            })

        messages.append({"role": "user", "content": tool_results})

    if step >= max_steps:
        print(f"\n[Warning] Reached maximum step limit ({max_steps})")

    print(f"\n{'='*60}")
    print(f"Agent finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output saved to: enriched_leads.csv")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "companies.csv"

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    run_agent(input_file)
