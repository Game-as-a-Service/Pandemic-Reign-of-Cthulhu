from enum import Enum
from typing import List
from pydantic import BaseModel, RootModel

# data transfer objects (DTO) in the application
# TODO, determine module path


class PlayerDto(BaseModel):
    id: str
    nickname: str


class CreateGameReqDto(BaseModel):
    players: List[PlayerDto]


class CreateGameRespDto(BaseModel):
    url: str


class Investigator(Enum):
    # 偵探
    DETECTIVE = "detective"
    # 博士
    DOCTOR = "doctor"
    # 司機
    DRIVER = "driver"
    # 獵人
    HUNTER = "hunter"
    # 魔術師
    MAGICIAN = "magician"
    # 神祕學家
    OCCULTIST = "occultist"
    # 記者
    REPORTER = "reporter"


class SingleInvestigatorDto(BaseModel):
    investigator: Investigator


ListInvestigatorsDto = RootModel[List[SingleInvestigatorDto]]
