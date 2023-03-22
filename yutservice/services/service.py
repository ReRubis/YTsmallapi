from tkinter.messagebox import NO
from yutservice.utils.db_session import session_init
from yutservice.utils.repository import VideoRepository
from yutservice.yureq.ytreq2 import search_for_videos
from yutservice.models.dbmodels import YouTubeVideo
from yutservice.schemas import respmodel


class Manager():
    def __init__(self):
        self.model = YouTubeVideo
        self.repository = VideoRepository(session_init())

    def search(self, q: str, pagetoken: str = None):
        """Makes a search with q"""
        data = search_for_videos(q, pagetoken)

        items = []
        for item in data['items']:
            video_to_save = YouTubeVideo()
            video_to_save.videoId = item['id']['videoId']
            video_to_save.title = item['snippet']['title']
            video_to_save.channelTitle = item['snippet']['channelTitle']
            video_to_save.thumbnail = item['snippet']['thumbnails']['default']['url']
            video_to_save.publishedAt = str(item['snippet']['publishedAt'])
            items.append(video_to_save)
            try:
                self.repository.save(video_to_save)
            except:
                continue

        dict_to_return = {
            'items': items
        }
        if 'nextPageToken' in data:
            dict_to_return['nextPageToken'] = data['nextPageToken']

        if 'prevPageToken' in data:
            dict_to_return['prevPageToken'] = data['prevPageToken']

        return dict_to_return

    def get_list(self):
        videos = self.repository.get_video_list(YouTubeVideo)
        result = []
        for video in videos:
            result.append(
                {
                    'videoId': f' https://youtu.be/{str(video.videoId)}',
                    'thumbnail': str(video.thumbnail),
                    'title': str(video.title),
                    'channelTitle': str(video.channelTitle),
                    'publishedAt': str(video.publishedAt)
                }
            )
        return {'items': result}
