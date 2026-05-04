
import yfinance as yf
from datetime import date, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Stock Prices")

@mcp.tool()
def get_stock_price_on_day(ticker: str, day: str) -> dict:
    """
    Get the opening and closing price of a stock on a specific day.
    
    Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'MSFT')
        day: The date in YYYY-MM-DD format (e.g. '2024-03-15')
    
    Returns:
        A dict with ticker, open, close, and percent_change. All price fields
        are null if there was no trading on that day (weekend, holiday, etc).
        percent_change is ((close - open) / open) * 100, rounded to 2 decimal places.
    """
    target = date.fromisoformat(day)
    next_day = target + timedelta(days=1)

    stock = yf.Ticker(ticker)
    hist = stock.history(start=target.isoformat(), end=next_day.isoformat(), interval="1d")

    if hist.empty:
        return {"ticker": ticker.upper(), "date": day, "open": None, "close": None, "percent_change": None}

    row = hist.iloc[0]
    open_price = round(row["Open"], 4)
    close_price = round(row["Close"], 4)
    return {
        "ticker": ticker.upper(),
        "date": day,
        "open": open_price,
        "close": close_price,
        "percent_change": round((close_price - open_price) / open_price * 100, 2),
    }
