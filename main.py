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
    
    def __init__(self, false, octaves, seed, min_size, max_size):
        bpy.ops.outliner.orphans_purge()
        self.dungeonarray = generateDungeon(_isDecorated=false, _octaves=octaves, _seed=seed, _minSize=min_size, _maxSize=max_size)
        self.nameArr = []
        self.minheight = self.getLowestTile()
        self.wallheight = 4
        self.stonebrick, self.stonebrick_cracked, self.stonebrick_mossy, self.water = self.texture()
        self.coordinate = {"minX": 0, "minY": 0, "maxX": 0, "maxY": 0, "maxZ": -50}
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
            if tile.x < self.coordinate["minX"]:
                self.coordinate["minX"] = tile.x
            if tile.y < self.coordinate["minY"]:
                self.coordinate["minY"] = tile.y
            if tile.x > self.coordinate["maxX"]:
                self.coordinate["maxX"] = tile.x
            if tile.y > self.coordinate["maxY"]:
                self.coordinate["maxY"] = tile.y
            if tile.tileDecoration == TileDecoration.WATER.value:
                if tile.height > self.coordinate["maxZ"]:
                    self.coordinate["maxZ"] = tile.height

        log(2, "Mesh", "", "", "sorting done")
        
        self.walls("Walls_Clean", "clean", wallDict)
        self.walls("Walls_Overgrown", "overgrown", wallDict)
        self.walls("Walls_Cracked", "cracked", wallDict)

        self.walls("Walls_W_Obj_Clean", "clean", wallObjectDict)
        self.walls("Walls_W_Obj_Overgrown", "overgrown", wallObjectDict)
        self.walls("Walls_W_Obj_Cracked", "cracked", wallObjectDict)

        log(2, "Mesh", "", "", "walls done")

        self.floor("Floor_Clean", "clean", floorDict)
        self.floor("Floor_Overgrown", "overgrown", floorDict)
        self.floor("Floor_Cracked", "cracked", floorDict)
        self.floor("Floor_Puddle", "puddle", floorDict)
        self.floor("Floor_Water", "water", floorDict)

        self.floor("Floor_W_Obj_Clean", "clean", floorObjectDict)
        self.floor("Floor_W_Obj_Overgrown", "overgrown", floorObjectDict)
        self.floor("Floor_W_Obj_Cracked", "cracked", floorObjectDict)
        self.floor("Floor_W_Obj_Puddle", "puddle", floorObjectDict)
        
        log(2, "Mesh", "", "", "floor done")

        self.doors("Door_Clean", "clean", doorDict)
        self.doors("Door_Overgrown", "overgrown", doorDict)
        self.doors("Door_Cracked", "cracked", doorDict)

        log(2, "Mesh", "", "", "door done")

        # self.water_level()

        bpy.ops.outliner.orphans_purge()              

    def getLowestTile(self):
        minZ = 3
        for tile in self.dungeonarray.values():
            if(tile.height < minZ):
                minZ = tile.height
        return minZ

    def texture(self):
        bpy.ops.image.open(directory="//images//",files=[{"name":"stonebrick.png", "name":"stonebrick.png"}, {"name":"stonebrick_cracked.png", "name":"stonebrick_cracked.png"}, {"name":"stonebrick_mossy.png", "name":"stonebrick_mossy.png"}, {"name":"water.png", "name":"water.png"}], relative_path=True)
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

        water = stonebrick.copy()
        water.name = "water"
        nodes = water.node_tree.nodes

        water_image_node = nodes.get("Image Texture")
        water_image_node.image = bpy.data.images["water.png"]

        water_BSDF = nodes.get("Principled BSDF")
        water_trans = nodes.new("ShaderNodeBsdfTransparent")
        water_mix = nodes.new("ShaderNodeMixShader")
        water_out = nodes.get("Material Output")

        water.node_tree.links.new(water_BSDF.outputs[0], water_mix.inputs[1])
        water.node_tree.links.new(water_trans.outputs[0], water_mix.inputs[2])
        water.node_tree.links.new(water_mix.outputs[0], water_out.inputs[0])

        water.blend_method = "BLEND"

        return stonebrick , stonebrick_cracked, stonebrick_mossy, water

    def walls(self, wall_name, vdict_type, dict):
        mesh = bpy.data.meshes.new(wall_name)
        wall = bpy.data.objects.new(wall_name, mesh)
        bpy.context.collection.objects.link(wall)
        bpy.context.view_layer.objects.active = wall
        wall.select_set(True)
        bm = bmesh.new()
        for tile in dict[vdict_type].values():
            for i in range(14):
                vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height + i/4))
                bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))
                vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height + (i+14)/4))
                bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))
                if i != 0:
                    vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height - i/4))
                    bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))

        for f in bm.faces:
            if(f.normal == mathutils.Vector((0,0,-1))):
                for v in f.verts:
                    v.co[2] = v.co[2] + 0.25

        bvhtree = BVHTree().FromBMesh(bm, epsilon=1e-7)
        faces = bm.faces[:]

        remove = list()
        while faces:        
            f = faces.pop()        
            pair = bvhtree.find_nearest_range(f.calc_center_median(), 1e-4)
            if len(pair) > 2:
                # mark face for removal
                remove.extend(p[2] for p in pair)
        
        bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm,geom=[bm.faces[i] for i in set(remove)],context='FACES_KEEP_BOUNDARY',)

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)

        bmesh.ops.dissolve_limit(bm, angle_limit=0.08, use_dissolve_boundaries=True, verts=bm.verts, edges=bm.edges)

        bm.to_mesh(mesh)
        bm.free()
        self.add_texture(vdict_type, wall)



    def floor(self, floor_name, vdict_type, dict):
        mesh = bpy.data.meshes.new(floor_name)
        floor = bpy.data.objects.new(floor_name, mesh)
        bpy.context.collection.objects.link(floor)
        bpy.context.view_layer.objects.active = floor
        floor.select_set(True)
        bm = bmesh.new()
        for tile in dict[vdict_type].values():
            vector = mathutils.Vector((tile.x*0.5, tile.y*0.5, tile.height))
            bmesh.ops.create_cube(bm, size=0.5, matrix=mathutils.Matrix.Translation(vector))

        for f in bm.faces:
            if(f.normal == mathutils.Vector((0,0,-1))):
                for v in f.verts:
                    v.co[2] = v.co[2] + 0.25
           

        bvhtree = BVHTree().FromBMesh(bm, epsilon=1e-7)
        faces = bm.faces[:]
        remove = list()
        while faces:        
            f = faces.pop()       
            pair = bvhtree.find_nearest_range(f.calc_center_median(), 1e-4)
            if len(pair) > 2:
                # mark face for removal
                remove.extend(p[2] for p in pair)

        bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm,geom=[bm.faces[i] for i in set(remove)],context='FACES_KEEP_BOUNDARY',)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)  

        bmesh.ops.dissolve_limit(bm, angle_limit=0.08, use_dissolve_boundaries=True, verts=bm.verts, edges=bm.edges)

        if(vdict_type == "puddle"):
            water_mesh = bpy.data.meshes.new("Water")
            water_floor = bpy.data.objects.new("Water", water_mesh)
            bpy.context.collection.objects.link(water_floor)
            bpy.context.view_layer.objects.active = water_floor
            water_floor.select_set(True)
            water_bm = bmesh.new()
            faces = bm.faces[:]
            inset = list()
            verts = list()
            while faces:
                f = faces.pop()
                if(f.normal == mathutils.Vector((0,0,1))):
                    inset.append(f)
                    for v in f.verts:
                        verts.append(water_bm.verts.new(v.co- mathutils.Vector((0,0,0.05))))
                    water_bm.faces.new(verts)
                    verts.clear()
            bmesh.ops.contextual_create(water_bm, geom=water_bm.faces)
            bmesh.ops.inset_individual(bm, faces=inset, thickness=0.2, depth=-0.1,use_even_offset=True)
            water_bm.to_mesh(water_mesh)
            water_bm.free
            self.add_texture("water_tile", water_floor)
            
        bm.to_mesh(mesh)
        bm.free()
        self.add_texture(vdict_type, floor)

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
        for f in bm.faces:
            if(f.normal == mathutils.Vector((0,0,-1))):
                for v in f.verts:
                    v.co[2] = v.co[2] + 0.25
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
        bm.to_mesh(mesh)
        bm.free()
        self.add_texture(vdict_type, door)    

    # def water_level(self):
    #     mesh = bpy.data.meshes.new("water_tile")
    #     water = bpy.data.objects.new("water_tile", mesh)        
    #     bpy.context.collection.objects.link(water)
    #     bpy.context.view_layer.objects.active = water
    #     water.select_set(True)
    #     bm = bmesh.new()
    #     bm.verts.new((self.coordinate["minX"]/2, self.coordinate["minY"]/2, self.coordinate["maxZ"]+ 0.1))
    #     bm.verts.new((self.coordinate["minX"]/2, self.coordinate["maxY"]/2, self.coordinate["maxZ"]+ 0.1))
    #     bm.verts.new((self.coordinate["maxX"]/2, self.coordinate["minY"]/2, self.coordinate["maxZ"]+ 0.1))
    #     bm.verts.new((self.coordinate["maxX"]/2, self.coordinate["maxY"]/2, self.coordinate["maxZ"]+ 0.1))
    #     bmesh.ops.contextual_create(bm, geom=bm.verts)
    #     bm.to_mesh(mesh)
    #     bm.free
    #     self.add_texture("water_tile", water)



    def add_texture(self, deco, ob):
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
        
        if(deco == "water_tile"):
            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = self.water
            else:
                # no slots
                ob.data.materials.append(self.water)               

