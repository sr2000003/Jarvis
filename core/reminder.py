# 📁 core/reminder.py

import schedule

def set_reminder(text, tts_engine, delay=10):
    from core.voice import speak

    def reminder_job():
        speak(tts_engine, f"Reminder: {text}")
    schedule.every(delay).seconds.do(reminder_job)
    speak(tts_engine, f"Reminder set kiya gaya: {text}, {delay} seconds ke baad.")