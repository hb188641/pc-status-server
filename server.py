import signal
import os
import sys
from flask import Response
from flask import render_template
import logging
from threading import Thread
from flask import Flask, jsonify, request
import time
log = logging.getLogger('werkzeug')
log.disabled = True
def generate_api_key():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

API_KEY = generate_api_key()
password = ""
app = Flask(__name__)
last_ping = 0
command = "Unlocked"
message = {"msg": "", "css_color": ""}
server_status = "Online"

@app.route("/")
def status():
    global server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    online = time.time() - last_ping < 7
    return render_template("index.html", online=online, command=command, message=message)

@app.route("/ping", methods=["POST"])
def ping():
    global last_ping, API_KEY, server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    api_key = request.headers.get("API-Key")
    if api_key != API_KEY:
        print("Unauthorized ping attempt with API Key:", api_key)
        return jsonify(ok=False), 401
    last_ping = time.time()
    return jsonify(ok=True)

@app.route("/get-command", methods=["GET"])
def get_command():
    global command, server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    if command:
        cmd = command
        return jsonify(command=cmd, online=(time.time() - last_ping < 7))
    return jsonify(command=None, online=(time.time() - last_ping < 7))

@app.route("/lock", methods=["POST"])
def lock():
    global command, message, server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    pw = request.json.get("password")
    if pw != password:
        message = {"msg": "Incorrect password.", "css_color": "red"}
        return "0"
    command = "TryingToLock"
    message = {"msg": "Lock request has been sent.", "css_color": "orange"}
    return "1"

@app.route("/unlock", methods=["POST"])
def unlock():
    global server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    global command, message
    pw = request.json.get("password")
    if pw != password:
        message = {"msg": "Incorrect password.", "css_color": "red"}
        return "0"
    command = "TryingToUnlock"
    message = {"msg": "Unlock request has been sent.", "css_color": "orange"}
    return "1"

@app.route("/change-password", methods=["POST"])
def set_password():
    global password, message, server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    pw = request.json.get("password")
    new_pw = request.json.get("new_password")
    if pw != password:
        message = {"msg": "Incorrect password.", "css_color": "red"}
        return "0"
    if pw == new_pw:
        message = {"msg": "New password cannot be the same as the old password.", "css_color": "orange"}
        return "2"
    message = {"msg": "Password changed successfully.", "css_color": "green"}
    password = new_pw
    return "1"

@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return Response(status=204)

@app.route("/set-message", methods=["POST"])
def set_message():
    global message, API_KEY, command
    if server_status == "Offline":
        return "Server is offline.", 503
    api_key = request.headers.get("API-Key")
    
    if api_key != API_KEY:
        return jsonify(ok=False), 401
    message = {
        "msg": request.json.get("msg", ""),
        "css_color": request.json.get("css_color", "")
    }
    if message["msg"] == "PC is unlocked.":
        command = "Unlocked"
    if message["msg"] == "PC is locked.":
        command = "Locked"
    return "1"

@app.route("/get-message", methods=["GET"])
def get_message():
    global message, server_status
    if server_status == "Offline":
        return "Server is offline.", 503
    return jsonify(msg=message["msg"], css_color=message["css_color"])

@app.route("/shell", methods=["POST"])
def shell_api():
    global server_status, API_KEY, message, password

    cmd = request.json.get("cmd", "")
    api_key = request.json.get("API_KEY", "")
    if api_key != API_KEY:
        return jsonify(result="❌ Unauthorized: Invalid API Key"), 401
    print(f"\rReceived shell command: {cmd}\n", end="")
    if cmd == "stop":
        server_status = "Offline"
        return {"result": "Server status set to Offline."}

    elif cmd.startswith("setkey "):
        API_KEY = cmd.split(" ", 1)[1]
        return {"result": f"New API Key set to: {API_KEY}"}

    elif cmd.startswith("setmsg "):
        msg = cmd[len("setmsg "):]
        message = {"msg": msg, "css_color": "blue"}
        return {"result": f"Message set to: {msg}"}

    elif cmd == "resetpw":
        password = ""
        return {"result": "Password reset."}

    elif cmd == "start":
        server_status = "Online"
        return {"result": "Server status set to Online."}

    elif cmd == "status":
        return {"result": f"Server status: {server_status}"}

    elif cmd == "help":
        return {"result": "stop, setkey, setmsg, resetpw, start, status, help"}

    else:
        return {"result": "Unknown command"}


if __name__ == "__main__":
    print("\033[93mPlease enter this API key in the client input:\033[92m", API_KEY, "\033[0m")
    app.run(host="0.0.0.0", port=8080)
