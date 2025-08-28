# 📁 core/voice.py

import speech_recognition as sr
import pyttsx3

def init_tts(rate=160, voice_index=1):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', rate)
    return engine

def speak(engine, text):
    print(f"🗣️ Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="en-IN")
        print(f"👤 You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def listen_from_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="en-IN").lower()
    except:
        return ""

def wait_for_wake_word(wake_word="jarvis"):
    while True:
        text = listen()
        if wake_word in text:
            return True