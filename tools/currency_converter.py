"""
currency_converter.py

Tool for converting an amount from one currency to another
using the free, no-API-key Frankfurter exchange rate API.
"""

try:
    import requests
except ImportError:
    requests = None

RATES_URL = "https://api.frankfurter.app/latest"


def execute(arguments: dict):
    if requests is None:
        return "Currency conversion error: requests library is not installed"

    amount = arguments.get("amount")
    from_currency = arguments.get("from_currency")
    to_currency = arguments.get("to_currency")

    if amount is None or not from_currency or not to_currency:
        return "Currency conversion error: 'amount', 'from_currency' and 'to_currency' are required"

    try:
        amount = float(amount)
        from_code = str(from_currency).strip().upper()
        to_code = str(to_currency).strip().upper()

        if from_code == to_code:
            return f"{amount} {from_code} = {amount} {to_code}"

        response = requests.get(
            RATES_URL,
            params={
                "amount": amount,
                "from": from_code,
                "to": to_code,
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})

        if to_code not in rates:
            return f"Currency conversion error: rate for '{to_code}' not found"

        converted = rates[to_code]

        return f"{amount} {from_code} = {round(converted, 4)} {to_code}"

    except Exception as e:
        return f"Currency conversion error: {e}"


if __name__ == "__main__":
    print("Currency converter tool\n")
    print(execute({"amount": 100, "from_currency": "USD", "to_currency": "INR"}))
