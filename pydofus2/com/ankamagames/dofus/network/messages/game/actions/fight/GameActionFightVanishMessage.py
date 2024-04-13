from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import (
    AbstractGameActionMessage,
)


class GameActionFightVanishMessage(AbstractGameActionMessage):
    targetId: int

    def init(self, targetId_: int, actionId_: int, sourceId_: int):
        self.targetId = targetId_

        super().init(actionId_, sourceId_)
