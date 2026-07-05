from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# ----------------------------
# load/save data
# ----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"subs": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------------------
# serve UI
# ----------------------------
@app.route("/")
def home():
    return send_file("index.html")


# ----------------------------
# get subscription configs
# /sub/name
# ----------------------------
@app.route("/sub/<name>")
def get_sub(name):
    data = load_data()

    for sub in data["subs"]:
        if sub["name"] == name:
            # خروجی plain text برای v2ray
            return "\n".join(sub.get("configs", [])), 200, {
                "Content-Type": "text/plain; charset=utf-8"
            }

    return "Subscription not found", 404


# ----------------------------
# add subscription
# ----------------------------
@app.route("/add", methods=["POST"])
def add_sub():
    data = load_data()
    body = request.json

    name = body.get("name")
    if not name:
        return jsonify({"error": "name required"}), 400

    # check duplicate
    for sub in data["subs"]:
        if sub["name"] == name:
            return jsonify({"error": "already exists"}), 400

    data["subs"].append({
        "name": name,
        "configs": []
    })

    save_data(data)
    return jsonify({"status": "ok"})


# ----------------------------
# add config to sub
# ----------------------------
@app.route("/add-config", methods=["POST"])
def add_config():
    data = load_data()
    body = request.json

    name = body.get("name")
    config = body.get("config")

    if not name or not config:
        return jsonify({"error": "name + config required"}), 400

    for sub in data["subs"]:
        if sub["name"] == name:
            if config in sub["configs"]:
                return jsonify({"error": "duplicate"}), 400

            sub["configs"].append(config)
            save_data(data)
            return jsonify({"status": "ok"})

    return jsonify({"error": "not found"}), 404


# ----------------------------
# delete sub
# ----------------------------
@app.route("/delete", methods=["POST"])
def delete_sub():
    data = load_data()
    body = request.json

    name = body.get("name")

    data["subs"] = [s for s in data["subs"] if s["name"] != name]
    save_data(data)

    return jsonify({"status": "deleted"})


# ----------------------------
# health check
# ----------------------------
@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "SubSync Backend is running 🚀",
        "routes": ["/", "/sub/<name>", "/add", "/add-config"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
