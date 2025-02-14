from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.friend.FriendInformations import FriendInformations


class FriendsListMessage(NetworkMessage):
    friendsList: list["FriendInformations"]

    def init(self, friendsList_: list["FriendInformations"]):
        self.friendsList = friendsList_

        super().__init__()
