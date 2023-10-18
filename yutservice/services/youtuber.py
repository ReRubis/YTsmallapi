from tkinter.messagebox import NO
from yutservice.utils.repository import VideoRepository
from yutservice.yureq.ytreq2 import search_for_videos
from yutservice.models.dbmodels import YouTubeVideo
from yutservice.schemas import respmodel
import yt_dlp


class YouTuber():
    def __init__(self, session):
        self.session = session
        self.model = YouTubeVideo
        self.repository = VideoRepository(self.session)

    def search(self, q: str, pagetoken: str = None, publishedAfter: str = None, publishedBefore: str = None):
        """Makes a search with q"""
        data = search_for_videos(q, pagetoken, publishedAfter, publishedBefore)
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

        for video in dict_to_return['items']:
            url = f'https://www.youtube.com/watch?v={video.videoId}'
            print(url)
            self.download_video(url)
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

    def download_video(self, url, format_code='bestvideo+bestaudio/best', output_template='%(title)s.%(ext)s'):

        options = {
            # Desired format: best video + best audio combined, or just the best overall.
            'format': format_code,
            # Naming template for downloaded files.
            'outtmpl': output_template,
            'postprocessors': [{
                # Use FFmpeg to convert video files to format...
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
