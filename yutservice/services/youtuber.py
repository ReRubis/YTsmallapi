from tkinter.messagebox import NO
from yutservice.utils.repository import VideoRepository
from yutservice.models.dbmodels import YouTubeVideo
from yutservice.schemas import respmodel
import yt_dlp

from yutservice.config import CONFIG
import requests
API_KEY = CONFIG['KEY']


class YouTuber():
    def __init__(self, session):
        self.session = session
        self.model = YouTubeVideo
        self.repository = VideoRepository(self.session)

    def search_for_videos(self, q: str,
                          pageToken: str = None,
                          publishedAfter: str = None,
                          publishedBefore: str = None
                          ):
        """Makes a YouTube API call"""
        search_params = {
            'key': API_KEY,
            'q': q,  # Search query
            'part': 'snippet',
            'type': 'video',
            'maxResults': 10,
            'pageToken': pageToken,
            'publishedAfter': publishedAfter,
            'publishedBefore': publishedBefore,
        }
        search_url = 'https://www.googleapis.com/youtube/v3/search'

        # Send the search request
        response = requests.get(search_url, params=search_params)

        # Handle the response
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'Request failed with status code {response.status_code}')
            return response.status_code

    def search(self, q: str, pagetoken: str = None, publishedAfter: str = None, publishedBefore: str = None):
        """Makes a search with q"""
        data = self.search_for_videos(
            q, pagetoken, publishedAfter, publishedBefore)
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
