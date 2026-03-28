import os
import shutil
from pathlib import Path
from typing import List, Dict, Any

def _resolve_path(path: str) -> str:
    """Helper to resolve ~/ and aliases like 'Desktop' to absolute paths."""
    # Handle 'Desktop' or 'desktop' at the start of the path
    if path.lower().startswith("desktop"):
        # Replace 'desktop' or 'Desktop' with the absolute path
        # If it's just 'desktop', result = ~/Desktop
        # If it's 'desktop/myfolder', result = ~/Desktop/myfolder
        suffix = path[7:].lstrip("/") # Remove 'desktop' or 'Desktop' and leading slash
        path = os.path.join(os.path.expanduser("~/Desktop"), suffix)
    
    # Expand ~ user shell alias
    return os.path.abspath(os.path.expanduser(path))

def create_folder(path: str) -> str:
    """Creates a new directory at the specified path."""
    try:
        abs_path = _resolve_path(path)
        os.makedirs(abs_path, exist_ok=True)
        return f"Successfully created folder: {abs_path}"
    except Exception as e:
        return f"Error creating folder: {str(e)}"

def delete_folder(path: str) -> str:
    """Deletes an existing directory."""
    try:
        abs_path = _resolve_path(path)
        if os.path.exists(abs_path):
            shutil.rmtree(abs_path)
            return f"Successfully deleted folder: {abs_path}"
        return f"Error: Folder '{abs_path}' does not exist."
    except Exception as e:
        return f"Error deleting folder: {str(e)}"

def list_files(path: str = ".") -> List[str]:
    """Lists entries in a directory."""
    try:
        abs_path = _resolve_path(path)
        if os.path.exists(abs_path):
            return os.listdir(abs_path)
        return [f"Error: Path does not exist: {abs_path}"]
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

# Schema for the tool registry
file_tools_schema = [
    {
        "name": "create_folder",
        "description": "Creates a new folder at the given path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The absolute or relative path to create."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "delete_folder",
        "description": "Deletes a folder and its contents recursively.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path to the folder to delete."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_files",
        "description": "Lists all items inside a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path to list contents from."}
            },
            "required": ["path"]
        }
    }
]
