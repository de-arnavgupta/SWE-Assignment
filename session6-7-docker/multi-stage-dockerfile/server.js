const express = require("express");

const app = express();
const PORT = process.env.PORT || 8080;

app.get("/", (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head><title>Docker Multi-Stage Build</title></head>
      <body style="font-family: sans-serif; text-align: center; padding: 40px;">
        <h1>Hello World from Docker multi-stage build</h1>
        <p>Student: <strong>Arnav Gupta</strong> (Roll: <strong>24bcs10063</strong>)</p>
        <p>Container Port: 8080 | Host Port: 8080</p>
      </body>
    </html>
  `);
});

app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    message: "Hello World from Docker multi-stage build",
    student: "Arnav Gupta",
    rollNumber: "24bcs10063",
    port: PORT
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});