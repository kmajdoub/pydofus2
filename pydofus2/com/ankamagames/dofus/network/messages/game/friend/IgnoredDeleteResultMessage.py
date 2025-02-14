from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.common.AccountTagInformation import AccountTagInformation


class IgnoredDeleteResultMessage(NetworkMessage):
    tag: "AccountTagInformation"
    success: bool
    session: bool
    success: bool
    session: bool

    def init(self, tag_: "AccountTagInformation", success_: bool, session_: bool):
        self.tag = tag_
        self.success = success_
        self.session = session_

        super().__init__()
