import subprocess
import os
from typing import Dict, Any, List
from .file_tools import _resolve_path

def open_app(app_name: str) -> str:
    """Opens a macOS application by its name."""
    try:
        subprocess.run(["open", "-a", app_name], check=True)
        return f"Successfully opened application: {app_name}"
    except subprocess.CalledProcessError as e:
        return f"Error opening application: {str(e)}"
    except Exception as e:
        return f"Unexpected error while opening app: {str(e)}"

def open_url(url: str) -> str:
    """Opens a URL in the default browser."""
    try:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        subprocess.run(["open", url], check=True)
        return f"Successfully opened URL: {url}"
    except subprocess.CalledProcessError as e:
        return f"Error opening URL: {str(e)}"
    except Exception as e:
        return f"Unexpected error while opening URL: {str(e)}"

def open_in_code(path: str) -> str:
    """Opens a file or folder in Visual Studio Code."""
    try:
        # Resolve path so 'Desktop/test' expands correctly
        resolved_path = _resolve_path(path)
        
        # First ensure the path exists before trying to open it
        if not os.path.exists(resolved_path):
            return f"Error: Path '{path}' ('{resolved_path}') does not exist. Please create it first."
            
        subprocess.run(["open", "-a", "Visual Studio Code", resolved_path], check=True)
        return f"Successfully opened in Visual Studio Code: {path}"
    except subprocess.CalledProcessError as e:
        return f"Error opening path in VS Code: {str(e)}"
    except Exception as e:
        return f"Unexpected error while opening VS Code: {str(e)}"

def open_safari_private(url: str = "google.com") -> str:
    """Opens Safari in Private/Incognito mode to a specific URL."""
    try:
        # Aggressive typo correction
        url = url.replace("chat.gpt.com", "chatgpt.com").replace("chat.openai.com", "chatgpt.com")
        
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        # Use -n for new instance, -a for Safari, --args --private for private mode
        subprocess.run(["open", "-na", "Safari", "--args", "--private", url], check=True)
        return f"Successfully opened Safari Private to: {url}"
    except Exception as e:
        return f"Error opening Safari Private: {str(e)}"

def search_youtube(query: str) -> str:
    """Searches YouTube for a specific query."""
    try:
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        subprocess.run(["open", url], check=True)
        return f"Successfully searched YouTube for: {query}"
    except Exception as e:
        return f"Error searching YouTube: {str(e)}"

def search_web(query: str) -> str:
    """Perform a general web search using Google in the default browser."""
    try:
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        subprocess.run(["open", url], check=True)
        return f"Successfully searched the web for: {query}"
    except Exception as e:
        return f"Error searching the web: {str(e)}"

def search_chatgpt(prompt: str) -> str:
    """Opens ChatGPT in Safari and automatically enters/submits the prompt."""
    try:
        url = "https://chatgpt.com/"
        subprocess.run(["open", "-a", "Safari", url], check=True)
        
        # Use AppleScript to type and press return
        applescript = f'''
        delay 3
        tell application "System Events"
            tell process "Safari"
                set frontmost to true
                keystroke "{prompt}"
                delay 0.5
                key code 36 -- Return key
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript], check=True)
        return f"Successfully opened ChatGPT and submitted prompt: {prompt}"
    except Exception as e:
        return f"Error using ChatGPT automation: {str(e)}"

# Schema for the tool registry
app_tools_schema = [
    {
        "name": "open_app",
        "description": "Opens a native macOS application by its name.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "The name of the application, e.g., 'Safari' or 'Chrome'."}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "open_url",
        "description": "Opens a web page in the default web browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to open, e.g., 'youtube.com'."}
            },
            "required": ["url"]
        }
    },
    {
        "name": "open_in_code",
        "description": "Opens a specific folder or file in Visual Studio Code.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The absolute or relative path to the folder/file."}
            },
            "required": ["path"]
        }
    },
    {
        "name": "open_safari_private",
        "description": "Opens Safari in a new Private/Incognito window at a specific URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to open (defaults to google.com)."}
            }
        }
    },
    {
        "name": "search_youtube",
        "description": "Searches YouTube for a query and opens the results in the default browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search term, e.g., 'best hindi songs'."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_chatgpt",
        "description": "Opens ChatGPT in Safari and automatically types/submits a search prompt.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The question or query to ask ChatGPT."}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "search_web",
        "description": "Performs a generic web search (e.g., Google search) for a query and opens it in the default browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search term to look up, e.g., 'time in indonesia'."}
            },
            "required": ["query"]
        }
    }
]
