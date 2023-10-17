from typing import List
from pydantic import BaseModel

# data transfer objects (DTO) in the application
# TODO, determine module path

class PlayerDto(BaseModel):
    id: str
    nickname: str

class CreateGameReqDto(BaseModel):
    players: List[PlayerDto]

class CreateGameRespDto(BaseModel):
    url:str

