from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.GameRolePlayNamedActorInformations import (
    GameRolePlayNamedActorInformations,
)

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
        EntityDispositionInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.HumanInformations import HumanInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook


class GameRolePlayHumanoidInformations(GameRolePlayNamedActorInformations):
    humanoidInfo: "HumanInformations"
    accountId: int

    def init(
        self,
        humanoidInfo_: "HumanInformations",
        accountId_: int,
        name_: str,
        look_: "EntityLook",
        contextualId_: int,
        disposition_: "EntityDispositionInformations",
    ):
        self.humanoidInfo = humanoidInfo_
        self.accountId = accountId_

        super().init(name_, look_, contextualId_, disposition_)
