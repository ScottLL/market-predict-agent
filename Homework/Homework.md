## Assignment: Build a Workflow-Ready Trading Tool with Cursor

### Objective

Build a small trading-focused app/tool that can plug into a workflow orchestration system later (e.g.,  **OpenClaw** ). Your tool should help automate part of a trader’s daily process—such as earnings tracking, sentiment analysis, or news summarization—while being designed as a **callable workflow “node”** (not just a standalone UI).

---

## What You’re Building

You will build **one workflow-ready tool** that can be triggered by an automation system and returns structured outputs that other workflow steps can consume.

Your tool must support:

* **Predictable inputs** (watchlist/tickers + settings)
* **Predictable outputs** (JSON + optional Markdown report)
* **A trigger interface** (CLI or API) so OpenClaw can run it later

---

## Tool Ideas (Pick One or Propose Your Own)

Choose one of the following, or propose a similar tool that improves trading efficiency:

### Option A — Earnings Radar

* Input: watchlist (tickers), date range
* Output: upcoming earnings calendar, key dates, and a short preview summary per ticker

### Option B — Sentiment Snapshot

* Input: watchlist + lookback window
* Output: sentiment score per ticker + top drivers (headlines / key phrases) + confidence score

### Option C — News Digest Generator

* Input: watchlist + timeframe
* Output: latest relevant news summarized into bullets with timestamps + source links

### Option D — Catalyst Monitor

* Input: watchlist + rules (alerts)
* Output: detects major catalyst events (guidance, ratings changes, filings) and flags “needs attention”

---

## Integration Requirements

### 1) Choose ONE Interface (Required)

Your tool must be runnable via  **one of these** :

**A. CLI Tool**

* Example:
  `trading_tool --tickers AAPL,MSFT --lookback 3d --format json`

**B. HTTP API**

* Example:
  * `POST /run` with JSON input
  * returns JSON output

**C. File-In / File-Out Job Runner**

* Workflow drops `input.json` into a folder
* Tool processes it
* Tool writes `output.json` + `report.md` to an output folder

---

### 2) Standardized Outputs (Required)

Your tool must produce:

**A. JSON output** (for workflow routing / automation decisions)
Must include at least:

* `generated_at` (timestamp)
* `tickers` (list)
* a per-ticker result object (score/date/list/etc.)
* `sources` (URLs or identifiers)
* `errors` (if any, even if empty)

**B. Markdown report** (human-readable summary)
A short report that could be posted to Slack/Notion/dashboard.

**Check the example input.json, output.json and report.md for reference.** 

---

### 3) Workflow-Friendly Behavior (Required)

Implement at least **one** of the following “automation hooks”:

* **Idempotent runs:** safe to run multiple times with same input
* **Since-last-run mode:** only processes new items since last execution
* **Caching:** avoid re-fetching or re-processing identical requests
* **Graceful failure:** if a data source fails, output partial results + errors

---

## Deliverables

1. **Working tool** (code)
2. **README** with:
   * setup instructions
   * how to run (example commands / API calls)
   * input/output examples
3. **I/O schema** (simple documentation):
   * sample `input.json`
   * sample `output.json`
   * sample `report.md`
4. **Workflow diagram** showing how this would plug into OpenClaw later
   * Example flow: Scheduler → Fetch watchlist → Run your tool → Decision step → Publish report/alert
5. **Demo output**
   * one real run with sample tickers + saved outputs

---

## Evaluation Rubric (100 pts)

* **Workflow compatibility (30 pts):** clean interface + structured output
* **Usefulness (25 pts):** genuinely helps daily trading workflow
* **Reliability (20 pts):** error handling + automation hook
* **Output quality (15 pts):** clear JSON + readable report + citations/links
* **Documentation & demo (10 pts):** easy to run and understand

---

## Suggested Scope (Keep It Practical)

* Start with a 5–20 ticker watchlist
* Optimize for “fast + useful” over “complex + fragile”
* UI is optional. Workflow integration is not.

---

If you can, please set up an new github repo like what we did here.
