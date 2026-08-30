import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text):
    print(f"ATLAS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=10)
            query = r.recognize_google(audio)
            print(f"You: {query}")
            return query
        except Exception:
            return ""
