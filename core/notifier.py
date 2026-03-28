import subprocess

def send_notification(title: str, message: str, sound: bool = True):
    """Sends a native Windows popup notification using PowerShell."""
    try:
        # Use WScript.Shell Popup (native to Windows)
        # Type 64 = Information Icon
        ps_command = f'(New-Object -ComObject WScript.Shell).Popup("{message}", 0, "{title}", 64)'
        subprocess.run(["powershell", "-Command", ps_command], check=True)
    except Exception as e:
        # Silently fail or log if powershell fails
        print(f"Notifier: Error sending Windows notification: {str(e)}")

if __name__ == "__main__":
    # Test notification
    send_notification("Agentic AI", "Notification system is now active! 🧭")
