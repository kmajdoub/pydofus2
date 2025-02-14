from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInformations import HouseInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInstanceInformations import (
        HouseInstanceInformations,
    )


class HouseOnMapInformations(HouseInformations):
    doorsOnMap: list[int]
    houseInstances: list["HouseInstanceInformations"]

    def init(
        self, doorsOnMap_: list[int], houseInstances_: list["HouseInstanceInformations"], houseId_: int, modelId_: int
    ):
        self.doorsOnMap = doorsOnMap_
        self.houseInstances = houseInstances_

        super().init(houseId_, modelId_)
