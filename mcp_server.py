from mcp.server.fastmcp import FastMCP
from tools.file_tools import create_folder, delete_folder, list_files
from tools.app_tools import open_app, open_url, open_in_code, open_safari_private, search_youtube
from tools.terminal_tools import run_command
import os

# Initialize FastMCP server
mcp = FastMCP("macOS-Agent")

@mcp.tool()
def make_directory(path: str) -> str:
    """Create a new folder at the specified path. Supports 'Desktop' and '~' aliases."""
    return create_folder(path)

@mcp.tool()
def remove_directory(path: str) -> str:
    """Delete a folder and its contents. WARNING: Dangerous action."""
    return delete_folder(path)

@mcp.tool()
def list_directory_contents(path: str) -> str:
    """List files and folders in a directory."""
    return list_files(path)

@mcp.tool()
def launch_application(name: str) -> str:
    """Open a macOS application by name."""
    return open_app(name)

@mcp.tool()
def navigate_to_url(url: str) -> str:
    """Open a URL in the default web browser."""
    return open_url(url)

@mcp.tool()
def launch_safari_private(url: str = "") -> str:
    """Open Safari in Private (Incognito) mode, optionally at a specific URL."""
    return open_safari_private(url)

@mcp.tool()
def youtube_search(query: str) -> str:
    """Search for a specific query directly on YouTube."""
    return search_youtube(query)

@mcp.tool()
def open_path_in_vscode(path: str) -> str:
    """Open a file or folder in Visual Studio Code."""
    return open_in_code(path)

@mcp.tool()
def execute_shell_command(cmd: str) -> str:
    """Execute a shell command. WARNING: Highly dangerous action."""
    return run_command(cmd)

if __name__ == "__main__":
    mcp.run()
