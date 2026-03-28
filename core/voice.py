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
                    print(f"\n[Voice] Heard: {text}")
                    
                    if "stop listening" in text.lower():
                        print("[Voice] Stopping voice listener...")
                        send_notification("Agentic AI", "Voice Control deactivated.")
                        self.stop()
                        break
                    # Add Semantic Noise Filtering
                    print("\n🛡️ Authenticating Intent...")
                    try:
                        import ollama
                        client = ollama.Client()
                        prompt = f"""You are a Voice Command Filter.
Analyze this microphone transcription: "{text}"
Is it a deliberate COMMAND meant for an AI Assistant, or just background NOISE/chatter?
Reply with ONLY "COMMAND" or "NOISE"."""
                        res = client.chat(model="gemma3:1b", messages=[{"role": "user", "content": prompt}])
                        intent = res.message.content.strip().upper()
                        
                        if "NOISE" in intent:
                            print(f"[Voice Filter] Ignored background noise: '{text}'")
                            continue
                    except Exception as e:
                        print(f"[Voice Filter Error] {e} - Passing through.")
                        
                    print(f"[Voice] Executing Command: {text}")
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
