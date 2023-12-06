import asyncio
import os

from typing import Dict
import socketio
from hypercorn.config import Config
from hypercorn.asyncio import serve

toplvl_namespace = "/game"
srv = socketio.AsyncServer(async_mode="asgi")


@srv.on("/chat", namespace=toplvl_namespace)
async def _forward_chat_msg(sid, data: Dict):
    if data.get("msg"):
        await srv.emit(
            "/chat", data, namespace=toplvl_namespace, room=data["gameID"], skip_sid=sid
        )
    else:
        print("missing message, %s" % sid)  # TODO, logger


@srv.on("/init", namespace=toplvl_namespace)
async def init_communication(sid, data: Dict):
    try:
        await srv.enter_room(sid, room=data["room"], namespace=toplvl_namespace)
        data["succeed"] = True
    except (ValueError, KeyError) as e:
        print("%s" % e)  # TODO, logger
        data["succeed"] = False
    await srv.emit("/init", data, namespace=toplvl_namespace, room=data["room"])


@srv.on("/deinit", namespace=toplvl_namespace)
async def deinit_communication(sid, data: Dict):
    try:
        await srv.leave_room(sid, room=data["room"], namespace=toplvl_namespace)
        data["succeed"] = True
    except KeyError as e:
        print("%s" % e)  # TODO, logger
        data["succeed"] = False
    await srv.emit("/deinit", data, namespace=toplvl_namespace, room=data["room"])


def gen_srv_task(host: str):
    cfg = Config()
    cfg.bind = [host]
    app = socketio.ASGIApp(srv, static_files={})
    return serve(app, cfg)


def entry() -> None:
    with open("pid.log", "w") as f:
        pid = os.getpid()
        f.write(str(pid))
    asyncio.run(gen_srv_task("localhost:8082"))
