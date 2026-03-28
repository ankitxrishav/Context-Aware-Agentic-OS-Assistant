import subprocess

def send_notification(title: str, message: str, sound: bool = True):
    """Sends a native macOS notification using AppleScript."""
    try:
        script = f'display notification "{message}" with title "{title}"'
        if sound:
            script += ' sound name "Glass"'
        
        subprocess.run(["osascript", "-e", script], check=True)
    except Exception as e:
        print(f"Notifier: Error sending notification: {str(e)}")

if __name__ == "__main__":
    # Test notification
    send_notification("Agentic AI", "Notification system is now active! 🧭")
