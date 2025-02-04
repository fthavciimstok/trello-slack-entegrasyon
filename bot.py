import os
import requests
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# .env dosyasındaki API anahtarlarını yükle
load_dotenv()

# Slack ve Trello API bilgileri
slack_token = os.getenv("SLACK_BOT_TOKEN")
trello_api_key = os.getenv("TRELLO_API_KEY")
trello_token = os.getenv("TRELLO_TOKEN")
board_id = os.getenv("TRELLO_BOARD_ID")
list_id = os.getenv("TRELLO_LIST_ID")

# Slack Client'ı başlatıyoruz
client = WebClient(token=slack_token)

# Slack'ten gelen mesajları Trello'ya ekleyen fonksiyon
def post_to_trello(text):
    # Trello'ya kart eklemek için API isteği
    url = f'https://api.trello.com/1/cards'
    query = {
        'key': trello_api_key,
        'token': trello_token,
        'idList': list_id,  # Hedef listeyi seçiyoruz
        'name': text,  # Kart adı
        'desc': text,  # Kart açıklaması
    }
    response = requests.post(url, params=query)
    
    if response.status_code == 200:
        print(f"Başarıyla Trello'ya eklendi: {text}")
    else:
        print(f"Hata: {response.text}")

# Slack'teki mesajları dinleyen fonksiyon
def listen_to_slack():
    try:
        # Slack botunun dinlemesi gereken kanal
        response = client.conversations_history(channel="C0123456789")  # Kanal ID'sini buraya ekleyin

        for message in response['messages']:
            # Mesajdan gelen metni al
            text = message.get('text', '')
            
            # Boş olmayan mesajları Trello'ya ekle
            if text:
                post_to_trello(text)

    except SlackApiError as e:
        print(f"Slack API hatası: {e.response['error']}")

# Uygulama başladığında Slack'teki mesajları dinlemeye başla
if __name__ == "__main__":
    listen_to_slack()
