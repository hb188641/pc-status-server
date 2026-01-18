from flask import Flask, jsonify, request
import time

app = Flask(__name__)

last_ping = 0
command = None   # 서버가 내릴 명령

@app.route("/")
def status():
    online = time.time() - last_ping < 20
    return f"""
    <h1>PC 상태: {'🟢 켜짐' if online else '🔴 꺼짐'}</h1>
    <form action="/lock" method="post">
        <button type="submit">🔒 PC 잠그기</button>
    </form>
    """

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
        command = None   # 한 번 보내면 삭제
        return jsonify(command=cmd)
    return jsonify(command=None)

@app.route("/lock", methods=["POST"])
def lock():
    global command
    command = "LOCK"
    return "잠금 명령 전송됨"
