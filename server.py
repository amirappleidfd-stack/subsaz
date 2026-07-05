from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__, static_folder=".")

DATA_FILE = "subs.json"

# ─── توابع کمکی ────────────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"subs": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ─── مسیرها ──────────────────────────────────────────────────────

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "SubSync Backend is running 🚀",
        "routes": ["/sub/<name>", "/sync", "/data", "/create"]
    })

@app.route("/sync", methods=["POST"])
def sync_data():
    data = request.json
    if not data or "subs" not in data:
        return jsonify({"error": "Invalid data, 'subs' field missing"}), 400
    save_data(data)
    return jsonify({"ok": True, "message": "Data synced successfully"})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(load_data())

@app.route("/create", methods=["POST"])
def create_sub():
    """
    ایجاد یک ساب جدید (برای مواقعی که فرانت‌اند کار نمی‌کند)
    ارسال JSON: {"name": "amir"}
    """
    req = request.json
    if not req or "name" not in req:
        return jsonify({"error": "Missing 'name' field"}), 400

    name = req["name"].strip()
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400

    data = load_data()
    # بررسی تکراری نبودن
    if any(s["name"] == name for s in data.get("subs", [])):
        return jsonify({"error": f"Subscription '{name}' already exists"}), 400

    data["subs"].append({"name": name, "configs": []})
    save_data(data)
    return jsonify({"ok": True, "message": f"Subscription '{name}' created"}), 201

@app.route("/add-config", methods=["POST"])
def add_config():
    """
    اضافه کردن کانفیگ به یک ساب
    ارسال JSON: {"name": "amir", "config": "vless://..."}
    """
    req = request.json
    if not req or "name" not in req or "config" not in req:
        return jsonify({"error": "Missing 'name' or 'config'"}), 400

    name = req["name"].strip()
    config = req["config"].strip()
    if not name or not config:
        return jsonify({"error": "Name and config cannot be empty"}), 400

    data = load_data()
    sub = next((s for s in data.get("subs", []) if s["name"] == name), None)
    if not sub:
        return jsonify({"error": f"Subscription '{name}' not found"}), 404

    # جلوگیری از تکراری
    if config in sub.get("configs", []):
        return jsonify({"error": "Config already exists"}), 400

    sub.setdefault("configs", []).append(config)
    save_data(data)
    return jsonify({"ok": True, "message": f"Config added to '{name}'"}), 200

@app.route("/sub/<name>")
def get_sub(name):
    data = load_data()
    sub = next((s for s in data.get("subs", []) if s["name"] == name), None)
    if not sub:
        return f"No subscription found for '{name}'", 404

    configs = sub.get("configs", [])
    if not configs:
        return f"No configs for '{name}'", 404

    return "\n".join(configs), 200, {"Content-Type": "text/plain; charset=utf-8"}

# ─── اجرا ────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        save_data({"subs": []})
        print(f"✅ فایل {DATA_FILE} ساخته شد.")

    print("🚀 SubSync Server running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
