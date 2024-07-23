import ssl
import certifi

import os
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()
slack_token = os.getenv('SLACK_BOT_TOKEN')
app_token = os.getenv('SLACK_APP_TOKEN')
channel_id = os.getenv('SLACK_CHANNEL_ID')

print(f"SLACK_BOT_TOKEN: {slack_token}")  # Отладочная информация
print(f"SLACK_APP_TOKEN: {app_token}")    # Отладочная информация
print(f"SLACK_CHANNEL_ID: {channel_id}")  # Отладочная информация

# Настройка SSL с использованием сертификатов certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

client = WebClient(token=slack_token, ssl=ssl_context)

def process_message(event_data):
    data = event_data['event']
    print(f"Received event: {data}")  # Отладочная информация
    if data.get('channel') == channel_id and 'subtype' not in data:
        try:
            response = client.reactions_add(
                channel=data['channel'],
                name='heart',  # Сердце-реакция
                timestamp=data['ts']
            )
            print(f"Добавлена реакция сердца к новому сообщению с timestamp {data['ts']}")
        except SlackApiError as e:
            print(f"Ошибка при добавлении реакции: {e.response['error']}")

def handle_socket_mode_request(client: SocketModeClient, req: SocketModeRequest):
    print(f"Received socket mode request: {req.type}")  # Отладочная информация
    if req.type == "events_api":
        event = req.payload['event']
        print(f"Handling event: {event}")  # Отладочная информация
        if event['type'] == 'message':
            process_message(req.payload)
        client.ack(req)

if __name__ == "__main__":
    print("Starting Slack Socket Mode client...")  # Отладочная информация
    socket_mode_client = SocketModeClient(app_token=app_token, web_client=client)
    socket_mode_client.socket_mode_request_listeners.append(handle_socket_mode_request)
    socket_mode_client.connect()

    # Keep the main thread alive to listen for events
    import time
    while True:
        print("Bot is running...")  # Отладочная информация
        time.sleep(10)
