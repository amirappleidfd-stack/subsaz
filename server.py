import subprocess
import sys

def install_requirements():
    try:
        import flask
    except ImportError:
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

install_requirements()


from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"subs": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "SubSync Backend is running 🚀"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
