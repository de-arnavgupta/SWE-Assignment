const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head><title>Node.js Hello World</title></head>
      <body style="font-family: sans-serif; text-align: center; padding: 40px;">
        <h1>Hello World from Node.js Application!</h1>
        <p>Student: <strong>Arnav Gupta</strong> (Roll: <strong>24bcs10063</strong>)</p>
        <p>Container Port: 3000</p>
      </body>
    </html>
  `);
});

app.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "nodejs-app", student: "Arnav Gupta" });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Node.js server listening on port ${PORT}`);
});
