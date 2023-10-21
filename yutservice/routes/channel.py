import imp
from fastapi import APIRouter, Depends
from yutservice.schemas import reqmodel, respmodel
from yutservice.services.channeldataer import YouTubeChannelService
from yutservice.routes.injectors import get_channel_service
from fastapi import HTTPException, status

router = APIRouter(
    prefix='/channel',
    tags=['videos']
)


@router.get('/')
async def get_data(
    id: str,
    service: YouTubeChannelService = Depends(get_channel_service),
):
    """
    endpoint that saves the data of the specified channel and returns it
    """
    result = await service.extract_channel_data(id)
    return result
