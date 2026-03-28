import sys
import os
import json
sys.path.append(os.getcwd())
try:
    from core.agent import Agent
    agent = Agent()
    test_prompts = [
        "open chat GPT and search how are you",
        "create a folder on desktop named high and open it in vs code"
    ]
    for prompt in test_prompts:
        print(f"\n--- Testing Prompt: '{prompt}' ---")
        action = agent.get_action(prompt)
        print(f"Action Plan: {json.dumps(action, indent=2)}")
except Exception as e:
    print(f"Error during test: {e}")
