from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class ArenaDuelRankCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = str(self._criterionValue)
        readableCriterionRef: str = I18n.getUiText("ui.common.pvpDuelRank")
        readableOperator = ">"
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableOperator = I18n.getUiText("ui.common.differentFrom") + " >"
        return readableCriterionRef + " " + readableOperator + " " + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return ArenaDuelRankCriterion(self.basicText)

    def getCriterion(self) -> int:
        from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

        frame = Kernel().partyFrame
        rank: int = 0
        if frame.arenaRankDuelInfos and frame.arenaRankDuelInfos.rank > rank:
            rank = frame.arenaRankDuelInfos.rank
        return rank
