from flask import Flask, jsonify, request
import time
from flask import *
password = "6974"
app = Flask(__name__)
last_ping = 0
command = "Released"   # 서버가 내릴 명령

@app.route("/")
def status():
    online = time.time() - last_ping < 20
    return render_template("index.html", online=online, command=command)

@app.route("/ping", methods=["POST"])
def ping():
    global last_ping
    last_ping = time.time()
    return jsonify(ok=True)

@app.route("/get-command", methods=["GET"])
def get_command():
    global command
    if command:
        cmd = command
        return jsonify(command=cmd)
    return jsonify(command=None)

@app.route("/lock", methods=["POST"])
def lock():
    global command
    pw = request.json.get("password")
    if pw != password:
        return "잘못된 비밀번호"
    command = "Locked"
    return "잠금 명령 전송됨"
@app.route("/release", methods=["POST"])
def release():
    global command
    pw = request.json.get("password")
    if pw != password:
        return "잘못된 비밀번호"
    command = "Released"
    return "잠금 해제 명령 전송됨"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

