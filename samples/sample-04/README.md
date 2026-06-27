# Sample 04 — Inbox Triage Agent

**Job:** Read a batch of email messages, categorise each, and draft a reply.

The agent fetches a batch of 6 emails, classifies each by category and priority, drafts a professional reply, saves all drafts to a JSON file, and prints a triage summary — no human required.

## Tools Used

| Tool | Purpose |
|------|---------|
| `read_emails` | Fetches the inbox batch (6 realistic mocked emails) |
| `categorise_email` | Assigns category and priority to one email |
| `draft_reply` | Writes a complete reply for one email |
| `save_drafts` | Saves all drafts to `drafts/triage_drafts.json` |

## Email Categories

- `critical_support` — production outage, data loss, security incident
- `billing` — invoice, payment, subscription questions
- `technical_support` — API questions, bug reports
- `partnership` — co-marketing, collaboration proposals
- `newsletter` — promotional or newsletter content
- `feature_request` — product feedback from customers

## Priorities

- `urgent` — respond within 1 hour
- `high` — respond within 4 hours
- `medium` — respond within 24 hours
- `low` — respond this week

## How to Run

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY

export $(cat .env | xargs)
python agent.py
```

## Output

- Console: step-by-step progress and final triage summary table
- `drafts/triage_drafts.json` — all drafted replies ready to review and send

See `sample_output.txt` for a complete run.
