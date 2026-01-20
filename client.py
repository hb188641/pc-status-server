import time
import requests
import os

SERVER = "https://pc-status-server-production.up.railway.app"
cmd = "Released"
while True:
    try:
        # 생존 신호
        requests.post(f"{SERVER}/ping", timeout=5)
        print("Ping sent to server.")
        # 명령 확인
        r = requests.get(f"{SERVER}/get-command", timeout=5)
        newcmd = r.json().get("command")
        print(cmd)
        if newcmd != cmd:
            cmd = newcmd
            if cmd == "Locked":
                os.system("cmd /c start C:\\Users\\jya06\\source\\repos\\JustLockedDisplay\\JustLockedDisplay\\bin\\Debug\\JustLockedDisplay.exe")
            elif cmd == "Released":
                os.system("taskkill /F /IM JustLockedDisplay.exe")
                os.system("cmd /c start explorer.exe")
        

    except Exception as e:
        pass

    time.sleep(2)
