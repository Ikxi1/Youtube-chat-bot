import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import key

DEVELOPER_KEY = key.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_authenticated_service():
    credentials = service_account.Credentials.from_service_account_file(
        'D:\Programming\Youtube chat\keyfile.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
    )
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 credentials=credentials)

def get_live_chat_id(video_id):
    youtube = get_authenticated_service()
    response = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()
    return response['items'][0]['liveStreamingDetails']['activeLiveChatId']

def get_live_chat_messages(chat_id):
    youtube = get_authenticated_service()
    response = youtube.liveChatMessages().list(
        liveChatId=chat_id,
        part='snippet, authorDetails'
    ).execute()
    return response['items']

if __name__ == '__main__':
    video_id = 'x2RK5dYMSv4'
    chat_id = get_live_chat_id(video_id)
    processed_messages = set()
    while True:
        messages = get_live_chat_messages(chat_id)
        for message in messages:
            message_id = message['id']
            if message_id not in processed_messages:
                processed_messages.add(message_id)
                message_text = message['snippet']['textMessageDetails']['messageText']
                message_author = message['authorDetails']['displayName']
                print(f'{message_author}: {message_text}')
        time.sleep(1)