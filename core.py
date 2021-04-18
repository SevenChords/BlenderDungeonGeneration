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
    def __init__(self, _tileType, _tileDecoration, _height):
        self.tileType = _tileType
        self.tileDecoration = _tileDecoration
        self.height = _height
        self.display = "##"
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

def generateTestDungeon():
    dungeonArray = {}
    for i in range(7):
        for j in range(7):
            if i == 0:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.CLEAN, 1.0)
                elif j <= 3:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.OVERGROWN, 1.0)
                elif j <= 5:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.CRACKED, 1.0)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.CLEAN, 1.0)
            elif i <= 2:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CLEAN, 1.0)
                elif j <= 4:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.OVERGROWN, 1.0)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CRACKED, 1.0)
            elif i <= 4:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.PUDDLE, 1.0)
                elif j <= 4:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR_WITH_OBJECT, TileDecoration.CLEAN, 1.5)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.WATER, 0.5)
            else:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CLEAN, 1.0)
                elif j <= 4:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.OVERGROWN, 1.0)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CRACKED, 1.0)
    for i in range(7):
        toPrint = ""
        for j in range(7):
            toPrint = toPrint + dungeonArray[i, j].display
        print(toPrint)
    return dungeonArray

testDungeon = generateTestDungeon()