import os
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

if not API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env file!")

# ✅ Persistent conversation with history
conversation_history = []

# ✅ Roast generator with memory & limit
MAX_MESSAGES = 100

def generate_abuse_with_groq(user_input):
    if not user_input.strip():
        return "❌ Bhai, kuch likh to sahi!"

    conversation_history.append({"role": "user", "content": user_input})

    if len(conversation_history) > MAX_MESSAGES:
        del conversation_history[0]

    prompt_intro = {
        "role": "system",
        "content": (
            "You are 'LEGEZT', a ChatGPT-style smart AI roaster — sarcastic, funny, savage, and full of attitude.\n"
            "Your style:\n"
            "- Hinglish with confidence\n"
            "- Use roasts that sound like intelligent burns, not just gaali\n"
            "- Smart insults like CarryMinati + ChatGPT hybrid\n"
            "- No full gaalis (use mild creative words only if needed)\n"
            "- Add intelligence, mockery, clever comebacks\n"
            "- One-liner replies only"
        )
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [prompt_intro] + conversation_history,
        "temperature": 1.8,
        "max_tokens": 80
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
        response.raise_for_status()
        roast = response.json()["choices"][0]["message"]["content"].strip()
        conversation_history.append({"role": "assistant", "content": roast})
        return roast
    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP Error: {http_err.response.status_code} - {http_err.response.text}"
    except Exception as err:
        return f"❌ Error: {str(err)}"

# ✅ Reset conversation if needed
def reset_conversation():
    conversation_history.clear()
    return "🧹 Conversation reset. Start roasting fresh!"

# ✅ CLI Testing Mode
if __name__ == "__main__":
    print("🧠 LEGEZT SMART ROASTER 🤖 — Smart roasts with swag!\n(Type 'exit' to quit | 'reset' to start fresh)")
    while True:
        try:
            user_input = input("🗣️  You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Shabaash! Agli baar fir milenge kisi ko udaane.")
                break
            if user_input.lower() == "reset":
                print(reset_conversation())
                continue
            print("🔥 LEGEZT Roaster AI:")
            print(generate_abuse_with_groq(user_input))
        except KeyboardInterrupt:
            print("\n👋 Roaster session closed.")
            break
