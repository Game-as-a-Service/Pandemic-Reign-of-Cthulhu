from enum import Enum
from typing import List
from pydantic import BaseModel, RootModel, ConfigDict
import flatbuffers

from .rtc import (
    CharacterSelection,
    Investigator as InvestigatorFbs,
    DifficultyConfig,
    Difficulty as DifficultyFbs,
)

# data transfer objects (DTO) in the application
# TODO, determine module path


class PlayerDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    nickname: str


class CreateGameReqDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
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

    @classmethod
    def from_fbs(cls, value):
        fbs = InvestigatorFbs.Investigator()
        match value:
            case fbs.DETECTIVE:
                return cls.DETECTIVE
            case fbs.DOCTOR:
                return cls.DOCTOR
            case fbs.DRIVER:
                return cls.DRIVER
            case fbs.HUNTER:
                return cls.HUNTER
            case fbs.MAGICIAN:
                return cls.MAGICIAN
            case fbs.OCCULTIST:
                return cls.OCCULTIST
            case fbs.REPORTER:
                return cls.REPORTER

    def to_fbs(self):
        fbs = InvestigatorFbs.Investigator()
        match self:
            case self.DETECTIVE:
                return fbs.DETECTIVE
            case self.DOCTOR:
                return fbs.DOCTOR
            case self.DRIVER:
                return fbs.DRIVER
            case self.HUNTER:
                return fbs.HUNTER
            case self.MAGICIAN:
                return fbs.MAGICIAN
            case self.OCCULTIST:
                return fbs.OCCULTIST
            case self.REPORTER:
                return fbs.REPORTER


class SingleInvestigatorDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    investigator: Investigator


ListInvestigatorsDto = RootModel[List[SingleInvestigatorDto]]


class UpdateInvestigatorDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    investigator: Investigator
    player_id: str


class Difficulty(Enum):
    # 教學難度
    INTRODUCTORY = "introductory"
    # 標準難度
    STANDARD = "standard"
    # 專家難度
    EXPERT = "expert"

    @classmethod
    def from_fbs(cls, value):
        fbs = DifficultyFbs.Difficulty()
        match value:
            case fbs.INTRODUCTORY:
                return cls.INTRODUCTORY
            case fbs.STANDARD:
                return cls.STANDARD
            case fbs.EXPERT:
                return cls.EXPERT

    def to_fbs(self):
        fbs = DifficultyFbs.Difficulty()
        match self:
            case self.INTRODUCTORY:
                return fbs.INTRODUCTORY
            case self.STANDARD:
                return fbs.STANDARD
            case self.EXPERT:
                return fbs.EXPERT


class UpdateDifficultyDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
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


class RtcCharacterMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gameID: str
    investigator: Investigator
    player_id: str

    def serialize(game_id: str, player_id: str, new_invstg: Investigator) -> bytes:
        builder = flatbuffers.Builder(256)
        game_id = builder.CreateString(game_id)
        player_id = builder.CreateString(player_id)
        investigator = new_invstg.to_fbs()
        CharacterSelection.Start(builder)
        CharacterSelection.AddGameId(builder, game_id)
        CharacterSelection.AddPlayerId(builder, player_id)
        CharacterSelection.AddInvestigator(builder, investigator)
        selection = CharacterSelection.End(builder)
        builder.Finish(selection)
        serial = builder.Output()  # byte-array
        return bytes(serial)

    def deserialize(data: bytes):
        buf = bytearray(data)
        obj = CharacterSelection.CharacterSelection.GetRootAs(buf, offset=0)
        game_id = obj.GameId().decode("utf-8")
        player = obj.PlayerId().decode("utf-8")
        investigator = Investigator.from_fbs(obj.Investigator())
        return RtcCharacterMsgData(
            gameID=game_id, investigator=investigator, player_id=player
        )


class RtcDifficultyMsgData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gameID: str
    level: Difficulty

    def serialize(game_id: str, lvl: Difficulty) -> bytes:
        builder = flatbuffers.Builder(128)
        game_id = builder.CreateString(game_id)
        lvl = lvl.to_fbs()
        DifficultyConfig.Start(builder)
        DifficultyConfig.AddGameId(builder, game_id)
        DifficultyConfig.AddLevel(builder, lvl)
        selection = DifficultyConfig.End(builder)
        builder.Finish(selection)
        serial = builder.Output()  # byte-array
        return bytes(serial)

    def deserialize(data: bytes):
        buf = bytearray(data)
        obj = DifficultyConfig.DifficultyConfig.GetRootAs(buf, offset=0)
        game_id = obj.GameId().decode("utf-8")
        lvl = Difficulty.from_fbs(obj.Level())
        return RtcDifficultyMsgData(gameID=game_id, level=lvl)
