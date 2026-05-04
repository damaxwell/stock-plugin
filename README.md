# Stock Prices Plugin

Look up historical stock opening and closing prices by ticker symbol and date.

## What it does

Provides a `get_stock_price_on_day` tool (via Yahoo Finance) that returns the opening and closing price for any publicly traded stock on a given trading day.

## Requirements

- [uv](https://docs.astral.sh/uv/) must be installed and on your PATH
- Internet access (data fetched live from Yahoo Finance)

## Usage

Ask Claude naturally:

- "What was Apple stock on March 15, 2024?"
- "Get me the price of MSFT on 2023-11-01"
- "How much was TSLA on last Friday?"

If the market was closed on the requested date, Claude will say so and offer to check an adjacent trading day.

## MCP Server

The plugin runs `stock_mcp_server.py` via `uv run`, which handles dependency installation automatically on first run (`mcp`, `yfinance`). No separate setup step is needed.
