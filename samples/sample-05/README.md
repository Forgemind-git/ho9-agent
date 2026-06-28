# HO9 Sample 5 — Recurring Report Generator

## What you'll build
An agent that turns this period's raw numbers into a polished **leadership report** — it does the maths
(growth %, churn rate, ARPU), picks out the headline takeaways, writes a clean summary, and saves it as
a file. The kind of weekly report you'd normally assemble by hand, done in one step so it could even run
on a schedule.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team).

1. Open **Claude.ai** (a **Cowork** session lets it save the report as a file you can download).
2. Open **`agent-prompt.md`** in this folder and copy the **whole** brief.
3. Paste it into Cowork. Replace the numbers under **"This period's data"** with your own.
4. Press send and let Claude calculate, write, and save the report on its own.
5. Read the report and grab the 2-line Slack summary it gives you at the end.

## The example prompt
Copy this whole brief into Cowork (it's also saved in `agent-prompt.md`):

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

## What a finished run looks like
See **`sample_output.txt`** for a real example of the report Claude produces from these numbers.

## Make it your own
- Paste in your own metrics — from a CSV export, a dashboard screenshot, or typed by hand.
- Change the cadence (daily / monthly) and the metrics that matter to your team.
- With Claude.ai you can schedule a recurring task so this report builds itself every Monday.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. The `main` branch has a Python version (`agent.py`) built to run
unattended on a cron schedule. It needs an Anthropic API key, which is separate from — and billed
separately to — your Claude.ai subscription.
