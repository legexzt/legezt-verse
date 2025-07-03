from flask import Flask, render_template, request, jsonify, Response
from roast_engine import generate_abuse_with_groq_conversation
from datetime import datetime
import logging
import subprocess

app = Flask(__name__)

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/roast", methods=["POST"])
def roast():
    try:
        data = request.get_json(force=True)
        history = data.get("history", [])

        if not history and "user_input" in data:
            user_input = data.get("user_input", "").strip()
            if not user_input:
                return jsonify({"roast": "❌ Bhai, kuch likh to sahi!"})
            history = [{"role": "user", "content": user_input}]

        if not history or not history[-1].get("content", "").strip():
            return jsonify({"roast": "❌ Bhai, kuch likh to sahi!"})

        user_message = history[-1]['content']
        logging.info(f"🔥 Incoming roast request: {user_message}")

        roast_response = generate_abuse_with_groq_conversation(history)

        logging.info("✅ Roast delivered successfully")
        return jsonify({"roast": roast_response})

    except Exception as e:
        logging.error(f"❌ Error in /roast route: {e}")
        return jsonify({"roast": "❌ Server pe kuch gadbad ho gayi!"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK", "timestamp": datetime.utcnow().isoformat()}), 200

@app.route("/stream-mp3", methods=["POST"])
def stream_mp3():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No YouTube URL provided"}), 400

    def generate():
        process = subprocess.Popen(
            [
                "yt-dlp",
                "-f", "bestaudio",
                "--extract-audio",
                "--audio-format", "mp3",
                "-o", "-",
                url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        for chunk in iter(lambda: process.stdout.read(4096), b""):
            yield chunk

    return Response(generate(), mimetype="audio/mpeg", headers={
        "Content-Disposition": "attachment; filename=converted.mp3"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")