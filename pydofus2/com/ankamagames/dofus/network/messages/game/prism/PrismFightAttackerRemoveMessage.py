from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class PrismFightAttackerRemoveMessage(NetworkMessage):
    subAreaId: int
    fightId: int
    fighterToRemoveId: int

    def init(self, subAreaId_: int, fightId_: int, fighterToRemoveId_: int):
        self.subAreaId = subAreaId_
        self.fightId = fightId_
        self.fighterToRemoveId = fighterToRemoveId_

        super().__init__()
