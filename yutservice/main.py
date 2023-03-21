from fastapi import FastAPI
from yutservice.routes import yt


def app_factory():
    app = FastAPI()

    app.include_router(yt.router)
    return app


app = app_factory()
