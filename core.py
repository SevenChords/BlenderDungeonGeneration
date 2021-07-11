from enum import Enum, unique

@unique
class TileType(Enum):
    FLOOR = 1
    WALL = 2
    DOOR = 3
    FLOOR_WITH_OBJECT = 4
    WALL_WITH_OBJECT = 5

@unique
class TileDecoration(Enum):
    CLEAN = 1
    OVERGROWN = 2
    CRACKED = 3
    PUDDLE = 4
    WATER = 5

class DungeonTile:
    def __init__(self):
        self.tileType = TileType.FLOOR
        self.tileDecoration = TileDecoration.CLEAN
        self.height = 0.0
        self.display = "  "
        self.neighbors = {}
        self.x = 0
        self.y = 0
        self.visited = False
        self.width: int[2] = [1, 1]
    def __init__(self, _tileType, _tileDecoration, _height, _x, _y, _width = [1, 1]):
        self.tileType = _tileType
        self.tileDecoration = _tileDecoration
        self.height = _height
        self.display = "##"
        self.neighbors = {}
        self.x = _x
        self.y = _y
        self.visited = False
        self.width = _width
        # the following code is for debugging purposes only
        if _tileType == TileType.WALL:
            if _tileDecoration == TileDecoration.CLEAN:
                self.display = "[]"
            elif _tileDecoration == TileDecoration.OVERGROWN:
                self.display = "[?"
            else:
                self.display = "//"
        elif _tileType == TileType.FLOOR:
            if _tileDecoration == TileDecoration.CLEAN:
                self.display = "  "
            elif _tileDecoration == TileDecoration.OVERGROWN:
                self.display = " ?"
            elif _tileDecoration == TileDecoration.CRACKED:
                self.display = " /"
            elif _tileDecoration == TileDecoration.PUDDLE:
                self.display = "()"
            else:
                self.display = "~~"
        else:
            self.display = "::"