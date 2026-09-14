
import yfinance as yf
from datetime import date, timedelta
from fastmcp import FastMCP
from collections import defaultdict

mcp = FastMCP("Stock Prices")

def _get_stock_price_on_day(ticker: str, target: date) -> dict:
    start_day = target + timedelta(days=-5)
    end_day = target + timedelta(days=1)

    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_day.isoformat(), end=end_day.isoformat(), interval="1d")

    record = {"ticker": ticker.upper(), "date": None, "open": None, "close": None, "previous": None, "percent_change": None}

    if len(hist) < 2:
        return record

    prev_row = hist.iloc[-2]
    final_row = hist.iloc[-1]

    record["date"] = final_row.name.date().isoformat()
    record["open"] = round(final_row["Open"], 4)
    close_price = round(final_row["Close"], 4)
    record["close"] = close_price
    prev_price = round(prev_row["Close"], 4)
    record["previous"] = prev_price
    rel_change = (close_price - prev_price) / prev_price
    record["percent_change"] = round(rel_change * 100.0, 4)

    return record


@mcp.tool()
def get_stock_price_on_day(tickers: list[str], day: str) -> dict[str, dict]:
    """
    Get the opening and closing price of one or more stocks on or before a specific day.

    Args:
        tickers: List of stock ticker symbols (e.g. ['AAPL', 'MSFT'])
        day: The date in YYYY-MM-DD format (e.g. '2024-03-15')

    Returns:
        A dict keyed by ticker symbol (uppercased). Each value contains:
          - ticker: the normalized symbol
          - date: the actual trading day used — the most recent trading day on or before the
            requested day. If a weekend or holiday is requested, this will differ from `day`
            (e.g. a Monday request after a holiday returns the prior Friday).
          - open: opening price on `date`
          - close: closing price on `date`
          - previous: closing price of the trading day immediately before `date` (the prior
            session's close, not the open of `date`)
          - percent_change: percentage change from `previous` to `close` — use this value
            directly; do not recalculate it from open/close

        All fields except `ticker` are null when no data is available. This occurs when the
        ticker is invalid OR when fewer than two trading days exist in the 5-day lookup window
        (e.g. the requested date is very early in the ticker's trading history).
    """
    print("get_stock_price_on_day " + str(tickers))
    target = date.fromisoformat(day)
    print("get_stock_price_on_day done")
    return {ticker.upper(): _get_stock_price_on_day(ticker, target) for ticker in tickers}


@mcp.tool()
def get_price_history(tickers: list[str], start: str, end: str) -> dict[str, dict[str, dict]]:
    """
    Get daily open and close prices for one or more stocks over a date range.

    Args:
        tickers: List of stock ticker symbols (e.g. ['VOO', 'AVUS'])
        start: Start date in YYYY-MM-DD format (inclusive)
        end: End date in YYYY-MM-DD format (exclusive — to include e.g. April 30, pass
             end='2026-05-01'; same semantics as yfinance)

    Returns:
        A dict keyed by date string (YYYY-MM-DD), then by ticker symbol (uppercased). Each
        leaf value has:
          - open: opening price on that date
          - close: closing price on that date

        Only actual trading days appear; weekends and market holidays are omitted. Example:
          {
            "2026-04-10": {
              "VOO":  {"open": 626.33, "close": 628.50},
              "AVUS": {"open": 94.50,  "close": 95.00}
            },
            "2026-04-13": {
              "VOO":  {"open": 619.00, "close": 622.75},
              "AVUS": {"open": 93.00,  "close": 94.50}
            }
          }
    """
    print("get_price_history " + str(tickers))
    result = defaultdict(dict)
    for ticker in tickers:
        symbol = ticker.upper()
        hist = yf.Ticker(ticker).history(start=start, end=end, interval="1d")
        for ts, row in hist.iterrows():
            day_str = ts.date().isoformat()
            result[day_str][symbol] = {
                "open": round(row["Open"], 4),
                "close": round(row["Close"], 4),
            }
    print("get_price_history done")
    return dict(result)