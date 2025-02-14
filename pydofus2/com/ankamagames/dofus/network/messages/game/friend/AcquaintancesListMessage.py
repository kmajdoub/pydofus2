from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.friend.AcquaintanceInformation import (
        AcquaintanceInformation,
    )


class AcquaintancesListMessage(NetworkMessage):
    acquaintanceList: list["AcquaintanceInformation"]

    def init(self, acquaintanceList_: list["AcquaintanceInformation"]):
        self.acquaintanceList = acquaintanceList_

        super().__init__()
