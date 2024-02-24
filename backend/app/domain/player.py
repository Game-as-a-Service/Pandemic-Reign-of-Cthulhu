from typing import Optional
from app.dto import Investigator


class Player:
    def __init__(self, id: str, nickname: str):
        self._id = id
        self._nickname: str = nickname
        self._investigator: Optional[Investigator] = None
        self._rdy_start: bool = False

    def set_investigator(self, value: Investigator):
        self._investigator = value

    def get_investigator(self) -> Optional[Investigator]:
        return self._investigator

    @property
    def id(self):
        return self._id

    @property
    def started(self) -> bool:
        return self._rdy_start

    def start(self):
        self._rdy_start = True
