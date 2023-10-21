from fastapi import APIRouter
from yutservice.routes import yt, byt, channel


def router_factory():
    """
    puts other routes under 1 prefix
    """
    router = APIRouter(
        prefix='/api'
    )
    router.include_router(yt.router)
    router.include_router(byt.router)
    router.include_router(channel.router)

    return router


router = router_factory()
