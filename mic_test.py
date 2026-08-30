import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    print("🎙️  Say something clearly into your headset mic...")
    audio = r.listen(source, timeout=5)
print("✅ Captured", len(audio.get_raw_data()), "bytes of audio.")