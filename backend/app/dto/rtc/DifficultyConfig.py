# automatically generated by the FlatBuffers compiler, do not modify

# namespace:

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class DifficultyConfig(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DifficultyConfig()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsDifficultyConfig(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)

    # DifficultyConfig
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DifficultyConfig
    def GameId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # DifficultyConfig
    def Level(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0


def DifficultyConfigStart(builder):
    builder.StartObject(2)


def Start(builder):
    DifficultyConfigStart(builder)


def DifficultyConfigAddGameId(builder, gameId):
    builder.PrependUOffsetTRelativeSlot(
        0, flatbuffers.number_types.UOffsetTFlags.py_type(gameId), 0
    )


def AddGameId(builder, gameId):
    DifficultyConfigAddGameId(builder, gameId)


def DifficultyConfigAddLevel(builder, level):
    builder.PrependInt8Slot(1, level, 0)


def AddLevel(builder, level):
    DifficultyConfigAddLevel(builder, level)


def DifficultyConfigEnd(builder):
    return builder.EndObject()


def End(builder):
    return DifficultyConfigEnd(builder)
