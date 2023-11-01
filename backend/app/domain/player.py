class Player:
    def __init__(self, id: str, nickname: str):
        self._id = id
        self._nickname = nickname
        self._investigator = None

    def set_investigator(self, investigator):
        self._investigator = investigator

    def get_investigator(self):
        return self._investigator
