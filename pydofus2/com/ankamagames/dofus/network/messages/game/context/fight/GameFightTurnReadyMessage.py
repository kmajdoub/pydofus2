from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class GameFightTurnReadyMessage(NetworkMessage):
    isReady: bool
    def init(self, isReady_: bool):
        self.isReady = isReady_
        
        super().__init__()
    