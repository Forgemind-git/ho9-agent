# Sample 01 — Research Brief Agent

**Job:** Given a topic, gather web sources and write a clean, sourced research brief — all in one
unattended run.

You hand the agent a topic; it plans its own searches, reads the best sources, synthesises the
findings into a structured markdown brief, and saves the file. No human steering after the topic.

## Use it with your Claude.ai subscription
**This is the way to do the hands-on — no API key needed.** Just your normal Claude.ai login
(Pro or Team, with **Cowork**).

1. Open **Claude.ai** and start a **Cowork** session (the mode where Claude can search the web and
   take several steps on its own).
2. Copy the brief under **"The example prompt"** below.
3. Paste it into Cowork and change the line under **"The topic"** to whatever you want researched.
4. Press send, then leave it — Claude plans the searches, reads sources, and writes the brief itself.
5. Read the brief (it also saves a `research-brief.md` you can download).

## The example prompt
```
# Research Brief Agent

You are a research analyst agent. Your job: take the topic I give you and produce a structured, sourced research brief — running the whole process yourself, without asking me to steer each step.

## The topic
Remote work productivity in 2025

## Steps to follow (do all of these on your own)
1. Plan 3–4 specific search queries that together cover the topic well — trends, hard data, opposing views, and recent developments.
2. Search the web for each query. Open and read the most relevant 4–6 sources in full.
3. Note the key facts, figures and quotes from each source, and keep the link for each one.
4. Synthesise everything into a single structured brief using the format below.
5. Save the brief as research-brief.md, then give me a short summary of what you found.

## Output format
# Research Brief: <topic>
**Date:** <today>
## Executive summary — 3–4 sentences capturing the big picture.
## Key findings — 4–6 bullets, each backed by a source number like [1].
## Implications — 2–4 bullets aimed at a decision-maker.
## Sources — numbered list with the title and full URL of every source.

## Rules
- Only state facts you can attribute to a source. If something is uncertain, say so.
- Prefer recent, reputable sources. Skip SEO spam and content farms.
```

## Make it your own
- Change the topic to something from your real work.
- Add a "Tone" line (e.g. "write for a non-technical board member").
- Ask for a specific length, or a slide-ready bullet summary at the end.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `agent.py` runs the same job automatically from your
terminal using the Anthropic API — useful if you want to schedule it or wire it into other tools.
The API key is **separate from your Claude.ai subscription and is billed separately**.

**Tools the script gives the agent**

| Tool | Purpose |
|------|---------|
| `search_web` | Search for sources (mocked with realistic results) |
| `read_url` | Read the full text of a URL (mocked) |
| `write_report` | Save the finished brief to `reports/` |

**Run it**
```bash
pip install -r requirements.txt
cp .env.example .env          # then add your ANTHROPIC_API_KEY (optional, advanced)
export $(cat .env | xargs)
python agent.py "artificial intelligence in healthcare"
```
Output: step-by-step progress in the console and `reports/<topic-slug>.md`.
See `sample_output.txt` for a real example run.
