# 🖥️ Remote PC Lock Controller

A Python-based project that allows you to **monitor a PC's online status and remotely lock or unlock it via a web interface**.

The system is built with a Flask server and a PC-side client, using simple password authentication and API Key–based communication.

---

## ✨ Features

* 🟢 Real-time PC online / 🔴 offline status
* 🔒 Remote PC lock / 🔓 unlock via web
* 🔑 Set and change password from the web UI
* 💬 Display status messages from the client
* 🔐 API Key–based client authentication

---

## 📁 Project Structure

```
C:.
│  client.py                 # Client running on the target PC
│  server.py                 # Flask web server
│  JustLockedDisplay_.exe    # Executed when the PC is locked (Windows)
│  requirements.txt          # Server dependencies
│  Procfile                  # Deployment configuration (e.g. Heroku)
│  README.md
│
└─templates
        index.html           # Web UI
```

---

## ⚙️ How It Works

```
[Web Browser]
      ↓
[Flask Server]  ←── API Key auth ──→  [PC Client]
      ↑                                  │
      └────── status / messages ─────────┘
```

* The server determines PC online status using periodic `ping` requests.
* The client polls the server for commands (`Locked` / `Unlocked`).
* When locked, `JustLockedDisplay_.exe` is executed.
* When unlocked, the lock process is terminated and Explorer is restarted.

---

## 🧪 How to Run

### 1️⃣ Start the Server

```bash
pip install -r requirements.txt
python server.py
```

When the server starts, an **API Key** will be printed to the console.

---

### 2️⃣ Run the Client (on the target PC)

```bash
python client.py http://SERVER_ADDRESS:8080 API_KEY
```

Example:

```bash
python client.py http://127.0.0.1:8080 AbC123...
```

---

### 3️⃣ Open the Web Interface

In your browser:

```
http://SERVER_ADDRESS:8080
```

---

## 🔐 Password System

* The initial password is **empty**.
* You must set a password from the web UI before locking/unlocking.
* Commands are rejected if an incorrect password is provided.

---

## 🔒 Security Notes

⚠️ This project is intended for **learning or personal use**.

Current limitations:

* No HTTPS
* Plaintext password storage
* Single API Key

For production use, consider:

* Enabling HTTPS
* Hashing passwords
* Implementing user/session authentication

---

## 🛠️ Tech Stack

* Python 3
* Flask
* HTML / JavaScript (Fetch API)
* Requests

---

## 📌 Notes

* `JustLockedDisplay_.exe` is **Windows-only**.
* Running the client with administrator privileges is recommended.
* Make sure port **8080** is allowed through the firewall.

---

## 📜 License

Free to use for personal and educational purposes.

---

## 🙌 Author

Hwangbo Yun

This project can be easily extended with features such as login systems, multi-PC support, or token-based authentication.
