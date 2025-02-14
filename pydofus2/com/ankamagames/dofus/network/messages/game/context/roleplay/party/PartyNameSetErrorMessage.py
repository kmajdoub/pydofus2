from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.party.AbstractPartyMessage import (
    AbstractPartyMessage,
)


class PartyNameSetErrorMessage(AbstractPartyMessage):
    result: int

    def init(self, result_: int, partyId_: int):
        self.result = result_

        super().init(partyId_)
