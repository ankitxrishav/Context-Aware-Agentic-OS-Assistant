import speech_recognition as sr
import threading
from core.notifier import send_notification

class VoiceListener:
    def __init__(self, callback):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.callback = callback
        self.is_listening = False
        self._stop_event = threading.Event()

    def _listen_loop(self):
        send_notification("Agentic AI", "Voice Control is now active. I am listening... 🎙️")
        print("\n[Voice Mode] Listening for input... (Say 'stop listening' or press Ctrl+C to exit)")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while not self._stop_event.is_set():
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio)
                    
                    # --- NOISE CLASSIFICATION ---
                    # 1. Length check: noise is often 1-2 words
                    words = text.lower().split()
                    if len(words) < 2 and "stop" not in words:
                        continue
                        
                    # 2. Actionable check: does it sound like a command?
                    action_keywords = ["open", "create", "search", "what", "find", "run", "delete", "code", "chat", "gpt"]
                    is_command = any(word in action_keywords for word in words)
                    
                    if not is_command:
                        print(f" [Voice] Ignoring noise: {text}")
                        continue
                        
                    print(f"\n[Voice] Classified Command: {text}")
                    
                    if "stop listening" in text.lower():
                        print("[Voice] Stopping voice listener...")
                        send_notification("Agentic AI", "Voice Control deactivated.")
                        self.stop()
                        break
                        
                    # Send text to callback (main loop)
                    self.callback(text)
                    
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    # Could not understand audio
                    continue
                except sr.RequestError as e:
                    print(f"[Voice] Request error: {str(e)}")
                    break
                except Exception as e:
                    print(f"[Voice] Error: {str(e)}")
                    break

    def start(self):
        """Starts the listener in a background thread."""
        self.is_listening = True
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stops the listener."""
        self.is_listening = False
        self._stop_event.set()

# For quick testing
if __name__ == "__main__":
    def dummy_callback(text):
        print(f"Callback received: {text}")
    
    listener = VoiceListener(dummy_callback)
    listener.start()
    try:
        while True: pass
    except KeyboardInterrupt:
        listener.stop()
