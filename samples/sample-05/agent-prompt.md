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
4. Save it as `report-<period>.md`.
5. Give me a 2-line summary I could paste straight into a Slack channel.

## Output format
# Weekly Report — <period>
## Headline takeaways
3 bullets.
## Metrics
A table: metric | this week | last week | % change.
## What to watch next week
2–3 bullets.

## Rules
- Do the maths carefully and show every % change.
- Keep it skimmable — a busy exec should get it in 30 seconds.
