# 📁 core/ai.py

from core.voice import speak  # add at top if not there

def ask_chatgpt(prompt, tts_engine=None):
    if not openai.api_key:
        if tts_engine:
            speak(tts_engine, "OpenAI API key missing. Ye feature abhi disabled hai.")
        return "GPT service unavailable (missing API key)."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
