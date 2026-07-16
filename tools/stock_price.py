"""
stock_price.py

Tool for fetching the latest quote for a stock ticker using
Yahoo Finance's public chart endpoint. No API key required.

Yahoo uses market suffixes to disambiguate tickers across exchanges,
e.g.:
  - US markets:      "AAPL", "TSLA"      (no suffix)
  - NSE (India):      "TATASTEEL.NS", "RELIANCE.NS"
  - BSE (India):       "TATASTEEL.BO", "RELIANCE.BO"

Rather than require the caller to know the right suffix, this tool
tries the bare symbol first, then NSE, then BSE, and returns the
first one with real data.
"""

try:
    import requests
except ImportError:
    requests = None

CHART_URL_TEMPLATE = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

CANDIDATE_SUFFIXES = ["", ".NS", ".BO"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def _fetch_quote(query_symbol: str):
    response = requests.get(
        CHART_URL_TEMPLATE.format(symbol=query_symbol),
        params={"interval": "1d", "range": "5d"},
        headers=HEADERS,
        timeout=10,
    )

    if response.status_code != 200:
        return None

    data = response.json()
    result = data.get("chart", {}).get("result")

    if not result:
        return None

    meta = result[0].get("meta", {})
    price = meta.get("regularMarketPrice")

    if price is None:
        return None

    return {
        "symbol": meta.get("symbol"),
        "price": price,
        "previous_close": meta.get("previousClose") or meta.get("chartPreviousClose"),
        "currency": meta.get("currency"),
        "day_high": meta.get("regularMarketDayHigh"),
        "day_low": meta.get("regularMarketDayLow"),
    }


def execute(arguments: dict):
    if requests is None:
        return "Stock price error: requests library is not installed"

    symbol = arguments.get("symbol") or arguments.get("ticker")

    if not symbol:
        return "Stock price error: 'symbol' (ticker) is required"

    raw_symbol = str(symbol).strip().upper()

    suffixes_to_try = [""] if "." in raw_symbol else CANDIDATE_SUFFIXES

    try:
        for suffix in suffixes_to_try:
            query_symbol = f"{raw_symbol}{suffix}"
            try:
                quote = _fetch_quote(query_symbol)
            except Exception:
                quote = None

            if quote:
                change = None
                if quote["previous_close"]:
                    change = quote["price"] - quote["previous_close"]

                change_str = f", change: {change:+.2f}" if change is not None else ""

                return (
                    f"{quote['symbol']}: {quote['price']} {quote.get('currency') or ''} "
                    f"(day high: {quote.get('day_high')}, day low: {quote.get('day_low')}"
                    f"{change_str})"
                )

        return f"Stock price error: ticker '{symbol}' not found"

    except Exception as e:
        return f"Stock price error: {e}"


if __name__ == "__main__":
    print("Stock price tool\n")
    print(execute({"symbol": "AAPL"}))
    print(execute({"symbol": "TSLA"}))
    print(execute({"symbol": "TATASTEEL"}))
    print(execute({"symbol": "RELIANCE"}))