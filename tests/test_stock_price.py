import types

from tools import stock_price


class MockResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_fetch_quote_parses_yahoo_payload(monkeypatch):
    payload = {
        "chart": {
            "result": [
                {
                    "meta": {"symbol": "AAPL"},
                    "timestamp": [1711929600],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0],
                                "high": [110.0],
                                "low": [95.0],
                                "close": [105.0],
                            }
                        ]
                    },
                }
            ],
            "error": None,
        }
    }

    monkeypatch.setattr(stock_price.requests, "get", lambda *args, **kwargs: MockResponse(payload))

    quote = stock_price._fetch_quote("AAPL")

    assert quote is not None
    assert quote["Symbol"] == "AAPL"
    assert quote["Close"] == "105.00"
    assert quote["Open"] == "100.00"
    assert quote["High"] == "110.00"
    assert quote["Low"] == "95.00"
    assert quote["Date"] == "2024-04-01"
