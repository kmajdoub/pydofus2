from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ExchangeBidHouseSearchMessage(NetworkMessage):
    objectGID:int
    

    def init(self, objectGID_:int):
        self.objectGID = objectGID_
        
        super().__init__()
    
    