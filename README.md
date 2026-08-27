# AEK Ticketmaster monitor — investigation notes

**Goal:** get notified as soon as a new AEK football match (in particular
vs. Real Madrid) becomes bookable at
https://www.ticketmaster.gr/aek/showProductList.html

## Finding: server-side automation is blocked

Two approaches were tried from GitHub Actions runners (which have normal
internet access, unlike a sandboxed agent environment):

1. **Plain HTTP (`requests`, with realistic browser headers, a warmed-up
   session, cookies, referer, etc.)** → `403`, body is an Akamai Bot
   Manager challenge page ("Let's Get Your Identity Verified").
2. **A real headless Chromium browser (Playwright)**, navigating the
   homepage first then the listing page → still `403`, same Akamai
   challenge page. Confirmed via `check.py`'s workflow run.

Akamai's bot detection here isn't just checking the User-Agent string —
it fingerprints the TLS/JS/browser-automation signals and the origin IP
range. GitHub Actions runner IPs are well-known datacenter ranges and get
flagged outright, and even a genuine Chromium engine run headless in that
environment doesn't pass. This isn't fixable by tweaking headers or
switching HTTP libraries — it would require a real residential browser
session, which server-side automation in a CI runner cannot provide.

**Conclusion: don't keep polling this from a script.** Use a
browser-extension-based page-change monitor instead (runs from a real,
logged-in, real-IP browser) — see the recommendation given in the Claude
Code session that produced this repo.

## Files here

- `check.py` — diagnostic script, confirms the block (kept for reference).
- `.github/workflows/monitor.yml` — manual-dispatch-only diagnostic
  workflow (**not scheduled**, so it won't run or waste Actions minutes on
  its own).
- `requirements.txt` — Playwright, used by the diagnostic script.
