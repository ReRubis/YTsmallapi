from fastapi import APIRouter
from yutservice.routes import yt


def router_factory():
    """
    puts other routes under 1 prefix
    """
    router = APIRouter(
        prefix='/api'
    )
    router.include_router(yt.router)

    return router


router = router_factory()