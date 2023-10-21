from yutservice.utils.repository import VideoRepository
from yutservice.yureq.ytreq2 import search_for_videos
from yutservice.models.dbmodels import YouTubeVideo
from yutservice.schemas import respmodel
import yt_dlp


class YouTubeVideoService():
    def __init__(self, session):
        self.session = session
        self.model = YouTubeVideo
        self.repository = VideoRepository(self.session)

    def video_search(self, query, page_token=None, published_after=None, published_before=None):
        options = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0',
            'nocheckcertificate': True
        }

        if published_after:
            options['dateafter'] = published_after

        if published_before:
            options['datebefore'] = published_before

        # If pagination is used, adjust the query
        if page_token:
            query = f"ytsearch{page_token}:{query}"
        else:
            # '10' indicates the number of results. Adjust as needed.
            query = f"ytsearch10:{query}"

        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(query, download=False)

        # Return the entries (video results)
        return result['entries']

    def search(self, q: str, pagetoken: str = None, publishedAfter: str = None, publishedBefore: str = None):
        """Makes a search with q"""
        data = self.video_search(q, pagetoken, publishedAfter, publishedBefore)
        items = []

        for item in data:
            video_to_save = YouTubeVideo()
            video_to_save.videoId = item['id']
            video_to_save.title = item['title']
            video_to_save.channelTitle = item['channel']
            video_to_save.thumbnail = item['thumbnails'][0]['url']
            video_to_save.publishedAt = str(item['release_timestamp'])
            items.append(video_to_save)
            try:
                self.repository.save(video_to_save)
            except:
                continue
        print(data)
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
