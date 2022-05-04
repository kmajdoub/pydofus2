from com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
from com.ankamagames.dofus.internalDatacenter.stats.Stat import Stat
from com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from com.ankamagames.dofus.logic.game.fight.fightEvents.FightEventsHelper import (
    FightEventsHelper,
)
from com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from com.ankamagames.dofus.logic.game.fight.steps.abstract.AbstractStatContextualStep import (
    AbstractStatContextualStep,
)
from com.ankamagames.dofus.logic.game.fight.types.FightEventEnum import FightEventEnum
from com.ankamagames.dofus.network.enums.GameContextEnum import GameContextEnum
from com.ankamagames.jerakine.logger.Logger import Logger
from com.ankamagames.jerakine.utils.display.EnterFrameDispatcher import (
    EnterFrameDispatcher,
)
from damageCalculation.tools.StatIds import StatIds

logger = Logger(__name__)


class FightMovementPointsVariationStep(AbstractStatContextualStep, IFightStep):

    COLOR: int = 26112

    BLOCKING: bool = False

    _intValue: int

    _voluntarlyUsed: bool

    _updateCharacteristicManager: bool

    _showChatmessage: bool

    def __init__(
        self,
        entityId: float,
        value: int,
        voluntarlyUsed: bool,
        updateCharacteristicManager: bool = True,
        showChatMessage: bool = True,
    ):
        super().__init__(
            self.COLOR,
            "+" + str(value) if value > 0 else str(value),
            entityId,
            GameContextEnum.FIGHT,
            self.BLOCKING,
        )
        self._showChatmessage = showChatMessage
        self._intValue = value
        self._voluntarlyUsed = voluntarlyUsed
        self._virtual = self._voluntarlyUsed
        self._updateCharacteristicManager = updateCharacteristicManager

    @property
    def stepType(self) -> str:
        return "movementPointsVariation"

    @property
    def value(self) -> int:
        return self._intValue

    def start(self) -> None:
        stats: EntityStats = StatsManager().getStats(self._targetId)
        newTotalValue: int = stats.getStat(StatIds.MOVEMENT_POINTS).totalValue + self._intValue
        stats.setStat(Stat(StatIds.MOVEMENT_POINTS, newTotalValue))
        if self._updateCharacteristicManager:
            FightEntitiesFrame.getCurrentInstance().setLastKnownEntityMovementPoint(
                self._targetId, -self._intValue, True
            )
            logger.debug(f"new movement points: {newTotalValue}")
        super().start()
