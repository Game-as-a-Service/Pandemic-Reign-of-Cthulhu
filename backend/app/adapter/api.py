import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, status as FastApiHTTPstatus
from fastapi.responses import JSONResponse
from hypercorn.config import Config
from hypercorn.asyncio import serve
from app.config import LOG_FILE_PATH

from app.dto import (
    CreateGameReqDto,
    CreateGameRespDto,
    ListInvestigatorsDto,
    UpdateInvestigatorDto,
    UpdateDifficultyDto,
    UpdateCommonRespDto,
)
from app.usecase import (
    CreateGameUseCase,
    GetAvailableInvestigatorsUseCase,
    SwitchInvestigatorUseCase,
    UpdateGameDifficultyUseCase,
)
from app.config import REST_HOST, REST_PORT
from app.domain import GameError
from app.adapter.repository import get_repository
from app.adapter.presenter import read_investigator_presenter, create_game_presenter

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)
_logger.addHandler(logging.FileHandler(LOG_FILE_PATH["REST"], mode="a"))

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


class GameErrorHTTPResponse(JSONResponse):
    def __init__(self, e: GameError):
        (app_err_code, h_status_code) = (e.error_code.value[0], e.error_code.value[1])
        super().__init__(status_code=h_status_code, content={"reason": app_err_code})


@_router.post("/games", response_model=CreateGameRespDto)
async def create_game(req: CreateGameReqDto):
    uc = CreateGameUseCase(
        repository=shared_context["repository"], settings=shared_context["settings"]
    )
    response = await uc.execute(req.players, create_game_presenter)
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


@_router.patch("/games/{game_id}/investigator", status_code=200)
async def switch_investigator(game_id: str, req: UpdateInvestigatorDto):
    uc = SwitchInvestigatorUseCase(shared_context["repository"])
    try:
        await uc.execute(game_id, req.player_id, req.investigator)
    except GameError as e:
        return GameErrorHTTPResponse(e)


@_router.patch("/games/{game_id}/difficulty", response_model=UpdateCommonRespDto)
async def update_game_difficulty(game_id: str, req: UpdateDifficultyDto):
    uc = UpdateGameDifficultyUseCase(
        repository=shared_context["repository"], settings=shared_context["settings"]
    )
    try:
        response = await uc.execute(game_id, req.level)
        return response
    except GameError as e:
        return GameErrorHTTPResponse(e)


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
    cfg.bind = ["%s:%s" % (REST_HOST, REST_PORT)]
    app = init_app_server()
    asyncio.run(serve(app, cfg))
