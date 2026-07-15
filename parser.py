import json


def parse_tool_call(response: str):
    try:
        tool_request = json.loads(response)
        
        if not isinstance(tool_request, dict):
            return None
        
        if "tool" not in tool_request:
            return None
        
        if not isinstance(tool_request["tool"], str):
            return None
        return tool_request
    
    except json.JSONDecodeError:
        return None
    except Exception:
        return None


if __name__ == "__main__":
    test_response = '{"tool": "calculator", "input": "2 + 2"}'
    tool_request = parse_tool_call(test_response)
    if tool_request:
        print(f"Tool: {tool_request['tool']}, Input: {tool_request['input']}")
    else:
        print("No tool call found.")