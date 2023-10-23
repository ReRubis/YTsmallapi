from yutservice.services.youtuber import YouTuber
from yutservice.services.badyoutuber import YouTubeVideoService
from yutservice.services.channeldataer import YouTubeChannelService
from yutservice.services.authser import CommonUserAuthenticator
from yutservice.utils.db_session import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, Cookie

# This is a list of injectors which are used in different endpoints to get a certain service object


def get_common_auth_service(session: Session = Depends(get_db)):
    return CommonUserAuthenticator(session)


def get_auth_user(auth_service: CommonUserAuthenticator = Depends(get_common_auth_service), auth: str = Cookie(None, alias='auth')):
    """
    Used as an authentication method

    Injector returns a user object if the cookie is correct and corresponds to a user
    """
    return auth_service.check_user(token=auth)


def get_youtube_service(session: Session = Depends(get_db)):
    return YouTuber(session)


def get_bad_youtube_service(session: Session = Depends(get_db)):
    return YouTubeVideoService(session)


def get_channel_service(session: Session = Depends(get_db)):
    return YouTubeChannelService(session)
