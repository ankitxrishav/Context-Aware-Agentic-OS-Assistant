from typing import Dict, Any, Callable, List
from .file_tools import create_folder, delete_folder, list_files, file_tools_schema
from .app_tools import open_app, open_url, open_in_code, open_safari_private, search_youtube, search_chatgpt, search_web, send_message, simulate_typing, app_tools_schema
from .terminal_tools import run_command, terminal_tools_schema

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []
        self._dangerous_tools = set()

        # Register tools
        self._register_file_tools()
        self._register_app_tools()
        self._register_terminal_tools()

    def _register_file_tools(self):
        self._tools["create_folder"] = create_folder
        self._tools["delete_folder"] = delete_folder
        self._tools["list_files"] = list_files
        self._schemas.extend(file_tools_schema)
        # Mark dangerous tools
        self._dangerous_tools.add("delete_folder")

    def _register_app_tools(self):
        self._tools["open_app"] = open_app
        self._tools["open_url"] = open_url
        self._tools["open_in_code"] = open_in_code
        self._tools["open_safari_private"] = open_safari_private
        self._tools["search_youtube"] = search_youtube
        self._tools["search_chatgpt"] = search_chatgpt
        self._tools["search_web"] = search_web
        self._tools["send_message"] = send_message
        self._tools["simulate_typing"] = simulate_typing
        self._schemas.extend(app_tools_schema)

    def _register_terminal_tools(self):
        self._tools["run_command"] = run_command
        self._schemas.extend(terminal_tools_schema)
        # Mark dangerous tools
        self._dangerous_tools.add("run_command")

    def get_tool(self, name: str) -> Callable:
        return self._tools.get(name)

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        return self._schemas

    def list_tool_names(self) -> List[str]:
        return list(self._tools.keys())

# Global registry instance
registry = ToolRegistry()
