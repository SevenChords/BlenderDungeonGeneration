from sys import maxsize
from generator import generateRoom
import bpy

bl_info = {
    "name": "Dun_Gen",
    "author": "Jonathan, Vincent & Oliver",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "category": "Add Mesh",
    "location": "UI Panel",
    "description": "Generates a random dungeon the size of the input parameters.",
    "warning": "",
    "doc_url": "",
    "tracker_url": ""
}

class MESH_OT_DunGen(bpy.types.Operator):
    """Create a random dungeon"""
    bl_idname = "mesh.dungeon_generator"
    bl_label = "Dungeon Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    min_size: bpy.props.IntProperty(
        name="Min room size",
        description="Smallest room size that shall be generated",
        default=10,
        min=7)
    max_size: bpy.props.IntProperty(
        name="Max room size",
        description="Biggest room size that shall be generated",
        default=50,
        min=7)
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Generation Seed (Can't be negative). 0 creates a random seed.",
        default=0,
        min=0,
        max=sys.maxsize)
    octaves: bpy.props.IntProperty(
        name="Octaves",
        description="Generation Octaves (Can't be 7 or negative)",
        default=1,
        min=1)
    
    def execute(self, context):
        if(self.octaves == 7):
            return{'CANCELED'}
        generateRoom(false, self.octaves, self.seed, self.min_size, self.max_size)
        return {'FINISHED'}
    
class VIEW3D_PT_DunGen(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Dungeon"
    bl_label = "Generator"

    def draw(self, context):
        self.layout.operator('mesh.dungeon_generator',
        text='Default Dungeon')
        sizecol = self.layout.column(align=True)
        sizecol.prop()
        sizecol.prop()
        self.layout.separator(0.5)
        perlincol = self.layout.column(align=True)
        perlincol.prop()
        perlincol.prop()
        perlincol.prop()

def mesh_add_menu_draw(self, context):
    self.layout.operator('mesh.dungeon_generator',
        text='Default Dungeon')

blender_classes = [
    MESH_OT_DunGen,
    VIEW3D_PT_DunGen

]

def register():
    for blender_class in blenderclasses:
        bpy.utils.register_class(blender_class)
    pby.types.VIEW3D_MT_mesh_add.append(mesh_add_menu_draw)
    
def unregister():
    for blender_class in blenderclasses:
        bpy.utils.unregister_class(blender_class)
    pby.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu_draw)