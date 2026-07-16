"""
stock_price.py

Tool for fetching the latest quote for a stock ticker using a public
Yahoo Finance quote endpoint.
"""

from datetime import datetime

try:
    import requests
except ImportError:
    requests = None

QUOTE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"


def _format_number(value):
    if value is None:
        return "N/A"
    return f"{float(value):.2f}"


def _fetch_quote(query_symbol: str):
    if requests is None:
        return None

    response = requests.get(
        f"{QUOTE_URL}{query_symbol}",
        params={"interval": "1d", "range": "1mo"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    response.raise_for_status()

    payload = response.json()
    result = payload.get("chart", {}).get("result", [])
    if not result:
        return None

    first_result = result[0]
    meta = first_result.get("meta", {})
    quote = first_result.get("indicators", {}).get("quote", [{}])[0]
    timestamps = first_result.get("timestamp", [])

    if not quote or not timestamps:
        return None

    latest_timestamp = timestamps[-1]
    close_price = quote.get("close", [None])[-1]
    open_price = quote.get("open", [None])[-1]
    high_price = quote.get("high", [None])[-1]
    low_price = quote.get("low", [None])[-1]

    if close_price is None:
        return None

    return {
        "Symbol": meta.get("symbol", query_symbol.upper()),
        "Close": _format_number(close_price),
        "Open": _format_number(open_price),
        "High": _format_number(high_price),
        "Low": _format_number(low_price),
        "Date": datetime.utcfromtimestamp(latest_timestamp).strftime("%Y-%m-%d"),
    }


def execute(arguments: dict):
    if requests is None:
        return "Stock price error: requests library is not installed"

    symbol = arguments.get("symbol") or arguments.get("ticker")

    if not symbol:
        return "Stock price error: 'symbol' (ticker) is required"

    raw_symbol = str(symbol).strip()
    if not raw_symbol:
        return "Stock price error: 'symbol' (ticker) is required"

    try:
        row = _fetch_quote(raw_symbol)
        if row:
            return (
                f"{row.get('Symbol')}: {row.get('Close')} "
                f"(open: {row.get('Open')}, high: {row.get('High')}, "
                f"low: {row.get('Low')}, date: {row.get('Date')})"
            )

        return (
            f"Stock price error: ticker '{symbol}' not found. "
            f"Try a well-known ticker such as AAPL or TSLA."
        )

    except Exception as e:
        return f"Stock price error: {e}"


if __name__ == "__main__":
    print("Stock price tool\n")
    print(execute({"symbol": "AAPL"}))
    print(execute({"symbol": "TSLA"}))
    print(execute({"symbol": "TATASTEEL"}))
