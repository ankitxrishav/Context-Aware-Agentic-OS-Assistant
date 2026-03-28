import os
from core.agent import Agent
from core.memory import MemoryManager
from core.executor import Executor

def run_test(prompt):
    print(f"\n--- Testing Prompt: '{prompt}' ---")
    memory_manager = MemoryManager()
    agent = Agent(model="gemma3:1b", memory=memory_manager)
    executor = Executor()
    
    print("-" * 30)
    print("Agent Thinking...")
    plan = agent.get_action(prompt)
    
    if not plan:
        print("FAILED: Agent returned no plan.")
        return
    
    print("Action Plan:")
    for i, step in enumerate(plan.get("plan", [])):
        print(f"  Step {i+1}: {step}")
        
    print("-" * 30)
    print("Executing Action...")
    result = executor.execute_plan(plan)
    print(f"Result: {result}")
    print("-" * 30)

if __name__ == "__main__":
    test_prompts = [
        "Create a folder on Desktop named 'SanityTest' and open it in VS Code",
        "Open church gpt and search for pizza recipes in Safari",
        "Finding tutorial for Next.js on YouTube",
        "What is the battery level?",
        "List files in the current folder"
    ]
    
    for prompt in test_prompts:
        run_test(prompt)
