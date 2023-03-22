from datetime import datetime
from yutservice.models.dbmodels import YouTubeVideo


class BaseRepository():
    __model__ = None

    def __init__(self, session):
        self.session = session

    def get(self, videoId):
        """Returns a content with a certain videoId"""
        return self.query.get(videoId)

    def get_list(self) -> list:
        """
        Returns a list of all non-removed items
        """
        return self.query.all()

    def save(self, model):
        """
        """
        self.session.add(model)
        self.session.commit()
        return model

    def delete(self, id):
        model = self.get(id)
        if not model:
            raise Exception('Model not found')
        self.session.query(self.__model__).filter_by(id=id).update(
            {'removed_at': datetime.now()}
        )
        return model

    @property
    def query(self):
        """
        The decorator sets the query function as a class attribute.
        The function returns it so I don't have to pass the __model__
        every time one needs to query. 
        """
        return self.session.query(self.__model__)


class VideoRepository(BaseRepository):
    def get_video(self, videoId):
        """
        gets certain video
        """
        return self.get(videoId)

    def get_video_list(self, model):
        """
        gets a list of certain videos
        based on filters.
        Currently only channeltitle
        """
        self.__model__ = model
        return self.query.order_by(YouTubeVideo.channelTitle.asc())

    def save_video(self, model):
        """
        saves video
        later will put a filter logic here
        """
        self.save(model)
