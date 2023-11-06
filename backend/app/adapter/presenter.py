from typing import List

from app.dto import SingleInvestigatorDto, ListInvestigatorsDto, Investigator


def read_investigator_presenter(items: List[Investigator]) -> ListInvestigatorsDto:
    def fn1(v):
        return SingleInvestigatorDto(investigator=v)

    return list(map(fn1, items))
