from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import Preset
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import Preset
    


class PresetsContainerPreset(Preset):
    presets:list['Preset']
    

    def init(self, presets_:list['Preset'], id_:int):
        self.presets = presets_
        
        super().init(id_)
    