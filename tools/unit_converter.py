"""
unit_converter.py

Tool for converting values between common units of
length, weight/mass, and temperature.
"""

LENGTH_TO_METERS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

WEIGHT_TO_GRAMS = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "lb": 453.59237,
    "oz": 28.349523125,
}


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Normalize to Celsius first
    if from_unit in ("c", "celsius"):
        celsius = value
    elif from_unit in ("f", "fahrenheit"):
        celsius = (value - 32) * 5 / 9
    elif from_unit in ("k", "kelvin"):
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit '{from_unit}'")

    if to_unit in ("c", "celsius"):
        return celsius
    elif to_unit in ("f", "fahrenheit"):
        return celsius * 9 / 5 + 32
    elif to_unit in ("k", "kelvin"):
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit '{to_unit}'")


def execute(arguments: dict):
    try:
        value = arguments.get("value")
        from_unit = arguments.get("from_unit")
        to_unit = arguments.get("to_unit")

        if value is None or not from_unit or not to_unit:
            return "Unit conversion error: 'value', 'from_unit' and 'to_unit' are required"

        value = float(value)
        from_key = str(from_unit).strip().lower()
        to_key = str(to_unit).strip().lower()

        if from_key in LENGTH_TO_METERS and to_key in LENGTH_TO_METERS:
            meters = value * LENGTH_TO_METERS[from_key]
            result = meters / LENGTH_TO_METERS[to_key]

        elif from_key in WEIGHT_TO_GRAMS and to_key in WEIGHT_TO_GRAMS:
            grams = value * WEIGHT_TO_GRAMS[from_key]
            result = grams / WEIGHT_TO_GRAMS[to_key]

        elif from_key in ("c", "celsius", "f", "fahrenheit", "k", "kelvin") and \
             to_key in ("c", "celsius", "f", "fahrenheit", "k", "kelvin"):
            result = _convert_temperature(value, from_key, to_key)

        else:
            return (
                f"Unit conversion error: cannot convert between "
                f"'{from_unit}' and '{to_unit}' (unsupported or mismatched unit types)"
            )

        return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

    except Exception as e:
        return f"Unit conversion error: {e}"


if __name__ == "__main__":
    print("Unit converter tool\n")
    print(execute({"value": 10, "from_unit": "km", "to_unit": "mi"}))
    print(execute({"value": 100, "from_unit": "f", "to_unit": "c"}))
    print(execute({"value": 5, "from_unit": "kg", "to_unit": "lb"}))
