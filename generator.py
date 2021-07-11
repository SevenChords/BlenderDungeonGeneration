from perlin_noise import PerlinNoise as pn
from core import DungeonTile
from logger import log
from random import randint
from sys import maxsize

def generateRoom(_dimX = 7, _dimY = 7, _doors = [False, False, False, False], _isDecorated = True, _octaves = 1, _seed = 0, _heightOffset = 0, _xOffset = 0, _yOffset = 0):

    while _dimX < 6 or _dimY < 6:
        log(3, "Generator", "Room", "", "couldn't start room generation: room size too small. Increasing Roomsize...")
        if(_dimX < _dimY):
            _dimX += 1
        else:
            _dimY += 1
    
    if _octaves == 7:
        _octaves += 1

    if _seed == 0:
        _seed = randint(1, maxsize)
    
    noise = pn(_octaves, _seed)
    heightLayer = [[noise([i/_dimX, j/_dimY]) for j in range(_dimY)] for i in range(_dimX)]
    minHeight = min([min(line) for line in heightLayer])
    maxHeight = max([max(line) for line in heightLayer])
    scale = 10/(maxHeight-minHeight)
    for i in range(_dimX):
        for j in range(_dimY):
            heightLayer[i][j] -= minHeight
            heightLayer[i][j] *= scale
            heightLayer[i][j] = round(heightLayer[i][j], 0)/2 + _heightOffset
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
    if _doors[0]:
        if _dimY % 2 == 0:
            typeLayer[0][_dimY/2] = 3
            typeLayer[0][_dimY/2 - 1] = 3
        else:
            typeLayer[0][_dimY/2 + 0.5] = 3
            typeLayer[0][_dimY/2 - 0.5] = 3
            typeLayer[0][_dimY/2 - 1.5] = 3
    if _doors[1]:
        if _dimX % 2 == 0:
            typeLayer[_dimX/2][_dimY - 1] = 3
            typeLayer[_dimX/2 - 1][_dimY - 1] = 3
        else:
            typeLayer[_dimX/2 + 0.5][_dimY - 1] = 3
            typeLayer[_dimX/2 - 0.5][_dimY - 1] = 3
            typeLayer[_dimX/2 - 1.5][_dimY - 1] = 3
    if _doors[2]:
        if _dimY % 2 == 0:
            typeLayer[_dimX - 1][_dimY/2] = 3
            typeLayer[_dimX - 1][_dimY/2 - 1] = 3
        else:
            typeLayer[_dimX - 1][_dimY/2 + 0.5] = 3
            typeLayer[_dimX - 1][_dimY/2 - 0.5] = 3
            typeLayer[_dimX - 1][_dimY/2 - 1.5] = 3
    if _doors[3]:
        if _dimX % 2 == 0:
            typeLayer[_dimX/2][0] = 3
            typeLayer[_dimX/2 - 1][0] = 3
        else:
            typeLayer[_dimX/2 + 0.5][0] = 3
            typeLayer[_dimX/2 - 0.5][0] = 3
            typeLayer[_dimX/2 - 1.5][0] = 3
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
            if heightLayer[i][j] <= 1.0:
                if typeLayer[i][j] == 4:
                    typeLayer[i][j] = 1
                if typeLayer[i][j] == 1:
                    decorationLayer[i][j] = 5
    log(4, "Generator", "Room", "", "type layer generated")
    log(5, "Generator", "Room", "", str(typeLayer))

    roomDict = {}
    for i in range(_dimX):
        for j in range(_dimY):
            roomDict[i, j] = DungeonTile(typeLayer[i][j], decorationLayer[i][j], heightLayer[i][j], i + _xOffset, j + _yOffset)
    
    log(4, "Generator", "Room", "", "room dict created")

    return roomDict
