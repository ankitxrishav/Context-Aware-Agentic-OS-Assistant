import json
import ollama
from typing import Dict, Any, List, Optional
from tools.registry import registry
from .memory import MemoryManager

class Agent:
    def __init__(self, model: str = "gemma3:1b", memory: Optional[MemoryManager] = None):
        self.model = model
        self.client = ollama.Client()
        self.memory = memory
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self, context: str = "", observation: str = "") -> str:
        tools_schema = json.dumps(registry.get_all_schemas(), indent=2)
        
        context_section = ""
        if context:
            context_section = f"\nRELEVANT MEMORY/CONTEXT:\n{context}\n"
            
        observation_section = ""
        if observation:
            observation_section = f"\nTOOL OBSERVATION:\n{observation}\n"

        prompt = f"""
SYSTEM: You are a macOS AI Assistant. You MUST respond in this JSON format: {{"reply": "text", "plan": []}}.

{context_section}
{observation_section}

TOOLS:
{tools_schema}

EXAMPLES:
User: "how are you?"
Response: {{"reply": "I am great! How can I help?", "plan": []}}

User: "open youtube"
Response: {{"reply": "Opening YouTube...", "plan": [{{"tool": "open_url", "args": {{"url": "youtube.com"}}}} ]}}

User: "check telegram unread" (Initial)
Response: {{"reply": "Reading Telegram screen...", "plan": [{{"tool": "open_app", "args": {{"app_name": "Telegram"}}}}, {{"tool": "read_screen_state", "args": {{"app_name": "Telegram"}}}} ]}}

User: "check telegram unread" (With Observation: "UPSC 45 unread")
Response: {{"reply": "You have 45 unread messages in the UPSC group.", "plan": []}}

User: "What's my battery?"
Response: {{"reply": "Checking battery...", "plan": [{{"tool": "run_command", "args": {{"cmd": "pmset -g batt"}}}} ]}}
"""
        return prompt

    def get_action(self, user_input: str, observation: str = "") -> Dict[str, Any]:
        """Sends user input to the LLM and parses the expected JSON response."""
        try:
            # Query memory for context
            context = ""
            if self.memory and not observation:
                context = self.memory.query_memory(user_input)
                if context:
                    print(f"-- Retrieved Context: {context[:100]}...")

            # Rebuild system prompt with context
            dynamic_prompt = self._build_system_prompt(context, observation)

            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": dynamic_prompt},
                    {"role": "user", "content": user_input}
                ],
                format="json"
            )
            
            content = response.message.content.strip()
            if not content:
                print("Agent: No response from LLM.")
                return {}

            return json.loads(content)
        except json.JSONDecodeError:
            print(f"Agent: Error decoding JSON response: {content}")
            return {}
        except Exception as e:
            print(f"Agent: Unexpected error: {str(e)}")
            return {}
