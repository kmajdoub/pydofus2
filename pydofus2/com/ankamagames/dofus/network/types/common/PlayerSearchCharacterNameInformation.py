from pydofus2.com.ankamagames.dofus.network.types.common.AbstractPlayerSearchInformation import (
    AbstractPlayerSearchInformation,
)


class PlayerSearchCharacterNameInformation(AbstractPlayerSearchInformation):
    name: str

    def init(self, name_: str):
        self.name = name_

        super().init()
