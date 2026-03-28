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
You are a persistent AI agent with FULL ACCESS to the user's macOS system. Your goal is to help them manage their system using available tools.
{context_section}
AVAILABLE TOOLS:
{tools_schema}

COMMON MACOS COMMANDS (Reference):
- Battery: `pmset -g batt`
- Network Services: `networksetup -listallnetworkservices`
- Dark Mode Toggle: `osascript -e 'tell application "System Events" to tell appearance preferences to set dark mode to not dark mode'`
- List Applications: `ls /Applications`
- Volume Control: `osascript -e "set volume output volume 50"`

You can perform any OS-level task by using the 'run_command' tool. **IMPORTANT: Use 'run_command' for ANY system inquiry (battery, network, system settings, etc.) rather than 'list_files'.** Be confident and use the exact syntax from the reference if applicable.
"""
        # Rest of the prompt remains the same, I'll update it in a separate block or include it here
        prompt += """
INSTRUCTIONS:
1. Analyze the user's input and ANY provided "Retrieved Context".
2. **Error Reflection**: Review the 'Retrieved Context' for any "Error" results from previous turns. If a previous similar tool call failed (e.g., "Tool not found"), LEARN from that mistake. DO NOT repeat the same failed tool name.
3. **Strict Tool Policy**: You ONLY have the tools listed below. DO NOT invent new tools like "open_chatgpt" or "search_folder". If no specific tool matches, map the intent to `open_url` (for web) or `run_command` (for system).
4. **Fuzzy Intent Mapping**:
    - "chat gpt" / "church gpt" / "check gpt" -> Use `open_url` with 'chatgpt.com'.
    - "open site [X]" -> Use `open_url` with 'X.com'.
    - "create folder [X]" -> Use `create_folder`.
5. Break complex requests into a logical sequence (a "plan").
6. ONLY respond with a JSON object: {"plan": [{"tool": "tool_name", "args": {...}}, ...]}

Example:
User: "open church gpt"
Context: [User said "open chat gpt" | Result: Tool 'open_chatgpt' not found]
Response: {"plan": [{"tool": "open_url", "args": {"url": "chatgpt.com"}}]}

--- PRECISION GALLERY ---
User: "create folder hihi on desktop" -> {"plan": [{"tool": "create_folder", "args": {"path": "Desktop/hihi"}}]}
User: "open safari in incognito and go on youtube" -> {"plan": [{"tool": "open_safari_private", "args": {"url": "youtube.com"}}]}
User: "search for best hindi songs on youtube" -> {"plan": [{"tool": "search_youtube", "args": {"query": "best hindi songs"}}]}
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
