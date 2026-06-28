# Sample 03 — Page Change Monitor Agent

**Job:** Check a set of web pages, work out what changed since last time, and report only what
actually matters.

The agent reads each page, compares it to the previous snapshot, decides which changes are
meaningful, and writes a clear "what changed" report — saving a fresh snapshot for next time.

## Use it with your Claude.ai subscription
**This is the way to do the hands-on — no API key needed.** Just your normal Claude.ai login
(Pro or Team, with **Cowork**).

1. Open **Claude.ai** and start a **Cowork** session (so Claude can open and read live web pages).
2. Copy the brief under **"The example prompt"** below.
3. Paste it into Cowork and list the URLs you care about under **"Pages to monitor"**.
4. Press send. On the **first run** Claude records a baseline and saves it as a file.
5. **Next time**, paste that saved snapshot into the "Previous snapshot" section and Claude tells you
   exactly what changed and why it matters.

## The example prompt
```
# Page Change Monitor Agent

You are a monitoring agent. Your job: check a set of web pages, work out what has changed since I last looked, and report only what actually matters — deciding for yourself what is worth flagging.

## Pages to monitor
- https://www.anthropic.com/pricing   (watching for: price or plan changes)
- https://openai.com/pricing           (watching for: price or plan changes)

## Previous snapshot
First run — no previous snapshot yet. Record a baseline this time.
(On later runs, paste the contents of the last snapshot file here so Claude can compare.)

## Steps to follow (do all of these on your own)
1. Open and read each page in full.
2. Compare what you see now to the previous snapshot above.
3. Decide which changes are meaningful (a price change, a new or removed plan, a removed feature, a status outage) versus noise (date stamps, cosmetic wording).
4. Produce a "What changed" report grouped by page, with a clear ⚠️ flag on anything important and a one-line "why it matters".
5. Save a fresh snapshot of each page's key content as snapshot-<today>.md so the next run can compare.

## Output format
# What Changed — <date>
For each page: the URL, a "Changed" or "No change" verdict, the specific change, and why it matters.

## Rules
- If nothing meaningful changed, say "No meaningful changes" — don't pad the report.
- Quote the exact old vs new value for any price or plan change.
```

## Make it your own
- Swap in your competitors' pricing pages, your own status page, or a docs/changelog page.
- Tell it what you care about ("only flag price changes, ignore blog posts").
- Run it on a routine: with Claude.ai you can schedule a recurring task to run this on a cadence.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `agent.py` fetches each page, diffs it against a saved
snapshot, and logs alerts automatically using the Anthropic API. The API key is **separate from your
Claude.ai subscription and is billed separately**.

**Tools the script gives the agent**

| Tool | Purpose |
|------|---------|
| `get_url_list` | Returns the list of URLs to monitor |
| `load_snapshot` | Loads the last saved snapshot for a URL |
| `fetch_page` | Fetches current page content (mocked with realistic changes) |
| `compare_content` | Runs a unified diff on old vs new content |
| `send_alert` | Prints an alert and appends to `alerts/alert_log.txt` |
| `save_snapshot` | Saves the new content as the snapshot for next run |

**Run it**
```bash
pip install -r requirements.txt
cp .env.example .env          # then add your ANTHROPIC_API_KEY (optional, advanced)
export $(cat .env | xargs)
python agent.py
```
Output: console progress, `alerts/alert_log.txt`, and one snapshot file per URL in `snapshots/`.
See `sample_output.txt` for a complete run.
