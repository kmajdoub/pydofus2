from pydofus2.com.ankamagames.dofus.network.messages.game.actions.AbstractGameActionMessage import (
    AbstractGameActionMessage,
)


class GameActionFightSpellImmunityMessage(AbstractGameActionMessage):
    targetId: int
    spellId: int

    def init(self, targetId_: int, spellId_: int, actionId_: int, sourceId_: int):
        self.targetId = targetId_
        self.spellId = spellId_

        super().init(actionId_, sourceId_)
