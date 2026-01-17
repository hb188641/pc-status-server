import time
import requests

#SERVER = "https://pc-status-server.up.railway.app/ping"
SERVER = "http://172.30.1.87:8080/ping"

while True:
    try:
        requests.post(SERVER, timeout=5)
        print("ping 보냄")
    except:
        print("실패")

    time.sleep(10)
