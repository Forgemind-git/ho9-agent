# Sample 05 — Recurring Report Generator

**Job:** Pull data from a source, build a structured report, and save it.

The agent fetches the latest product metrics, computes derived KPIs, builds a complete markdown report, and saves it to the `reports/` folder — designed to run unattended on a schedule (cron job, GitHub Actions, etc.).

## Tools Used

| Tool | Purpose |
|------|---------|
| `fetch_data` | Fetches metrics for the report period (mocked with realistic SaaS data) |
| `compute_kpis` | Derives KPIs: churn rate, ARPU, growth percentages |
| `build_report` | Formats everything as a structured markdown report |
| `save_report` | Writes the report to `reports/` with a date-stamped filename |

## Steps the Agent Takes

1. Fetches latest metrics with `fetch_data`
2. Computes derived KPIs with `compute_kpis`
3. Builds a formatted markdown report with `build_report`
4. Saves the report to `reports/daily-YYYY-MM-DD.md` with `save_report`
5. Prints a summary with key headline numbers

## How to Run

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY

export $(cat .env | xargs)

# Daily report (default)
python agent.py

# Weekly report
python agent.py weekly
```

## Running on a Schedule

Add to crontab to run every morning:

```bash
# Run daily report at 7am UTC
0 7 * * * cd /path/to/sample-05 && /usr/bin/python3 agent.py daily >> /var/log/report-agent.log 2>&1

# Run weekly report every Monday at 8am UTC
0 8 * * 1 cd /path/to/sample-05 && /usr/bin/python3 agent.py weekly >> /var/log/report-agent.log 2>&1
```

## Output

- `reports/daily-YYYY-MM-DD.md` — daily report with sign-ups, revenue, API usage, feature adoption
- `reports/weekly-YYYY-WNN.md` — weekly report with MRR metrics

See `sample_output.txt` for a complete run.
