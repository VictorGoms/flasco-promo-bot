import os
import threading
from flask import Flask
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID   = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION  = os.environ["TG_SESSION"]

CANAIS = {
    # "@HardTecPromocoes": {
    #     "webhook": os.environ["DISCORD_WEBHOOK"],
    #     "username": "HardTec Promoções"
    # },
    "@jogosbaratos": {
        "webhook": os.environ["DISCORD_WEBHOOK_JOGOS"],
        "username": "Jogos Baratos"
    },
}

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=list(CANAIS.keys())))
async def handler(event):
    texto = event.message.text or ""
    if not texto:
        return

    canal = getattr(event.chat, "username", None)
    canal_key = f"@{canal}" if canal else None
    config = CANAIS.get(canal_key)
    if not config:
        return

    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": texto
    })
    print(f"[{canal_key}] Encaminhado: {texto[:80]}", flush=True)

def run_telegram():
    with client:
        client.run_until_disconnected()

threading.Thread(target=run_telegram, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
