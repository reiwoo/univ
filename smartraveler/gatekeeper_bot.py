import os
import json
import sqlite3
import requests
from datetime import datetime
from flask import Flask, request
 
BOT_TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
 

ADMIN_CHAT_ID = 1004876755
 
CHANNELS = {
    "pro":     -1003915032385,
    "premium": -1003779275829,
}
 
 
DB_PATH = "/opt/gatekeeper/orders.db"
 
app = Flask(__name__)
 
 
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT NOT NULL,
        tariff TEXT NOT NULL,
        channel_id INTEGER NOT NULL,
        orderid TEXT,
        name TEXT,
        created TEXT NOT NULL,
        claimed_by_tg_id TEXT
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_phone ON orders(phone)")
    return conn
 
 
def normalize_phone(s):
    digits = "".join(ch for ch in (s or "") if ch.isdigit())
    return digits[-10:] if len(digits) >= 10 else digits
 
 
def tg(method, **params):
    return requests.post(f"{API}/{method}", json=params, timeout=15).json()
 
 
def notify_admin(text):
    if ADMIN_CHAT_ID:
        tg("sendMessage", chat_id=ADMIN_CHAT_ID, text=text)
 
 
@app.post("/tilda")
def tilda():
    data = request.form.to_dict() or (request.get_json(silent=True) or {})
    if not data or data.get("test") == "test":
        return "ok"
 
    print("TILDA PAYLOAD:", dict(data), flush=True)
 
    tg_id = data.get("tg_id")
    try:
        payment = json.loads(data.get("payment", "{}"))
    except Exception:
        payment = {}
    products = " ".join(payment.get("products", [])).lower()
    tariff = "premium" if "premium" in products else "pro" if "pro" in products else None
 
    phone_raw = data.get("Phone", "")
    phone = normalize_phone(phone_raw)
    name = data.get("Name", "?")
    orderid = payment.get("orderid", "?")
    info = f"{name}, тел. {phone_raw}, заказ #{orderid}, тариф: {tariff}"
 
    if tariff not in CHANNELS:
        notify_admin("⚠️ Оплата по непонятному тарифу:\n" + info)
        return "ok"
 
    conn = db()
    cur = conn.execute(
        "INSERT INTO orders(phone, tariff, channel_id, orderid, name, created, claimed_by_tg_id) "
        "VALUES (?,?,?,?,?,?,?)",
        (phone, tariff, CHANNELS[tariff], orderid, name,
         datetime.utcnow().isoformat(), None))
    row_id = cur.lastrowid
    conn.commit()
 
    if not tg_id:
        notify_admin("⚠️ Оплата без привязки к Telegram. Покупатель сможет "
                     "получить доступ, написав боту телефон, либо вы выдадите вручную:\n" + info)
        conn.close()
        return "ok"
 
    invite = tg("createChatInviteLink", chat_id=CHANNELS[tariff],
                member_limit=1, name=f"paid {tg_id}")
    link = (invite.get("result") or {}).get("invite_link")
    if link:
        tg("sendMessage", chat_id=int(tg_id),
           text="Оплата получена ✅\n\nВаша персональная одноразовая ссылка для входа в канал:\n" + link)
        conn.execute("UPDATE orders SET claimed_by_tg_id=? WHERE id=?", (str(tg_id), row_id))
        conn.commit()
    else:
        tg("sendMessage", chat_id=int(tg_id),
           text="Оплата получена ✅ С доступом возникла техническая заминка — напишите администратору.")
        notify_admin("❌ Не удалось создать инвайт:\n" + info + f"\n{invite}")
    conn.close()
    return "ok"
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    
#app = Flask(__name__)
 
 
#def tg(method, **params):
#    return requests.post(f"{API}/{method}", json=params, timeout=15).json()
 
 
#def notify_admin(text):
#    if ADMIN_CHAT_ID:
#        tg("sendMessage", chat_id=ADMIN_CHAT_ID, text=text)
 
 
#@app.post("/tilda")
#def tilda():
#    data = request.form.to_dict() or (request.get_json(silent=True) or {})
#    if not data or data.get("test") == "test":
#        return "ok"
 
#    print("TILDA PAYLOAD:", dict(data), flush=True)
 
#    tg_id = data.get("tg_id")
#    try:
#        payment = json.loads(data.get("payment", "{}"))
#    except Exception:
#        payment = {}
#    products = " ".join(payment.get("products", [])).lower()
#    tariff = "premium" if "premium" in products else "pro" if "pro" in products else None
 
#    info = (f"{data.get('Name', '?')}, тел. {data.get('Phone', '')}, "
#            f"заказ #{payment.get('orderid', '?')}, тариф: {tariff}")
 
#    if tariff not in CHANNELS:
#        notify_admin("⚠️ Оплата по непонятному тарифу, разберитесь вручную:\n" + info)
#        return "ok"
 
#    if not tg_id:
#        notify_admin("⚠️ Оплата без привязки к Telegram — выдайте доступ вручную:\n" + info)
#        return "ok"
 
#    invite = tg("createChatInviteLink", chat_id=CHANNELS[tariff],
#                member_limit=1, name=f"paid {tg_id}")
#    link = (invite.get("result") or {}).get("invite_link")
 
#    if link:
#        tg("sendMessage", chat_id=int(tg_id),
#           text="Оплата получена ✅\n\nВаша персональная одноразовая ссылка для входа в канал:\n" + link)
#    else:
#        tg("sendMessage", chat_id=int(tg_id),
#           text="Оплата получена ✅ С доступом возникла техническая заминка — напишите администратору.")
#        notify_admin("❌ Не удалось создать инвайт:\n" + info + f"\n{invite}")
#    return "ok"
 
 
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8080)