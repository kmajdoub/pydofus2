from pydofus2.com.ankamagames.dofus.network.types.game.mount.UpdateMountCharacteristic import UpdateMountCharacteristic


class UpdateMountBooleanCharacteristic(UpdateMountCharacteristic):
    value: bool

    def init(self, value_: bool, type_: int):
        self.value = value_

        super().init(type_)
