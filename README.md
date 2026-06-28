# HO9 — Agent That Does a Real Job

> Hands-on portfolio project · **Week 4** · **Solo** · module M13. Part of the **ForgeMind AI — AI Productivity Essentials** course.

## Goal

**Done when:** A multi-step job completed unattended

## What to ship

The agent config/script + a recording of it running end-to-end + a README of the job it does.

## Pick a problem statement

Choose **one** of these real use-cases — or bring your own (get it approved first):

1. As an analyst you lose half a day researching every new topic by hand. Build an agent that, given a topic, gathers sources, reads them, and outputs a structured brief, running the full chain without you steering each step. Success: a recording of one unattended run that takes a topic in and produces a sourced brief out.

2. Your sales team imports company names but the rows are mostly empty. Build a lead-enrichment agent that takes a list of companies and fills in details (industry, size, website, a contact) from the web, step by step on its own. Success: an unattended run that turns a bare list into an enriched one, recorded end to end.

3. You manage pages or competitor sites and only notice changes when it is too late. Build a monitoring agent that checks a set of pages daily and reports what changed, deciding what is worth flagging without supervision. Success: a recording of an unattended run that detects a change and produces a clear 'what changed' report.

4. Your shared inbox piles up faster than you can sort it. Build an inbox-triage agent that reads incoming requests, categorises them, and drafts replies for your review, running the whole loop unattended. Success: a recorded run where a batch of messages comes back sorted with draft responses ready for a human to approve.

5. Leadership wants a recurring summary and assembling it by hand is a chore. Build a reporting agent that pulls data, builds a summary, and posts it to a channel, completing every step on its own. Success: a recording of one unattended run from data pull to a posted summary, with no manual steps in between.

## How to use this repo

The 5 folders in `samples/` are worked reference agents. The **primary way to run each one is in
Claude Cowork on your Claude.ai subscription — no API key, no coding.** Open a sample's `README.md`,
copy its filled-in **example prompt** into a Cowork session (Pro or Team), swap in your own input,
and let Claude run the job on its own. Each sample also ships an optional Python version (`agent.py`)
for advanced learners who want to automate it with the Anthropic API (billed separately).

1. Click **Use this template** to create your own copy.
2. Pick the sample closest to your job, copy its example prompt into Cowork, and run it.
3. Adapt it to your own use case, then replace this section of the README with: what you built, the
   problem it solves, and how to run it.

> Browse the samples on the live landing page (GitHub Pages) — see `index.html`. No API key needed.

---

*HO9 · Solo · ForgeMind AI Course · module M13 (Week 4)*
