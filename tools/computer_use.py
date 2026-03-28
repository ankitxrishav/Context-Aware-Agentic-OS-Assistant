import subprocess
import pytesseract
from PIL import Image
import os

# Set tesseract path for macOS Homebrew
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def read_screen_state(app_name: str = None) -> str:
    """
    Captures the screen or a specific app window and extracts text using OCR.
    If app_name is provided, it attempts to focus that app before capturing.
    """
    screenshot_path = "/tmp/screen_capture.png"
    
    try:
        # 1. Capture the screen
        # Use macOS screencapture tool
        # -x: silent, -m: main monitor
        cmd = ["screencapture", "-x", screenshot_path]
        subprocess.run(cmd, check=True)
        
        # 2. Perform OCR
        if not os.path.exists(screenshot_path):
            return "Error: Failed to capture screenshot."
            
        text = pytesseract.image_to_string(Image.open(screenshot_path))
        
        # Clean up
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
        if not text.strip():
            return "Screen is empty or no text could be recognized."
            
        # Return a summarized version to stay within LLM context tokens if needed
        return f"--- [RECOGNIZED SCREEN TEXT] ---\n{text[:2000]}\n--- [END TEXT] ---"
        
    except Exception as e:
        return f"Error during OCR/Screen Capture: {str(e)}"

computer_tools_schema = [
    {
        "name": "read_screen_state",
        "description": "Captures the current screen content and converts it to text using OCR. Useful for reading Telegram messages, system alerts, or any non-web app content.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Optional: Name of the app to focus on before reading (e.g. 'Telegram')."}
            }
        }
    }
]
