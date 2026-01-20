from flask import Flask, jsonify, request
import time
from flask import *

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

@app.route("/")
def status():
    online = time.time() - last_ping < 20
    return render_template("index.html", online=online, command=command, message=message)

@app.route("/ping", methods=["POST"])
def ping():
    global last_ping, API_KEY
    api_key = request.headers.get("API-Key")
    if api_key != API_KEY:
        print("Unauthorized ping attempt with API Key:", api_key)
        return jsonify(ok=False), 401
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
    global command, message
    pw = request.json.get("password")
    if pw != password:
        message = {"msg": "Incorrect password.", "css_color": "red"}
        return "0"
    message = {"msg": "Lock request has been sent.", "css_color": "orange"}
    return "1"

@app.route("/unlock", methods=["POST"])
def unlock():
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
    global password, message
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
    global message
    return jsonify(msg=message["msg"], css_color=message["css_color"])

if __name__ == "__main__":
    print("\033[93mPlease enter this API key in the client input:\033[92m", API_KEY, "\033[0m")
    app.run(host="0.0.0.0", port=8080)
