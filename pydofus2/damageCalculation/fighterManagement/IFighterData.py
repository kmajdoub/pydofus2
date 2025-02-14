from typing import List, Protocol

from pydofus2.damageCalculation.fighterManagement.fighterStats.HaxeStat import HaxeStat


class IFighterData(Protocol):

    def useSummonSlot(self) -> bool: ...

    def setStat(self, stat: HaxeStat) -> None: ...

    def resolveDodge(self) -> int: ...

    def resetStats(self) -> None: ...

    def isSummon(self) -> bool: ...

    def isInvisible(self) -> bool: ...

    def isAlly(self) -> bool: ...

    def getUsedPM(self) -> int: ...

    def getTurnBeginPosition(self) -> int: ...

    def getSummonerId(self) -> float: ...

    def getStatIds(self) -> List[int]: ...

    def getStat(self, param: int) -> HaxeStat: ...

    def getStartedPositionCell(self) -> int: ...

    def getPreviousPosition(self) -> int: ...

    def getMaxHealthPoints(self) -> int: ...

    def getHealthPoints(self) -> int: ...

    def getDamageHealEquipmentSpellMod(self, param1: int, param2: int) -> int: ...

    def getCharacteristicValue(self, param: int) -> int: ...

    def getBaseDamageHealEquipmentSpellMod(self, param: int) -> int: ...

    def canBreedUsePortals(self) -> bool: ...

    def canBreedSwitchPosOnTarget(self) -> bool: ...

    def canBreedSwitchPos(self) -> bool: ...

    def canBreedBePushed(self) -> bool: ...

    def canBreedBeCarried(self) -> bool: ...
