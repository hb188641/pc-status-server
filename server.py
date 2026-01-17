from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

LAST_PING = None

@app.route("/ping", methods=["POST"])
def ping():
    global LAST_PING
    LAST_PING = datetime.utcnow()
    return jsonify({"ok": True})

@app.route("/")
def status():
    if LAST_PING and datetime.utcnow() - LAST_PING < timedelta(seconds=15):
        return "🟢 PC 켜짐"
    return "🔴 PC 꺼짐"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
