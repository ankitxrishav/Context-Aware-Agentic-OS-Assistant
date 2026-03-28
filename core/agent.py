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

    def _build_system_prompt(self, context: str = "") -> str:
        tools_schema = json.dumps(registry.get_all_schemas(), indent=2)
        
        context_section = ""
        if context:
            context_section = f"\nRELEVANT MEMORY/CONTEXT:\n{context}\n"

        prompt = f"""
You are an advanced, multi-modal macOS Intelligence Agent with FULL OS ACCESS.
{context_section}
AVAILABLE TOOLS:
{tools_schema}

CORE LOGIC & MAPPING:
1. **System Stats (Battery, Volume, OS)**: ALWAYS use `run_command`.
   - Mapping: "battery" -> `pmset -g batt`.
   - Mapping: "volume" -> `osascript -e "get volume settings"`.
2. **ChatGPT & Research**:
   - If user asks to search/query/open GPT, ALWAYS use `search_chatgpt`.
   - The argument MUST be exactly `{{"prompt": "your search query"}}`. NEVER use `url`.
3. **Multi-Step Chains (CRITICAL)**:
   - Break complex commands (e.g., "create X and open it") into MULTIPLE steps in the 'plan' array.
   - **Path Consistency**: Use the SAME path for creation and subsequent actions (e.g., folder 'high' -> `open_in_code` 'Desktop/high').
4. **App Mapping**:
   - "vs code" -> `open_in_code`.

INSTRUCTIONS:
- RESPONSE FORMAT: ONLY JSON {{"plan": [{{"tool": "name", "args": {{...}}}}, ...]}}
- Treat 'Desktop' as '~/Desktop/'.
- If a path is provided like 'high', use 'Desktop/high'.

EXAMPLES:
User: "create a folder on desktop named high and open it in vs code"
Response: {{"plan": [
    {{"tool": "create_folder", "args": {{"path": "Desktop/high"}}}},
    {{"tool": "open_in_code", "args": {{"path": "Desktop/high"}}}}
]}}

User: "open chat gpt and search for pizza"
Response: {{"plan": [{{"tool": "search_chatgpt", "args": {{"prompt": "pizza"}}}}]}}

User: "What's my battery?"
Response: {{"plan": [{{"tool": "run_command", "args": {{"cmd": "pmset -g batt"}}}}]}}
"""
        return prompt

    def get_action(self, user_input: str) -> Dict[str, Any]:
        """Sends user input to the LLM and parses the expected JSON response."""
        try:
            # Query memory for context
            context = ""
            if self.memory:
                context = self.memory.query_memory(user_input)
                if context:
                    print(f"-- Retrieved Context: {context[:100]}...")

            # Rebuild system prompt with context
            dynamic_prompt = self._build_system_prompt(context)

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
