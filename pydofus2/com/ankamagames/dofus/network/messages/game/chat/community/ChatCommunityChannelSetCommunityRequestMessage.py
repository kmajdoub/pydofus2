from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class ChatCommunityChannelSetCommunityRequestMessage(NetworkMessage):
    communityId: int

    def init(self, communityId_: int):
        self.communityId = communityId_

        super().__init__()
