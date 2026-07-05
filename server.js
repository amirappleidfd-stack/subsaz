import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

// 📦 دیتای موقت (بعداً می‌تونی ببری دیتابیس)
const db = {
  amir: [
    "vless://example-1",
    "vmess://example-2",
    "trojan://example-3"
  ]
};

// 🟢 سلامت سرور
app.get("/", (req, res) => {
  res.json({
    status: "ok",
    message: "SubSync Backend is running 🚀",
    routes: ["/sub/:name", "/add"]
  });
});

// 📡 گرفتن ساب
app.get("/sub/:name", (req, res) => {
  const name = req.params.name;

  if (!db[name]) {
    return res.status(404).send("Subscription not found");
  }

  res.setHeader("Content-Type", "text/plain");
  res.send(db[name].join("\n"));
});

// ➕ اضافه کردن کانفیگ
app.post("/add", (req, res) => {
  const { name, config } = req.body;

  if (!name || !config) {
    return res.status(400).json({ error: "Missing name or config" });
  }

  if (!db[name]) db[name] = [];

  if (!db[name].includes(config)) {
    db[name].push(config);
  }

  res.json({
    ok: true,
    message: "Config added"
  });
});

// 🚀 start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("SubSync running on port", PORT);
});
