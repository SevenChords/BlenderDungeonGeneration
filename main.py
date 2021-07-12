from typing import Type
from bmesh.types import BMVert

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
from mathutils.bvhtree import BVHTree

class Generation:
    
    def __init__(self):
        bpy.ops.outliner.orphans_purge()
        self.dungeonarray = generateDungeon(_seed = 5216211572811331767)
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
        
        self.walls("Walls_Clean", "clean", wallDict)
        self.walls("Walls_Overgrown", "overgrown", wallDict)
        self.walls("Walls_Cracked", "cracked", wallDict)

        self.walls("Walls_W_Obj_Clean", "clean", wallObjectDict)
        self.walls("Walls_W_Obj_Overgrown", "overgrown", wallObjectDict)
        self.walls("Walls_W_Obj_Cracked", "cracked", wallObjectDict)

        log(2, "Mesh", "", "", "walls done")

        self.floors("Floor_Clean", "clean", floorDict)
        self.floors("Floor_Overgrown", "overgrown", floorDict)
        self.floors("Floor_Cracked", "cracked", floorDict)
        self.floors("Floor_Puddle", "puddle", floorDict)
        self.floors("Floor_Water", "water", floorDict)

        self.floors("Floor_W_Obj_Clean", "clean", floorObjectDict)
        self.floors("Floor_W_Obj_Overgrown", "overgrown", floorObjectDict)
        self.floors("Floor_W_Obj_Cracked", "cracked", floorObjectDict)
        self.floors("Floor_W_Obj_Puddle", "puddle", floorObjectDict)
        
        log(2, "Mesh", "", "", "floor done")

        self.doors("Door_Clean", "clean", doorDict)
        self.doors("Door_Overgrown", "overgrown", doorDict)
        self.doors("Door_Cracked", "cracked", doorDict)



        bpy.ops.outliner.orphans_purge()              

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
        stonebrick_image_node.interpolation = "Closest"
        
        stonebrick_geometry_node = nodes.new("ShaderNodeNewGeometry")

        stonebrick_mapping_node = nodes.new("ShaderNodeMapping")
        stonebrick_mapping_node.inputs[3].default_value[0] = 2
        stonebrick_mapping_node.inputs[3].default_value[1] = 2
        stonebrick_mapping_node.inputs[3].default_value[2] = 2

        stonebrick.node_tree.links.new(stonebrick_geometry_node.outputs[0], stonebrick_mapping_node.inputs[0])
        stonebrick.node_tree.links.new(stonebrick_mapping_node.outputs[0], stonebrick_image_node.inputs[0])
        stonebrick.node_tree.links.new(stonebrick_image_node.outputs[0], stonebrick_bsdf.inputs[0])

        stonebrick_cracked = stonebrick.copy()
        stonebrick_cracked.name = "stonebrick_cracked"
        nodes = stonebrick_cracked.node_tree.nodes

        stonebrick_cracked_image_node = nodes.get("Image Texture")
        stonebrick_cracked_image_node.image = bpy.data.images["stonebrick_cracked.png"]
    
        stonebrick_mossy = stonebrick.copy()
        stonebrick_mossy.name = "stonebrick_mossy"
        nodes = stonebrick_mossy.node_tree.nodes

        stonebrick_mossy_image_node = nodes.get("Image Texture")
        stonebrick_mossy_image_node.image = bpy.data.images["stonebrick_mossy.png"]
        

        return stonebrick , stonebrick_cracked, stonebrick_mossy

    def walls(self, wall_name, vdict_type, dict):
        mesh = bpy.data.meshes.new(wall_name)
        wall = bpy.data.objects.new(wall_name, mesh)
        bpy.context.collection.objects.link(wall)
        bpy.context.view_layer.objects.active = wall
        wall.select_set(True)
        bm = bmesh.new()
        for tile in dict[vdict_type].values():
            for i in range(7):
                vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height + i/2))
                bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
        bm.to_mesh(mesh)
        bm.free()
        self.add_texture(vdict_type)

    def floors(self, floor_name, vdict_type, dict):
        mesh = bpy.data.meshes.new(floor_name)
        floor = bpy.data.objects.new(floor_name, mesh)
        bpy.context.collection.objects.link(floor)
        bpy.context.view_layer.objects.active = floor
        floor.select_set(True)
        bm = bmesh.new()
        for tile in dict[vdict_type].values():
            vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height))
            bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
        bmesh.utils.face_join(bm.faces, True)
        bm.to_mesh(mesh)
        bm.free()
        self.add_texture(vdict_type)

    def doors(self, door_name, vdict_type, dict):
        mesh = bpy.data.meshes.new(door_name)
        door = bpy.data.objects.new(door_name, mesh)
        bpy.context.collection.objects.link(door)
        bpy.context.view_layer.objects.active = door
        door.select_set(True)
        bm = bmesh.new()
        for tile in dict[vdict_type].values():
            vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height))
            bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
        bm.to_mesh(mesh)
        bm.free()
        self.add_texture(vdict_type)    



    def add_texture(self, deco):
        ob = bpy.context.active_object
        if(deco == "clean" or deco == "puddle"):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.stonebrick
            else:
                # no slots
                ob.data.materials.append(self.stonebrick)

        if(deco == "cracked"):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.stonebrick_cracked
            else:
                # no slots
                ob.data.materials.append(self.stonebrick_cracked)

        if(deco == "overgrown" or deco == "water"):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.stonebrick_mossy
            else:
                # no slots
                ob.data.materials.append(self.stonebrick_mossy)              

