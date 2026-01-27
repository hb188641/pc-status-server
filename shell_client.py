import requests

URL = "https://pc-status-server-production.up.railway.app/shell"  # 여기 수정
# URL = "http://localhost:8080/shell"
API_KEY = input("Enter API Key: ")
print("🔥 Railway Shell Connected. type 'help'")



while True:
    cmd = input("> ")

    if cmd == "exit":
        break

    try:
        r = requests.post(URL, json={"cmd": cmd, "API_KEY": API_KEY}, timeout=5)
        print(r.json()["result"])
    except Exception as e:
        print("❌ error:", e)
