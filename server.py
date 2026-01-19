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
        return jsonify(command=cmd, online=(time.time() - last_ping < 20))
    return jsonify(command=None, online=(time.time() - last_ping < 20))

@app.route("/lock", methods=["POST"])
def lock():
    global command
    pw = request.json.get("password")
    if pw != password:
        return "0"
    command = "Locked"
    return "1"
@app.route("/release", methods=["POST"])
def release():
    global command
    pw = request.json.get("password")
    if pw != password:
        return "0"
    command = "Released"
    return "1"
@app.route("/change-password", methods=["POST"])
def set_password():
    global password
    pw = request.json.get("password")
    new_pw = request.json.get("new_password")
    if pw != password:
        return "0"
    password = new_pw
    return "1"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

