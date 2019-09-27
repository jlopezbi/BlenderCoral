import importlib
import unittest

import bmesh
import Coral
import vector_utils as vu
import viz

importlib.reload(Coral)


def ico_seed():
    bme = bmesh.new()
    bmesh.ops.create_icosphere(bme, subdivisions=5, diameter=10)
    return bme


class DisplaceVertTestCase(unittest.TestCase):
    def setUp(self):
        self.cube = bmesh.new()
        bmesh.ops.create_cube(self.cube, size=10)
        self.cube.verts.ensure_lookup_table()
        self.cube.verts.remove(self.cube.verts[0])
        self.cube.verts.ensure_lookup_table()
        # update vert normals
        for vert in self.cube.verts:
            vert.normal_update()

    def test_displaces_one_vert(self):
        viz.add_bmesh(self.cube, "before vert displace")
        # checked visually using bpy.app.debug=True (display mesh indices)
        # know that this should be in unitZ direction
        cube = self.cube.copy()
        cube.verts.ensure_lookup_table()
        vert = cube.verts[0]
        original_pos = vert.co.copy()
        length = 20.0
        Coral.displace_vert(vert, length)
        viz.add_bmesh(cube, "after vert displace")
        vu.assert_nearly_same_vecs(vert.co, original_pos + vu.UNIT_Z * length)

    def test_sequential_displace_of_verts(self):
        """sequential displaces should not update the original vert normals
        """
        viz.add_bmesh(self.cube, "before vert displace")
        # checked visually using bpy.app.debug=True (display mesh indices)
        # know that this should be in unitZ direction
        cube = self.cube.copy()
        cube.verts.ensure_lookup_table()
        vert = cube.verts[0]
        original_pos = vert.co.copy()
        length = 20.0
        Coral.displace_vert(vert, length)
        vu.assert_nearly_same_vecs(vert.co, original_pos + vu.UNIT_Z * length)

        vert = cube.verts[4]
        original_pos = vert.co.copy()
        Coral.displace_vert(vert, length)
        vu.assert_nearly_same_vecs(
            vert.co, original_pos + (vu.UNIT_Z + vu.UNIT_X).normalized() * length
        )

        viz.add_bmesh(cube, "after two verts displace")


class GetNeighborsTestCase(unittest.TestCase):
    def setUp(self):
        self.seed = ico_seed()
        self.coral = Coral.Coral(bme=self.seed)

    def _test(self):
        """get a visual that neighbors look right and no dup spheres
        """
        viz.add_bmesh(self.seed)
        vert = self.seed.verts[0]
        # viz.add_sphere(vert.co, str(0), diam=1)
        levels = 20
        neighbors = self.coral.neighbor_levels(vert, levels=levels)

        diam = 1.0
        step = (diam - 0.1) / levels
        for neighborhood in neighbors:
            for vert in neighborhood:
                viz.add_sphere(vert.co, diam=diam)
            diam -= step


if __name__ == "__main__":
    unittest.main(exit=False)
