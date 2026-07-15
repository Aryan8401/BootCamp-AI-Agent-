import os
import sys

if __package__ is None and __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))

try:
    from calculator import execute as calculator
    from time_tool import execute as time_tool
    from weather import execute as weather
    from unit_converter import execute as unit_converter
    from currency_converter import execute as currency_converter
except ImportError:
    from tools.calculator import execute as calculator
    from tools.time_tool import execute as time_tool
    from tools.weather import execute as weather
    from tools.unit_converter import execute as unit_converter
    from tools.currency_converter import execute as currency_converter

TOOLS = {
    "calculator": calculator,
    "time": time_tool,
    "weather": weather,
    "unit_converter": unit_converter,
    "currency_converter": currency_converter,
}


def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)
    
    if tool is None:
        return f"Unknown tool: {tool_name}"
    
    return tool(arguments)


def list_tools():
    return list(TOOLS.keys())

if __name__ == "__main__":
    print("Registered tools\n")
    print(
        execute_tool(
            "calculator",
            {
                "expression": "25*18"
            }
        )
    )
    print("\n")
    
    print(
        execute_tool(
            "time",
            {}
        )       
    )
    
    print("\n")
    
    print(
        execute_tool(
            "weather",
            {
                "city": "New York"
            }
        )
    )

    print("\n")

    print(
        execute_tool(
            "unit_converter",
            {
                "value": 10,
                "from_unit": "km",
                "to_unit": "mi"
            }
        )
    )

    print("\n")

    print(
        execute_tool(
            "currency_converter",
            {
                "amount": 100,
                "from_currency": "USD",
                "to_currency": "INR"
            }
        )
    )