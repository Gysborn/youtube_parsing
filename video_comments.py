import json
import os
from googleapiclient.discovery import build


def snippet_to_dict(comment_id, channel_id, snippet, parent_comment_id=False):
    t = {
        'comment_id': comment_id,
        'parent_id': parent_comment_id,
        'video_id': snippet['videoId'],
        'text': snippet['textOriginal'],
        'author': snippet['authorDisplayName'],
        'author_channel_id': snippet['authorChannelId']['value'] if 'authorChannelId' in snippet else False,
        'date': snippet['publishedAt'],
        'likes': snippet['likeCount']
    }

    t['author_comment'] = t['author_channel_id'] and t['author_channel_id'] == channel_id
    return t


if __name__ == '__main__':
    print("Hello youtube")

    channel_id = 'UCrWWcscvUWaqdQJLQQGO6BA'
    service = build('youtube', 'v3', developerKey=os.getenv('API_KEY'))  # api_key замени на свой

    args = {
        'allThreadsRelatedToChannelId': channel_id,
        'part': 'id,snippet,replies',
        'maxResults': 100
    }

    comments = []
    for page in range(0, 100):  # Квота составляет 10k запросов в сутки, для теста использую 100
        res = service.commentThreads().list(**args).execute()
        # print(json.dumps(r))

        print(f"{page}/9 000 = {res['pageInfo']['totalResults']}")

        for top_level in res['items']:
            comment_id = top_level['snippet']['topLevelComment']['id']
            snippet = top_level['snippet']['topLevelComment']['snippet']
            comments.append(snippet_to_dict(comment_id, channel_id, snippet))

            if 'replies' in top_level:
                for reply in top_level['replies']['comments']:
                    comments.append(snippet_to_dict(
                        reply['id'], channel_id,
                        reply['snippet'], comment_id
                    )
                    )
        args['pageToken'] = res.get('nextPageToken')
        if not args['pageToken']:
            break

    with open(f"data/{channel_id}.json", "w+", encoding='utf-8') as file:
        file.write(json.dumps(comments))
