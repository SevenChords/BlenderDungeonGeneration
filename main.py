from . import generateTestDungeon
from core import TileType
import bpy

class mainclass():
    dungeonarray = generateTestDungeon()

    for tile in dungeonarray.values():
        if(tile.tileType == TileType.WALL and not tile.visited):
            NameArr = []
            for neighbor in tile.neighbors.values():
                if(neighbor.tileType == TileType.WALL and neighbor.tileDecoration == tile.tileDecoration and not tile.visited):
                    bpy.ops.mesh.primitive_cube_add(align='WORLD', location=(0, 0, 0), scale=(0.5, 0.5, 2))
                    cube = bpy.context.object
                    NameArr.append(cube)

    #        for cube in NameArr:
    #            cube.select_set(True)
    #
    #        bpy.ops.object.join()
    #        bpy.ops.object.mode_set(mode = 'EDIT')
    #        bpy.ops.mesh.remove_doubles()
    #        bpy.ops.mesh.select_all(False)
    #        bpy.ops.mesh.select_interior_faces()
    #        bpy.ops.mesh.delete(type='FACE')

