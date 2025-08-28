import os
import speech_recognition as sr
import pyttsx3
import openai
import subprocess
import datetime
import logging
from dotenv import load_dotenv

# ⚡️ Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ⚡️ Logging setup
logging.basicConfig(
    filename="jarvis.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ⚡️ Text-To-Speech Setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 160)

def speak(text: str):
    """Text ko bolne ke liye"""
    print(f"🗣️ Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()
    logging.info(f"Spoke: {text}")

def listen():
    """Mic se sunne ke liye"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("👂 Sun raha hoon...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="en-IN")  # Hindi + English
        command = command.lower().strip()
        print(f"🗣️ Aapne kaha: {command}")
        logging.info(f"Heard: {command}")
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Google Speech Service available nahi hai abhi.")
        return ""

def ask_chatgpt(prompt: str) -> str:
    """ChatGPT se jawab lena"""
    if not openai.api_key:
        return "OpenAI API key missing."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error from ChatGPT: {e}"

def clear_cache():
    """Windows ka cache clear karne ke liye"""
    speak("Windows cache clear kiya ja raha hai...")
    try:
        subprocess.run("del /q /s %temp%\\*", shell=True)
        speak("Cache saaf ho gaya.")
    except Exception as e:
        speak(f"Cache saaf karte samay error aayi: {e}")

def execute_command(command: str) -> bool:
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
    elif "open chrome" in command:
        speak("Chrome khola ja raha hai...")
        os.system("start chrome")
    elif "clear cache" in command:
        clear_cache()
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Abhi samay hai {now}")
    elif "date" in command:
        today = datetime.date.today().strftime("%d %B %Y")
        speak(f"Aaj ki tareekh hai {today}")
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
