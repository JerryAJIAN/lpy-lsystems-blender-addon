bl_info = {
    "name": "Lindenmaker",
    "description": "Lindenmayer systems for Blender via the L-Py framework.",
    "author": "Addon by Nikolaus Leopold. L-Py framework by Frederic Boudon et al.",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "View3D > Add > Mesh",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Add Mesh"
}

from lindenmaker import turtle_interpretation
import lpy
# reload scripts even if already imported, in case they have changed.
# this allows use of operator "Reload Scripts" (key F8)
import imp
imp.reload(turtle_interpretation)
imp.reload(lpy)

import bpy
from math import radians
from mathutils import Vector, Matrix

class LindenmakerPanel(bpy.types.Panel):
    """Lindenmaker Panel"""
    bl_label = "Lindenmaker"
    bl_idname = "OBJECT_PT_lindenmaker"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world" # TODO put somewhere else??
    
    # get text from open editor file
#    for area in bpy.context.screen.areas:
#        if area.type == 'TEXT_EDITOR':
#            text_editor = area.spaces.active
#            text = text_editor.text.as_string()
#    print(text)

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "lpyfile_path")
        layout.prop_search(context.scene, "internode_mesh_name", bpy.data, "meshes")
        layout.prop(context.scene, "turtle_step_size")
        layout.operator(Lindenmaker.bl_idname)


class Lindenmaker(bpy.types.Operator):
    """Generate a mesh via a Lindenmayer system""" # tooltip for menu items and buttons.
    bl_idname = "mesh.lindenmaker" # unique identifier for buttons and menu items to reference.
    bl_label = "Add Mesh via Lindenmayer System" # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} # enable undo for the operator.

    def execute(self, context):
        
        #bpy.ops.object.select_all(action='DESELECT')
        
        # Clear last objects (TODO remove this)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        for item in bpy.data.meshes:
            if item.users is 0:
                bpy.data.meshes.remove(item)
        for item in bpy.data.materials:
            if item.users is 0:
                bpy.data.materials.remove(item)
        
        # load L-Py framework lsystem specification file (.lpy) and derive lstring
        lsys = lpy.Lsystem(context.scene.lpyfile_path)
        #print("LSYSTEM DEFINITION: {}".format(lsys.__str__()))
        lstring = str(lsys.derive())
        #print("LSYSTEM DERIVATION RESULT: {}".format(lstring))
        
        # interpret derived lstring via turtle graphics
        turtle_interpretation.interpret(lstring)
            
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(Lindenmaker.bl_idname, icon='PLUGIN')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)
    bpy.types.Scene.lpyfile_path = bpy.props.StringProperty(name="File Path", description="Path of .lpy file to be imported", maxlen=1024, subtype='FILE_PATH')
    bpy.types.Scene.turtle_step_size = bpy.props.FloatProperty(name="Step Size", default=2, min=0.05, max=100)
    bpy.types.Scene.internode_mesh_name = bpy.props.StringProperty(name="Internode Mesh", description="Name of Mesh to be used for drawing internodes via the F command")
    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
    del bpy.types.Scene.lpyfile_path
    del bpy.types.Scene.turtle_step_size
    del bpy.types.Scene.internode_mesh_name

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
    