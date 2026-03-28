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
        plan = agent.get_action(user_input)
        
        if not plan:
            print("Agent: I'm not sure which tool to use or I failed to generate a valid plan.")
            return

        # Check if it's a list (multi-step) or single action
        steps = plan.get("plan", [])
        print(f"-- Agent generated a plan with {len(steps)} step(s).")
        
        result = executor.execute_plan(plan)
        print("\n" + result)

        # Store interaction in memory
        memory_text = f"User said: {user_input} | Result: {result}"
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
