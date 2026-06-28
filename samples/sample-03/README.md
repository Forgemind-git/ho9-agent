# HO9 Sample 3 — Page Change Monitor Agent

## What you'll build
An agent that watches a set of web pages for you — competitor pricing, a status page, a changelog —
reads each one, and tells you **what actually changed** since last time, deciding for itself what is
worth flagging. No more finding out about a price change or an outage days too late.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, with **Cowork**).

1. Open **Claude.ai** and start a **Cowork** session (so Claude can open and read live web pages).
2. Open **`agent-prompt.md`** in this folder and copy the **whole** brief.
3. Paste it into Cowork. Put the URLs you care about under **"Pages to monitor"**.
4. Press send. On the **first run** Claude records a baseline snapshot and saves it as a file.
5. **Next time**, paste the contents of that saved snapshot into the "Previous snapshot" section, and
   Claude will tell you exactly what changed and why it matters.

## The example prompt
Copy this whole brief into Cowork (it's also saved in `agent-prompt.md`):

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
5. Save a fresh snapshot of each page's key content as snapshot-<today>.md so the next run can compare against it.

## Output format
# What Changed — <date>
For each page: the URL, a "Changed" or "No change" verdict, the specific change, and why it matters.

## Rules
- If nothing meaningful changed, say "No meaningful changes" — don't pad the report.
- Quote the exact old vs new value for any price or plan change.
```

## What a finished run looks like
See **`sample_output.txt`** for a real example of the "What changed" report Claude produces.

## Make it your own
- Swap in your competitors' pricing pages, your own status page, or a docs/changelog page.
- Tell it what you care about ("only flag price changes, ignore blog posts").
- Run it on a routine: with Claude.ai you can schedule a recurring task to run this on a cadence.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. The `main` branch has a Python version (`agent.py`) that
fetches each page, diffs it against a saved snapshot, and logs alerts automatically. It needs an
Anthropic API key, which is separate from — and billed separately to — your Claude.ai subscription.
