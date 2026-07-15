from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_call
from tools.registry import execute_tool


class Agent:
    
    def run(self, user_input):
        
        memory = load_memory()
        
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
            
        messages.extend(memory)
        
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        llm_response = chat(messages)
        
        tool_request = parse_tool_call(llm_response)
        
        if tool_request is None:
            
            memory.append({
                "role": "user",
                "content": user_input
            })
            
            memory.append({
                "role": "assistant",
                "content": llm_response
            })
            
            save_memory(memory)
            
            return llm_response
        
        print("Tool requested")
        
        tool_name = tool_request.get("tool")
        arguments = tool_request.copy()
        arguments.pop("tool", None)
                
        print(f"\nTool requested: {tool_name}")
        print(f"Arguments: {arguments}")
        
        tool_result = execute_tool(
            tool_name,
            arguments
        )
        
        print(f"\nTool result: {tool_result}")
        
        messages.append({
            "role": "assistant",
            "content": llm_response
        })
        
        messages.append({
            "role": "user",
            "content":
            f"""
            Tool Result: {tool_result}
            Using this result answer the user's original question:
            """     
        })
        
        final_response = chat(messages)
        
        memory.append({
            "role": "user",
            "content": user_input
        })
        
        memory.append({
            "role": "assistant",
            "content": final_response
        })
        
        save_memory(memory)
        
        return final_response
            


