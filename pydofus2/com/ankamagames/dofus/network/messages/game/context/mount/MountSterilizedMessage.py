from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class MountSterilizedMessage(NetworkMessage):
    mountId: int
    def init(self, mountId_: int):
        self.mountId = mountId_
        
        super().__init__()
    