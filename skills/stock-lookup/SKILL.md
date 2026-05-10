---
name: stock-lookup
description: >
  Use when the user asks about a stock price, share price, or market data for
  a specific date. Trigger phrases: "what was X stock on", "price of TICKER on",
  "how much was TICKER", "stock price for", "look up stock", "get stock price".
tools:
  - mcp__stock-prices__get_stock_price_on_day
---

When the user asks for a stock price on a specific date:

1. Extract the ticker symbol(s) and date from the user's request. If the date is ambiguous (e.g., "last Monday"), resolve it to YYYY-MM-DD using today's date as reference.

2. Call `get_stock_price_on_day` with a list of tickers and the date. Always pass tickers as a list, even for a single ticker.

3. Interpret the result — it is a dict keyed by ticker symbol:
   - If a ticker's `open` and `close` are both `null`, the market was closed on that date (weekend or holiday). Say so clearly and offer to look up the nearest trading day.
   - If both are present, report the opening price, closing price, and percent change. Use `percent_change` directly from the tool — do not recalculate it.

4. Format the response concisely. Example:
   > **AAPL on 2024-03-15**: opened at $172.77, closed at $173.72 (+0.55%)

5. If the user asks about multiple tickers for the same date, pass them all in a single call. Summarize results in a table if there are three or more tickers. For different dates, make one call per date.

6. Do not speculate about why a price moved. Stick to the data returned by the tool.
