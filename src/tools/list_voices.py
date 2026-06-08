import pyttsx3

engine = pyttsx3.init()
for voice in engine.getProperty('voices'):
    print(f"Ses Adı: {voice.name}")
    print(f"Ses ID'si: {voice.id}\n")