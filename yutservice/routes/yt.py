import imp
from fastapi import APIRouter, Depends
from yutservice.schemas import reqmodel, respmodel
from yutservice.services.youtuber import YouTuber
from yutservice.routes.injectors import get_youtube_service
from fastapi import HTTPException, status

router = APIRouter(
    prefix='/yt',
    tags=['videos']
)


@router.post('/', response_model=respmodel.YouTubeSearchResponce)
async def request(
    request: reqmodel.SearchReq,
    service: YouTuber = Depends(get_youtube_service),
):
    """
    returns 10 videos from youtube API
    """
    return service.search(request.q, request.page_token, request.publishedAfter, request.publishedBefore)


@router.get('/',
            response_model=respmodel.YouTubeSearchResponce,
            )
async def get_list(
    service: YouTuber = Depends(get_youtube_service),
):
    """
    returns all the videos that were searched before
    """
    result = service.get_list()
    if result['items'][0] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="None in the database")
    return result
