from yutservice.utils.repository import VideoRepository
from yutservice.yureq.ytreq2 import search_for_videos
from yutservice.models.dbmodels import YouTubeVideo
from yutservice.schemas import respmodel
import yt_dlp


class YouTubeChannelService():
    def __init__(self, session):
        self.session = session

    async def get_channel_data(self, id):
        channel_url = f'https://www.youtube.com/channel/{id}'
        options = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'source_address': '0.0.0.0',
            'nocheckcertificate': True
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(channel_url, download=False)

        return result