
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
        A dict keyed by ticker symbol. Each value has ticker, date, open, close, previous trading
        day close, and percent_change from previous close. The returned date is the most recent
        trading day on or before the requested day (e.g. if a weekend or holiday is requested,
        the preceding Friday's data is returned). All price fields are null only if no trading
        data could be found (e.g. invalid ticker).
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
        end: End date in YYYY-MM-DD format (exclusive, same semantics as yfinance)

    Returns:
        A dict keyed by date (YYYY-MM-DD), then by ticker symbol. Each value has open and close
        prices. Only trading days with data are included.
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