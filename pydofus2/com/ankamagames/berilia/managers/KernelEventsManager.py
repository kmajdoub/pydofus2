from pydofus2.com.ankamagames.berilia.managers.EventsHandler import EventsHandler
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from enum import Enum


class KernelEvent(Enum):
    MOVEMENT_STOPPED = 0
    SERVERS_LIST = 1
    CHARACTERS_LIST = 2
    CRASH = 3
    LOGGED_IN = 4
    IN_GAME = 5
    DEAD = 6
    ALIVE = 7
    ACTORSHOWED = 8
    CHARACTER_SELECTION_SUCCESS = 9
    SHUTDOWN = 10
    RESTART = 11
    MAPLOADED = 12
    MAPPROCESSED = 13
    FRAME_PUSHED = 14
    FRAME_PULLED = 15
    RECONNECT = 16
    FIGHT_RESUMED = 17


class KernelEventsManager(EventsHandler, metaclass=Singleton):
    def __init__(self):
        super().__init__()

    def onFramePush(self, frameName, callback, args=[]):
        def onEvt(e, frame):
            if str(frame) == frameName:
                callback(*args)

        self.on(KernelEvent.FRAME_PUSHED, onEvt)

    def onceFramePushed(self, frameName, callback, args=[]):
        def onEvt(e, frame):
            if str(frame) == frameName:
                self.remove_listener(KernelEvent.FRAME_PUSHED, onEvt)
                callback(*args)

        self.on(KernelEvent.FRAME_PUSHED, onEvt)

    def send(self, event_id: KernelEvent, *args, **kwargs):
        if event_id == KernelEvent.CRASH:
            self._crashMessage = kwargs.get("message", None)
        super().send(event_id, *args, **kwargs)
