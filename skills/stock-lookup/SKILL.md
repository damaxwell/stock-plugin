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

1. Extract the ticker symbol and date from the user's request. If the date is ambiguous (e.g., "last Monday"), resolve it to YYYY-MM-DD using today's date as reference.

2. Call `get_stock_price_on_day` with the ticker and date.

3. Interpret the result:
   - If `open` and `close` are both `null`, the market was closed on that date (weekend or holiday). Say so clearly and offer to look up the nearest trading day.
   - If both are present, report the opening price, closing price, and percent change. Use `percent_change` directly from the tool — do not recalculate it.

4. Format the response concisely. Example:
   > **AAPL on 2024-03-15**: opened at $172.77, closed at $173.72 (+0.55%)

5. If the user asks about multiple tickers or a date range, call the tool once per ticker/date combination. Summarize results in a table if there are three or more rows.

6. Do not speculate about why a price moved. Stick to the data returned by the tool.
