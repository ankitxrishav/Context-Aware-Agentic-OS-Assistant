import os
import time
from core.agent import Agent
from core.executor import Executor
from core.memory import MemoryManager
from core.notifier import send_notification
from dotenv import load_dotenv

load_dotenv()

COMMAND_FILE = "agent_command.txt"
RESULT_FILE = "agent_result.txt"

def main():
    print("Agentic AI: Daemon Mode Started. Monitoring for commands...")
    send_notification("Agentic AI", "Daemon is now active and monitoring in the background. 🧭")
    
    # Initialize Agent and Executor
    memory_manager = MemoryManager()
    agent = Agent(model="gemma3:1b", memory=memory_manager)
    executor = Executor()

    while True:
        if os.path.exists(COMMAND_FILE):
            try:
                with open(COMMAND_FILE, "r") as f:
                    user_input = f.read().strip()
                
                if user_input:
                    print(f"Daemon: Processing command -> {user_input}")
                    
                    # Generate plan
                    plan = agent.get_action(user_input)
                    if plan:
                        # Automate the "Y" for confirmation in daemon mode for SAFE tools
                        # Note: In a real daemon, you might need a separate UI for confirmation
                        result = executor.execute_plan(plan)
                        
                        # Write result and notify
                        with open(RESULT_FILE, "w") as f:
                            f.write(result)
                        
                        send_notification("Task Completed", f"Processed: {user_input[:40]}...")
                        
                        # Store in memory
                        steps = plan.get("plan", [])
                        memory_text = f"Daemon processed: {user_input} | Result: {result}"
                        memory_manager.add_memory(memory_text, metadata={"type": "daemon_interaction"})
                    else:
                        with open(RESULT_FILE, "w") as f:
                            f.write("Error: Failed to generate plan.")

                # Cleanup command file to avoid re-runs
                os.remove(COMMAND_FILE)

            except Exception as e:
                print(f"Daemon Error: {str(e)}")
                with open(RESULT_FILE, "w") as f:
                    f.write(f"Error: {str(e)}")
                if os.path.exists(COMMAND_FILE): os.remove(COMMAND_FILE)

        # Sleep to save CPU
        time.sleep(2)

if __name__ == "__main__":
    main()
