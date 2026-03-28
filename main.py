from core.agent import Agent
from core.executor import Executor
from core.memory import MemoryManager
from core.voice import VoiceListener
from core.notifier import send_notification
from dotenv import load_dotenv

# Load environment variables (optional, for later phases)
load_dotenv()

def main():
    print("""
==========================================
 🧭 AGENTIC AI - PERSISTENT MACOS AGENT
==========================================
(Type 'exit' or 'quit' to stop)
(Type 'voice' to start listening)
""")
    
    # Initialize Agent and Executor
    memory_manager = MemoryManager()
    agent = Agent(model="gemma3:1b", memory=memory_manager)
    executor = Executor()

    # Voice Callback
    def voice_callback(text):
        print(f"\n[Voice Command]: {text}")
        process_input(text)

    listener = VoiceListener(voice_callback)

    def process_input(user_input):
        print("-- Thinking...")
        response = agent.get_action(user_input)
        
        if not response:
            print("Agent: I'm not sure how to respond or I failed to generate a valid response.")
            return

        # 1. Handle Conversational Reply
        reply = response.get("reply")
        if reply:
            print(f"\nAssistant: {reply}")

        # 2. Handle Plan Execution
        steps = response.get("plan", [])
        if steps:
            print(f"-- Agent generated a plan with {len(steps)} step(s).")
            result = executor.execute_plan(response)
            
            # --- START ReAct LOOP (Summary Pass) ---
            # If the tool returned something useful, let the AI summarize it.
            if result and "Step 1" in result:
                print("-- Perfecting the answer...")
                summary_response = agent.get_action(user_input, observation=result)
                final_reply = summary_response.get("reply", "Action complete.")
                print(f"\nAssistant (Final): {final_reply}")
                reply = f"{reply} | Final: {final_reply}"
            else:
                print("\n" + result)
        else:
            result = "No actions needed."

        # Store interaction in memory
        memory_text = f"User said: {user_input} | Agent replied: {reply} | Result: {result}"
        memory_manager.add_memory(memory_text, metadata={"type": "interaction"})

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input or user_input.lower() in ["exit", "quit"]:
                if user_input: print("Exiting Agentic AI. Goodbye!")
                if listener.is_listening: listener.stop()
                break

            if user_input.lower() == "voice":
                listener.start()
                continue
            
            if user_input.lower() == "stop voice":
                listener.stop()
                continue

            process_input(user_input)

        except KeyboardInterrupt:
            print("\nExiting Agentic AI. Goodbye!")
            if listener.is_listening: listener.stop()
            break
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
