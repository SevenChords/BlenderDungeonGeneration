from core import DungeonTile
from logger import log

def generateRoom(_dimX, _dimY, _doors, _isDecorated):
    if(_dimX < 6 or dimY < 6):
        log(1, "Generator", "Room", "", "couldn't start room generation: room size too small.")
        return