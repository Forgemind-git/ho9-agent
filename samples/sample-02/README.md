# Sample 02 — Lead Enrichment Agent

**Job:** Take a list of company names and fill in industry, size, website, HQ, and a named contact —
working through the whole list automatically.

The agent reads a list of companies, researches each one on the web, and produces an enriched table
ready for your CRM.

## Use it with your Claude.ai subscription
**This is the way to do the hands-on — no API key needed.** Just your normal Claude.ai login
(Pro or Team, with **Cowork**).

1. Open **Claude.ai** and start a **Cowork** session (so Claude can search the web).
2. Copy the brief under **"The example prompt"** below.
3. Paste it into Cowork and replace the names under **"The companies to enrich"** with your own.
4. Press send and let Claude work through every company on its own.
5. Download the **`enriched_leads.csv`** it produces and open it in Excel or Google Sheets.

## The example prompt
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
4. Save the result as enriched_leads.csv with columns: company_name, industry, size, website, hq_location, contact_name, contact_role, source.
5. Give me a short summary: how many you fully enriched and any fields you couldn't confirm.

## Rules
- Real, verifiable data only. The source column should hold the URL where you confirmed the contact.
- Do not fabricate emails or phone numbers — leave them out.
```

## Make it your own
- Paste in 10–20 of your own real prospect companies.
- Add columns you care about (funding stage, tech stack, LinkedIn URL).
- Add a rule: "only include contacts whose role contains 'Sales' or 'Marketing'".

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `agent.py` reads a CSV and enriches every row automatically
using the Anthropic API. The API key is **separate from your Claude.ai subscription and is billed
separately**.

**Tools the script gives the agent**

| Tool | Purpose |
|------|---------|
| `read_companies_csv` | Read company names from input CSV (creates a sample if none exists) |
| `lookup_company` | Fetch industry, size, website, and contact for one company (mocked) |
| `save_results` | Append enriched row to output CSV |

**Run it**
```bash
pip install -r requirements.txt
cp .env.example .env          # then add your ANTHROPIC_API_KEY (optional, advanced)
export $(cat .env | xargs)
python agent.py               # or: python agent.py my_companies.csv
```
Input `companies.csv` has one column, `company_name` (a sample is auto-created on first run).
Output: `enriched_leads.csv`. See `sample_output.txt` for a complete run log.
