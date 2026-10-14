from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fact_checking_system.api.router import api_router
from fact_checking_system.config import get_settings
from fact_checking_system.db.session import dispose_engine
from fact_checking_system.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(api_router)
    return application


app = create_app()


def run() -> None:
    uvicorn.run("fact_checking_system.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
