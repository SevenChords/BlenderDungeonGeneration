from typing import Dict
from perlin_noise import PerlinNoise as pn
if __package__ is None or __package__ == "":
    from core import DungeonTile, TileType
    from logger import log
else:
    from .core import DungeonTile, TileType
    from .logger import log
from random import randint
from sys import maxsize

def generateRoom(_dimX = 7, _dimY = 7, _doors = [False, False, False, False], _isDecorated = True, _octaves = 1, _seed = 0, _heightOffset = 0, _xOffset = 0, _yOffset = 0, _room = True):

    while(_dimX < 6 or _dimY < 6) and _room:
        log(3, "Generator", "Room", "", "couldn't start room generation: room size too small. Increasing Roomsize...")
        if(_dimX < _dimY):
            _dimX += 1
        else:
            _dimY += 1

    if _seed == 0:
        _seed = randint(1, maxsize)
    
    noise = pn(_octaves, _seed)
    heightLayer = [[noise([i/_dimX, j/_dimY]) for j in range(_dimY)] for i in range(_dimX)]
    minHeight = min([min(line) for line in heightLayer])
    maxHeight = max([max(line) for line in heightLayer])
    scale = 10/(maxHeight-minHeight)
    if _room:
        for i in range(_dimX):
            for j in range(_dimY):
                heightLayer[i][j] -= minHeight
                heightLayer[i][j] *= scale
                heightLayer[i][j] = round(heightLayer[i][j], 0)/4 + _heightOffset
    else:
        for i in range(_dimX):
            for j in range(_dimY):
                heightLayer[i][j] = _heightOffset
    log(4, "Generator", "Room", "", "height layer generated")
    log(5, "Generator", "Room", "", str(heightLayer))

    noise = pn(_octaves, abs(_seed - maxsize) + 1)
    decorationLayer = [[noise([i/_dimX, j/_dimY]) for j in range(_dimY)] for i in range(_dimX)]
    minDecoration = min([min(line) for line in decorationLayer])
    maxDecoration = max([max(line) for line in decorationLayer])
    scale = 3/(maxDecoration-minDecoration)
    for i in range(_dimX):
        for j in range(_dimY):
            decorationLayer[i][j] -= minDecoration
            decorationLayer[i][j] *= scale
            decorationLayer[i][j] = int(round(decorationLayer[i][j], 0) + 1)
    log(4, "Generator", "Room", "", "decoration layer generated")
    log(5, "Generator", "Room", "", str(decorationLayer))

    noise = pn(_octaves, abs(_seed - int(round(maxsize/2, 0))) + 1)
    typeLayer = [[noise([i/_dimX, j/_dimY]) for j in range(_dimY)] for i in range(_dimX)]
    minType = min([min(line) for line in typeLayer])
    maxType = max([max(line) for line in typeLayer])
    scale = 3/(maxType-minType)
    if _isDecorated:
        for i in range(_dimX):
            for j in range(_dimY):
                typeLayer[i][j] -= minType
                typeLayer[i][j] *= scale
                typeLayer[i][j] = int(round(typeLayer[i][j], 0))
                if typeLayer[i][j] < 3:
                    typeLayer[i][j] = 1
                else:
                    typeLayer[i][j] = 4
    else:
        for i in range(_dimX):
            for j in range(_dimY):
                typeLayer[i][j] = 1

    doorHeights = [0, 0, 0, 0]
    doorWidths = [0, 0, 0, 0]

    if _doors[0]:
        if _dimY % 2 == 0:
            typeLayer[0][int(round(_dimY/2, 0))] = 3
            typeLayer[0][int(round(_dimY/2 - 1, 0))] = 3
            heightLayer[0][int(round(_dimY/2, 0))] = heightLayer[1][int(round(_dimY/2, 0))]
            heightLayer[0][int(round(_dimY/2 - 1, 0))] = heightLayer[0][int(round(_dimY/2, 0))]
            doorHeights[0] = heightLayer[1][int(round(_dimY/2, 0))]
            doorWidths[0] = 2
        else:
            typeLayer[0][int(round(_dimY/2 + 0.5, 0))] = 3
            typeLayer[0][int(round(_dimY/2 - 0.5, 0))] = 3
            typeLayer[0][int(round(_dimY/2 - 1.5, 0))] = 3
            heightLayer[0][int(round(_dimY/2 - 0.5, 0))] = heightLayer[1][int(round(_dimY/2 - 0.5, 0))]
            heightLayer[0][int(round(_dimY/2 + 0.5, 0))] = heightLayer[0][int(round(_dimY/2 - 0.5, 0))]
            heightLayer[0][int(round(_dimY/2 - 1.5, 0))] = heightLayer[0][int(round(_dimY/2 - 0.5, 0))]
            doorHeights[0] = heightLayer[1][int(round(_dimY/2 - 0.5, 0))]
            doorWidths[0] = 3
    if _doors[1]:
        if _dimX % 2 == 0:
            typeLayer[int(round(_dimX/2, 0))][_dimY - 1] = 3
            typeLayer[int(round(_dimX/2 - 1, 0))][_dimY - 1] = 3
            heightLayer[int(round(_dimX/2, 0))][_dimY - 1] = heightLayer[int(round(_dimX/2, 0))][_dimY - 2]
            heightLayer[int(round(_dimX/2 - 1, 0))][_dimY - 1] = heightLayer[int(round(_dimX/2, 0))][_dimY - 1]
            doorHeights[1] = heightLayer[int(round(_dimX/2, 0))][_dimY - 2]
            doorWidths[1] = 2
        else:
            typeLayer[int(round(_dimX/2 + 0.5, 0))][_dimY - 1] = 3
            typeLayer[int(round(_dimX/2 - 0.5, 0))][_dimY - 1] = 3
            typeLayer[int(round(_dimX/2 - 1.5, 0))][_dimY - 1] = 3
            heightLayer[int(round(_dimX/2 - 0.5, 0))][_dimY - 1] = heightLayer[int(round(_dimX/2 - 0.5, 0))][_dimY - 2]
            heightLayer[int(round(_dimX/2 + 0.5, 0))][_dimY - 1] = heightLayer[int(round(_dimX/2 - 0.5, 0))][_dimY - 1]
            heightLayer[int(round(_dimX/2 - 1.5, 0))][_dimY - 1] = heightLayer[int(round(_dimX/2 - 0.5, 0))][_dimY - 1]
            doorHeights[1] = heightLayer[int(round(_dimX/2 - 0.5, 0))][_dimY - 2]
            doorWidths[1] = 3
    if _doors[2]:
        if _dimY % 2 == 0:
            typeLayer[_dimX - 1][int(round(_dimY/2, 0))] = 3
            typeLayer[_dimX - 1][int(round(_dimY/2 - 1, 0))] = 3
            heightLayer[_dimX - 1][int(round(_dimY/2, 0))] = heightLayer[_dimX - 2][int(round(_dimY/2, 0))]
            heightLayer[_dimX - 1][int(round(_dimY/2 - 1, 0))] = heightLayer[_dimX - 1][int(round(_dimY/2, 0))]
            doorHeights[2] = heightLayer[_dimX - 2][int(round(_dimY/2, 0))]
            doorWidths[2] = 2
        else:
            typeLayer[_dimX - 1][int(round(_dimY/2 + 0.5, 0))] = 3
            typeLayer[_dimX - 1][int(round(_dimY/2 - 0.5, 0))] = 3
            typeLayer[_dimX - 1][int(round(_dimY/2 - 1.5, 0))] = 3
            heightLayer[_dimX - 1][int(round(_dimY/2 - 0.5, 0))] = heightLayer[_dimX - 2][int(round(_dimY/2 - 0.5, 0))]
            heightLayer[_dimX - 1][int(round(_dimY/2 + 0.5, 0))] = heightLayer[_dimX - 1][int(round(_dimY/2 - 0.5, 0))]
            heightLayer[_dimX - 1][int(round(_dimY/2 - 1.5, 0))] = heightLayer[_dimX - 1][int(round(_dimY/2 - 0.5, 0))]
            doorHeights[2] = heightLayer[_dimX - 2][int(round(_dimY/2 - 0.5, 0))]
            doorWidths[2] = 3
    if _doors[3]:
        if _dimX % 2 == 0:
            typeLayer[int(round(_dimX/2, 0))][0] = 3
            typeLayer[int(round(_dimX/2 - 1, 0))][0] = 3
            heightLayer[int(round(_dimX/2, 0))][0] = heightLayer[int(round(_dimX/2, 0))][1]
            heightLayer[int(round(_dimX/2 - 1, 0))][0] = heightLayer[int(round(_dimX/2, 0))][0]
            doorHeights[3] = heightLayer[int(round(_dimX/2, 0))][1]
            doorWidths[3] = 2
        else:
            typeLayer[int(round(_dimX/2 + 0.5, 0))][0] = 3
            typeLayer[int(round(_dimX/2 - 0.5, 0))][0] = 3
            typeLayer[int(round(_dimX/2 - 1.5, 0))][0] = 3
            heightLayer[int(round(_dimX/2 - 0.5, 0))][0] = heightLayer[int(round(_dimX/2 - 0.5, 0))][1]
            heightLayer[int(round(_dimX/2 + 0.5, 0))][0] = heightLayer[int(round(_dimX/2 - 0.5, 0))][0]
            heightLayer[int(round(_dimX/2 - 1.5, 0))][0] = heightLayer[int(round(_dimX/2 - 0.5, 0))][0]
            doorHeights[3] = heightLayer[int(round(_dimX/2 - 0.5, 0))][1]
            doorWidths[3] = 3

    for i in range(_dimX):
        for j in range(_dimY):
            if (i == 0 or j == 0):
                if typeLayer[i][j] == 1:
                    typeLayer[i][j] = 2
                if typeLayer[i][j] == 4:
                    typeLayer[i][j] = 5
                if decorationLayer[i][j] == 4:
                    decorationLayer[i][j] = 1
            if (i == _dimX - 1 or j == _dimY - 1):
                if typeLayer[i][j] == 1:
                    typeLayer[i][j] = 2
                if typeLayer[i][j] == 4:
                    typeLayer[i][j] = 5
                if decorationLayer[i][j] == 4:
                    decorationLayer[i][j] = 1
            if heightLayer[i][j] <= 0.5:
                if typeLayer[i][j] == 4:
                    typeLayer[i][j] = 1
                if typeLayer[i][j] == 1:
                    decorationLayer[i][j] = 5
    log(4, "Generator", "Room", "", "type layer generated")
    log(5, "Generator", "Room", "", str(typeLayer))

    roomDict = {}
    for i in range(_dimX):
        for j in range(_dimY):
            roomDict[i + _xOffset, j + _yOffset] = DungeonTile(typeLayer[i][j], decorationLayer[i][j], heightLayer[i][j], i + _xOffset, j + _yOffset)
    
    log(4, "Generator", "Room", "", "room dict created")

    return {"room": roomDict, "doorHeights": doorHeights, "doorWidths": doorWidths}

def generateBridge(_isDecorated = False, _octaves = 1, _seed = 0, _vertical = False, _width1 = 2, _width2 = 2, _xOffset = 0, _yOffset = 0, _height = 0, _length = 5):
    if _seed == 0:
        _seed = randint(1, maxsize)

    bridgeDict: DungeonTile = {}

    if _vertical:
        bridgeDict.update(generateRoom(_length, 5, [True, False, True, False], _isDecorated, _octaves, _seed, _height, _xOffset, _yOffset, False)["room"])
        if _width1 == 2:
            bridgeDict[_xOffset, _yOffset + 3].tileType = TileType.WALL.value
        if _width2 == 2:
            bridgeDict[_xOffset + _length - 1, _yOffset + 3].tileType = TileType.WALL
    else:
        bridgeDict.update(generateRoom(5, _length, [False, True, False, True], _isDecorated, _octaves, _seed, _height, _xOffset, _yOffset, False)["room"])
        if _width1 == 2:
            bridgeDict[_xOffset + 3, _yOffset].tileType = TileType.WALL.value
        if _width2 == 2:
            bridgeDict[_xOffset + 3, _yOffset + _length - 1].tileType = TileType.WALL
    
    return {"room": bridgeDict}

def offsetHeight(_dungeon, _offset):
    for tile in _dungeon["room"].values():
        tile.height += _offset
    for i in range(4):
        _dungeon["doorHeights"][i] += _offset
    return _dungeon

def generateDungeon(_isDecorated = True, _octaves = 1, _seed = 0, _minSize = 15, _maxSize = 30):
    if _seed == 0:
        _seed = randint(1, maxsize)

    log(2, "Generator", "", "", "Seed: " + str(_seed))

    if _minSize < 7:
        _minSize = 7
    if _maxSize < 7:
        _maxSize = 7

    noise = pn(_octaves, abs(_seed - int(round(maxsize/2, 0))) + 1)
    sizes = [noise(i/10) for i in range(10)]
    minSize = min(sizes)
    maxSize = max(sizes)
    for i in range(10):
        sizes[i] = int(round((sizes[i]-minSize)*(_maxSize-_minSize)/(maxSize-minSize), 0) + _minSize)

    dungeon = {}

    bridgeLengths = [5, 5, 5, 5]
    while sizes[2] > (sizes[4] + 2 * bridgeLengths[0]):
        bridgeLengths[0] += 1
    while sizes[1] > (sizes[5] + 2 * bridgeLengths[2]):
        bridgeLengths[2] += 1
    while sizes[6] > (sizes[4] + 2 * bridgeLengths[3]):
        bridgeLengths[3] += 1
    while sizes[9] > (sizes[5] + 2 * bridgeLengths[1]):
        bridgeLengths[1] += 1

    offsets = {}
    offsets[2, 0] = 0
    offsets[2, 1] = 0
    offsets[5, 0] = offsets[2, 0] - (bridgeLengths[0] - 1)
    offsets[5, 1] = offsets[2, 1] + int(round((sizes[5] - 5)/2, 0))
    offsets[0, 0] = offsets[5, 0] - (sizes[0] - 1)
    offsets[0, 1] = offsets[5, 1] - int(round((sizes[1] - 5)/2, 0))
    offsets[6, 0] = offsets[2, 0] + int(round((sizes[4] - 5)/2, 0))
    offsets[6, 1] = offsets[2, 1] - (bridgeLengths[1] - 1)
    offsets[1, 0] = offsets[6, 0] - int(round((sizes[2] - 5)/2, 0))
    offsets[1, 1] = offsets[6, 1] - (sizes[3] - 1)
    offsets[7, 0] = offsets[2, 0] + int(round((sizes[4] - 5)/2, 0))
    offsets[7, 1] = offsets[2, 1] + (sizes[5] - 1)
    offsets[3, 0] = offsets[7, 0] - int(round((sizes[6] - 5)/2, 0))
    offsets[3, 1] = offsets[7, 1] + (bridgeLengths[2] - 1)
    offsets[8, 0] = offsets[2, 0] + (sizes[4] - 1)
    offsets[8, 1] = offsets[2, 1] + int(round((sizes[5] - 5)/2, 0))
    offsets[4, 0] = offsets[8, 0] + (bridgeLengths[3] - 1)
    offsets[4, 1] = offsets[8, 1] - int(round((sizes[9] - 5)/2, 0))
    
    result = {}
    result[0] = generateRoom(sizes[0], sizes[1], [False, False, True , False], _isDecorated, _octaves, _seed, 0, offsets[0, 0], offsets[0, 1], True)
    result[2] = generateRoom(sizes[4], sizes[5], [True , True , True , True ], _isDecorated, _octaves, _seed, 0, offsets[2, 0], offsets[2, 1], True)
    while result[0]["doorHeights"][2] > result[2]["doorHeights"][0]:
        result[2] = offsetHeight(result[2], 1)
    while result[0]["doorHeights"][2] < result[2]["doorHeights"][0]:
        result[0] = offsetHeight(result[0], 1)
    result[5] = generateBridge(_isDecorated, _octaves, _seed, True , result[0]["doorWidths"][2], result[2]["doorWidths"][0], offsets[5, 0], offsets[5, 1], result[0]["doorHeights"][2], bridgeLengths[0])
    result[1] = generateRoom(sizes[2], sizes[3], [False, True , False, False], _isDecorated, _octaves, _seed, 0, offsets[1, 0], offsets[1, 1], True)
    while result[1]["doorHeights"][1] > result[2]["doorHeights"][3]:
        result[1] = offsetHeight(result[1], -1)
    while result[1]["doorHeights"][1] < result[2]["doorHeights"][3]:
        result[1] = offsetHeight(result[1], 1)
    result[6] = generateBridge(_isDecorated, _octaves, _seed, False, result[1]["doorWidths"][1], result[2]["doorWidths"][3], offsets[6, 0], offsets[6, 1], result[1]["doorHeights"][1], bridgeLengths[1])
    result[3] = generateRoom(sizes[6], sizes[7], [False, False, False, True ], _isDecorated, _octaves, _seed, 0, offsets[3, 0], offsets[3, 1], True)
    while result[3]["doorHeights"][3] > result[2]["doorHeights"][1]:
        result[3] = offsetHeight(result[3], -1)
    while result[3]["doorHeights"][3] < result[2]["doorHeights"][1]:
        result[3] = offsetHeight(result[3], 1)
    result[7] = generateBridge(_isDecorated, _octaves, _seed, False, result[2]["doorWidths"][1], result[3]["doorWidths"][3], offsets[7, 0], offsets[7, 1], result[2]["doorHeights"][1], bridgeLengths[2])
    result[4] = generateRoom(sizes[8], sizes[9], [True , False, False, False], _isDecorated, _octaves, _seed, 0, offsets[4, 0], offsets[4, 1], True)
    while result[4]["doorHeights"][0] > result[2]["doorHeights"][2]:
        result[4] = offsetHeight(result[4], -1)
    while result[4]["doorHeights"][0] < result[2]["doorHeights"][2]:
        result[4] = offsetHeight(result[4], 1)
    result[8] = generateBridge(_isDecorated, _octaves, _seed, True , result[2]["doorWidths"][2], result[4]["doorWidths"][0], offsets[8, 0], offsets[8, 1], result[2]["doorHeights"][2], bridgeLengths[3])

    for i in range(9):
        dungeon.update(result[i]["room"])

    for tile in dungeon.values():
        i = -1
        while(i <= 1):
            j = -1
            while(j <= 1):
                tempTile = dungeon.get((tile.x + i, tile.y + j))
                if(tempTile):
                    tile.neighbors[i, j] = dungeon[tile.x + i, tile.y + j]
                j += 1
                if(i == 0 and j == 0):
                    j += 1
            i += 1

    return dungeon

generateDungeon()