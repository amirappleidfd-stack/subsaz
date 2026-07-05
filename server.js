import express from "express";
import cors from "cors";
import fs from "fs";

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

// خواندن دیتا
function loadData() {
  return JSON.parse(fs.readFileSync("./data.json", "utf8"));
}

// گرفتن ساب
app.get("/sub/:name", (req, res) => {
  const name = req.params.name;
  const data = loadData();

  if (!data[name]) {
    return res.status(404).send("Subscription not found");
  }

  // خروجی خام مناسب V2Ray
  res.setHeader("Content-Type", "text/plain");
  res.send(data[name].join("\n"));
});

// اضافه کردن کانفیگ (اختیاری برای پنل تو)
app.post("/add", (req, res) => {
  const { name, config } = req.body;

  if (!name || !config) {
    return res.status(400).json({ error: "Missing data" });
  }

  const data = loadData();

  if (!data[name]) data[name] = [];

  if (!data[name].includes(config)) {
    data[name].push(config);
  }

  fs.writeFileSync("./data.json", JSON.stringify(data, null, 2));

  res.json({ ok: true });
});

app.listen(PORT, () => {
  console.log("Server running on port", PORT);
});
