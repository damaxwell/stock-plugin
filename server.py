
import yfinance as yf
from datetime import date, timedelta
from fastmcp import FastMCP

mcp = FastMCP("Stock Prices")

@mcp.tool()
def get_stock_price_on_day(ticker: str, day: str) -> dict:
    """
    Get the opening and closing price of a stock on a specific day.
    
    Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'MSFT')
        day: The date in YYYY-MM-DD format (e.g. '2024-03-15')
    
    Returns:
        A dict with ticker, open, close, previous trading day close and percent_change from previous close. All price fields
        are null if there was no trading on that day (weekend, holiday, etc).
    """
    target = date.fromisoformat(day)
    start_day = target + timedelta(days=-5)
    end_day = target + timedelta(days=1)

    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_day.isoformat(), end=end_day.isoformat(), interval="1d")
    print(hist)

    record = {"ticker": ticker.upper(), "date": day, "open": None, "close": None, "previous": None, "percent_change": None}

    if len(hist) < 2:
        return record
    
    prev_row = hist.iloc[-2]
    final_row = hist.iloc[-1]

    if final_row.name.date() != target:
        return record

    record["open"] = round(final_row["Open"], 4)
    close_price = round(final_row["Close"], 4)
    record["close"] = close_price
    prev_price = round(prev_row["Close"], 4)
    record["previous"] = prev_price
    rel_change = (close_price - prev_price) / prev_price
    record["percent_change"] = round(rel_change * 100.0, 4)

    return record