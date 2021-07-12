from typing import Type

from bpy.ops import image

if __package__ is None or __package__ == "":
    from core import TileDecoration, TileType
    from generator import generateDungeon
    from logger import log
else:
    from .core import TileDecoration, TileType
    from .generator import generateDungeon
    from .logger import log
import bpy
import bmesh
import mathutils

class Generation:
    
    def __init__(self):
        bpy.ops.outliner.orphans_purge()
        self.dungeonarray = generateDungeon()
        self.nameArr = []
        self.minheight = self.getLowestTile()
        self.wallheight = 4
        self.stonebrick, self.stonebrick_cracked, self.stonebrick_mossy = self.texture()
        self.generate()
        


    def generate(self):
        wallDict = {"clean": {}, "overgrown": {}, "cracked": {}}
        wallObjectDict = {"clean": {}, "overgrown": {}, "cracked": {}}
        floorDict = {"clean": {}, "overgrown": {}, "cracked": {}, "puddle": {}, "water": {}}
        floorObjectDict = {"clean": {}, "overgrown": {}, "cracked": {}, "puddle": {}}
        doorDict = {"clean": {}, "overgrown": {}, "cracked": {}}

        for tile in self.dungeonarray.values():
            if tile.tileType == TileType.WALL.value:
                if tile.tileDecoration == TileDecoration.CLEAN.value:
                    wallDict["clean"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.OVERGROWN.value:
                    wallDict["overgrown"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.CRACKED.value:
                    wallDict["cracked"][tile.x, tile.y] = tile
            if tile.tileType == TileType.WALL_WITH_OBJECT.value:
                if tile.tileDecoration == TileDecoration.CLEAN.value:
                    wallObjectDict["clean"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.OVERGROWN.value:
                    wallObjectDict["overgrown"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.CRACKED.value:
                    wallObjectDict["cracked"][tile.x, tile.y] = tile
            if tile.tileType == TileType.FLOOR.value:
                if tile.tileDecoration == TileDecoration.CLEAN.value:
                    floorDict["clean"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.OVERGROWN.value:
                    floorDict["overgrown"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.CRACKED.value:
                    floorDict["cracked"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.PUDDLE.value:
                    floorDict["puddle"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.WATER.value:
                    floorDict["water"][tile.x, tile.y] = tile
            if tile.tileType == TileType.FLOOR_WITH_OBJECT.value:
                if tile.tileDecoration == TileDecoration.CLEAN.value:
                    floorObjectDict["clean"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.OVERGROWN.value:
                    floorObjectDict["overgrown"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.CRACKED.value:
                    floorObjectDict["cracked"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.PUDDLE.value:
                    floorObjectDict["puddle"][tile.x, tile.y] = tile
            if tile.tileType == TileType.DOOR.value:
                if tile.tileDecoration == TileDecoration.CLEAN.value:
                    doorDict["clean"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.OVERGROWN.value:
                    doorDict["overgrown"][tile.x, tile.y] = tile
                if tile.tileDecoration == TileDecoration.CRACKED.value:
                    doorDict["cracked"][tile.x, tile.y] = tile

        log(2, "Mesh", "", "", "sorting done")
        
        mesh = bpy.data.meshes.new('Walls_Clean')
        walls_clean = bpy.data.objects.new("Walls_Clean", mesh)
        bpy.context.collection.objects.link(walls_clean)
        bpy.context.view_layer.objects.active = walls_clean
        walls_clean.select_set(True)
        bm = bmesh.new()
        for tile in wallDict["clean"].values():
            for i in range(7):
                vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height + i/2))
                bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
        bm.to_mesh(mesh)
        bm.free()
            
        log(2, "Mesh", "", "", "clean walls done")

        # for tile in self.dungeonarray.values():
        #     if(not tile.visited):
        #         self.recursion(tile)

        #         if(tile.tileDecoration == TileDecoration.PUDDLE.value):
        #             ob = bpy.context.object
        #             bpy.ops.object.mode_set(mode = 'EDIT')
        #             bpy.ops.mesh.select_mode(type="VERT")
        #             bpy.ops.mesh.select_all(action = 'DESELECT')
        #             bpy.ops.object.mode_set(mode = 'OBJECT')
        #             for i, v in enumerate(ob.data.vertices):
        #                 if(v.co[2] > 0):
        #                     v.select = True
        #             bpy.ops.object.mode_set(mode = 'EDIT') 
        #             bpy.ops.mesh.inset(thickness=0.2, depth=-0.1, release_confirm=True)
        #             bpy.ops.object.mode_set(mode = 'OBJECT')
        #         self.nameArr = []
        #         bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')                      
        #bpy.ops.outliner.orphans_purge()


    def recursion(self, tile):
        if(tile.tileType == TileType.WALL.value):
            bpy.ops.mesh.primitive_cube_add(align="WORLD", location=(0.5 * tile.x, 0.5 * tile.y, tile.height + self.wallheight/2 - 0.25), scale=(0.5, 0.5, self.wallheight))
            bpy.ops.mesh.primitive_cube_add(align='WORLD', location=(0.5 * tile.x, 0.5 * tile.y, tile.height - 1.75 + 0.5 * self.wallheight), scale=(0.5, 0.5, self.wallheight))
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Wall"           

        if(tile.tileType == TileType.WALL_WITH_OBJECT.value):
            bpy.ops.mesh.primitive_cube_add(align="WORLD", location=(0.5 * tile.x, 0.5 * tile.y, tile.height + self.wallheight/2 - 0.25), scale=(0.5, 0.5, self.wallheight))
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Wall"

        if(tile.tileType == TileType.FLOOR.value):
            if(tile.height == self.minheight):
                bpy.ops.mesh.primitive_cube_add(align="WORLD", location=(0.5 * tile.x, 0.5 * tile.y, tile.height), scale=(0.5, 0.5, 0.5))
            else:
                bpy.ops.mesh.primitive_cube_add(align="WORLD", location=(0.5 * tile.x, 0.5 * tile.y,  tile.height), scale=(0.5, 0.5, 0.5))
            
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Floor"

        if(tile.tileType == TileType.FLOOR_WITH_OBJECT.value):
            bpy.ops.mesh.primitive_cube_add(align="WORLD", location=(0.5 * tile.x, 0.5 * tile.y,tile.height), scale=(0.5, 0.5, 0.5))
            tile.visited = True
            cube = bpy.context.object
            cube.name = "Floor"
        

        ob = bpy.context.active_object
        if(tile.tileDecoration == TileDecoration.CLEAN.value or tile.tileDecoration == TileDecoration.PUDDLE.value):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.stonebrick
            else:
                # no slots
                ob.data.materials.append(self.stonebrick)

        if(tile.tileDecoration == TileDecoration.CRACKED.value):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.stonebrick_cracked
            else:
                # no slots
                ob.data.materials.append(self.stonebrick_cracked)

        if(tile.tileDecoration == TileDecoration.OVERGROWN.value or tile.tileDecoration == TileDecoration.WATER.value):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.stonebrick_mossy
            else:
                # no slots
                ob.data.materials.append(self.stonebrick_mossy)            


    def getLowestTile(self):
        minZ = 3
        for tile in self.dungeonarray.values():
            if(tile.height < minZ):
                minZ = tile.height
        return minZ

    def texture(self):
        bpy.ops.image.open(directory="//images//",files=[{"name":"stonebrick.png", "name":"stonebrick.png"}, {"name":"stonebrick_cracked.png", "name":"stonebrick_cracked.png"}, {"name":"stonebrick_mossy.png", "name":"stonebrick_mossy.png"}], relative_path=True)
        stonebrick = bpy.data.materials.new("stonebrick")
        stonebrick.use_nodes = True
        nodes = stonebrick.node_tree.nodes

        stonebrick_bsdf = nodes.get("Principled BSDF")

        stonebrick_image_node = nodes.new("ShaderNodeTexImage")
        stonebrick_image_node.image = bpy.data.images["stonebrick.png"]
        stonebrick_image_node.projection = "BOX"
        
        stonebrick_geometry_node = nodes.new("ShaderNodeNewGeometry")

        stonebrick_mapping_node = nodes.new("ShaderNodeMapping")
        stonebrick_mapping_node.inputs[3].default_value[0] = 2
        stonebrick_mapping_node.inputs[3].default_value[1] = 2
        stonebrick_mapping_node.inputs[3].default_value[2] = 2

        stonebrick.node_tree.links.new(stonebrick_geometry_node.outputs[0], stonebrick_mapping_node.inputs[0])
        stonebrick.node_tree.links.new(stonebrick_mapping_node.outputs[0], stonebrick_image_node.inputs[0])
        stonebrick.node_tree.links.new(stonebrick_image_node.outputs[0], stonebrick_bsdf.inputs[0])

        stonebrick_cracked = bpy.data.materials.new("stonebrick_cracked")
        stonebrick_cracked = stonebrick.copy()
        nodes = stonebrick_cracked.node_tree.nodes

        stonebrick_cracked_image_node = nodes.get("Image Texture")
        stonebrick_cracked_image_node.image = bpy.data.images["stonebrick_cracked.png"]
    
        stonebrick_mossy = bpy.data.materials.new("stonebrick_mossy")
        stonebrick_mossy = stonebrick.copy()
        nodes = stonebrick_mossy.node_tree.nodes

        stonebrick_mossy_image_node = nodes.get("Image Texture")
        stonebrick_mossy_image_node.image = bpy.data.images["stonebrick_mossy.png"]
        

        return stonebrick , stonebrick_cracked, stonebrick_mossy

        




        




        
        



