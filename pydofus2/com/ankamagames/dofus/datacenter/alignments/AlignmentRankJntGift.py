from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData


class AlignmentRankJntGift:
    MODULE = "AlignmentRankJntGift"

    id: int

    gifts: list[int]

    levels: list[int]

    @classmethod
    def getAlignmentRankJntGifts(cls) -> list["AlignmentRankJntGift"]:
        return GameData().getObjects(cls.MODULE)

    @classmethod
    def getAlignmentRankJntGiftById(cls, id) -> "AlignmentRankJntGift":
        return GameData().getObject(cls.MODULE, id)

    idAccessors = IdAccessors(getAlignmentRankJntGiftById, getAlignmentRankJntGifts)
