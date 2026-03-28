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
1. **System Stats (Battery, Volume, OS)**: ALWAYS use `run_command` via PowerShell.
   - Mapping: "battery" -> `WMIC Path Win32_Battery Get EstimatedChargeRemaining`.
   - Mapping: "volume" -> `(Get-AudioDevice).Volume`.
2. **ChatGPT & Research**:
   - If user asks to search/query on ChatGPT, ALWAYS use `search_chatgpt`.
   - **CRITICAL**: Normalize `chat.gpt.com` or `church gpt` to `chatgpt.com`.
3. **Web & Video**:
   - "search on youtube" -> `search_youtube`.
4. **App Control**:
   - "vs code" -> `open_in_code`.

AUTONOMOUS WINDOWS MISSION:
You are not restricted to these mappings. Use your LLM context to understand the user's DEEP intent. If they say "make things happen in real time", combine multiple tools. If a tool fails, reflect on the error in context and try a different approach (e.g., if one URL fails, search for the correct one).

INSTRUCTIONS:
1. RESPONSE FORMAT: ONLY JSON {{"plan": [{{"tool": "name", "args": {{...}}}}]}}
2. **Submission**: When searching ChatGPT, provide the full query in `prompt`.

EXAMPLES:
User: "What's my battery?"
Response: {{"plan": [{{"tool": "run_command", "args": {{"cmd": "WMIC Path Win32_Battery Get EstimatedChargeRemaining"}}}}]}}

User: "open church gpt and search for what is logic gate"
Response: {{"plan": [{{"tool": "search_chatgpt", "args": {{"prompt": "what is logic gate"}}}}]}}
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
