# automatically generated by the FlatBuffers compiler, do not modify

# namespace:

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class CharacterSelection(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = CharacterSelection()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsCharacterSelection(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)

    # CharacterSelection
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # CharacterSelection
    def GameId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # CharacterSelection
    def PlayerId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # CharacterSelection
    def Investigator(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0


def CharacterSelectionStart(builder):
    builder.StartObject(3)


def Start(builder):
    CharacterSelectionStart(builder)


def CharacterSelectionAddGameId(builder, gameId):
    builder.PrependUOffsetTRelativeSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(gameId), 0
    )


def AddGameId(builder, gameId):
    CharacterSelectionAddGameId(builder, gameId)


def CharacterSelectionAddPlayerId(builder, playerId):
    builder.PrependUOffsetTRelativeSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(playerId), 0
    )


def AddPlayerId(builder, playerId):
    CharacterSelectionAddPlayerId(builder, playerId)


def CharacterSelectionAddInvestigator(builder, investigator):
    builder.PrependInt8Slot(2, investigator, 0)


def AddInvestigator(builder, investigator):
    CharacterSelectionAddInvestigator(builder, investigator)


def CharacterSelectionEnd(builder):
    return builder.EndObject()


def End(builder):
    return CharacterSelectionEnd(builder)
