from core.agent import Agent
from core.executor import Executor
from core.memory import MemoryManager

def test_safety():
    print("\n--- Testing Safety Confirmation Loop ---")
    mm = MemoryManager(db_path="./test_safety_db")
    agent = Agent(model="gemma3:1b", memory=mm)
    executor = Executor()

    user_input = "What is my battery level?"
    print(f"\nUser: {user_input}")
    plan = agent.get_action(user_input)
    
    if plan and "plan" in plan:
        print(f"Agent wants to: {plan['plan']}")
        # Note: This will wait for (y/N) input in the test environment if dangerous
        result = executor.execute_plan(plan)
        print("\n" + result)

if __name__ == "__main__":
    test_safety()
