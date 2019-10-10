import unittest

import bmesh
import mathutils
import primitives as prims
import vector_utils as vu
import viz

bme = prims.ico_seed(radius=10)
viz.add_bmesh(bme, "seed")


tree = mathutils.bvhtree.BVHTree.FromBMesh(bme, epsilon=0.0)
origin = mathutils.Vector((0, 0, 15))
direction = -vu.UNIT_Z
distance = 9.0
result = tree.ray_cast(origin, direction, distance)
print(result)

if result[0] != None:
    viz.add_sphere(result[0], name="intersection")
