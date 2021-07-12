from sys import maxsize
from generator import generateRoom
import bpy

bl_info = {
    "name": "Dun_Gen",
    "blender": (2, 92, 0),
    "category": "Add Mesh"
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
        min=1)
    max_size: bpy.props.IntProperty(
        name="Max room size",
        description="Biggest room size that shall be generated",
        default=50,
        min=1)
    seed: bpy.props.IntProperty(
        name="Seed",
        description="Generation Seed (Can't be negative)",
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
    
def register():
    bpy.utils.register_class(MESH_OT_DunGen)
    
def unregister():
    bpy.utils.unregister_class(MESH_OT_DunGen)
    
if __name__ == '__main__':
    register()