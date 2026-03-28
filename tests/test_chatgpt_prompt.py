import sys
import os
sys.path.append(os.getcwd())
from tools.app_tools import search_chatgpt
from core.agent import Agent

agent = Agent()
prompt = "open church gpt and search for what is logic gate"
print(f"--- Prompt: {prompt} ---")
action = agent.get_action(prompt)
print(f"Agent Plan: {action}")

# Manually test the tool if it matches
if action and "plan" in action:
    for step in action["plan"]:
        if step["tool"] == "search_chatgpt":
            print(f"Executing search_chatgpt with args: {step['args']}")
            result = search_chatgpt(**step["args"])
            print(f"Result: {result}")
