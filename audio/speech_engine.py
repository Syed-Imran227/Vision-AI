# speech_engine.py

import speech_recognition as sr
import pyttsx3
import time

# TTS
_tts_engine = None
def speak(text: str):
    global _tts_engine
    
    print(f"[Nova]: {text}")
    
    try:
        # Re-initialize engine every time to avoid threading issues
        # This is less efficient but much more stable for threaded apps
        engine = pyttsx3.init()
        engine.setProperty("rate", 185)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        if engine._inLoop:
            engine.endLoop()
    except Exception as e:
        print(f"TTS Error: {e}")


# Continuous listening in a generator loop
def listen_continuous():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Nova always-listening…")
        from audio.sound_engine import play_listening_start
        play_listening_start()

    while True:
        with mic as source:
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=6)
                text = r.recognize_google(audio, language="en-IN")
                print(f"[You]: {text}")
                yield text.lower()
            except sr.UnknownValueError:
                continue
            except sr.WaitTimeoutError:
                continue
            except Exception:
                continue
