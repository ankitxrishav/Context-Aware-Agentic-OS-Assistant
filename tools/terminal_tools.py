import subprocess
from typing import Dict, Any, List

def run_command(cmd: str) -> str:
    """Runs a shell command and returns output or error message."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            return output if output else "Command executed successfully with no output."
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error while running command: {str(e)}"

# Schema for the tool registry
terminal_tools_schema = [
    {
        "name": "run_command",
        "description": "Executes any shell command in the terminal. Use this for OS-level tasks like checking battery status, network info, system config, or running AppleScript (osascript).",
        "parameters": {
            "type": "object",
            "properties": {
                "cmd": {"type": "string", "description": "The exact shell command to execute."}
            },
            "required": ["cmd"]
        }
    }
]
