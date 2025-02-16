import os
import sys
import re

import creds
import googleapiclient
from google.auth.transport import requests
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError
import pickle
import time
import datetime
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import logging

logging.basicConfig(level=logging.DEBUG)
res_video_clips = "resources/videoclips1/"
all_mp4 = '.mp4'
all_video_clips = [os.path.join(res_video_clips, f) for f in os.listdir(res_video_clips) if f.endswith(all_mp4)]
index_video_clips = 0
playlist_id = "PLe2IRTUrJhyeXWcb1KSQtfdkis3rXOy06"
client_secrets_file = "resources/client_secret_.json"
scopes = ["https://www.googleapis.com/auth/youtube"]
# Путь к файлу с сохраненными учетными данными.
creds_file = "resources/tokenYT.pickle"

# Функция для аутентификации с помощью OAuth 2.0
def get_authenticated_service():
    creds = None
    # Попробуйте загрузить учетные данные
    if os.path.exists(creds_file):
        with open(creds_file, 'rb') as token:
            creds = pickle.load(token)

    # Проверьте действительность загруженных учетных данных
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            creds = None  # Очистка учетных данных, если произошла ошибка обновления

    # Получение новых учетных данных, если предыдущие недействительны или отсутствуют
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        creds = flow.run_local_server(port=0)

        # Сохранение новых учетных данных для будущего использования
        with open(creds_file, 'wb') as token:
            pickle.dump(creds, token)
        print("Аутентификация прошла успешно.")  # Сообщение о успешном завершении аутентификации
    return build('youtube', 'v3', credentials=creds)


# Получаем клиентский сервис с аутентифицированными учетными данными
youtube = get_authenticated_service()
if youtube:
    print("Аутентификация прошла успешно, клиентский интерфейс YouTube API доступен.")


# Функция для получения номера последнего видео и времени последней публикации
def get_last_video_details(youtube, playlist_id):
    last_video_number = 0
    last_publish_time = None
    last_video_id = None

    # Запрос последних 20 видео (указываем последнюю страницу, если номер плейлиста отсчитывается от последнего)
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50   # при 20 у меня получалось 66 строк в дебаге. Надо сравнить с 50 сколько строк будет и 66 видосов всего загружаю
    )

    # Получаем последнюю страницу содержимого плейлиста
    # Замечание: YouTube Data API не позволяет напрямую отсортировать результаты плейлиста по дате,
    # попробуйте использовать параметр 'pageToken' для получения последних добавленных видео, если это возможно.
    last_page = None
    while request is not None:
        response = request.execute()
        last_page = response
        request = youtube.playlistItems().list_next(request, response)

    # Если есть последняя страница, анализируем и обрабатываем видео
    if last_page:
        for item in last_page['items']:
            video_id = item['contentDetails']['videoId']
            video_details = youtube.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()

            for video in video_details['items']:
                # Предполагаем, что номер видео содержится в заголовке и извлекаем его
                video_title = video['snippet']['title']
                match = re.search(r'\b\d+\b', video_title)
                if match:
                    video_number = int(match.group())
                    # Если номер видео больше последнего, обновляем информацию
                    if video_number > last_video_number:
                        last_video_number = video_number
                        last_video_id = video_id
                        if 'publishAt' in video['status']:
                            # Информация о планировании видео
                            last_publish_time = parser.parse(video['status']['publishAt'])
                        else:
                            last_publish_time = parser.parse(video['snippet']['publishedAt'])
                        # Нет нужды продолжать цикл, если мы уже обновили информацию
                        break

    # Определение времени для следующей публикации
    current_utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    if last_publish_time and last_publish_time > current_utc_time:
        next_publish_time = last_publish_time + timedelta(minutes=30)
    else:
        next_publish_time = current_utc_time + timedelta(minutes=30)

    print(f'Последнее видео (№{last_video_number}) запланировано к публикации на: {last_publish_time}')
    print(f'Следующее видео будет запланировано на: {next_publish_time}')

    return last_video_number, next_publish_time


def count_local_videos():
    return len([f for f in os.listdir(res_video_clips) if f.endswith(all_mp4)])


# Функция для загрузки видео на YouTube
def upload_video(youtube, video_path, title, description, publish_at, playlist_id):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "scheduledStartTime": publish_at.isoformat(),  # Время должно быть в RFC 3339
        },
        "status": {
            "privacyStatus": "private",  # Используйте "private" для запланированной публикации
            "publishAt": publish_at.isoformat(),
        }
    }

    media = MediaFileUpload(video_path)
    response_upload = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    ).execute()

    # Как только видео загружено, добавляем его в плейлист
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": response_upload["id"]
                }
            }
        }
    ).execute()



try:
    if __name__ == "__main__":
        # Получаем данные о последнем видео и используем функцию для определения следующего времени публикации
        last_video_num, next_publish_time = get_last_video_details(youtube, playlist_id)

        # Определение номера, который будет присвоен следующему видео
        next_video_number = last_video_num + 1 if last_video_num is not None else 1

        # Проверяем, есть ли еще видео для загрузки
        if next_video_number >= len(all_video_clips):
            print('А видео то и закончились.')
            sys.exit()

        # Проходимся по всем видео, начиная с следующего после последнего загруженного
        for index, video_path in enumerate(all_video_clips[next_video_number:], start=next_video_number):
            title = f"Unsolvable exercise of GODFATHER SERGEI №{index}"
            description = ("He was a brilliant man, he came up with such exercise. "
                           "All answer options are in Telegram or VK or RuTube @WhoDedSergey\n"
                           "Гениальный был мужик, такие задачи придумывал. "
                           "Про него есть канал в Telegram, VK и RuTube с его великими цитатами и приколами @WhoDedSergey")
            # Загружаем видео с назначенным временем публикации
            upload_video(youtube, video_path, title, description, next_publish_time, playlist_id)

            # Выводим информацию о загруженном видео
            print(f"Видео загружено и запланировано на публикацию: №{index} в {next_publish_time.isoformat()}")

            # Увеличиваем next_publish_time на 30 минут для следующего видео
            next_publish_time += timedelta(minutes=30)

            # Задержка, чтобы избежать спама запросами
            time.sleep(9)

        # Если использовали Google API, рекомендуется отозвать учетные данные по окончании работы
        if creds and creds.valid:
            creds.revoke(Request())

except googleapiclient.errors.HttpError as e:
    if e.resp.status == 403:
        error_content = e.content.decode('utf-8')
        if 'quotaExceeded' in error_content:
            print("Превышена квота. Завершение программы.")
            sys.exit()
    if 'uploadLimitExceeded' in str(e):
        print("Вы достигли максимального количества загружаемых видео. Пожалуйста, подождите или используйте другой аккаунт.")
    else:
        print(f"Произошла ошибка при загрузке видео: {e}")

