from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class PresetUseResultMessage(NetworkMessage):
    presetId: int
    code: int

    def init(self, presetId_: int, code_: int):
        self.presetId = presetId_
        self.code = code_

        super().__init__()
