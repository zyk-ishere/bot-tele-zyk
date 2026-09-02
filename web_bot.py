import time
import requests

TOKEN = "8640534048:AAF8HEHjq5hWPPu2_za_nLs2wymJsYapXk8"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    try:
        res = requests.get(URL + "getUpdates", params={"timeout": 100, "offset": offset})
        return res.json()
    except Exception as e:
        print("Error connection:", e)
        return None

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def main():
    print("Bot Telegram Remote Zaki Berjalan...")
    last_update_id = None
    
    while True:
        updates = get_updates(last_update_id)
        if updates and "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                message = update.get("message")
                
                if not message:
                    continue
                
                chat_id = message["chat"]["id"]
                
                # Mengubah HTML jika dikirim Teks / Kode
                if "text" in message:
                    text = message["text"]
                    if text == "/start":
                        send_message(chat_id, "👋 Halo Zaki!\n\nKirimkan kode HTML (teks) ke bot ini untuk langsung memperbarui tampilan website Debian kamu.")
                    else:
                        with open("/var/www/html/index.html", "w", encoding="utf-8") as f:
                            f.write(text)
                        send_message(chat_id, "✅ Berhasil! File /var/www/html/index.html telah diperbarui.")

                # Mengubah HTML jika dikirimkan File .html / dokumen
                elif "document" in message:
                    doc = message["document"]
                    file_id = doc["file_id"]
                    file_info = requests.get(URL + f"getFile?file_id={file_id}").json()
                    file_path = file_info["result"]["file_path"]
                    file_data = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}").text
                    
                    with open("/var/www/html/index.html", "w", encoding="utf-8") as f:
                        f.write(file_data)
                    send_message(chat_id, "✅ File .html berhasil diunduh dan dipasang di server!")

        time.sleep(1)

if __name__ == "__main__":
    main()
