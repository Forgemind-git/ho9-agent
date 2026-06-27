# Sample 02 — Lead Enrichment Agent

**Job:** Take a list of company names and fill in industry, size, website, and a contact name.

The agent reads a CSV of company names, looks up enrichment data for each one, saves the enriched rows to an output CSV, and prints a summary — fully automated.

## Tools Used

| Tool | Purpose |
|------|---------|
| `read_companies_csv` | Read company names from input CSV (creates a sample if none exists) |
| `lookup_company` | Fetch industry, size, website, and contact for one company (mocked) |
| `save_results` | Append enriched row to output CSV |

## Steps the Agent Takes

1. Reads company names from `companies.csv`
2. Looks up each company with `lookup_company`
3. Saves each enriched row to `enriched_leads.csv`
4. Prints a final summary

## How to Run

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

export $(cat .env | xargs)
python agent.py
# or specify your own CSV:
python agent.py my_companies.csv
```

## Input Format

`companies.csv` — one column, `company_name`:

```
company_name
Stripe
Notion
Linear
```

(A sample file is auto-created on first run if none exists.)

## Output

`enriched_leads.csv` — enriched data with industry, size, website, contact name, and more.

See `sample_output.txt` for a complete run log.
