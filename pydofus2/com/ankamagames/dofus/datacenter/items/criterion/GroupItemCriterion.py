from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.utils.misc.StringUtils import \
    StringUtils


class GroupItemCriterion(IItemCriterion):

    _criteria: list[ItemCriterion]
    _operators: list[str]
    _criterionTextForm: str
    _cleanCriterionTextForm: str
    _malformated: bool
    _singleOperatorType: bool

    def __init__(self, pCriterion: str):
        super().__init__()
        self._criterionTextForm = pCriterion
        self._cleanCriterionTextForm = self._criterionTextForm
        self._malformated = False
        self._singleOperatorType = False
        if not pCriterion:
            return
        self._cleanCriterionTextForm = str.replace(self._cleanCriterionTextForm, " ", "")
        delimitedlist = StringUtils.getDelimitedText(self._cleanCriterionTextForm, "(", ")", True)
        if len(delimitedlist) > 0 and delimitedlist[0] == self._cleanCriterionTextForm:
            self._cleanCriterionTextForm = self._cleanCriterionTextForm[1:]
            self._cleanCriterionTextForm = self._cleanCriterionTextForm[:-1]
        self.split()
        self.createNewGroups()

    @classmethod
    def create(cls, pCriteria: list[ItemCriterion], pOperators: list[str]) -> "GroupItemCriterion":
        textForm = ""
        criterionIndex = 0
        operatorIndex = 0
        tabLength = len(pCriteria) + len(pOperators)

        for i in range(tabLength):
            if i % 2 == 0:
                textForm += pCriteria[criterionIndex].basicText
                criterionIndex += 1
            else:
                textForm += pOperators[operatorIndex]
                operatorIndex += 1

        return GroupItemCriterion(textForm)

    @property
    def criteria(self) -> list[ItemCriterion]:
        return self._criteria

    @property
    def inlineCriteria(self) -> list[ItemCriterion]:
        criteria = list[ItemCriterion]()
        for criterion in self._criteria:
            criteria = criteria.extend(criterion.inlineCriteria)
        return criteria

    @property
    def isRespected(self) -> bool:
        if not self._criteria:
            return True
        
        player = PlayedCharacterManager()
        
        if not player or not player.characteristics:
            Logger().error("Character or characteristics doesn't exist !, returning true")
            return True
        
        if self._criteria and len(self._criteria) == 1 and isinstance(self._criteria[0], ItemCriterion):
            return self._criteria[0].isRespected
        
        if len(self._operators) > 0 and self._operators[0] == "|":
            for criterion in self._criteria:
                if criterion.isRespected:
                    return True
            return False
        
        for criterion in self._criteria:
            if not criterion.isRespected:
                return False
            
        return True

    @property
    def text(self) -> str:
        textForm = ""
        if self._criteria == None:
            return textForm
        tabLength: int = len(self._criteria) + len(self._operators)
        criterionIndex = 0
        operatorIndex = 0
        for i in range(0, tabLength, 1):
            if textForm != "":
                textForm += " "
            if i % 2 == 0:
                textForm += self._criteria[criterionIndex]
                criterionIndex += 1
            else:
                textForm += self._operators[operatorIndex]
                operatorIndex += 1
        return textForm

    @property
    def basicText(self) -> str:
        return self._criterionTextForm

    def clone(self) -> IItemCriterion:
        return GroupItemCriterion(self.basicText)

    def createNewGroups(self) -> None:
        crit: IItemCriterion = None
        ope: str = None
        curIndex: int = 0
        exit: bool = False
        crits: list[IItemCriterion] = None
        ops: list[str] = None
        group: GroupItemCriterion = None
        if self._malformated or not self._criteria or len(self._criteria) <= 2 or self._singleOperatorType:
            return
        copyCriteria = list[ItemCriterion]()
        copyOperators = list[str]()
        for crit in self._criteria:
            copyCriteria.append(crit.clone())
        for ope in self._operators:
            copyOperators.append(ope)
        curIndex = 0
        exit = False
        while not exit:
            if len(copyCriteria) <= 2:
                exit = True
            else:
                if copyOperators[curIndex] == "&":
                    crits = list[IItemCriterion]()
                    crits.append(copyCriteria[curIndex])
                    crits.append(copyCriteria[curIndex + 1])
                    ops = [copyOperators[curIndex]]
                    group = GroupItemCriterion.create(crits, ops)
                    copyCriteria[curIndex:curIndex + 2] = [group]
                    del copyOperators[curIndex]
                    curIndex -= 1
                curIndex += 1
                if curIndex >= len(copyOperators):
                    exit = True
        self._criteria = copyCriteria
        self._operators = copyOperators
        self._singleOperatorType = self.checkSingleOperatorType(self._operators)

    def split(self) -> None:
        if not self._cleanCriterionTextForm:
            return
        searchingstr = self._cleanCriterionTextForm
        self._criteria = list[ItemCriterion]()
        self._operators = list[str]()
        andIndexes = StringUtils.getAllIndexOf("&", searchingstr)
        orIndexes = StringUtils.getAllIndexOf("|", searchingstr)
        if len(andIndexes) == 0 or len(orIndexes) == 0:
            self._singleOperatorType = True
            exit = False
            while not exit:
                criterion = self.getFirstCriterion(searchingstr)
                if not criterion:
                    indexNextCriterion = searchingstr.find("&")
                    if indexNextCriterion == -1:
                        indexNextCriterion = searchingstr.find("|")
                    if indexNextCriterion == -1:
                        searchingstr = ""
                    else:
                        searchingstr = searchingstr[indexNextCriterion + 1 :]
                else:
                    self._criteria.append(criterion)
                    index = searchingstr.index(criterion.basicText)
                    op = searchingstr[index + len(criterion.basicText) : index + 1 + len(criterion.basicText)]
                    if op:
                        self._operators.append(op)
                    searchingstr = searchingstr[index + 1 + len(criterion.basicText):]
                if not searchingstr:
                    exit = True
        else:
            exit = False
            next = 0
            while not exit:
                if not searchingstr:
                    exit = True
                elif next == 0:
                    criterion2 = self.getFirstCriterion(searchingstr)
                    if not criterion2:
                        indexNextCriterion2 = searchingstr.find("&")
                        if indexNextCriterion2 == -1:
                            indexNextCriterion2 = searchingstr.find("|")
                        if indexNextCriterion2 == -1:
                            searchingstr = ""
                        else:
                            searchingstr = searchingstr[indexNextCriterion2 + 1 :]
                    else:
                        self._criteria.append(criterion2)
                        next = 1
                        index2 = searchingstr.index(criterion2.basicText)
                        firstPart = searchingstr[0:index2]
                        secondPart = searchingstr[index2 + len(criterion2.basicText):]
                        searchingstr = firstPart + secondPart
                else:
                    operator = searchingstr[:1]
                    if not operator:
                        exit = True
                    else:
                        self._operators.append(operator)
                        next = 0
                        searchingstr = searchingstr[1:]
            self._singleOperatorType = self.checkSingleOperatorType(self._operators)
        if len(self._operators) >= len(self._criteria) and len(self._operators) > 0 and len(self._criteria) > 0:
            self._malformated = True

    def checkSingleOperatorType(self, pOperators: list[str]) -> bool:
        for op in pOperators:
            if op != pOperators[0]:
                return False
        return True

    def getFirstCriterion(self, pCriteria: str) -> ItemCriterion:
        if not pCriteria:
            return None
        
        pCriteria = str.replace(pCriteria, " ", "")
        
        if pCriteria.startswith("("):
            dl = StringUtils.getDelimitedText(pCriteria, "(", ")", True)
            criterion = GroupItemCriterion(dl[0])
        else:
            ANDindex = pCriteria.find("&")
            ORindex = pCriteria.find("|")
            
            from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionFactory import \
                ItemCriterionFactory

            if ANDindex == -1 and ORindex == -1:
                criterion = ItemCriterionFactory.create(pCriteria)
                
            elif (ANDindex < ORindex or ORindex == -1) and ANDindex != -1:
                criterion = ItemCriterionFactory.create(pCriteria.split("&")[0])
                
            else:
                criterion = ItemCriterionFactory.create(pCriteria.split("|")[0])
                
        return criterion

    @property
    def operators(self) -> list[str]:
        return self._operators
