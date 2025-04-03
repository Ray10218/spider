from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def serve_weather():
    return send_from_directory(".", "weather.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 
