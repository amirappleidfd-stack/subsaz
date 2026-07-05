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
from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__, static_folder=".")

DATA_FILE = "subs.json"   # فایل ذخیره‌سازی داده‌ها

# ─── توابع کمکی ────────────────────────────────────────────────

def load_data():
    """خواندن داده‌ها از فایل JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # اگر فایل وجود نداشت، یک ساختار پیش‌فرض برمی‌گردانیم
    return {"subs": []}

def save_data(data):
    """نوشتن داده‌ها در فایل JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ─── مسیرها ──────────────────────────────────────────────────────

@app.route("/")
def home():
    """صفحه اصلی (index.html)"""
    return send_from_directory(".", "index.html")

@app.route("/status")
def status():
    """وضعیت سرور (اختیاری)"""
    return jsonify({
        "status": "ok",
        "message": "SubSync Backend is running 🚀",
        "routes": ["/sub/<name>", "/sync", "/data"]
    })

@app.route("/sync", methods=["POST"])
def sync_data():
    """
    هم‌گام‌سازی داده‌ها از فرانت‌اند به سرور
    انتظار دریافت JSON با کلید 'subs'
    """
    data = request.json
    if not data or "subs" not in data:
        return jsonify({"error": "Invalid data, 'subs' field missing"}), 400

    save_data(data)
    return jsonify({"ok": True, "message": "Data synced successfully"})

@app.route("/data", methods=["GET"])
def get_data():
    """دریافت کل داده‌ها به صورت JSON (برای دیباگ)"""
    return jsonify(load_data())

@app.route("/sub/<name>")
def get_sub(name):
    """
    برگرداندن کانفیگ‌های یک ساب به صورت plain text
    هر کانفیگ در یک خط
    """
    data = load_data()
    sub = next((s for s in data.get("subs", []) if s["name"] == name), None)
    if not sub:
        return f"No subscription found for '{name}'", 404

    configs = sub.get("configs", [])
    if not configs:
        return f"No configs for '{name}'", 404

    # خروجی به صورت متن ساده با خط‌های جداگانه
    return "\n".join(configs), 200, {"Content-Type": "text/plain; charset=utf-8"}

# ─── اجرا ────────────────────────────────────────────────────────

if __name__ == "__main__":
    # اگر فایل داده وجود نداشت، یک نمونه خالی می‌سازیم
    if not os.path.exists(DATA_FILE):
        save_data({"subs": []})
        print(f"✅ فایل {DATA_FILE} ساخته شد.")

    print("🚀 SubSync Server running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

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
