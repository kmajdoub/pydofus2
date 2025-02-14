from pydofus2.com.ankamagames.dofus.datacenter.world.SuperArea import SuperArea
from pydofus2.com.ankamagames.dofus.datacenter.world.WorldMap import WorldMap
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.misc.StringUtils import StringUtils
from pydofus2.flash.geom.Rectangle import Rectangle


class Area(IDataCenter):
    _allAreas: list = None
    MODULE: str = "Areas"

    def __init__(self):
        self.id: int = None

        self.nameId: int = None

        self.superAreaId: int = None

        self.containHouses: bool = None

        self.containPaddocks: bool = None

        self.bounds: Rectangle = None

        self.worldmapId: int = None

        self.hasWorldMap: bool = None

        self.hasSuggestion: bool = None

        self._name: str = None

        self._undiatricalName: str = None

        self._superArea: SuperArea = None

        self._hasVisibleSubAreas: bool = None

        self._hasVisibleSubAreasInitialized: bool = None

        self._worldMap: WorldMap = None
        super().__init__()

    @classmethod
    def getAreaById(cls, id: int) -> "Area":
        area: Area = GameData().getObject(cls.MODULE, id)
        if not area or not area.superArea or not area.hasVisibleSubAreas:
            return None
        return area

    @classmethod
    def getAllArea(cls) -> list["Area"]:
        if cls._allAreas:
            return cls._allAreas
        cls._allAreas = GameData().getObjects(cls.MODULE)
        return cls._allAreas

    idAccessors: IdAccessors = IdAccessors(getAreaById, getAllArea)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def undiatricalName(self) -> str:
        if not self._undiatricalName:
            self._undiatricalName = StringUtils.noAccent(self.name).lower()
        return self._undiatricalName

    @property
    def superArea(self) -> SuperArea:
        if not self._superArea:
            self._superArea = SuperArea.getSuperAreaById(self.superAreaId)
        return self._superArea

    @property
    def hasVisibleSubAreas(self) -> bool:
        if not self._hasVisibleSubAreasInitialized:
            self._hasVisibleSubAreas = True
            self._hasVisibleSubAreasInitialized = True
        return self._hasVisibleSubAreas

    @property
    def worldmap(self) -> WorldMap:
        if not self._worldMap:
            if not self.hasWorldMap:
                self._worldMap = self.superArea.worldmap
            else:
                self._worldMap = WorldMap.getWorldMapById(self.worldmapId)
        return self._worldMap
