# Sample 01 — Research Brief Agent

**Job:** Given a topic, gather web context and write a sourced brief.

The agent plans its own search queries, fetches the most relevant sources, reads them in full, synthesises the findings into a structured markdown brief, and saves the file — all without human input after you provide the topic.

## Tools Used

| Tool | Purpose |
|------|---------|
| `search_web` | Search for sources (mocked with realistic results) |
| `read_url` | Read the full text of a URL (mocked) |
| `write_report` | Save the finished brief to `reports/` |

## Steps the Agent Takes

1. Plans 2-3 specific search queries to cover the topic
2. Runs each query with `search_web`
3. Reads the top 2 sources with `read_url`
4. Synthesises findings into a structured markdown brief
5. Saves the brief with `write_report`

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Load env and run
export $(cat .env | xargs)
python agent.py "artificial intelligence in healthcare"

# Or try another topic
python agent.py "remote work productivity"
```

## Output

- Console: step-by-step progress, tool calls, and results
- File: `reports/<topic-slug>.md` — the finished research brief

See `sample_output.txt` for a real example run.
