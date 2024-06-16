import requests
import os
import time
from google import generativeai

URL = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_SECRET_KEY")}/'

def getUpdates(offset=None):
    return requests.get(URL+"getUpdates", params={ "timeout": 3000, "offset": offset}).json()

def handleUpdates(updates):
    for update in updates.get("result"):
        if "message" in update and "text" in update["message"]:
            chatId = update["message"]["chat"]["id"]
            text = update['message']['text']
            generativeai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = generativeai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(text)
            requests.post(URL+"sendMessage", data={"chat_id": chatId, "text": response.text, "parse_mode": "Markdown"})

if __name__ == "__main__":
    offset = None
    while True:
        updates = getUpdates(offset)
        print(updates)
        if updates.get("result"):
            handleUpdates(updates)
            offset = updates["result"][-1]["update_id"] + 1
        time.sleep(1)



