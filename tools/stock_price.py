"""
stock_price.py

Tool for fetching the latest quote for a stock ticker using
Stooq's free, no-API-key CSV quote endpoint.
"""

try:
    import requests
except ImportError:
    requests = None

QUOTE_URL = "https://stooq.com/q/l/"


def _looks_like_bare_us_ticker(symbol: str) -> bool:
    return symbol.isalpha() and "." not in symbol


def execute(arguments: dict):
    if requests is None:
        return "Stock price error: requests library is not installed"

    symbol = arguments.get("symbol") or arguments.get("ticker")

    if not symbol:
        return "Stock price error: 'symbol' (ticker) is required"

    try:
        raw_symbol = str(symbol).strip().lower()
        query_symbol = f"{raw_symbol}.us" if _looks_like_bare_us_ticker(raw_symbol) else raw_symbol

        response = requests.get(
            QUOTE_URL,
            params={"s": query_symbol, "f": "sd2t2ohlcv", "h": "", "e": "csv"},
            timeout=10,
        )
        response.raise_for_status()

        lines = response.text.strip().splitlines()
        if len(lines) < 2:
            return f"Stock price error: no data returned for '{symbol}'"

        header = lines[0].split(",")
        values = lines[1].split(",")
        row = dict(zip(header, values))

        close_price = row.get("Close")
        if not close_price or close_price == "N/D":
            return f"Stock price error: ticker '{symbol}' not found or market data unavailable"

        return (
            f"{symbol.upper()}: {close_price} "
            f"(open: {row.get('Open')}, high: {row.get('High')}, "
            f"low: {row.get('Low')}, date: {row.get('Date')})"
        )

    except Exception as e:
        return f"Stock price error: {e}"