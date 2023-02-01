from types import FunctionType
from pydofus2.com.ankamagames.dofus import Constants
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.astar.AStar import AStar
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Edge import Edge
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldGraph import WorldGraph
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.tools.TimeDebug import TimeDebug
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class WorldPathFinder(metaclass=Singleton):
    def __init__(self):
        self.callback: FunctionType = None
        self.src: Vertex = None
        self.dst: float = None
        self.linkedZone: int = None
        super().__init__()

    @property
    def playedCharacterManager(self) -> PlayedCharacterManager:
        return PlayedCharacterManager()

    @property
    def currPlayerVertex(self) -> Vertex:
        if PlayedCharacterManager().currentZoneRp is None or PlayedCharacterManager().currentMap is None:
            return None
        vertex = WorldGraph().getVertex(
            PlayedCharacterManager().currentMap.mapId, PlayedCharacterManager().currentZoneRp
        )
        return vertex

    def findPath(self, destinationMapId: float, callback: FunctionType, linkedZone: int = 1) -> None:
        TimeDebug.reset()
        self.src = self.currPlayerVertex
        Logger().info(
            f"[WoldPathFinder] Start searching path from {self.currPlayerVertex} to destMapId {destinationMapId}"
        )
        if self.src is None:
            callback(None)
            return
        if linkedZone is None:
            linkedZone = 1
        self.linkedZone = linkedZone
        self.callback = callback
        self.dst = destinationMapId
        if int(PlayedCharacterManager().currentMap.mapId) == int(self.dst):
            callback([])
            return
        self.next()

    def abortPathSearch(self) -> None:
        AStar().stopSearch()

    def onAStarComplete(self, path: list[Edge]) -> None:
        if path is None:
            self.next()
        else:
            Logger().debug(f"[WoldPathFinder] Path to map {str(self.dst)} found in {str(TimeDebug.getElapsedTime())}s")
            self.callback(path)

    def next(self) -> None:
        dstV: Vertex = WorldGraph().getVertex(self.dst, self.linkedZone)
        self.linkedZone += 1
        if dstV is None:
            Logger().debug(f"[WoldPathFinder] No path found to map {str(self.dst)}")
            cb = self.callback
            self.callback = None
            cb(None)
            return
        AStar().search(WorldGraph(), self.src, dstV, self.onAStarComplete)
