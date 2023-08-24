import os
import pickle
from googleapiclient.discovery import build

base_video_url = 'https://www.youtube.com/watch?v=' # Базовая ссылка для формирования ссылок
channel_id = 'UCrWWcscvUWaqdQJLQQGO6BA' # Ай ди канала

# Этот код для того чтобы достать ссылки из файла и загрузить в переменную
# если надо
# with open('video_links.data', 'rb') as fp:
#     video_links = pickle.load(fp)


if __name__ == '__main__':
    print("Получаем ссылки на видео из канала")

    channel_id = 'UCrWWcscvUWaqdQJLQQGO6BA' # id канала который парсим
    # Данный сервис помогает сформировать api запрос и передать query параметры
    service = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))  # api_key замени на свой

    args = { # Формируем query параметры
        'channelId': channel_id, # id канала
        'part': 'snippet', # область данных для парсинга
        'order': 'date', # сортировка по дате
        'maxResults': 25 # пагинация по 25 страниц
    }
    video_links = []
    for page in range(0, 100): # Цикл по парсингу ссылок
        res = service.search().list(**args).execute() # Достаем пакет из 25 ссылок

        for i in res['items']: # упаковываем ресультат в список
            if i['id']['kind'] == "youtube#video":
                video_links.append([base_video_url + i['id']['videoId'], # Формируем ссылку на осн. базовой
                                    i['id']['videoId'],
                                    i['snippet']['title'],
                                    i['snippet']['publishTime']])

        args['pageToken'] = res.get('nextPageToken') # Добавляем токен следующей стр.
        if not args['pageToken']: # А иначе получим эту же
            break

    with open('data/video_links.data', 'wb') as fp: # Сохраняем с помощью pickle(консервация)
        pickle.dump(video_links, fp) # наш список ссылок, затем можно будет из файла создать ту же переменную

