import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def get_live_search_results(query):
    """Fetch latest results from Serper API (Google Search)."""
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 3}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data.get("organic", []):
            results.append(f"{item['title']}: {item['link']}")
        return "\n".join(results) if results else "No fresh data found."
    return "Unable to fetch live data."

def format_code_response(language, code):
    """Wrap code in 'Python Code:' style like the screenshot."""
    return f"**{language} Code:**\n```{language.lower()}\n{code}\n```"

def enforce_code_formatting(ai_text):
    """If AI response contains code, format it in the screenshot style."""
    if "```" in ai_text:
        try:
            parts = ai_text.split("```")
            # Extract language name
            first_line = parts[1].split("\n")[0].strip()
            language = first_line if first_line else "Python"
            # Extract actual code
            code_block = "\n".join(parts[1].split("\n")[1:]).strip()
            return format_code_response(language, code_block)
        except Exception:
            pass
    return ai_text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # Add live search results for certain queries
    if any(word in user_message.lower() for word in ["current", "today", "now", "latest", "president", "prime minister"]):
        search_info = get_live_search_results(user_message)
        user_message += f"\n\nLatest search results:\n{search_info}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }

    ai_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if ai_response.status_code == 200:
        ai_text = ai_response.json()["choices"][0]["message"]["content"]

        # Always enforce code formatting
        ai_text = enforce_code_formatting(ai_text)

        return jsonify({"reply": ai_text})

    return jsonify({"reply": "Error connecting to AI service."})

if __name__ == "__main__":
    app.run(debug=True)
