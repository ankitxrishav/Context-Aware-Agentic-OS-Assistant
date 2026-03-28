import os
from core.agent import Agent
from core.executor import Executor

def test_multi_step():
    print("\n--- Testing Multi-Step Planner ---")
    agent = Agent(model="gemma3:1b")
    executor = Executor()

    # Multi-step request
    user_input = "create a folder named 'multi_test' on the desktop and then open safari"
    
    print(f"\nUser: {user_input}")
    print("-- Thinking...")
    plan = agent.get_action(user_input)
    
    if plan and "plan" in plan:
        print(f"-- Agent generated a plan with {len(plan['plan'])} step(s).")
        result = executor.execute_plan(plan)
        print("\n" + result)
    else:
        print("Agent failed to generate a multi-step plan.")

    # Cleanup
    folder_path = "/Users/ankitkumar/Desktop/multi_test"
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        print("\nCleaned up 'multi_test' folder.")

if __name__ == "__main__":
    test_multi_step()
