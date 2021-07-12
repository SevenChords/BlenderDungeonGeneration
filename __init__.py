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
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        from . import core
        from . import generator
        from . import main
        from . import config
        from . import logger
        main.Generation()
        return{"FINISHED"}
    
def register():
    python = os.path.join(sys.prefix, 'bin', 'python.exe')
    subprocess.call([python, "-m", "pip", "install", "perlin_noise"])
    bpy.utils.register_class(myop)

def unregister():
    bpy.utils.unregister_class(myop)