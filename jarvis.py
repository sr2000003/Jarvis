import os
import speech_recognition as sr
import pyttsx3
import openai
import subprocess
import datetime

# ⚡️ OPENAI KEY
openai.api_key = "OPEN_API_KEY"  # Yahan apna OpenAI API key daalein 

# ⚡️ Text-To-Speech Setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 160)

def speak(text):
    """Text ko bolne ke liye"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Mic se sunne ke liye"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("👂 Sun raha hoon...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="en-IN")  # Hindi + English
        print(f"🗣️ Aapne kaha: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Google Speech Service available nahi hai abhi.")
        return ""

def ask_chatgpt(prompt):
    """ChatGPT se jawab lena"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def clear_cache():
    """Windows ka cache clear karne ke liye"""
    speak("Windows cache clear kiya ja raha hai...")
    try:
        subprocess.run("del /q /s %temp%\\*", shell=True)
        speak("Cache saaf ho gaya.")
    except Exception as e:
        speak(f"Cache saaf karte samay error aayi: {e}")

def execute_command(command):
    """Commands ke hisaab se action lena"""
    if "hello" in command:
        speak("Hello! Main aapka personal assistant hoon.")
    elif "open notepad" in command:
        speak("Notepad khola ja raha hai...")
        os.system("notepad")
    elif "open excel" in command:
        speak("Excel khola ja raha hai...")
        os.system("start excel")
    elif "open word" in command:
        speak("Word khola ja raha hai...")
        os.system("start winword")
    elif "clear cache" in command:
        clear_cache()
    elif "exit" in command or "quit" in command:
        speak("Bye! Aapka din shubh ho.")
        return False
    else:
        speak("Ye command samajh nahi aayi. Main ChatGPT se poochta hoon...")
        answer = ask_chatgpt(command)
        speak(answer)

    return True

if __name__ == "__main__":
    speak("Jarvis activated. Main sunne ke liye tayyar hoon.")
    while True:
        command = listen()
        if command:
            if not execute_command(command):
                break
