---
name: stock-lookup
description: >
  Use when the user asks about a stock price, share price, or market data for
  a specific date or date range. Trigger phrases: "what was X stock on", "price of TICKER on",
  "how much was TICKER", "stock price for", "look up stock", "get stock price",
  "price history", "prices from X to Y", "over the past N days/weeks/months".
tools:
  - mcp__stock-prices__get_stock_price_on_day
  - mcp__stock-prices__get_price_history
---

## Single-day lookup

When the user asks for a stock price on a specific date:

1. Extract the ticker symbol(s) and date from the user's request. If the date is ambiguous (e.g., "last Monday"), resolve it to YYYY-MM-DD using today's date as reference.

2. Call `get_stock_price_on_day` with a list of tickers and the date. Always pass tickers as a list, even for a single ticker.

3. Interpret the result — it is a dict keyed by ticker symbol:
   - The returned `date` is the most recent trading day on or before the requested date. If the requested date was a weekend or holiday, the `date` field will differ — mention this to the user.
   - If `open` and `close` are both `null`, no data could be found (e.g. invalid ticker). Say so clearly.
   - If both are present, report the opening price, closing price, and percent change. Use `percent_change` directly from the tool — do not recalculate it.

4. Format the response concisely. Example:
   > **AAPL on 2024-03-15**: opened at $172.77, closed at $173.72 (+0.55%)

   If the returned date differs from the requested date:
   > **AAPL** (most recent trading day: 2024-03-14): opened at $172.77, closed at $173.72 (+0.55%)

5. If the user asks about multiple tickers for the same date, pass them all in a single call. Summarize results in a table if there are three or more tickers. For different dates, make one call per date.

6. Do not speculate about why a price moved. Stick to the data returned by the tool.

## Date range / history lookup

When the user asks for prices over a range of dates:

1. Extract ticker symbol(s), start date, and end date. Resolve ambiguous ranges (e.g., "past month", "last week") to concrete YYYY-MM-DD dates using today's date as reference. The `end` date is exclusive (e.g., to include April 30, pass `end="2026-05-01"`).

2. Call `get_price_history` with a list of tickers, `start`, and `end`. Always pass tickers as a list.

3. Interpret the result — it is a dict keyed by date string, then by ticker symbol, each with `open` and `close`:
   ```
   {
     "2026-04-10": { "VOO": { "open": 626.33, "close": 628.50 }, ... },
     ...
   }
   ```
   Only trading days appear; weekends and holidays are absent.

4. Format the response as a table when the range spans more than a few days or involves multiple tickers. For short ranges or single tickers, a concise list is fine. Example table:

   | Date       | VOO open | VOO close | AVUS open | AVUS close |
   |------------|----------|-----------|-----------|------------|
   | 2026-04-10 | $626.33  | $628.50   | $94.50    | $95.00     |

5. Do not speculate about price movements. Stick to the data returned by the tool.
