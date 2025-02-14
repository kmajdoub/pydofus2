from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristic import (
    CharacterCharacteristic,
)


class CharacterCharacteristicValue(CharacterCharacteristic):
    total: int

    def init(self, total_: int, characteristicId_: int):
        self.total = total_

        super().init(characteristicId_)
