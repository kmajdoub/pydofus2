from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import (
    KernelEvent, KernelEventsManager)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.NpcDialogCreationMessage import NpcDialogCreationMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.npc.NpcDialogQuestionMessage import NpcDialogQuestionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.dialog.LeaveDialogMessage import LeaveDialogMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeLeaveMessage import ExchangeLeaveMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedMessage import ExchangeStartedMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class NpcFrame(Frame):

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def pulled(self):
        return True

    def process(self, msg) -> bool:

        if isinstance(msg, NpcDialogCreationMessage):
            KernelEventsManager().send(KernelEvent.NPC_DIALOG_OPEN, msg.mapId, msg.npcId)
            return True

        elif isinstance(msg, NpcDialogQuestionMessage):
            KernelEventsManager().send(KernelEvent.NPC_QUESTION, msg.messageId, msg.dialogParams, msg.visibleReplies)
            return True
        
        elif isinstance(msg, LeaveDialogMessage):
            if isinstance(msg, ExchangeLeaveMessage):
                KernelEventsManager().send(KernelEvent.EXCHANGE_CLOSE, msg)
                return True
            KernelEventsManager().send(KernelEvent.NPC_DIALOG_LEFT)
            return True
        
        elif isinstance(msg, ExchangeStartedMessage):
            KernelEventsManager().send(KernelEvent.EXCHANGE_OPEN, msg)
            return True
