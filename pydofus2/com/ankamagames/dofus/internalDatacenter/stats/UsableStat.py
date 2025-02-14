from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.DetailedStats import DetailedStat


class UsableStat(DetailedStat):
    usedValue: float = 0

    def __init__(
        self,
        id: float,
        baseValue: float,
        additionalValue: float,
        objectsAndMountBonusValue: float,
        alignGiftBonusValue: float,
        contextModifValue: float,
        usedValue: float,
    ):
        super().__init__(
            id=id,
            baseValue=baseValue,
            additionalValue=additionalValue,
            objectsAndMountBonusValue=objectsAndMountBonusValue,
            alignGiftBonusValue=alignGiftBonusValue,
            contextModifValue=contextModifValue,
        )
        self.usedValue = usedValue

    @property
    def totalValue(self) -> float:
        return super().totalValue

    def __str__(self) -> str:
        return self.getFormattedMessage(
            "base: "
            + str(self._baseValue)
            + " additional: "
            + str(self._additionalValue)
            + " objectsAndMountBonus: "
            + str(self._objectsAndMountBonusValue)
            + " alignGiftBonus: "
            + str(self._alignGiftBonusValue)
            + " contextModif: "
            + str(self._contextModifValue)
            + " used: "
            + str(self.usedValue)
            + " total: "
            + str(self._totalValue)
        )

    def reset(self) -> None:
        self._baseValue = self._additionalValue = self._objectsAndMountBonusValue = self._alignGiftBonusValue = (
            self._contextModifValue
        ) = self.usedValue = self._totalValue = 0
