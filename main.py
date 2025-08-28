# 📁 main.py

from core.voice import init_tts, speak, wait_for_wake_word, listen
from core.tasks import execute_command, auto_wish
import schedule
import time as t

# ✅ Initialize text-to-speech engine
tts_engine = init_tts()

if __name__ == "__main__":
    speak(tts_engine, "Jarvis activated. Main wake word ka intezaar kar raha hoon.")

    # ✅ Schedule daily birthday/festival wishes at 8 AM
    schedule.every().day.at("08:00").do(lambda: auto_wish(tts_engine))

    while True:
        triggered = wait_for_wake_word("jarvis")

        if triggered:
            speak(tts_engine, "Haan, boliye?")
            command = listen()
            if command:
                keep_running = execute_command(command, tts_engine)
                if keep_running is False:
                    break

        schedule.run_pending()
        t.sleep(1)
