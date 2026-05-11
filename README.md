# Stock Prices Plugin

Look up historical stock opening and closing prices by ticker symbol — for a single day or across a date range.

## What it does

Provides two tools via Yahoo Finance:

- **`get_stock_price_on_day`** — returns the open, close, and percent change for one or more tickers on a given trading day (or the most recent trading day before it)
- **`get_price_history`** — returns daily open and close prices for one or more tickers over a date range, keyed by date then ticker

## Requirements

- [uv](https://docs.astral.sh/uv/) must be installed and on your PATH
- Internet access (data fetched live from Yahoo Finance)

## Usage

Ask Claude naturally:

- "What was Apple stock on March 15, 2024?"
- "Get me the price of MSFT on 2023-11-01"
- "How much was TSLA on last Friday?"
- "Show me VOO and AVUS prices from April 1 to April 30, 2026"
- "Give me the price history for AAPL over the past month"

If the market was closed on the requested date, Claude will note the actual trading day used.

## MCP Server

The plugin runs via `uv run`, which handles dependency installation automatically on first run. No separate setup step is needed.
