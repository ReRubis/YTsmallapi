from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from yutservice.routes import route
from yutservice.utils.db_session import DB_init
import uvicorn


def app_factory():
    app = FastAPI()

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(route.router)

    DB_init()
    return app


app = app_factory()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
