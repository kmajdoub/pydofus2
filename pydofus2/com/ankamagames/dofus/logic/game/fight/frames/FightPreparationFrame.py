from typing import TYPE_CHECKING
from pydofus2.com.ankamagames.atouin.utils.DataMapProvider import DataMapProvider
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameContextKickAction import GameContextKickAction
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightPlacementPositionRequestAction import (
    GameFightPlacementPositionRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightPlacementSwapPositionsAcceptAction import (
    GameFightPlacementSwapPositionsAcceptAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightPlacementSwapPositionsCancelAction import (
    GameFightPlacementSwapPositionsCancelAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightPlacementSwapPositionsRequestAction import (
    GameFightPlacementSwapPositionsRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.GameFightReadyAction import GameFightReadyAction
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.RemoveEntityAction import RemoveEntityAction

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import FightEntitiesFrame

    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import (
        FightContextFrame,
    )

from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SwapPositionRequest import SwapPositionRequest
from pydofus2.com.ankamagames.dofus.network.enums.TeamEnum import TeamEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightEndMessage import GameFightEndMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightLeaveMessage import (
    GameFightLeaveMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementPositionRequestMessage import (
    GameFightPlacementPositionRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementPossiblePositionsMessage import (
    GameFightPlacementPossiblePositionsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsAcceptMessage import (
    GameFightPlacementSwapPositionsAcceptMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsCancelledMessage import (
    GameFightPlacementSwapPositionsCancelledMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsCancelMessage import (
    GameFightPlacementSwapPositionsCancelMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsErrorMessage import (
    GameFightPlacementSwapPositionsErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsMessage import (
    GameFightPlacementSwapPositionsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsOfferMessage import (
    GameFightPlacementSwapPositionsOfferMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsRequestMessage import (
    GameFightPlacementSwapPositionsRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightRemoveTeamMemberMessage import (
    GameFightRemoveTeamMemberMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightUpdateTeamMessage import (
    GameFightUpdateTeamMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextDestroyMessage import (
    GameContextDestroyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextKickMessage import GameContextKickMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameEntitiesDispositionMessage import (
    GameEntitiesDispositionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameEntityDispositionErrorMessage import (
    GameEntityDispositionErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.idol.IdolFightPreparationUpdateMessage import (
    IdolFightPreparationUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.entities.messages.EntityClickMessage import EntityClickMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

class FightPreparationFrame(Frame):

    PLAYER_TEAM_ALPHA: float = 1

    ENEMY_TEAM_ALPHA: float = 0.3

    SELECTION_CHALLENGER: str = "FightPlacementChallengerTeam"

    SELECTION_DEFENDER: str = "FightPlacementDefenderTeam"

    _fightContextFrame: "FightContextFrame"

    _playerTeam: int

    _challengerPositions: list[int]

    _defenderPositions: list[int]

    _swapPositionRequests: list[SwapPositionRequest] = []

    _fightersId: list[float]

    def __init__(self, fightContextFrame: "FightContextFrame"):
        super().__init__()
        self._fightContextFrame = fightContextFrame

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def fightersList(self) -> list[float]:
        return self._fightersId

    def pushed(self) -> bool:
        self._fightContextFrame.entitiesFrame.untargetableEntities = True
        DataMapProvider().isInFight = True
        self._swapPositionRequests = list[SwapPositionRequest]()
        self._fightersId = list[float]()
        return True

    def updateSwapPositionRequestsIcons(self) -> None:
        swapPositionRequest = None
        for swapPositionRequest in self._swapPositionRequests:
            pass

    def setSwapPositionRequestsIconsVisibility(self, pVisible: bool) -> None:
        swapPositionRequest: SwapPositionRequest = None
        for swapPositionRequest in self._swapPositionRequests:
            pass

    def removeSwapPositionRequest(self, pRequestId: int) -> None:
        swapPositionRequest: SwapPositionRequest = None
        for swapPositionRequest in self._swapPositionRequests:
            if swapPositionRequest.requestId == pRequestId:
                del self._swapPositionRequests[self._swapPositionRequests.index(swapPositionRequest)]

    def isSwapPositionRequestValid(self, pRequestId: int) -> bool:
        swapPositionRequest: SwapPositionRequest = None
        for swapPositionRequest in self._swapPositionRequests:
            if swapPositionRequest.requestId == pRequestId:
                return True
        return False

    def process(self, msg: Message) -> bool:
        alreadyInTeam: bool = False
        indexOfCharToRemove: int = 0

        if isinstance(msg, GameFightLeaveMessage):
            gflmsg = msg
            if gflmsg.charId == PlayedCharacterManager().id:
                PlayedCharacterManager().fightId = -1
                Kernel().worker.removeFrame(self)
                gfemsg = GameFightEndMessage()
                gfemsg.init()
                fightContextFrame2: "FightContextFrame" = Kernel().worker.getFrameByName("FightContextFrame")
                if fightContextFrame2:
                    fightContextFrame2.process(gfemsg)
                else:
                    Kernel().worker.process(gfemsg)
                return True
            fighterSwapPositionRequests = self.getPlayerSwapPositionRequests(gflmsg.charId)
            for swapPositionRequest in fighterSwapPositionRequests:
                swapPositionRequest.destroy()
            return False

        if isinstance(msg, GameFightPlacementPossiblePositionsMessage):
            gfpppmsg = msg
            self._playerTeam = gfpppmsg.teamNumber
            return True

        if isinstance(msg, GameFightPlacementPositionRequestAction):
            gfppra = msg
            if not self._fightContextFrame.onlyTheOtherTeamCanPlace:
                gfpprmsg2 = GameFightPlacementPositionRequestMessage()
                gfpprmsg2.init(gfppra.cellId)
                ConnectionsHandler().send(gfpprmsg2)
            return True

        if isinstance(msg, GameEntitiesDispositionMessage) or isinstance(msg, GameFightPlacementSwapPositionsMessage):
            for iedi in msg.dispositions:
                entitySwapPositionsRequests = self.getPlayerSwapPositionRequests(iedi.id)
                for swapPositionRequest in entitySwapPositionsRequests:
                    swapPositionRequest.destroy()
            return False

        if isinstance(msg, GameFightPlacementSwapPositionsRequestAction):
            gfpspra = msg
            gfpsprmsg = GameFightPlacementSwapPositionsRequestMessage()
            gfpsprmsg.init(gfpspra.requestedId, gfpspra.cellId)
            ConnectionsHandler().send(gfpsprmsg)
            return True

        if isinstance(msg, GameFightPlacementSwapPositionsOfferMessage):
            gfpspomsg = msg
            entitiesFrame = Kernel().worker.getFrameByName("FightEntitiesFrame")
            swapPositionRequest = SwapPositionRequest(
                gfpspomsg.requestId, gfpspomsg.requesterId, gfpspomsg.requestedId
            )
            if swapPositionRequest.requestedId == PlayedCharacterManager().id:
                self._swapPositionRequests.append(swapPositionRequest)
            elif swapPositionRequest.requesterId == PlayedCharacterManager().id:
                self._swapPositionRequests.append(swapPositionRequest)
            return True

        if isinstance(msg, GameFightPlacementSwapPositionsErrorMessage):
            return True

        if isinstance(msg, GameFightPlacementSwapPositionsAcceptAction):
            gfpspaa = msg
            gfpspamsg = GameFightPlacementSwapPositionsAcceptMessage()
            gfpspamsg.init(gfpspaa.requestId)
            ConnectionsHandler().send(gfpspamsg)
            return True

        if isinstance(msg, GameFightPlacementSwapPositionsCancelAction):
            gfpspca = msg
            gfpspcmsg = GameFightPlacementSwapPositionsCancelMessage()
            gfpspcmsg.init(gfpspca.requestId)
            ConnectionsHandler().send(gfpspcmsg)
            return True

        if isinstance(msg, GameFightPlacementSwapPositionsCancelledMessage):
            gfpspcdmsg = msg
            swapPositionRequest = self.getSwapPositionRequest(gfpspcdmsg.requestId)
            if swapPositionRequest:
                swapPositionRequest.destroy()
                if (
                    swapPositionRequest.requesterId == PlayedCharacterManager().id
                    and gfpspcdmsg.cancellerId != PlayedCharacterManager().id
                ):
                    entitiesFrame = Kernel().worker.getFrameByName("FightEntitiesFrame")
                    entitiesFrame.getEntityInfos(gfpspcdmsg.cancellerId)
            return True

        if isinstance(msg, GameEntityDispositionErrorMessage):
            Logger().error("Cette position n'est pas accessible.")
            return True

        if isinstance(msg, EntityClickMessage):
            ecmsg = msg
            clickedEntity = ecmsg.entity
            if clickedEntity:
                entitiesFrame = Kernel().worker.getFrameByName("FightEntitiesFrame")
                fighterInfos = entitiesFrame.getEntityInfos(clickedEntity.id)
                playerInfos = entitiesFrame.getEntityInfos(PlayedCharacterManager().id)
                if not (
                    fighterInfos
                    and playerInfos
                    and fighterInfos.contextualId != playerInfos.contextualId
                    and fighterInfos.spawnInfo.teamId == playerInfos.spawnInfo.teamId
                ):
                    return True
            return True

        if isinstance(msg, GameContextKickAction):
            gcka = msg
            gckmsg = GameContextKickMessage()
            gckmsg.init(gcka.targetId)
            ConnectionsHandler().send(gckmsg)
            return True

        if isinstance(msg, GameFightUpdateTeamMessage):
            gfutmsg = msg
            gfutmsg_myId = PlayedCharacterManager().id
            alreadyInTeam = False
            for teamMember in gfutmsg.team.teamMembers:
                if teamMember.id == gfutmsg_myId:
                    alreadyInTeam = True
                if teamMember.id not in self._fightersId:
                    self._fightersId.append(teamMember.id)
            if alreadyInTeam or len(gfutmsg.team.teamMembers) >= 1 and gfutmsg.team.teamMembers[0].id == gfutmsg_myId:
                PlayedCharacterManager().teamId = gfutmsg.team.teamId
                self._fightContextFrame.isFightLeader = gfutmsg.team.leaderId == gfutmsg_myId
            return True

        if isinstance(msg, GameFightRemoveTeamMemberMessage):
            gfrtmmsg = msg
            self._fightContextFrame.entitiesFrame.process(RemoveEntityAction.create(gfrtmmsg.charId))
            if gfrtmmsg.charId in self._fightersId:
                self._fightersId.remove(gfrtmmsg.charId)
            return True

        if isinstance(msg, GameContextDestroyMessage):
            gfemsg2 = GameFightEndMessage()
            gfemsg2.init()
            fightContextFrame: "FightContextFrame" = Kernel().worker.getFrameByName("FightContextFrame")
            if fightContextFrame:
                fightContextFrame.process(gfemsg2)
            else:
                Kernel().worker.process(gfemsg2)
            return False

        if isinstance(msg, IdolFightPreparationUpdateMessage):
            return True

        else:
            return False

    def pulled(self) -> bool:
        swapPositionRequest: SwapPositionRequest = None
        DataMapProvider().isInFight = False
        self.removeSelections()
        for swapPositionRequest in self._swapPositionRequests:
            swapPositionRequest.destroy()
        return True

    def removeSelections(self) -> None:
        pass

    def isValidPlacementCell(self, cellId: int, team: int) -> bool:
        mapPoint: MapPoint = MapPoint.fromCellId(cellId)
        if not DataMapProvider().pointMov(mapPoint.x, mapPoint.y, False):
            return False
        validCells: list[int] = list[int]()
        if team == TeamEnum.TEAM_CHALLENGER:
            validCells = self._challengerPositions
        if team == TeamEnum.TEAM_DEFENDER:
            validCells = self._defenderPositions
        if team == TeamEnum.TEAM_SPECTATOR:
            return False
        if validCells:
            for vc in validCells:
                if vc == cellId:
                    return True
        return False

    def getSwapPositionRequest(self, pRequestId: int) -> SwapPositionRequest:
        swapPositionRequest: SwapPositionRequest = None
        for swapPositionRequest in self._swapPositionRequests:
            if swapPositionRequest.requestId == pRequestId:
                return swapPositionRequest
        return None

    def getPlayerSwapPositionRequests(self, pPlayerId: float) -> list[SwapPositionRequest]:
        swapPositionRequest: SwapPositionRequest = None
        swapPositionRequests: list[SwapPositionRequest] = list[SwapPositionRequest]()
        for swapPositionRequest in self._swapPositionRequests:
            if swapPositionRequest.requesterId == pPlayerId or swapPositionRequest.requestedId == pPlayerId:
                swapPositionRequests.append(swapPositionRequest)
        return swapPositionRequests
