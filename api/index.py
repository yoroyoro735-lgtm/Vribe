from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Key එක Vercel Environment Variables වලින් ගන්නවා. Github එකේ key එක නෑ
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"reply": "Error: API Key සෙට් කරලා නෑ"}), 500

    data = request.get_json()
    user_msg = data.get('message', '')

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_msg}],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        ai_reply = res.json()['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": "AI reply එක ගන්න බැරි උනා. ආපහු try කරපන්."}), 500

@app.route('/')
def home():
    return "API Running - Chat website එකට /index.html open කරපන්"
