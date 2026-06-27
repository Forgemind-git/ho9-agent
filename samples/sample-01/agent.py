"""
Research Brief Agent
====================
Given a topic, the agent plans search queries, finds sources, reads them,
synthesises a sourced brief, and saves it to a file — all unattended.

Usage:
    python agent.py "artificial intelligence in healthcare"
    python agent.py "remote work productivity"
"""

import json
import os
import sys
from datetime import datetime

import anthropic
from tools import TOOLS, TOOL_FUNCTIONS

MODEL = "claude-haiku-3-5-20251001"

SYSTEM_PROMPT = """You are a research analyst. When given a topic you:
1. Plan 2-3 specific search queries to cover the topic well
2. Run those searches using the search_web tool
3. Read the full content of the 2 most relevant URLs using read_url
4. Synthesise what you found into a clear, sourced research brief in markdown
5. Save the brief using write_report

The brief must include:
- An executive summary (3-5 sentences)
- Key findings (bullet points with source citations)
- Implications / so-what
- Sources section listing all URLs consulted

Work through these steps methodically. Do not ask for clarification — complete the job end-to-end."""


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


def run_agent(topic: str) -> None:
    """Run the research brief agent for the given topic."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print(f"\n{'='*60}")
    print(f"Research Brief Agent")
    print(f"Topic: {topic}")
    print(f"Model: {MODEL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    messages = [
        {"role": "user", "content": f"Research this topic and produce a sourced brief: {topic}"}
    ]

    step = 0
    max_steps = 20

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

        # Collect text and tool calls from the response
        tool_calls = []
        text_parts = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
                if block.text.strip():
                    print(f"\n[Claude]: {block.text[:300]}{'...' if len(block.text) > 300 else ''}\n")
            elif block.type == "tool_use":
                tool_calls.append(block)
                print(f"[Tool call]: {block.name}({json.dumps(block.input, indent=2)[:200]})")

        # Append assistant message
        messages.append({"role": "assistant", "content": response.content})

        # If no tool calls, the agent is done
        if response.stop_reason == "end_turn" or not tool_calls:
            print("\n[Agent] Job complete — no further tool calls needed.")
            break

        # Execute each tool call and collect results
        tool_results = []
        for tc in tool_calls:
            print(f"\n[Executing] {tc.name}...")
            result_str = run_tool(tc.name, tc.input)
            result_data = json.loads(result_str)

            # Print a brief summary of the result
            if tc.name == "search_web":
                count = len(result_data.get("results", []))
                print(f"  -> Returned {count} results")
            elif tc.name == "read_url":
                wc = result_data.get("word_count", 0)
                print(f"  -> Read {wc} words from {tc.input.get('url', '')[:60]}")
            elif tc.name == "write_report":
                path = result_data.get("path", "")
                size = result_data.get("bytes_written", 0)
                print(f"  -> Saved {size} bytes to {path}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result_str,
            })

        # Add tool results to the conversation
        messages.append({"role": "user", "content": tool_results})

    if step >= max_steps:
        print(f"\n[Warning] Reached maximum step limit ({max_steps})")

    print(f"\n{'='*60}")
    print(f"Agent finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total conversation turns: {len(messages)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        topic = "artificial intelligence in healthcare"
        print(f"No topic provided — using default: '{topic}'")
    else:
        topic = " ".join(sys.argv[1:])

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Copy .env.example to .env and add your key.")
        sys.exit(1)

    run_agent(topic)
