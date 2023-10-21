from yutservice.services.youtuber import YouTuber
from yutservice.services.badyoutuber import YouTubeVideoService
from yutservice.utils.db_session import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, Cookie

# This is a list of injectors which are used in different endpoints to get a certain service object


# def get_auth_service(session: Session = Depends(get_db)):
#     return UserAuthentificator(session)

def get_youtube_service(session: Session = Depends(get_db)):
    return YouTuber(session)


def get_bad_youtube_service(session: Session = Depends(get_db)):
    return YouTubeVideoService(session)
