import os
from tools.registry import registry

def test_file_tools():
    print("\n--- Testing File Tools ---")
    test_folder = "test_data"
    
    # Test create_folder
    print(registry.get_tool("create_folder")(test_folder))
    
    # Test list_files
    print(f"Files in current dir: {registry.get_tool('list_files')('.')}")
    
    # Test delete_folder
    print(registry.get_tool("delete_folder")(test_folder))

def test_app_tools():
    print("\n--- Testing App Tools ---")
    # Using 'Safari' and 'google.com' as basic macOS tests
    print(registry.get_tool("open_app")("Safari"))
    print(registry.get_tool("open_url")("google.com"))

def test_terminal_tools():
    print("\n--- Testing Terminal Tools ---")
    print(f"Current Date/Time: {registry.get_tool('run_command')('date')}")
    print(f"Python Version: {registry.get_tool('run_command')('python3 --version')}")

if __name__ == "__main__":
    test_file_tools()
    test_terminal_tools()
    # test_app_tools() # Commented out by default to avoid opening apps repeatedly, but ready for manual run
    
    print("\nRegistry tool names:", registry.list_tool_names())
