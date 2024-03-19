import locale
import sys
import threading
import traceback
from datetime import datetime
from time import perf_counter
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.atouin.HaapiEventsManager import \
    HaapiEventsManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import \
    ElementsAdapter
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.berilia.managers.Listener import Listener
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import \
    DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.frames.MiscFrame import \
    MiscFrame
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import \
    LoginValidationWithTokenAction as LVA_WithToken
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import \
    AuthentificationManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiEvent import HaapiEvent
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import \
    HaapiKeyManager
from pydofus2.com.ankamagames.jerakine.data.ModuleReader import ModuleReader
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.messages.TerminateWorkerMessage import \
    TerminateWorkerMessage
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import \
    AdapterFactory
from pydofus2.Zaap.ZaapDecoy import ZaapDecoy

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
    from pydofus2.com.ankamagames.jerakine.network.ServerConnection import \
        ServerConnection

# Set the locale to the locale identifier associated with the current language
# The '.UTF-8' suffix specifies the character encoding
locale.setlocale(locale.LC_ALL, Kernel().getLocaleLang() + ".UTF-8")


class DofusClient(threading.Thread):
    APIKEY_NOT_FOUND = 36363
    UNEXPECTED_CLIENT_ERROR = 36364
    lastLoginTime = None
    minLoginInterval = 60 * 3
    LOGIN_TIMEOUT = 35

    def __init__(self, name="DofusClient"):
        super().__init__(name=name)
        self._registredInitFrames = []
        self._registredGameStartFrames = []
        self._lock = None
        self._apikey = None
        self._accountId = None
        self._chatToken = None
        self._certId = ""
        self._certHash = ""
        self._serverId = 0
        self._characterId = None
        self._loginToken = None
        self._mule = False
        self._shutDownReason = None
        self._crashed = False
        self._shutDownMessage = ""
        self._reconnectRecord = []
        self._shutDownListeners = []
        self.kernel = None
        self.terminated = threading.Event()

    def initListeners(self):
        KernelEventsManager().once(
            KernelEvent.CharacterSelectedSuccessfully,
            self.onCharacterSelectionSuccess,
            originator=self,
        )
        KernelEventsManager().onceMapProcessed(self.onInGame)
        KernelEventsManager().onMultiple(
            [
                (KernelEvent.SelectedServerRefused, self.onServerSelectionRefused),
                (KernelEvent.ClientCrashed, self.crash),
                (KernelEvent.ClientShutdown, self.shutdown),
                (KernelEvent.ClientRestart, self.onRestart),
                (KernelEvent.ClientReconnect, self.onReconnect),
                (KernelEvent.ClientClosed, self.onConnectionClosed),
                (KernelEvent.PlayerLoggedIn, self.onloginSuccess),
                (KernelEvent.CharacterImpossibleSelection, self.onCharacterImpossibleSelection),
                (KernelEvent.FightStarted, self.onFight),  
                (KernelEvent.HaapiApiKeyReady, self.onHaapiApiKeyReady)
            ],
            originator=self
        )

    @property
    def worker(self):
        return Kernel().worker

    def init(self):
        Logger().info("Initializing ...")
        self.zaap = ZaapDecoy()
        self.kernel = Kernel()
        self.kernel.init()
        self.registerInitFrame(MiscFrame)
        AdapterFactory.addAdapter("ele", ElementsAdapter)
        # AdapterFactory.addAdapter("dlm", MapsAdapter)
        self.kernel.isMule = self._mule
        ModuleReader._clearObjectsCache = True
        self._shutDownReason = None
        self.initListeners()
        Logger().info("Initialized")

    def setApiKey(self, apiKey):
        self._apikey = apiKey

    def setLoginToken(self, token):
        self._loginToken = token

    def setCertificate(self, certId, certHash):
        self._certId = certId
        self._certHash = certHash
        
    def setAutoServerSelection(self, serverId, characterId=None):
        self._serverId = serverId
        self._characterId = characterId

    def registerInitFrame(self, frame: "Frame"):
        self._registredInitFrames.append(frame)

    def registerGameStartFrame(self, frame: "Frame"):
        self._registredGameStartFrames.append(frame)

    def onCharacterSelectionSuccess(self, event, return_value):
        Logger().info("Adding game start frames")
        for frame in self._registredGameStartFrames:
            self.worker.addFrame(frame())

    def onInGame(self):
        Logger().info("Character entered game server successfully")

    def crash(self, event, message, reason=DisconnectionReasonEnum.EXCEPTION_THROWN):
        self._crashed = True
        self._shutDownReason = reason
        self.shutdown(message, reason)

    def onRestart(self, event, message):
        Logger().debug(f"Restart requested by event {event} for reason: {message}")
        self.onReconnect(event, message)

    def onLoginTimeout(self, listener: Listener):
        self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))
        listener.armTimer()
        self.lastLoginTime = perf_counter()

    def onFight(self, event):
        pass
    
    def onHaapiApiKeyReady(self, event, apikey):
        pass

    def onloginSuccess(self, event, ismsg):
        HaapiKeyManager().on(HaapiEvent.GameSessionReadyEvent, self.onGameSessionReady)
        Haapi().getLoadingScreen(page=1, accountId=PlayerManager().accountId, lang="en", count=20)
        Haapi().getAlmanaxEvent(lang="en")
        Haapi().getCmsFeeds(site="DOFUS", page=0, lang="en", count=20, apikey=self._apikey)
        HaapiKeyManager().askToken(GameID.CHAT)

    def onGameSessionReady(self, event, gameSessionId):
        Haapi().game_sessionId = gameSessionId
        HaapiEventsManager().sendStartEvent(gameSessionId)
        
    def onCharacterImpossibleSelection(self, event):
        self.shutdown(
            DisconnectionReasonEnum.EXCEPTION_THROWN,
            f"Character {self._characterId} impossible to select in server {self._serverId}!",
        )

    def onServerSelectionRefused(self, event, serverId, err_type, server_status, error_text, selectableServers):            
        self._shutDownReason = f"Server selection refused for reason : {error_text}"
        self._crashed = True
        self.shutdown(DisconnectionReasonEnum.EXCEPTION_THROWN, error_text)

    def onConnectionClosed(self, event, connId):
        pass

    def prepareLogin(self):
        PlayedCharacterManager().instanceId = self.name
        if self._characterId:
            PlayerManager().allowAutoConnectCharacter = True
            PlayedCharacterManager().id = int(self._characterId)
            PlayerManager().autoConnectOfASpecificCharacterId = int(self._characterId)
        Logger().info("Adding game start frames")
        for frame in self._registredInitFrames:
            self.worker.addFrame(frame())
        if not self._loginToken:
            if self._apikey is None:
                return self.shutdown(
                    reason=DisconnectionReasonEnum.EXCEPTION_THROWN,
                    message="Unable to login for reason : No apikey and certificate or login token provided!",
                )
            self._loginToken = self.zaap.getLoginToken(GameID.DOFUS, self._certId, self._certHash, self._apikey)
            if self._loginToken is None:
                return self.shutdown(
                    reason=DisconnectionReasonEnum.EXCEPTION_THROWN,
                    message="Unable to login for reason : Unable to generate login token!",
                )
        AuthentificationManager().setToken(self._loginToken)
        self.waitNextLogin()
        self._loginToken = None

    def onReconnect(self, event, message, afterTime=0):
        Logger().warning(f"Reconnect requested for reason: {message}")
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self._reconnectRecord.append({"restartTime": formatted_time, "reason": message})
        Kernel().reset(reloadData=True)
        if afterTime:
            self.terminated.wait(afterTime)
        self.initListeners()
        self.prepareLogin()
        self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))

    def waitNextLogin(self):
        if DofusClient.lastLoginTime is not None:
            diff = DofusClient.minLoginInterval - (perf_counter() - DofusClient.lastLoginTime)
            if diff > 0:
                Logger().info(f"ave to wait {diff}sec before reconnecting again")
                self.terminated.wait(diff)
        self.lastLoginTime = perf_counter()

    def shutdown(self, message="", reason=None):
        self._shutDownReason = reason if reason else DisconnectionReasonEnum.WANTED_SHUTDOWN
        self._shutDownMessage = message if message else "Wanted shutdown"
        if self.kernel:
            Logger().info(f"Shutting down client {self.name} for reason : {self._shutDownReason}")
            self.kernel.worker.process(TerminateWorkerMessage())
        else:
            Logger().warning("Kernel is not running, kernel running instances : " + str(Kernel._instances))
        return

    def addShutDownListener(self, callback):
        self._shutDownListeners.append(callback)

    @property
    def connection(self) -> "ServerConnection":
        return ConnectionsHandler().conn

    @property
    def registeredInitFrames(self) -> list:
        return self._registredInitFrames

    @property
    def registeredGameStartFrames(self) -> list:
        return self._registredGameStartFrames

    def run(self):
        try:
            self.init()
            self.prepareLogin()
            self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))
            self.worker.run()
        except Exception as e:
            _, exc_value, exc_traceback = sys.exc_info()
            traceback_in_var = traceback.format_tb(exc_traceback)
            # Start with the current exception's traceback
            error_trace = "\n".join(traceback_in_var) + "\n" + str(exc_value)
            # Check for and add traceback from the cause, if any
            cause = e.__cause__
            while cause:
                cause_traceback = traceback.format_tb(cause.__traceback__)
                error_trace += "\n\n-- Chained Exception --\n"
                error_trace += "\n".join(cause_traceback) + "\n" + str(cause)
                cause = cause.__cause__
            self._shutDownMessage = error_trace
            self._crashed = True
            self._shutDownReason = DisconnectionReasonEnum.EXCEPTION_THROWN

        if self._shutDownReason != DisconnectionReasonEnum.WANTED_SHUTDOWN:
            Logger().error(f"Crashed for reason : {self._shutDownReason} :\n{self._shutDownMessage}")

        if Haapi().game_sessionId:
            HaapiEventsManager().sendEndEvent()
        Kernel().reset()
        Logger().info("goodby crual world")
        self.terminated.set()
        for callback in self._shutDownListeners:
            Logger().info(f"Calling shutdown callback {callback}")
            callback(self.name, self._shutDownMessage, self._shutDownReason)