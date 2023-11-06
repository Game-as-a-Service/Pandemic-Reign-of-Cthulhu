import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, status as FastApiHTTPstatus
from hypercorn.config import Config
from hypercorn.asyncio import serve

from app.dto import (
    CreateGameReqDto,
    CreateGameRespDto,
    ListInvestigatorsDto,
)
from app.usecase import CreateGameUseCase, GetAvailableInvestigatorsUseCase
from app.adapter.repository import get_repository
from app.adapter.presenter import read_investigator_presenter

_router = APIRouter(
    prefix="",  # could be API versioning e.g. /v0.0.1/* ,  /v2.0.1/*
    dependencies=[],
    responses={
        FastApiHTTPstatus.HTTP_404_NOT_FOUND: {"description": "not found"},
        FastApiHTTPstatus.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "internal error"
        },
    },
)

shared_context = {}


@_router.post("/games", response_model=CreateGameRespDto)
async def create_game(req: CreateGameReqDto):
    uc = CreateGameUseCase(
        repository=shared_context["repository"], settings=shared_context["settings"]
    )
    response = await uc.execute(req.players)
    return response


@_router.get(
    "/games/{game_id}/investigator",
    status_code=200,
    response_model=ListInvestigatorsDto,
)
async def read_unselected_investigators(game_id: str):
    uc = GetAvailableInvestigatorsUseCase(shared_context["repository"])
    result = await uc.execute(game_id, read_investigator_presenter)
    return result


@asynccontextmanager
async def lifetime_server_context(app: FastAPI):
    # TODO, parameters should be in separate python module or `json` , `toml` file
    settings = {"host": "localhost:8081"}
    shared_context["repository"] = get_repository()
    shared_context["settings"] = settings
    yield
    ## TODO, de-initialize the context if necessary,
    # e.g. close database connections
    shared_context.clear()


def init_app_server() -> FastAPI:
    app = FastAPI(lifespan=lifetime_server_context)
    app.include_router(_router)
    return app


def start_web_app() -> None:
    # TODO, parameterize with separate python module or `toml` file
    cfg = Config()
    cfg.bind = ["localhost:8081"]
    app = init_app_server()
    asyncio.run(serve(app, cfg))
