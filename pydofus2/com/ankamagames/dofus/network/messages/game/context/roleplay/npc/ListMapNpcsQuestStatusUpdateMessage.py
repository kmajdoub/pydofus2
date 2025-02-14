from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.npc.MapNpcQuestInfo import MapNpcQuestInfo


class ListMapNpcsQuestStatusUpdateMessage(NetworkMessage):
    mapInfo: list["MapNpcQuestInfo"]

    def init(self, mapInfo_: list["MapNpcQuestInfo"]):
        self.mapInfo = mapInfo_

        super().__init__()
