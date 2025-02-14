from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.CharacterMinimalInformations import (
        CharacterMinimalInformations,
    )


class BreachKickResponseMessage(NetworkMessage):
    target: "CharacterMinimalInformations"
    kicked: bool

    def init(self, target_: "CharacterMinimalInformations", kicked_: bool):
        self.target = target_
        self.kicked = kicked_

        super().__init__()
