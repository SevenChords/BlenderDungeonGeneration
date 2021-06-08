from typing import Type

from .core import TileDecoration, generateTestDungeon, TileType
import bpy

class Generation:
    
    def __init__(self):
        self.dungeonarray = generateTestDungeon()
        self.nameArr = []
        self.minheight = self.getLowestTile()
        self.wallheight = 4
        self.generate()
        


    def generate(self):
        for tile in self.dungeonarray.values():
            if(not tile.visited):
                self.recursion(tile)

                if(len(self.nameArr) > 1):
                    for cube in self.nameArr:
                        cube.select_set(True)
                    bpy.ops.object.join()
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.mesh.select_all(False)
                    bpy.ops.mesh.select_interior_faces()
                    bpy.ops.mesh.delete(type='FACE')
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.modifier_add(type='DECIMATE')
                    bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
                    bpy.context.object.modifiers["Decimate"].delimit = {'NORMAL'}
                    bpy.ops.object.modifier_apply(modifier="Decimate")

                if(tile.tileDecoration == TileDecoration.PUDDLE):
                    ob = bpy.context.object
                    for i, v in enumerate(ob.data.vertices):
                        if(v.co[2] > 0):
                            v.select = True
                    bpy.ops.object.mode_set(mode = 'EDIT') 
                    bpy.ops.mesh.inset(thickness=0.2, depth=-0.1, release_confirm=True)
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                self.nameArr = []
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')                      
        bpy.ops.outliner.orphans_purge()


    def recursion(self, tile):
        if(tile.tileType == TileType.WALL):
            bpy.ops.mesh.primitive_cube_add(align='WORLD', location=(0.5 * tile.x, 0.5 * tile.y, tile.height - 1.75 + 0.5 * self.wallheight), scale=(0.5, 0.5, self.wallheight))
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Wall"
            self.nameArr.append(cube)

            for neighbor in tile.neighbors.values():
                if(neighbor.tileType == TileType.WALL and neighbor.tileDecoration == tile.tileDecoration and not neighbor.visited):
                    self.recursion(neighbor)

        if(tile.tileType == TileType.FLOOR):
            if(tile.height == self.minheight):
                bpy.ops.mesh.primitive_cube_add(align='WORLD', location=(0.5 * tile.x, 0.5 * tile.y, tile.height - 1), scale=(0.5, 0.5, 0.5))
            else:
                bpy.ops.mesh.primitive_cube_add(align='WORLD', location=(0.5 * tile.x, 0.5 * tile.y, 0.5 * (tile.height - 1) - self.minheight/2), scale=(0.5, 0.5, 0.5 + tile.height - self.minheight))
            
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Floor"
            self.nameArr.append(cube)

            for neighbor in tile.neighbors.values():
                if(neighbor.tileType == TileType.FLOOR and neighbor.tileDecoration == tile.tileDecoration and not neighbor.visited):
                    self.recursion(neighbor)

        if(tile.tileType == TileType.FLOOR_WITH_OBJECT):
            bpy.ops.mesh.primitive_cube_add(align='WORLD', location=(0.5 * tile.x, 0.5 * tile.y, 0.5 *  (tile.height - 1) - self.minheight/2), scale=(0.5, 0.5, 0.5 + tile.height - self.minheight))
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Floor"
            self.nameArr.append(cube)

            for neighbor in tile.neighbors.values():
                if(neighbor.tileType == TileType.FLOOR_WITH_OBJECT and neighbor.tileDecoration == tile.tileDecoration and not neighbor.visited):
                    self.recursion(neighbor)          


    def getLowestTile(self):
        minZ = 3
        for tile in self.dungeonarray.values():
            if(tile.height < minZ):
                minZ = tile.height
        return minZ



        
        



