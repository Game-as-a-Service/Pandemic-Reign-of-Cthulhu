from typing import List, Dict

from app.dto import (
    SingleInvestigatorDto,
    ListInvestigatorsDto,
    Investigator,
    CreateGameRespDto,
)


def read_investigator_presenter(items: List[Investigator]) -> ListInvestigatorsDto:
    def fn1(v):
        return SingleInvestigatorDto(investigator=v)

    return list(map(fn1, items))


def create_game_presenter(settings: Dict, game_id: str) -> CreateGameRespDto:
    url = "https://{}/games/{}".format(settings["host"], game_id)
    return CreateGameRespDto(url=url)
