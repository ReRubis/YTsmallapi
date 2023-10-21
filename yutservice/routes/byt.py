import imp
from fastapi import APIRouter, Depends
from yutservice.schemas import reqmodel, respmodel
from yutservice.services.badyoutuber import BadYouTuber
from yutservice.routes.injectors import get_bad_youtube_service
from fastapi import HTTPException, status

router = APIRouter(
    prefix='/byt',
    tags=['videos']
)


@router.post('/',
             response_model=respmodel.YouTubeSearchResponce
             )
async def search_videos(
    request: reqmodel.SearchReq,
    service: YouTubeVideoService = Depends(get_bad_youtube_service),
):
    """
    returns 10 videos from youtube API
    """
    return service.search(request.q, request.page_token, request.publishedAfter, request.publishedBefore)


@router.post('/download',)
async def download_video(
    request: reqmodel.VideoId,
    service: YouTubeVideoService = Depends(get_bad_youtube_service),
):
    if request.video_id:
        url = f'https://www.youtube.com/watch?v={request.video_id}'
        return service.download_video(url)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='provided no data')


@router.get('/',
            # response_model=respmodel.YouTubeSearchResponce,
            )
async def get_list(
    service: YouTubeVideoService = Depends(get_bad_youtube_service),
):
    """
    returns all the videos that were searched before
    """
    result = service.get_list()
    if result['items'][0] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="None in the database")
    return result
