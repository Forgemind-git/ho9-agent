# Sample 04 — Inbox Triage Agent

**Job:** Read a batch of incoming messages, categorise each by type and priority, and draft a reply
for every one that needs it — ready for a human to approve.

The agent sorts the whole batch and writes the drafts in one unattended run.

## Use it with your Claude.ai subscription
**This is the way to do the hands-on — no API key needed.** Just your normal Claude.ai login
(Pro or Team).

1. Open **Claude.ai** (a **Cowork** session is ideal so it can save the drafts as a file; a normal
   chat works too).
2. Copy the brief under **"The example prompt"** below.
3. Paste it into Cowork and replace the messages under **"The inbox"** with your own (anonymise if needed).
4. Press send and let Claude sort the whole batch and draft every reply.
5. Review the triage table and drafts, tweak anything, then send the ones you're happy with.

## The example prompt
```
# Inbox Triage Agent

You are an inbox-triage agent. Your job: read a batch of incoming messages, sort each one, and draft a reply for me to approve — handling the whole batch on your own.

## The inbox (replace with your own messages)
1. From: angry-customer@acme.com — "Your API has been down for 2 hours and we're losing orders. This is unacceptable. When will it be fixed?"
2. From: finance@bigcorp.com — "Can you resend invoice #4471? We never received it and payment is due Friday."
3. From: jamie@startup.io — "Love the product! Any chance you'll add a dark mode? Would be huge for our team."
4. From: newsletter@somevendor.com — "🎉 50% off our annual plan this week only!"
5. From: partnerships@growthco.com — "We'd like to explore a co-marketing webinar with your team next quarter."

## Steps to follow (do all of these on your own)
1. Read every message.
2. For each, assign a Category (Critical support / Billing / Feature request / Partnership / Newsletter / Other) and a Priority (Urgent / High / Medium / Low).
3. Draft a warm, professional reply for each message that needs one. For newsletters/spam, mark "No reply needed".
4. Put everything in a triage table, then list the full draft replies below it.
5. Save the drafts to a file named triage-drafts.md.

## Output format
A triage table: # | from | category | priority | needs reply?
Then, for each message that needs a reply, the full draft text under a heading with its number.

## Rules
- Don't promise dates, refunds or features you can't be sure of — keep replies safe for a human to send after a quick check.
- Put anything Urgent at the top so I see it first.
```

## Make it your own
- Paste in your real inbox messages (remove names/emails if they're sensitive).
- Change the categories to match your team (e.g. "Recruiting", "Press", "Refund").
- Add your brand voice: "sign every reply as 'The Acme Team' and keep it friendly but brief".

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `agent.py` triages a batch of emails and saves all drafts to
JSON automatically using the Anthropic API. The API key is **separate from your Claude.ai subscription
and is billed separately**.

**Tools the script gives the agent**

| Tool | Purpose |
|------|---------|
| `read_emails` | Fetches the inbox batch (6 realistic mocked emails) |
| `categorise_email` | Assigns category and priority to one email |
| `draft_reply` | Writes a complete reply for one email |
| `save_drafts` | Saves all drafts to `drafts/triage_drafts.json` |

**Run it**
```bash
pip install -r requirements.txt
cp .env.example .env          # then add your ANTHROPIC_API_KEY (optional, advanced)
export $(cat .env | xargs)
python agent.py
```
Output: console triage summary and `drafts/triage_drafts.json`. See `sample_output.txt` for a complete run.
