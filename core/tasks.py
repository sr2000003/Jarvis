# 📁 core/tasks.py 

import datetime
import logging
import os
from core.voice import speak
from core.ai import ask_jarvis   # ⚡ AI aggregator import

logging.basicConfig(
    filename="jarvis.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# -----------------------
# Auto Reply System
# -----------------------
def auto_reply(message, contact="Friend"):
    msg = message.lower()
    reply = None

    if "good morning" in msg:
        reply = f"Good Morning 🌞 {contact}!"
    elif "good night" in msg:
        reply = f"Good Night 😴 {contact}!"
    elif "hello" in msg or "hi" in msg:
        reply = f"Hello {contact}, kaise ho?"

    if reply:
        logging.info(f"Auto-reply to {contact}: {reply}")
        return reply
    return None


# -----------------------
# Auto Wish System
# -----------------------
def auto_wish(tts_engine=None):
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Mock events (replace later with Google Calendar API)
    events = [
        {"title": "Rohit Birthday", "date": today, "contact": "Rohit"},
        {"title": "Diwali", "date": today, "contact": "All"}
    ]

    for event in events:
        if "birthday" in event["title"].lower():
            wish = f"Happy Birthday 🎂 {event['contact']}!"
        else:
            wish = f"Happy {event['title']} ✨"

        logging.info(f"Auto-wish sent: {wish}")
        print(f"[Jarvis → {event['contact']}]: {wish}")
        if tts_engine:
            speak(tts_engine, wish)


# -----------------------
# Command Execution
# -----------------------
def execute_command(command, tts_engine=None):
    cmd = command.lower()

    # Direct replies
    reply = auto_reply(cmd, "User")
    if reply:
        if tts_engine:
            speak(tts_engine, reply)
        print(f"[Jarvis → User]: {reply}")
        return True

    # Special commands
    if "wish birthdays" in cmd or "festival wish" in cmd:
        auto_wish(tts_engine)
        return True

    if "shutdown" in cmd or "exit" in cmd:
        if tts_engine:
            speak(tts_engine, "System shutting down. Goodbye.")
        return False

    # Default fallback → AI Aggregator
    if tts_engine:
        speak(tts_engine, "Ye command samajh nahi aayi. Main AI experts se poochta hoon...")
        response = ask_jarvis(cmd)

        # Console pe sab AI ke answers
        print("🔹 AI Raw Replies:")
        for source, reply in response["all"].items():
            print(f"{source}: {reply}\n")

        # Final merged reply
        best_reply = response["final"]
        speak(tts_engine, f"Merged answer: {best_reply}")
    return True
