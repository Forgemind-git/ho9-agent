# HO9 Sample 2 — Lead Enrichment Agent

## What you'll build
An agent that takes a bare list of **company names** and fills in the blanks for each one —
industry, size, website, headquarters, and a real named contact — by researching the web on its
own. It turns a half-empty spreadsheet into a usable sales list without you looking up each row
by hand.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, with **Cowork**).

1. Open **Claude.ai** and start a **Cowork** session (so Claude can search the web).
2. Open **`agent-prompt.md`** in this folder and copy the **whole** brief.
3. Paste it into Cowork. Replace the company names under **"The companies to enrich"** with your own.
4. Press send and let Claude work through every company on its own.
5. Download the **`enriched_leads.csv`** file it produces and open it in Excel or Google Sheets.

## The example prompt
Copy this whole brief into Cowork (it's also saved in `agent-prompt.md`):

```
# Lead Enrichment Agent

You are a sales-operations agent. Your job: take my list of company names and fill in the missing details for each one by researching the web — working through the whole list on your own.

## The companies to enrich
Stripe
Notion
Linear
Figma
Vercel

## Steps to follow (do all of these on your own)
1. For each company, search the web and find: industry, approximate employee count (a size band like 51–200), official website, headquarters city/country, and one named senior contact (e.g. a founder or head of sales) with their role.
2. If you genuinely can't confirm a field, write "unknown" — never guess or invent a person, email, or phone number.
3. Collect everything into one table.
4. Save the result as a CSV file named enriched_leads.csv with these columns: company_name, industry, size, website, hq_location, contact_name, contact_role, source.
5. Give me a short summary: how many you fully enriched and any fields you couldn't confirm.

## Rules
- Real, verifiable data only. The source column should hold the URL where you confirmed the contact.
- Do not fabricate emails or phone numbers — leave them out.
```

## What a finished run looks like
See **`sample_output.txt`** for a real example of the enriched table Claude produces.

## Make it your own
- Paste in 10–20 of your own real prospect companies.
- Add columns you care about (funding stage, tech stack, LinkedIn URL).
- Add a rule: "only include contacts whose role contains 'Sales' or 'Marketing'".

## Optional — automate it with the API (advanced)
You do **not** need this for the course. The `main` branch has a Python version (`agent.py`) that
reads a CSV and enriches every row automatically. It needs an Anthropic API key, which is separate
from — and billed separately to — your Claude.ai subscription.
