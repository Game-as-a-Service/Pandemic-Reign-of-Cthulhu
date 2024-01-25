import logging
import asyncio
import os
from typing import Dict

import socketio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from pydantic import ValidationError

from app.constant import RealTimeCommConst as RtcConst
from app.config import RTC_HOST, RTC_PORT, LOG_FILE_PATH
from app.adapter.repository import get_rtc_room_repository
from app.dto import RtcRoomMsgData, ChatMsgData, RtcInitMsgData
from app.domain import GameError, GameErrorCodes, GameFuncCodes

srv = socketio.AsyncServer(async_mode="asgi")
# currently the logger is configured in simple way, anyone who needs to run it
# in production environment can switch to more advanced architecture e.g.
# centralized logging architecture, ELK stack, EFK stack ...etc
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)
_logger.addHandler(logging.FileHandler(LOG_FILE_PATH["RTC"], mode="a"))

# there is no use-case layer in this socketio server, all the game logic should
# be implemented in the http sserver
_repo = get_rtc_room_repository()


@srv.on(RtcConst.EVENTS.CHAT.value, namespace=RtcConst.NAMESPACE)
async def _forward_chat_msg(sid, data: Dict):
    try:
        ChatMsgData(**data)
        await srv.emit(
            RtcConst.EVENTS.CHAT.value,
            data,
            namespace=RtcConst.NAMESPACE,
            room=data["gameID"],
            skip_sid=sid,
        )
    except ValidationError as e:
        error = e.errors(include_url=False, include_input=False)
        await srv.emit(
            RtcConst.EVENTS.CHAT.value, data=error, namespace=RtcConst.NAMESPACE, to=sid
        )


async def check_room_exist(repo, data: RtcInitMsgData):
    fetched_room = await repo.get(data.gameID)
    if fetched_room is None or fetched_room.gameID != data.gameID:
        ecode = GameErrorCodes.GAME_NOT_FOUND
    elif data.player.id not in fetched_room.players:
        ecode = GameErrorCodes.INVALID_PLAYER
    else:
        ecode = None
    if ecode:
        raise GameError(ecode, fn_code=GameFuncCodes.RTC_ENDPOINT)


## TODO, error handling decorator
@srv.on(RtcConst.EVENTS.INIT.value, namespace=RtcConst.NAMESPACE)
async def init_communication(sid, data: Dict):
    _logger.debug("init-rtc, raw-req-data: %s", data)
    error = None
    try:
        validated = RtcInitMsgData(**data)
        await check_room_exist(_repo, data=validated)
        await srv.enter_room(sid, room=validated.gameID, namespace=RtcConst.NAMESPACE)
        data["succeed"] = True
        await srv.emit(
            RtcConst.EVENTS.INIT.value,
            data,
            namespace=RtcConst.NAMESPACE,
            room=validated.gameID,
        )
    except ValidationError as e:
        _logger.error("%s", e)
        error = e.errors(include_url=False, include_input=False)
        error["succeed"] = False
    except GameError as e:
        _logger.error("req-room-ID:%s , error:%s", validated.gameID, e)
        error = {
            "succeed": False,
            "code": e.error_code.value[0],
            "func": e.func_code.value,
        }
    if error:
        await srv.emit(
            RtcConst.EVENTS.INIT.value,
            namespace=RtcConst.NAMESPACE,
            data=error,
            to=sid,
        )


@srv.on(RtcConst.EVENTS.DEINIT.value, namespace=RtcConst.NAMESPACE)
async def deinit_communication(sid, data: Dict):
    error = None
    try:
        validated = RtcInitMsgData(**data)
        await check_room_exist(_repo, data=validated)
        await srv.leave_room(sid, room=validated.gameID, namespace=RtcConst.NAMESPACE)
        data["succeed"] = True
        await srv.emit(
            RtcConst.EVENTS.DEINIT.value,
            data,
            namespace=RtcConst.NAMESPACE,
            room=validated.gameID,
        )
    except ValidationError as e:
        _logger.error("%s", e)
        error = e.errors(include_url=False, include_input=False)
        error["succeed"] = False
    except GameError as e:
        _logger.error("req-room-ID:%s , error:%s", validated.gameID, e)
        error = {
            "succeed": False,
            "code": e.error_code.value[0],
            "func": e.func_code.value,
        }
    if error:
        await srv.emit(
            RtcConst.EVENTS.DEINIT.value,
            namespace=RtcConst.NAMESPACE,
            data=error,
            to=sid,
        )


@srv.on(RtcConst.EVENTS.NEW_ROOM.value, namespace=RtcConst.NAMESPACE)
async def _new_game_room(sid, data: Dict):
    try:  # TODO, ensure this event is sent by authorized http server
        validated = RtcRoomMsgData(**data)
        await _repo.save(validated)
    except ValidationError as e:
        _logger.error("%s", e)


def gen_srv_task(host: str):
    cfg = Config()
    cfg.bind = [host]
    app = socketio.ASGIApp(srv, static_files={})
    return serve(app, cfg)


def entry() -> None:
    with open("pid.log", "w") as f:
        pid = os.getpid()
        f.write(str(pid))
    url = "%s:%s" % (RTC_HOST, RTC_PORT)
    asyncio.run(gen_srv_task(url))
