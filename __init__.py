bl_info = {
"name" : "BlenderDungeonGenerator",
"author" : "me",
"blender": (2, 92, 0),
"category" : "Add Mesh"
}
import bpy
import subprocess
import sys
import os

class myop(bpy.types.Operator):

    bl_idname = "my_operator.blender_dungeon_generator"
    bl_label = "Dungeon Generator"
    bl_description = "It generates a Dungeon DUH"
    bl_options = {"REGISTER", 'UNDO'}

    min_size: bpy.props.IntProperty(
        name="Min room size",
        description="Smallest room size that shall be generated",
        default=10,
        min=7,
        soft_max=20)
    max_size: bpy.props.IntProperty(
        name="Max room size",
        description="Biggest room size that shall be generated",
        default=50,
        min=7,
        soft_max=100)
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Generation Seed (Can't be negative). 0 creates a random seed.",
        default=0,
        min=0)
    octaves: bpy.props.IntProperty(
        name="Octaves",
        description="Generation Octaves (Can't be 7 or negative)",
        default=1,
        min=1)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        if __package__ is None or __package__ == "":
            import core
            import generator
            import main
            import config
            import logger
        else:
            from . import core
            from . import generator
            from . import main
            from . import config
            from . import logger

        main.Generation(False, self.octaves, self.seed, self.min_size, self.max_size)
        return{"FINISHED"}


class VIEW3D_PT_DunGen(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Dungeon"
    bl_label = "Generator"

    def draw(self, context):
        self.layout.operator("my_operator.blender_dungeon_generator",
        text='Default Dungeon')
"""         sizecol = self.layout.column(align=True)
        sizecol.prop()
        sizecol.prop()
        self.layout.separator(0.5)
        perlincol = self.layout.column(align=True)
        perlincol.prop()
        perlincol.prop()
        perlincol.prop() """

def mesh_add_menu_draw(self, context):
    self.layout.operator("my_operator.blender_dungeon_generator",
        text='Default Dungeon')

blender_classes = [
    myop,
    VIEW3D_PT_DunGen
]
    
def register():
    if os.name == "nt":
        python = os.path.join(sys.prefix, "bin", "python.exe")
    if os.name == "posix":
        python = os.path.join(sys.prefix, "bin", "python3.7m")
    subprocess.call([python, "-m", "pip", "install", "perlin_noise"])
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu_draw)

def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)
    bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu_draw)