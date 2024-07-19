from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()
slack_token = os.getenv('SLACK_BOT_TOKEN')
app_token = os.getenv('SLACK_APP_TOKEN')
channel_id = os.getenv('SLACK_CHANNEL_ID')

client = WebClient(token=slack_token)

def process_message(event_data):
    data = event_data['event']
    if data.get('channel') == channel_id and 'subtype' not in data:
        try:
            client.reactions_add(
                channel=data['channel'],
                name='thumbsup',  # Лайк-реакция
                timestamp=data['ts']
            )
            print(f"Лайкнуто новое сообщение с timestamp {data['ts']}")
        except SlackApiError as e:
            print(f"Ошибка при добавлении реакции: {e.response['error']}")

def handle_socket_mode_request(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api" and req.payload['event']['type'] == 'message':
        process_message(req.payload)
        client.ack(req)

if __name__ == "__main__":
    socket_mode_client = SocketModeClient(app_token=app_token, web_client=client)
    socket_mode_client.socket_mode_request_listeners.append(handle_socket_mode_request)
    socket_mode_client.connect()

    # Keep the main thread alive to listen for events
    import time
    while True:
        time.sleep(1)
