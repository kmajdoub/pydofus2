from pydofus2.com.ankamagames.dofus.network.types.game.interactive.skill.SkillActionDescription import \
    SkillActionDescription


class SkillActionDescriptionCraft(SkillActionDescription):
    probability: int
    def init(self, probability_: int, skillId_: int):
        self.probability = probability_
        
        super().init(skillId_)
    