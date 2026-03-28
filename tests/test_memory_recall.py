import os
import shutil
from core.agent import Agent
from core.executor import Executor

def test_memory_recall():
    print("\n--- Testing Memory System Recall ---")
    
    test_db = "./test_memory_db"
    
    # Reset memory for a clean test
    if os.path.exists(test_db):
        shutil.rmtree(test_db)
        print("Reset memory database for testing.")
    
    # Re-initialize memory manager with test path
    from core.memory import MemoryManager
    mm = MemoryManager(db_path=test_db)
    
    agent = Agent(model="gemma3:1b", memory=mm)
    executor = Executor()

    # 1. Store a fact
    print("\nStep 1: Storing a fact...")
    user_input_1 = "My favorite application is Safari."
    mm.add_memory(f"User preference: {user_input_1}", metadata={"type": "preference"})
    
    # 2. Store a path
    print("\nStep 2: Storing a path...")
    user_input_2 = "My project logs are in a folder named 'logs_dir' on the desktop."
    mm.add_memory(f"Project info: {user_input_2}", metadata={"type": "project"})

    # 3. Ask a question requiring recall
    print("\nStep 3: Testing recall...")
    user_input_3 = "Create my project logs folder and then open my favorite application."
    
    print(f"\nUser: {user_input_3}")
    print("-- Thinking with memory...")
    
    plan = agent.get_action(user_input_3)
    
    if plan and "plan" in plan:
        print(f"-- Agent generated a plan with {len(plan['plan'])} step(s) using memory context.")
        result = executor.execute_plan(plan)
        print("\n" + result)
    else:
        print("Agent failed to generate a plan with memory.")

    # Cleanup
    folder_path = "/Users/ankitkumar/Desktop/logs_dir"
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        print("\nCleaned up 'logs_dir' folder.")

if __name__ == "__main__":
    test_memory_recall()
