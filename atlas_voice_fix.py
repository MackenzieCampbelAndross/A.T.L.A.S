import pyttsx3, time

engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

time.sleep(1)
engine.say("Initializing Adaptive Terminal for Logical Analysis and Simulation. A.T.L.A.S. ready. Welcome Mac.")
engine.runAndWait()