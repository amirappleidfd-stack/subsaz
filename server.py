from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder=".")

# ─── API ───
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "SubSync Backend is running 🚀",
        "routes": ["/sub/<name>", "/add"]
    })


@app.route("/add", methods=["POST"])
def add():
    data = request.json
    return jsonify({"ok": True, "received": data})


@app.route("/sub/<name>")
def get_sub(name):
    return f"Subscription: {name}"


# ─── RUN ───
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
