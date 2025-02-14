from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectCreature import (
    ObjectEffectCreature,
)


class ObjectEffectLadder(ObjectEffectCreature):
    monsterCount: int

    def init(self, monsterCount_: int, monsterFamilyId_: int, actionId_: int):
        self.monsterCount = monsterCount_

        super().init(monsterFamilyId_, actionId_)
