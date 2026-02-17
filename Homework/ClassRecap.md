### Class Recap

From the class today, we build an app to predict the market price, we use Alpaca API to collecting data from the market and use randomforest to build ml model to analysis the data and produce the result in UI where we build with Streamlit. All the process we have were build with Cursor agent.

Tools:

* [Cursor](https://cursor.com/)
* [Alpaca](https://app.alpaca.markets/dashboard/overview)

What you should do next:

* Build the app yourself, if you have trouble to build it, downlaod this repo and use it as reference, check process in README.md
* Make sure your app is running as expected
* Choice a different time period or a different stock and try out the different result
* Think about what other model that you can use to make the result better (edit ml_core.py)

## Student Task: Explore Workflow Tools (Zapier + OpenClaw) with Two Simple Automations

### Goal

Before building any custom apps, you’ll **self-learn the basics of workflow automation** by exploring tools like **Zapier** and  **OpenClaw** . You’ll implement simple, practical automations that mimic real trading operations (daily reporting + alerts). This is meant to help you understand core workflow concepts— **triggers, actions, scheduling, filters/conditions, and delivery channels** —so you’re ready for more advanced projects later.

---

## Requirements

### Tool Exploration (Required)

* Pick **at least two** workflow tools to explore:
  * **Zapier** (required)
  * **OpenClaw** (required)
  * (Optional: Make, n8n, Pipedream, etc.)

You do **not** need to build an app yet. The focus is on using existing workflow features.

---

## Automation 1: Daily Market Brief (Required)

Build an automation that runs **once per day** (scheduled) and does the following:

1. Pull **daily stock price summary** for a chosen set of tickers (e.g., 5–10 tickers or your watchlist)
2. Pull **top news headlines** related to those tickers (or market headlines)
3. Generate a short summary (bullets are fine)
4. **Send an email report** to yourself with:
   * date/time
   * price moves (daily % change)
   * 3–8 key headlines + links
   * 3–5 bullet “what to watch” summary

**Deliverable:** a screenshot or short screen recording of the workflow + a sample email you received.

---

## Automation 2: Portfolio Move Alert (Required)

Build an automation that checks a portfolio of **~20 stocks** and sends an email alert if:

* **Any ticker moves more than 2% in a day** (up or down)

The alert email must include:

* ticker(s) that triggered the rule
* % move
* current price (if available)
* a link to the data source or chart (if available)

**Deliverable:** screenshot/recording of the workflow + a test alert (you can simulate input if needed).

---

## Suggested Workflow Features to Learn (Checklist)

You should explicitly demonstrate at least **3** of the following across your workflows:

* Scheduled trigger (daily / hourly / market open)
* Conditional logic (filters like “if move > 2%”)
* Looping over a list of tickers (portfolio/watchlist)
* Aggregation (combine multiple tickers into one email)
* Error handling / fallbacks (e.g., if data missing, still send report with partial info)
* Logging or a history view of runs

---

## Submission Checklist

1. Tool(s) used (Zapier + OpenClaw)
2. Links/screenshots showing both workflows
3. One sample **Daily Market Brief email**
4. One sample **Portfolio Move Alert email**
5. A short paragraph:
   * what worked well
   * what was confusing / limiting
   * what you want to automate next

---

## Success Criteria

By completing this task, you should be able to explain (in plain English):

* what your trigger is
* what actions run
* how conditions/filtering work
* how data moves between steps
* how the final report/alert gets delivered

This foundation is required before we move on to building more involved apps and plugging them into a larger workflow system.
