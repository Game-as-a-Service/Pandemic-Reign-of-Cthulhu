from enum import Enum
from typing import List
from pydantic import BaseModel, RootModel, ConfigDict

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


class UpdateInvestigatorDto(BaseModel):
    investigator: Investigator
    player_id: str


class Difficulty(Enum):
    # 教學難度
    INTRODUCTORY = "introductory"
    # 標準難度
    STANDARD = "standard"
    # 專家難度
    EXPERT = "expert"


class UpdateDifficultyDto(BaseModel):
    level: Difficulty


class UpdateCommonRespDto(BaseModel):
    message: str


class RtcRoomMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gameID: str
    players: List[str]


class ChatMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    msg: str
    nickname: str  # TODO, replace with PlayerDto
    gameID: str
    client: str  ## client session ID


class RtcInitMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    player: PlayerDto
    gameID: str
    client: str  # client session ID
