from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.AllianceInformation import (
        AllianceInformation,
    )


class TaxCollectorStaticInformations(NetworkMessage):
    firstNameId: int
    lastNameId: int
    allianceIdentity: "AllianceInformation"
    callerId: int
    uid: str

    def init(
        self, firstNameId_: int, lastNameId_: int, allianceIdentity_: "AllianceInformation", callerId_: int, uid_: str
    ):
        self.firstNameId = firstNameId_
        self.lastNameId = lastNameId_
        self.allianceIdentity = allianceIdentity_
        self.callerId = callerId_
        self.uid = uid_

        super().__init__()
