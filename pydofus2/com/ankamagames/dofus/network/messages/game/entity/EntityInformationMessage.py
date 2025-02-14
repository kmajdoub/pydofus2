from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.entity.EntityInformation import EntityInformation


class EntityInformationMessage(NetworkMessage):
    entity: "EntityInformation"

    def init(self, entity_: "EntityInformation"):
        self.entity = entity_

        super().__init__()
