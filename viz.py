import bmesh
import bpy
import mathutils

DEFAULT_BMESH_COLOR = (0.5, 0, 0.2)


def add_bmesh(bm, objname="Object", color=DEFAULT_BMESH_COLOR, alpha=0):
    me = bpy.data.meshes.new("mesh")
    bm.to_mesh(me)

    mat = bpy.data.materials.new(name="Mat")

    obj = bpy.data.objects.new(objname, me)

    if alpha != 0:
        obj.show_transparent = True
        mat.transparency_method = "Z_TRANSPARENCY"
        # need the following 2 lines for alpha to work
        mat.use_transparency = True
        mat.alpha = alpha

    mat.diffuse_color = color

    obj.data.materials.append(mat)
    bpy.context.scene.objects.link(obj)

    return obj
