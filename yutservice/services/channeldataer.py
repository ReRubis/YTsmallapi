from yutservice.utils.repository import VideoRepository, ChannelRepository
from yutservice.yureq.ytreq2 import search_for_videos
from yutservice.models.dbmodels import YouTubeVideo, Channel
from yutservice.schemas import respmodel
import yt_dlp


class YouTubeChannelService():
    def __init__(self, session):
        self.session = session
        self.channel_repository = ChannelRepository(self.session)

    async def get_channel_data(self, id):
        """
        Gets the data of a channel with specified id
        """
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

    async def extract_channel_data(self, id):
        """
        Gets data of a youtube channel
        Saves the data to DB
        """
        data = await self.get_channel_data(id)
        channel_to_save = Channel()

        channel_to_save.channelid = data['id']
        channel_to_save.channelTitle = data['channel']
        channel_to_save.followercount = data['channel_follower_count']
        channel_to_save.description = data['description']
        self.channel_repository.save(channel_to_save)

        return data
