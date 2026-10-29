import os
import time
import sqlite3
import requests
 
BOT_TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
 
PAY_PAGE = "https://smartraveler.ru/?tg_id={tg}"
DB_PATH = "/opt/gatekeeper/orders.db"
 
session = requests.Session()
 
 
def tg(method, **params):
    return session.post(f"{API}/{method}", json=params, timeout=(5, 20)).json()
 
 
def normalize_phone(s):
    digits = "".join(ch for ch in (s or "") if ch.isdigit())
    return digits[-10:] if len(digits) >= 10 else digits
 
 
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
    return conn
 
 
def send_menu(chat_id):
    url = PAY_PAGE.format(tg=chat_id)
    buttons = [[{"text": "Перейти к выбору тарифа и оплате", "url": url}]]
    tg("sendMessage", chat_id=chat_id,
       text=("👋 Это бот доступа к закрытым каналам «Умный путешественник».\n\n"
             "▸ Если ещё не оплачивали — нажмите кнопку ниже, выберите тариф (PRO или PREMIUM) "
             "и оплатите. Ссылка для входа в канал придёт сюда сразу после оплаты.\n\n"
             "▸ Если уже оплатили — просто пришлите номер телефона, который указывали "
             "при заказе (например, +79644779115), и я выдам вам ссылку."),
       reply_markup={"inline_keyboard": buttons})
 
 
def try_claim(chat_id, phone):
    conn = db()
    cur = conn.execute(
        "SELECT id, tariff, channel_id FROM orders "
        "WHERE phone=? AND claimed_by_tg_id IS NULL "
        "ORDER BY id DESC LIMIT 1",
        (phone,))
    row = cur.fetchone()
    if not row:
        cur = conn.execute("SELECT COUNT(*) FROM orders WHERE phone=?", (phone,))
        already = cur.fetchone()[0] > 0
        conn.close()
        if already:
            tg("sendMessage", chat_id=chat_id,
               text="По этому номеру доступ уже был выдан. "
                    "Если возникла проблема — напишите администратору.")
        else:
            tg("sendMessage", chat_id=chat_id,
               text="Не нашёл оплаченного заказа с этим номером. "
                    "Проверьте, что номер совпадает с тем, что указывали при оплате. "
                    "Если всё верно — напишите администратору.")
        return
 
    order_id, tariff, channel_id = row
    invite = tg("createChatInviteLink", chat_id=channel_id,
                member_limit=1, name=f"claim {chat_id}")
    link = (invite.get("result") or {}).get("invite_link")
    if link:
        tg("sendMessage", chat_id=chat_id,
           text=f"Спасибо за покупку! 🎉\n\nВаша персональная одноразовая ссылка "
                f"для входа в канал ({tariff.upper()}):\n{link}")
        conn.execute("UPDATE orders SET claimed_by_tg_id=? WHERE id=?",
                     (str(chat_id), order_id))
        conn.commit()
    else:
        tg("sendMessage", chat_id=chat_id,
           text="Заказ найден, но с выдачей доступа возникла техническая заминка. "
                "Напишите администратору.")
        print("CLAIM INVITE FAILED:", invite, flush=True)
    conn.close()
 
 
def handle(update):
    msg = update.get("message") or {}
    text = (msg.get("text") or "").strip()
    chat_id = (msg.get("chat") or {}).get("id")
    if not chat_id:
        return
 
    if text.startswith("/start"):
        send_menu(chat_id)
        return
 
    phone = normalize_phone(text)
    if len(phone) >= 10:
        try_claim(chat_id, phone)
        return
 
    send_menu(chat_id)
 
 
def main():
    db().close()
    tg("deleteWebhook")
    offset = None
    while True:
        try:
            r = tg("getUpdates", offset=offset, timeout=10, allowed_updates=["message"])
            for upd in r.get("result", []):
                offset = upd["update_id"] + 1
                handle(upd)
        except Exception as e:
            print("poll error:", e)
            time.sleep(3)
 
 
if __name__ == "__main__":
    main()






#import os
#import time
#import requests

#BOT_TOKEN = os.environ["BOT_TOKEN"]
#API = f"https://api.telegram.org/bot{BOT_TOKEN}"

#PAY_PAGE = "https://smartraveler.ru/?tg_id={tg}"

#session = requests.Session()


#def tg(method, **params):
#    # (5, 20): 5 c на подключение, 20 c на ответ — зависшее соединение умрёт за ~20 c, не за 40.
#    return session.post(f"{API}/{method}", json=params, timeout=(5, 20)).json()


#def handle(update):
#    msg = update.get("message") or {}
#    text = (msg.get("text") or "").strip()
#    chat_id = (msg.get("chat") or {}).get("id")
#    if not chat_id:
#        return
#    if text.startswith("/start"):
#        url = PAY_PAGE.format(tg=chat_id)
#        buttons = [[{"text": "Перейти к выбору тарифа и оплате", "url": url}]]
#        tg("sendMessage", chat_id=chat_id,
#           text=("Нажмите кнопку, выберите тариф (PRO или PREMIUM) и оплатите. "
#                 "Сразу после оплаты сюда придёт ссылка для входа в канал."),
#           reply_markup={"inline_keyboard": buttons})


#def main():
#    tg("deleteWebhook")
#    offset = None
#    while True:
#        try:
#            r = tg("getUpdates", offset=offset, timeout=10, allowed_updates=["message"])
#            for upd in r.get("result", []):
#                offset = upd["update_id"] + 1
#                handle(upd)
#        except Exception as e:
#            print("poll error:", e)
#            time.sleep(3)


#if __name__ == "__main__":
#    main()