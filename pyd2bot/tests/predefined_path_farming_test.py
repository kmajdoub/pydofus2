from unittest import skip
from com.DofusClient import DofusClient
from pyd2bot.frames.BotPhenixAutoRevive import BotPhenixAutoRevive
from pyd2bot.frames.BotWorkflowFrame import BotWorkflowFrame
from pyd2bot.frames.BotFarmPathFrame import BotFarmPathFrame
from com.ankamagames.jerakine.logger.Logger import Logger
from pyd2bot.managers.BotCredsManager import BotCredsManager
from pyd2bot.models.FarmParcours import FarmParcours

logger = Logger("Dofus2")

# Goujon path incarnam
FISHING_SKILL_ID = 124
ANKARNAM_PHENIX_MAPID = 153879809.0

bouftou_incarnam = {
    "startMapId": 153879300,
    "path": [(1, -4), (0, -4), (0, -5), (1, -5)],
    "fightOnly": True,
    "skills": [FISHING_SKILL_ID],
}

pioute_astrub = {
    "startMapId": 191104002,
    "path": [(4, -18), (4, -19), (3, -19), (3, -18), (3, -17), (4, -17), (5, -17), (5, -18)],
    "skills": [],
    "fightOnly": True,
}

goujon_incarnam = {
    "startMapId": 154010882,
    "path": [
        (-2, -2),
        (-1, -2),
        (0, -2),
        (0, -1),
        (1, -1),
        (1, 0),
        (0, 0),
        (-1, 0),
        (-2, 0),
        (-2, -1),
        (-1, -1),
        (-1, -2),
    ],
    "skills": [FISHING_SKILL_ID],
    "fightOnly": True,
}

pioute_amakna = {
    "startMapId": 88212244,
    "path": [(0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (2, 2), (1, 2), (0, 2)],
    "skills": [FISHING_SKILL_ID],
    "fightOnly": True,
}

if __name__ == "__main__":
    botName = "foobar"
    creds = BotCredsManager.getEntry(botName)
    dofus2 = DofusClient()
    BotFarmPathFrame.parcours = FarmParcours(**goujon_incarnam)
    BotPhenixAutoRevive.PHENIX_MAPID = ANKARNAM_PHENIX_MAPID
    dofus2.registerFrame(BotWorkflowFrame())
    dofus2.login(**creds)
    dofus2.join()
