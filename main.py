# main.py
import os
import time
from datetime import datetime
import speech_recognition as sr
import win32com.client as wincl
from openai import OpenAI
from dotenv import load_dotenv

from core.memory import (
    init_database,
    load_user_memory,
    update_user_memory,
    save_conversation,
    add_reminder,
    get_reminders,
)

# ====== SETUP ======
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

init_database()
user_data = load_user_memory()
user_name = user_data.get("name", "Mac")

# ====== TTS (Windows SAPI) ======
speaker = wincl.Dispatch("SAPI.SpVoice")

def speak(text: str):
    # small delay helps avoid overlap with mic stream on some systems
    time.sleep(0.2)
    speaker.Speak(text)

# ====== MIC ======
recognizer = sr.Recognizer()

# Set a specific device index if needed:
# from speech_recognition import Microphone
# for i, n in enumerate(Microphone.list_microphone_names()):
#     print(i, n)
# microphone = sr.Microphone(device_index=<YOUR_INDEX>)
microphone = sr.Microphone()

# ====== SHORT-TERM CONTEXT MEMORY ======
conversation_history = []  # list of {"user": str, "assistant": str}
MAX_MEMORY = 5             # keep last N exchanges in RAM

def remember_exchange(user_text: str, assistant_text: str):
    conversation_history.append({"user": user_text, "assistant": assistant_text})
    # cap memory
    if len(conversation_history) > MAX_MEMORY:
        conversation_history.pop(0)

# ====== HELPERS ======
def now_time_str():
    return datetime.now().strftime("%I:%M %p").lstrip("0")

def today_date_str():
    return datetime.now().strftime("%A, %B %d, %Y")

def build_messages(current_user_text: str):
    sys = {
        "role": "system",
        "content": (
            "You are A.T.L.A.S., a friendly, adaptive AI assistant. "
            "Speak naturally and concisely. You have short-term context memory with recent exchanges."
        )
    }
    msgs = [sys]
    # inject short-term memory
    for turn in conversation_history:
        msgs.append({"role": "user", "content": turn["user"]})
        msgs.append({"role": "assistant", "content": turn["assistant"]})
    # current prompt
    msgs.append({"role": "user", "content": current_user_text})
    return msgs

def listen():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("\n🎧 Listening (standby)...")
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            query = recognizer.recognize_google(audio)
            print(f"{user_name}: {query}")
            return query.lower().strip()
        except sr.WaitTimeoutError:
            print("No voice detected — restarting listener.")
            return None
        except sr.UnknownValueError:
            print("Couldn't understand that — try again.")
            return None
        except sr.RequestError:
            speak("Microphone connection issue detected.")
            return None
        except KeyboardInterrupt:
            speak("Manual shutdown detected. Goodbye, Mac.")
            raise SystemExit

# ====== GREETING ======
time.sleep(0.8)
speak(f"Initializing Adaptive Terminal for Logical Analysis and Simulation. ATLAS ready. Welcome {user_name}.")

# ====== MAIN LOOP ======
while True:
    command = listen()
    if not command:
        continue

    # Wake words
    if any(w in command for w in ["hey atlas", "ok atlas", "yo atlas", "atlas"]):
        speak("Yes, Mac?")
        continue

    # Exit
    if command in ["exit", "quit", "stop atlas", "goodbye"]:
        speak("Shutting down. Goodbye, Mac.")
        break

    # ====== SYSTEM AWARENESS (no API cost) ======
    if "time" in command and any(k in command for k in ["what", "tell", "current"]):
        reply = f"It's {now_time_str()}, {user_name}."
        speak(reply)
        remember_exchange(command, reply)
        save_conversation(user_name, command, reply)
        user_data["last_seen"] = datetime.now().isoformat(timespec="seconds")
        update_user_memory(user_data)
        continue

    if any(k in command for k in ["date", "day"]) and any(t in command for t in ["what", "today", "current"]):
        reply = f"Today is {today_date_str()}."
        speak(reply)
        remember_exchange(command, reply)
        save_conversation(user_name, command, reply)
        user_data["last_seen"] = datetime.now().isoformat(timespec="seconds")
        update_user_memory(user_data)
        continue

    # Reminders (simple natural capture)
    # e.g., "remind me to drink water", "add reminder to call mom"
    if "remind me" in command or ("add" in command and "reminder" in command):
        text = command
        # naive extraction
        if "remind me to" in command:
            text = command.split("remind me to", 1)[1].strip()
        elif "add reminder" in command:
            text = command.split("add reminder", 1)[1].strip(" to").strip()
        if text:
            add_reminder(text)
            reply = f"Saved a reminder to {text}."
        else:
            reply = "I can save that. What should I remind you about?"
        speak(reply)
        remember_exchange(command, reply)
        save_conversation(user_name, command, reply)
        user_data["last_seen"] = datetime.now().isoformat(timespec="seconds")
        update_user_memory(user_data)
        continue

    if "list reminders" in command or "show reminders" in command:
        items = get_reminders()
        if items:
            reply = "Your reminders are: " + "; ".join(items) + "."
        else:
            reply = "You have no saved reminders yet."
        speak(reply)
        remember_exchange(command, reply)
        save_conversation(user_name, command, reply)
        user_data["last_seen"] = datetime.now().isoformat(timespec="seconds")
        update_user_memory(user_data)
        continue

    # ====== EMOTION / TONE ADAPTATION (rule-based) ======
    tone = "neutral"
    if any(k in command for k in ["tired", "exhausted", "sleepy", "drained"]):
        tone = "care"
    elif any(k in command for k in ["happy", "great", "awesome", "excited"]):
        tone = "upbeat"
    elif any(k in command for k in ["sad", "down", "upset"]):
        tone = "support"

    preface = {
        "care":   "You sound a bit tired. Keep it light and encouraging.",
        "upbeat": "User is in a good mood. Keep it energetic and concise.",
        "support":"Be kind and supportive. Keep it gentle and short.",
        "neutral":"Be concise and helpful.",
    }[tone]

    # ====== GPT RESPONSE (with short-term context) ======
    try:
        messages = build_messages(f"{preface}\nUser said: {command}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        reply = response.choices[0].message.content.strip()

        speak(reply)

        remember_exchange(command, reply)
        save_conversation(user_name, command, reply)
        user_data["last_seen"] = datetime.now().isoformat(timespec="seconds")
        update_user_memory(user_data)

    except Exception as e:
        print("Error:", e)
        speak("Sorry Mac, something went wrong while processing that.")
