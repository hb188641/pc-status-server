import time
import requests
import os
import sys

if len(sys.argv) < 3:
    print("Usage: python client.py <server_address> <api_key>")
    sys.exit(1)

SERVER = sys.argv[1]
API_KEY = sys.argv[2]



cmd = "Unlocked"
while True:
    try:
        # Send heartbeat signal
        requests.post(f"{SERVER}/ping", timeout=5,headers={"API-Key": API_KEY})
        print("Ping sent to server.")
        # Check for new command
        r = requests.get(f"{SERVER}/get-command", timeout=5)
        newcmd = r.json().get("command")
        print(cmd)
        if newcmd != cmd:
            cmd = newcmd
            if cmd == "Locked":
                print("Lock command received.")
                os.system("cmd /c start ./JustLockedDisplay_.exe")
                requests.post(f"{SERVER}/set-message", json={"msg":"PC is locked.", "css_color":"red"}, headers={"API-Key": API_KEY}, timeout=5)
            elif cmd == "Unlocked":
                print("Unlock command received.")
                os.system("taskkill /F /IM JustLockedDisplay_.exe")
                os.system("cmd /c start explorer.exe")
                requests.post(f"{SERVER}/set-message", json={"msg":"PC is unlocked.", "css_color":"green"}, headers={"API-Key": API_KEY}, timeout=5)
        
    except Exception as e:
        print("Error communicating with server:", e)
        pass

    time.sleep(2)
