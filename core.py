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
    def __init__(self, _tileType, _tileDecoration, _height, _x, _y):
        self.tileType = _tileType
        self.tileDecoration = _tileDecoration
        self.height = _height
        self.display = "##"
        self.neighbors = {}
        self.x = _x
        self.y = _y
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
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.CLEAN, 1.0, i, j)
                elif j <= 3:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.OVERGROWN, 1.0, i, j)
                elif j <= 5:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.CRACKED, 1.0, i, j)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.WALL, TileDecoration.CLEAN, 1.0, i, j)
            elif i <= 2:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CLEAN, 1.0, i, j)
                elif j <= 4:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.OVERGROWN, 1.0, i, j)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CRACKED, 1.0, i, j)
            elif i <= 4:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.PUDDLE, 1.0, i, j)
                elif j <= 4:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR_WITH_OBJECT, TileDecoration.CLEAN, 1.5, i, j)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.WATER, 0.5, i, j)
            else:
                if j <= 1:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CLEAN, 1.0, i, j)
                elif j <= 4:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.OVERGROWN, 1.0, i, j)
                else:
                    dungeonArray[i, j] = DungeonTile(TileType.FLOOR, TileDecoration.CRACKED, 1.0, i, j)

    for tile in dungeonArray.values():
        i = -1
        while(i <= 1):
            j = -1
            while(j <= 1):
                tempTile = dungeonArray.get((tile.x + i, tile.y + j))
                if(tempTile):
                    tile.neighbors[i, j] = dungeonArray[tile.x + i, tile.y + j]
                j += 1
                if(i == 0 and j == 0):
                    j += 1
            i += 1

    for i in range(7):
        toPrint = ""
        for j in range(7):
            toPrint = toPrint + dungeonArray[i, j].display
        print(toPrint)
    return dungeonArray