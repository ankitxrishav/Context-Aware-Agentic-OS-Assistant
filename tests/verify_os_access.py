import os
from core.agent import Agent
from core.executor import Executor
from core.memory import MemoryManager

def test_full_os_access():
    print("\n--- Testing Full OS Access & Real-Time Interaction ---")
    
    # Using a dedicated test memory DB
    test_db = "./test_os_access_db"
    mm = MemoryManager(db_path=test_db)
    agent = Agent(model="gemma3:1b", memory=mm)
    executor = Executor()

    test_inputs = [
        "What is my battery level?",
        "Show me my local network services",
        "Toggle Dark Mode"
    ]

    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        print("-- Thinking with full access...")
        plan = agent.get_action(user_input)
        
        if plan and "plan" in plan:
            print(f"-- Agent generated a plan with {len(plan['plan'])} step(s).")
            result = executor.execute_plan(plan)
            print("\n" + result)
        else:
            print("Agent failed to generate a plan for OS-level task.")

if __name__ == "__main__":
    test_full_os_access()
