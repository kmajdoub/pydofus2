from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import ObjectEffect


class ObjectEffectCreature(ObjectEffect):
    monsterFamilyId: int

    def init(self, monsterFamilyId_: int, actionId_: int):
        self.monsterFamilyId = monsterFamilyId_

        super().init(actionId_)
