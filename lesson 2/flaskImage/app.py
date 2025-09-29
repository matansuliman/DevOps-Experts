# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Docker + Flask!"

if __name__ == "__main__":
    # Flask ירוץ על כל ה־IPs בתוך הקונטיינר (0.0.0.0) ויפתח את פורט 5000
    app.run(host="0.0.0.0", port=5000)
