# Sample 05 — Recurring Report Generator

**Job:** Take this period's raw numbers, compute the KPIs, write a structured leadership report, and
save it — every step on its own, so it could run on a schedule.

## Use it with your Claude.ai subscription
**This is the way to do the hands-on — no API key needed.** Just your normal Claude.ai login
(Pro or Team).

1. Open **Claude.ai** (a **Cowork** session lets it save the report as a file you can download).
2. Copy the brief under **"The example prompt"** below.
3. Paste it into Cowork and replace the numbers under **"This period's data"** with your own.
4. Press send and let Claude calculate, write, and save the report on its own.
5. Read the report and grab the 2-line Slack summary it gives you at the end.

## The example prompt
```
# Recurring Report Generator

You are a reporting agent. Your job: take this period's raw numbers, turn them into a clean leadership report, and save it — doing every step yourself so this could run on a schedule.

## This period's data (replace with your real numbers)
Period: Week of 2025-06-23
New sign-ups: 412 (last week: 358)
Active users: 9,240 (last week: 8,910)
Revenue (MRR): $48,300 (last week: $46,100)
Support tickets: 73 (last week: 88)
Churned customers: 11 (last week: 14)

## Steps to follow (do all of these on your own)
1. Compute the derived KPIs: week-over-week % change for each metric, the churn rate, and average revenue per active user (ARPU).
2. Decide the 3 headline takeaways a leader should notice (both good and bad).
3. Build a structured markdown report using the format below.
4. Save it as report-<period>.md.
5. Give me a 2-line summary I could paste straight into a Slack channel.

## Output format
# Weekly Report — <period>
## Headline takeaways — 3 bullets.
## Metrics — a table: metric | this week | last week | % change.
## What to watch next week — 2–3 bullets.

## Rules
- Do the maths carefully and show every % change.
- Keep it skimmable — a busy exec should get it in 30 seconds.
```

## Make it your own
- Paste in your own metrics — from a CSV export, a dashboard screenshot, or typed by hand.
- Change the cadence (daily / monthly) and the metrics that matter to your team.
- With Claude.ai you can schedule a recurring task so this report builds itself every Monday.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `agent.py` is built to run unattended on a cron schedule
using the Anthropic API. The API key is **separate from your Claude.ai subscription and is billed
separately**.

**Tools the script gives the agent**

| Tool | Purpose |
|------|---------|
| `fetch_data` | Fetches metrics for the report period (mocked with realistic SaaS data) |
| `compute_kpis` | Derives KPIs: churn rate, ARPU, growth percentages |
| `build_report` | Formats everything as a structured markdown report |
| `save_report` | Writes the report to `reports/` with a date-stamped filename |

**Run it**
```bash
pip install -r requirements.txt
cp .env.example .env          # then add your ANTHROPIC_API_KEY (optional, advanced)
export $(cat .env | xargs)
python agent.py               # daily (default); or: python agent.py weekly
```
**Run on a schedule (cron):**
```bash
# Daily report at 7am UTC
0 7 * * * cd /path/to/sample-05 && /usr/bin/python3 agent.py daily >> /var/log/report-agent.log 2>&1
```
Output: `reports/daily-YYYY-MM-DD.md` (and `reports/weekly-YYYY-WNN.md`). See `sample_output.txt`.
