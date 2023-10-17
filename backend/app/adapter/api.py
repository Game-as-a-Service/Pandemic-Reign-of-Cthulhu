import asyncio

from fastapi import FastAPI, APIRouter, status as FastApiHTTPstatus
from hypercorn.config  import Config
from hypercorn.asyncio import serve

from app.dto import CreateGameReqDto, CreateGameRespDto

_router = APIRouter(
        prefix='', # could be API versioning e.g. /v0.0.1/* ,  /v2.0.1/*
        dependencies=[],
        responses={
                FastApiHTTPstatus.HTTP_404_NOT_FOUND: {'description':'not found'},
                FastApiHTTPstatus.HTTP_500_INTERNAL_SERVER_ERROR: {'description':'internal error'}
            }
        )

@_router.post('/games', response_model=CreateGameRespDto)
async def create_game(req:CreateGameReqDto):
    response = CreateGameRespDto(
                url = 'https://localhost:8081/games/1234'
                )
    return response


def init_app_server() -> FastAPI:
    app = FastAPI()
    app.include_router(_router)
    return app

def start_web_app() -> None:
    # TODO, parameterize with separate python module or `toml` file
    cfg = Config()
    cfg.bind = ['localhost:8081']
    app = init_app_server()
    asyncio.run(serve(app, cfg))

