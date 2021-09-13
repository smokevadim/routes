import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import settings
from api.errors import catch_error


def create_app() -> FastAPI:
    app = FastAPI(title='Routes App', debug=False)
    app.middleware('http')(catch_error)
    return app


app = create_app()

from api.main_api import *

origins = [
    "http://localhost",
    f"http://localhost:{settings.SERVER_PORT}",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=settings.SERVER_PORT,
        debug=True,
        log_level='info',
    )
