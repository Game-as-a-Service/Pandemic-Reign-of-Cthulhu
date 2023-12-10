import logging
import asyncio
import os
from typing import Dict

import socketio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from pydantic import BaseModel, ConfigDict, ValidationError

from app.constant import RealTimeCommConst as RtcConst
from app.config import RTC_HOST, RTC_PORT, LOG_FILE_PATH

srv = socketio.AsyncServer(async_mode="asgi")
# currently the logger is configured in simple way, if someone needs to run it
# in production environment, maybe they can switch to more advanced architecture
# e.g. centralized logging architecture, ELK stack, EFK stack ...etc
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)
_logger.addHandler(logging.FileHandler(LOG_FILE_PATH["RTC"], mode="a"))


class ChatMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    msg: str
    nickname: str
    gameID: str
    client: str  ## client session ID


class RtcInitMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nickname: str
    gameID: str
    client: str


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


@srv.on(RtcConst.EVENTS.INIT.value, namespace=RtcConst.NAMESPACE)
async def init_communication(sid, data: Dict):
    try:
        RtcInitMsgData(**data)
        await srv.enter_room(sid, room=data["gameID"], namespace=RtcConst.NAMESPACE)
        data["succeed"] = True
        await srv.emit(
            RtcConst.EVENTS.INIT.value,
            data,
            namespace=RtcConst.NAMESPACE,
            room=data["gameID"],
        )
    except ValidationError as e:
        _logger.error("%s", e)
        error = e.errors(include_url=False, include_input=False)
        error["succeed"] = False
        await srv.emit(
            RtcConst.EVENTS.INIT.value,
            namespace=RtcConst.NAMESPACE,
            data=error,
            to=sid,
        )


@srv.on(RtcConst.EVENTS.DEINIT.value, namespace=RtcConst.NAMESPACE)
async def deinit_communication(sid, data: Dict):
    try:
        RtcInitMsgData(**data)
        await srv.leave_room(sid, room=data["gameID"], namespace=RtcConst.NAMESPACE)
        data["succeed"] = True
        await srv.emit(
            RtcConst.EVENTS.DEINIT.value,
            data,
            namespace=RtcConst.NAMESPACE,
            room=data["gameID"],
        )
    except ValidationError as e:
        _logger.error("%s", e)
        error = e.errors(include_url=False, include_input=False)
        data["succeed"] = False
        await srv.emit(
            RtcConst.EVENTS.DEINIT.value,
            namespace=RtcConst.NAMESPACE,
            data=error,
            to=sid,
        )


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
