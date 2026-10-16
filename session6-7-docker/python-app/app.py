from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
      <head><title>Python Hello World</title></head>
      <body style="font-family: sans-serif; text-align: center; padding: 40px;">
        <h1>Hello World from Python Flask Application!</h1>
        <p>Student: <strong>Arnav Gupta</strong> (Roll: <strong>24bcs10063</strong>)</p>
        <p>Container Port: 5000</p>
      </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy", service="python-app", student="Arnav Gupta")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)