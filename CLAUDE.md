# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Claude Code plugin that provides a `get_stock_price_on_day` MCP tool backed by Yahoo Finance. It runs as either a stdio MCP server (for local plugin use) or an HTTP server (for deployment).

## Commands

**Run as HTTP server (local dev):**
```
uv run --with-requirements requirements.txt run_http.py
```
Defaults to port 8000; override with `PORT` env var.

**Run as stdio MCP server (manual test):**
```
uv run --with-requirements requirements.txt run_stdio.py
```

**Build the plugin archive:**
```
make
```
Produces `stock-prices.plugin` (a zip). `make clean` removes it.

## Architecture

All tool logic lives in [`server.py`](server.py). The two entry points — [`run_stdio.py`](run_stdio.py) and [`run_http.py`](run_http.py) — just import the `mcp` object from `server.py` and call `mcp.run()` with different transports.

The server uses [FastMCP](https://github.com/jlowin/fastmcp) and [yfinance](https://github.com/ranaroussi/yfinance). Dependencies are in [`requirements.txt`](requirements.txt) and managed by `uv` at runtime — no separate install step needed.

**Plugin packaging** ([`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), [`.mcp.json`](.mcp.json), [`Makefile`](Makefile)):
- `.mcp.json` tells Claude Code how to launch the server via `uv run`
- `.claude-plugin/plugin.json` provides plugin metadata (name, version, author)
- `make` zips the required source files into `stock-prices.plugin` for distribution

**Skill** ([`skills/stock-lookup/SKILL.md`](skills/stock-lookup/SKILL.md)):
Defines when and how Claude invokes the tool — handles ambiguous dates, null responses (market closed), multi-ticker queries, and response formatting.

## Key behavior in `get_stock_price_on_day`

The tool fetches a 5-day window ending the day after the target date and uses the last row, which is the most recent trading day on or before the requested date. The returned `date` field reflects the actual trading day used, which may differ from the requested date (e.g. a weekend request returns the preceding Friday). All price fields are `null` only when no data is found (e.g. invalid ticker). Percent change is relative to the previous trading day's close (not the open).
