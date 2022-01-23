
import math


class Point:
    def __init__(self, x, y):    
        self.x = x
        self.y = y
        
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
class MapPoint:
    RIGHT = 0
    DOWN_RIGHT = 1
    DOWN = 2
    DOWN_LEFT = 3
    LEFT = 4
    UP_LEFT = 5
    UP = 6
    UP_RIGHT = 7
    MAP_WIDTH = 14
    MAP_HEIGHT = 20
    CELLPOS = dict[int, Point]()
    VECTOR_RIGHT = Point(1, 1)
    VECTOR_DOWN_RIGHT = Point(1, 0)
    VECTOR_DOWN = Point(1, -1)
    VECTOR_DOWN_LEFT = Point(0, -1)
    VECTOR_LEFT = Point(-1, -1)
    VECTOR_UP_LEFT = Point(-1, 0)
    VECTOR_UP = Point(-1, 1)
    VECTOR_UP_RIGHT = Point(0, 1)
    _bInit = False
    _nCellId = None
    _nX = None
    _nY = None
    
    @staticmethod
    def fromCellId(cellId:int):
        mp = MapPoint()
        mp._nCellId = cellId
        mp.setFromCellId()
        return mp

    @staticmethod
    def fromCoords(x:int, y:int):
        mp = MapPoint()
        mp._nX = x
        mp._nY = y
        mp.setFromCoords()
        return mp

    @staticmethod
    def getOrientationsDistance(i1:int, i2:int) -> int:
        return min(abs(i2 - i1), abs(8 - i2 + i1))

    @staticmethod
    def isInMap(i1:int, i2:int):
        return i1 + i2 >= 0 and i1 - i2 >= 0 and i1 - i2 < MapPoint.MAP_HEIGHT * 2 and i1 + i2 < MapPoint.MAP_WIDTH * 2

    def init(self):
        self._bInit = True
        i1 = 0
        i2 = 0
        i3 = 0
        for i in range(self.MAP_HEIGHT):
            for j in range(self.MAP_WIDTH):
                self.CELLPOS[i3] = Point(i1 + j, i2 + j)
                i3+=1
            i1+=1
            for j in range(self.MAP_WIDTH):
                self.CELLPOS[i3] = Point(i1 + j, i2 + j)
                i3+=1
            i2-=1
    
    @property
    def cellID(self) -> int:
        return self._nCellId

    @cellID.setter
    def cellId(self, i:int):
        self._nCellId = i
        self.setFromCellId()

    @property
    def x(self) -> int:
        return self._nX

    @x.setter
    def x(self, i:int): 
        self._nX = i
        self.setFromCoords()
    
    @property
    def y(self) -> int: 
        return self._nY
    
    @y.setter
    def y(self, i:int):
        self._nY = i
        self.setFromCoords()
    
    def getCoordinates(self) -> Point:
        return Point(self._nX, self._nY)
    
    def distanceTo(self, mp:'MapPoint') -> int:
        return math.sqrt((self.y - mp.y)**2 + (self.y - mp.y)**2)
    
    def distanceToCell(self, mp:'MapPoint'):
        return abs(self.y - mp.y) + abs(self.y - mp.y)
    
    def orientationTo(self, mp:'MapPoint'):
        if mp.x > self.x:
            if mp.y > self.y:
                return self.DOWN_RIGHT
            elif mp.y < self.y:
                return self.UP_RIGHT
            else:
                return self.RIGHT
        elif mp.x < self.x:
            if mp.y > self.y:
                return self.DOWN_LEFT
            elif mp.y < self.y:
                return self.UP_LEFT
            else:
                return self.LEFT
        else:
            if mp.y > self.y:
                return self.DOWN
            elif mp.y < self.y:
                return self.UP
            else:
                return -1
        
    def advancedOrientationTo(self, mp:'MapPoint', b:bool) -> int:
        if mp == None:
            return 0
        i1 = mp.x - self.x
        i2 = self.y - mp.y
        i3 = math.acos(i1 / math.sqrt(math.pow(i1, 2) + math.pow(i2, 2))) * 180 / math.pi * (-1 if mp.y > self.y else 1)
        if b:
            i3 = round(i3 / 90) * 2 + 1
        else:
            i3 = round(i3 / 45) + 1
        if i3 < 0:
            i3 += 8
        return i3 

    def pointSymetry(self, mp:'MapPoint') -> 'MapPoint': 
        i1 = 2 * mp.x - self.x
        i2 = 2 * mp.y - self.y
        if self.isInMap(i1, i2):
            return MapPoint.fromCoords(i1, i2)
        return None
    
    def __eq__(self, mp:'MapPoint') -> bool:
        return self._nCellId == mp._nCellId 

    def __str__(self): 
        return "[MapPoint(x:" + self.x + ", y:" + self.y + ", id:" + self.cellID + ")]"

    def setFromCoords(self): 
        if not self._bInit:
            self.init()
        self._nCellId = (self.x - self.y) * self.MAP_WIDTH + self.y + (self.x - self.y) / 2
    
    def setFromCellId(self): 
        if not self._bInit:
            self.init()
        p = self.CELLPOS[self._nCellId]
        if p is None:
            raise Exception("Cell identifier out of bound.")
        self._nX = p.x
        self._nY = p.y
