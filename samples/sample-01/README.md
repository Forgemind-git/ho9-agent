# HO9 Sample 1 — Research Brief Agent

## What you'll build
An agent that does a real analyst job for you: you hand it a **topic**, and it plans its own
searches, reads several sources on the web, and writes you a clean, **sourced research brief** —
all in one go, without you steering each step. It turns "half a day of googling" into a few
minutes of Claude working on its own.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, with **Cowork**).

1. Open **Claude.ai** and start a **Cowork** session (the mode where Claude can search the web
   and take several steps on its own).
2. Open **`agent-prompt.md`** in this folder. Copy the **whole** brief.
3. Paste it into Cowork. Change the line under **"The topic"** to whatever you want researched.
4. Press send, then leave it alone — Claude will plan searches, read sources, and write the
   brief step by step on its own.
5. Read the brief it produces (it also saves a `research-brief.md` file you can download).

## The example prompt
Copy this whole brief into Cowork (it's also saved in `agent-prompt.md`):

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
5. Save the brief as a markdown file named research-brief.md, then give me a short summary of what you found.

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

## What a finished run looks like
See **`sample_output.txt`** for a real example of the brief Claude produces from this prompt.

## Make it your own
- Change the topic to something from your real work ("our competitor's new pricing", "the EU AI Act").
- Add a "Tone" line (e.g. "write for a non-technical board member").
- Ask for a specific length, or for a slide-ready bullet summary at the end.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. The `main` branch of this repo has a Python version
(`agent.py`) that runs the same job automatically from your terminal. It needs an Anthropic API
key, which is separate from — and billed separately to — your Claude.ai subscription.
