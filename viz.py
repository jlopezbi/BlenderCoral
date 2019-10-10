import bmesh
import bpy
import mathutils

DEFAULT_BMESH_COLOR = (0.5, 0, 0.2)


def add_box(lower_corner, upper_corner, name="Box"):
    """
    Args:
        lower_corner (tuple or np array)
        upper_corner (tuple or np array)
    """
    bme = bmesh.new()

    v1 = bme.verts.new(lower_corner)
    v2 = bme.verts.new((lower_corner[0], upper_corner[1], lower_corner[2]))
    bme.edges.new((v1, v2))
    v3 = bme.verts.new((upper_corner[0], upper_corner[1], lower_corner[2]))
    bme.edges.new((v2, v3))
    v4 = bme.verts.new((upper_corner[0], lower_corner[1], lower_corner[2]))
    bme.edges.new((v3, v4))
    bme.edges.new((v4, v1))
    v5 = bme.verts.new((lower_corner[0], lower_corner[1], upper_corner[2]))
    bme.edges.new((v1, v5))
    v6 = bme.verts.new((lower_corner[0], upper_corner[1], upper_corner[2]))
    bme.edges.new((v2, v6))
    bme.edges.new((v5, v6))
    v7 = bme.verts.new(upper_corner)
    bme.edges.new((v3, v7))
    bme.edges.new((v6, v7))
    v8 = bme.verts.new((upper_corner[0], lower_corner[1], upper_corner[2]))
    bme.edges.new((v4, v8))
    bme.edges.new((v7, v8))
    bme.edges.new((v8, v5))

    add_bmesh(bme, objname=name)


def add_sphere(pos, name="Sphere", diam=20, color=(0.5, 0.0, 0.5)):
    pos = mathutils.Vector(pos)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=20, diameter=diam)
    me = bpy.data.meshes.new("Mesh")
    bm.to_mesh(me)

    mat = bpy.data.materials.new(name="Mat")
    mat.diffuse_color = color

    obj = bpy.data.objects.new(name, me)
    obj.data.materials.append(mat)
    obj.location = pos
    bpy.context.scene.objects.link(obj)

    return obj


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


def add_polyline(pnts, name="Polyline"):
    bme = bmesh.new()
    for i in range(len(pnts) - 1):
        _add_line_to_bmesh(bme, pnts[i], pnts[i + 1])
    add_bmesh(bme, objname=name)


def add_line(a, b, name="Line"):
    """
    a = mathutils.Vector
    b = mathutils.Vector
    """

    bme = bmesh.new()
    _add_line_to_bmesh(bme, a, b)
    add_bmesh(bme, objname=name)


def _add_line_to_bmesh(bme, start, end):
    v_start = bme.verts.new(start)
    v_end = bme.verts.new(end)
    bme.edges.new((v_start, v_end))
