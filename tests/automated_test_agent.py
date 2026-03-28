import os
from core.agent import Agent
from core.executor import Executor

def test_agent_loop():
    print("\n--- Testing Agent-Executor Loop ---")
    agent = Agent(model="gemma3:1b")
    executor = Executor()

    test_inputs = [
        "open safari",
        "create a folder named 'agent_test' on the desktop",
        "list files in current directory"
    ]

    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        print("-- Thinking...")
        action = agent.get_action(user_input)
        
        if action:
            print(f"-- Agent decided: {action.get('tool')}")
            result = executor.execute_action(action)
            print(f"Agent: {result}")
        else:
            print("Agent: No action decided.")

    # Cleanup
    if os.path.exists("/Users/ankitkumar/Desktop/agent_test"):
        os.rmdir("/Users/ankitkumar/Desktop/agent_test")
        print("\nCleaned up 'agent_test' folder.")

if __name__ == "__main__":
    test_agent_loop()
