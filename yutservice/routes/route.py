from fastapi import APIRouter
from yutservice.routes import yt, byt


def router_factory():
    """
    puts other routes under 1 prefix
    """
    router = APIRouter(
        prefix='/api'
    )
    router.include_router(yt.router)
    router.include_router(byt.router)

    return router


router = router_factory()
