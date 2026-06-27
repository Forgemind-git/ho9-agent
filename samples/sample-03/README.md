# Sample 03 — Page Change Monitor Agent

**Job:** Check a set of URLs for content changes and report what changed.

The agent loads previous snapshots, fetches current page content, diffs old vs new, fires alerts for any changes, and saves fresh snapshots for the next run — entirely automated.

## Tools Used

| Tool | Purpose |
|------|---------|
| `get_url_list` | Returns the list of URLs to monitor |
| `load_snapshot` | Loads the last saved snapshot for a URL |
| `fetch_page` | Fetches current page content (mocked with realistic changes) |
| `compare_content` | Runs a unified diff on old vs new content |
| `send_alert` | Prints an alert and appends to `alerts/alert_log.txt` |
| `save_snapshot` | Saves the new content as the snapshot for next run |

## Monitored URLs (mock)

- `https://status.example-saas.com` — status page (now shows webhook outage)
- `https://changelog.example-tool.io` — changelog (v2.4.0 released with breaking change)
- `https://pricing.example-platform.com` — pricing page (Pro plan price increased)

## How to Run

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY

export $(cat .env | xargs)
python agent.py
```

## Output

- Console: step-by-step progress with diff summaries
- `alerts/alert_log.txt` — all change alerts appended
- `snapshots/` — one `.txt` file per URL for next-run comparison

See `sample_output.txt` for a complete run.
