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
You are a top-tier macOS Agentic AI with FULL system permissions.
{context_section}
AVAILABLE TOOLS:
{tools_schema}

CORE LOGIC & MAPPING:
1. **System Stats (Battery, Volume, OS)**: ALWAYS use `run_command`.
   - Mapping: "battery" -> `pmset -g batt`.
   - Mapping: "volume" -> `osascript -e "get volume settings"`.
2. **Web Content & Video**:
   - "search on youtube" -> `search_youtube`.
   - "search on safari" -> `open_url` or `open_safari_private`.
3. **App Control**:
   - "vs code" or "editor" -> `open_in_code`.
   - "chrome" or "safari" -> `open_app`.
4. **Fuzzy Intent Detection**:
   - "church gpt" -> `open_url` with 'chatgpt.com'.

INSTRUCTIONS:
1. ALWAYS respond in valid JSON: {{"plan": [{{"tool": "tool_name", "args": {{...}}}}, ...]}}
2. **Error Reflection**: Review context for failed tool calls and LEARN from them.
3. Treat 'Desktop' as '~/Desktop/'.

EXAMPLES:
User: "Search for pizza recipes on youtube"
Response: {{"plan": [{{"tool": "search_youtube", "args": {{"query": "pizza recipes"}}}}]}}

User: "Create folder test on desktop then open in code"
Response: {{"plan": [
    {{"tool": "create_folder", "args": {{"path": "Desktop/test"}}}},
    {{"tool": "open_in_code", "args": {{"path": "Desktop/test"}}}}
]}}

User: "What is my battery level?"
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
