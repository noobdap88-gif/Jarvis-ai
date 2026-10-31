import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


@app.route("/")
def home():
    return "JARVIS AI is online!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    if not client:
        return jsonify({"error": "API key is not configured"}), 500

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        return jsonify({"reply": response.text})

    except Exception:
        app.logger.exception("Gemini request failed")
        return jsonify({"error": "AI service temporarily unavailable"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
