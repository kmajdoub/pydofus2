import json
import os
from time import perf_counter

from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Edge import Edge
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Transition import Transition
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.TransitionTypeEnum import TransitionTypeEnum
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum

WORLDGRAPH_PATH = XmlConfig().getEntry("config.data.pathFinding")
__dir__ = os.path.dirname(os.path.abspath(__file__))
NPC_TRAVEL_DATA_FILE = os.path.join(__dir__, "npc_travel_data.json")
EDGE_PATCHES_FILE = os.path.join(__dir__, "edge_patches.json")


class WorldGraph(metaclass=ThreadSharedSingleton):
    def __init__(self):
        self._vertices = dict[int, dict[int, Vertex]]()
        self._edges = dict[float, Edge]()
        self._outgoingEdges = dict[float, list[Edge]]()
        self._vertexUid: float = 0
        self.init()

    def addEdgePatches(self):
        with open(EDGE_PATCHES_FILE, "r") as f:
            edges_patches = json.load(f)
            for patch in edges_patches:
                src_vertex = self.getVertex(patch["src_vertex"]["mapId"], patch["src_vertex"]["zoneId"])
                dst_vertex = self.getVertex(patch["dst_vertex"]["mapId"], patch["dst_vertex"]["zoneId"])
                patch_edge = self.addEdge(src_vertex, dst_vertex)
                for tr in patch["transitions"]:
                    patch_edge.addTransition(**tr)

    def addNpcTravelEdges(self):
        with open(NPC_TRAVEL_DATA_FILE, "r") as f:
            npc_travel_infos = json.load(f)
            for info in npc_travel_infos.values():
                src_vertex = self.getVertex(info["npcMapId"], 1)
                dst_vertex = self.getVertex(info["landingMapId"], 1)
                npc_travel_transition = Transition(
                    TransitionTypeEnum.NPC_TRAVEL, -1, -1, "", -1, -1, -1, npc_travel_infos=info
                )
                npc_travel_edge = self.addEdge(src_vertex, dst_vertex)
                npc_travel_edge.transitions.append(npc_travel_transition)

    def nextMapInDirection(self, mapId, direction):
        for vertex in self.getVertices(mapId).values():
            for edge in self.getOutgoingEdgesFromVertex(vertex):
                for transition in edge.transitions:
                    if transition.direction != -1 and transition.direction == direction:
                        return edge.dst.mapId

    def init(self):
        s = perf_counter()
        with open(WORLDGRAPH_PATH, "rb") as binaries:
            data = ByteArray(binaries.read())
            edgeCount: int = data.readInt()
            for _ in range(edgeCount):
                src = self.addVertex(data.readDouble(), data.readInt())
                dest = self.addVertex(data.readDouble(), data.readInt())
                edge = self.addEdge(src, dest)
                transitionCount = data.readInt()
                for _ in range(transitionCount):
                    tr_dir, tr_type, tr_skill, tr_criterion, tr_tran_mapId, tr_cell, tr_ieId = (
                        data.readByte(),
                        data.readByte(),
                        data.readInt(),
                        data.readUTFBytes(data.readInt()),
                        data.readDouble(),
                        data.readInt(),
                        data.readDouble(),
                    )
                    edge.addTransition(tr_dir, tr_type, tr_skill, tr_criterion, tr_tran_mapId, tr_cell, tr_ieId)
            del data
        self.addNpcTravelEdges()
        self.addEdgePatches()
        Logger().debug("WorldGraph loaded in %s seconds", perf_counter() - s)

    def addEdge(self, src: Vertex, dest: Vertex) -> Edge:
        edge: Edge = self._edges.get(src.UID, {}).get(dest.UID)
        if edge:
            return edge
        if not self.doesVertexExist(src) or not self.doesVertexExist(dest):
            return None
        edge = Edge(src, dest)
        if self._edges.get(src.UID) is None:
            self._edges[src.UID] = dict()
        self._edges[src.UID][dest.UID] = edge
        outgoing = self._outgoingEdges.get(src.UID)
        if outgoing is None:
            outgoing = list[Edge]()
            self._outgoingEdges[src.UID] = outgoing
        outgoing.append(edge)
        return edge

    def addVertex(self, mapId: float, zone: int) -> Vertex:
        vertex: Vertex = self._vertices.get(mapId, {}).get(zone)
        if vertex is None:
            vertex = Vertex(mapId, zone, self._vertexUid)
            self._vertexUid += 1
            if mapId not in self._vertices:
                self._vertices[mapId] = dict()
            self._vertices[mapId][zone] = vertex
        return vertex

    def doesVertexExist(self, v: Vertex) -> bool:
        return v.mapId in self._vertices and v.zoneId in self._vertices[v.mapId]

    def getEdges(self) -> dict:
        return self._edges

    def getVertex(self, mapId: float, mapRpZone: int) -> Vertex:
        mapId = float(mapId)
        mapRpZone = int(mapRpZone)
        return self._vertices.get(mapId, {}).get(mapRpZone)

    def getVertices(self, mapId) -> dict[int, Vertex]:
        return self._vertices.get(mapId)

    def getOutgoingEdgesFromVertex(self, src: Vertex) -> list[Edge]:
        if src is None:
            Logger().error("Got a None edge!")
            return None
        return self._outgoingEdges.get(src.UID, [])

    def getEdge(self, src: Vertex, dest: Vertex) -> Edge:
        return self._edges.get(src.UID, {}).get(dest.UID)

    def reset(self):
        self._vertices.clear()
        self._edges.clear()
        self._outgoingEdges.clear()
        self._vertexUid: float = 0

    def canChangeMap(self, mapId, direction):
        if not self.getVertices(mapId):
            return False
        for vertex in self.getVertices(mapId).values():
            for edge in WorldGraph().getOutgoingEdgesFromVertex(vertex):
                for transition in edge.transitions:
                    if transition.direction and DirectionsEnum(transition.direction) == direction:
                        return True
        return False

    def currMapActionCells(self):
        from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
            PlayedCharacterManager,
        )

        res = []
        currVertex = PlayedCharacterManager().currVertex
        if not currVertex:
            return res
        for edge in WorldGraph().getOutgoingEdgesFromVertex(currVertex):
            for tr in edge.transitions:
                if TransitionTypeEnum(tr.type) == TransitionTypeEnum.MAP_ACTION:
                    res.append(tr.cell)
        return res
