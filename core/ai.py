# 📁 core/ai.py

import os
import openai
import google.generativeai as genai
import requests
from dotenv import load_dotenv

# -------------------------
# Load ENV variables
# -------------------------
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
META_API_KEY = os.getenv("META_API_KEY")

# -------------------------
# ChatGPT
# -------------------------
def ask_chatgpt(prompt: str) -> str:
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message["content"]
    except Exception as e:
        return f"[ChatGPT Error] {e}"

# -------------------------
# Gemini
# -------------------------
def ask_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"[Gemini Error] {e}"

# -------------------------
# Meta LLaMA (via HuggingFace API)
# -------------------------
def ask_meta(prompt: str) -> str:
    try:
        headers = {"Authorization": f"Bearer {META_API_KEY}"}
        url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf"
        resp = requests.post(url, headers=headers, json={"inputs": prompt})
        data = resp.json()
        if "error" in data:
            return f"[Meta Error] {data['error']}"
        return data[0]["generated_text"]
    except Exception as e:
        return f"[Meta Error] {e}"

# -------------------------
# Aggregator with Summary
# -------------------------
def ask_jarvis(prompt: str) -> dict:
    # Step 1: Collect raw answers
    results = {
        "ChatGPT": ask_chatgpt(prompt),
        "Gemini": ask_gemini(prompt),
        "Meta": ask_meta(prompt)
    }

    # Step 2: Combine into one string for summary
    combined_text = (
        f"ChatGPT reply: {results['ChatGPT']}\n\n"
        f"Gemini reply: {results['Gemini']}\n\n"
        f"Meta reply: {results['Meta']}\n\n"
        "👉 In teeno replies ko mila kar ek concise aur best answer bana (Hindi-English mix allowed)."
    )

    # Step 3: Ask ChatGPT to summarise
    try:
        final_resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": combined_text}]
        )
        final_answer = final_resp.choices[0].message["content"]
    except Exception as e:
        final_answer = f"[Summary Error] {e}"

    return {"all": results, "final": final_answer}
