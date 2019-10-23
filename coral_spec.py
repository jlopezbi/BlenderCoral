import importlib
import unittest

import numpy as np

import bmesh
import Coral
import nutrients
import primitives as prims
import vector_utils as vu
import viz

importlib.reload(Coral)
importlib.reload(nutrients)


class FeedOffOfTestCase(unittest.TestCase):
    def setUp(self):
        self.coral = Coral.Coral(prims.ico_seed(radius=50))
        self.particle = nutrients.Particle(
            np.array((0.0, 0.0, 60.0)), radius=None, motion_thresh=0.001
        )

    def test_feed_off_of_base_case(self):
        # viz.add_sphere(self.particle.position, "particle init pos")
        self.particle.move(magnitude=30.0, randomness=0.0)
        # viz.add_sphere(self.particle.position, "particle final pos")
        self.particle.show(viz.add_polyline)
        self.coral.prepare_for_interaction()
        location = self.coral.interact_with(self.particle)
        viz.add_sphere(location, name="collision")
        viz.add_bmesh(self.coral.bme, "coral after collision")


class GrowLengthsTestCase(unittest.TestCase):
    def test_falloff_neighborhood_grow_lengths(self):
        lengths = Coral.falloff_neighborhood_grow_lengths(
            3, last_grow_length=1, center_grow_length=11
        )
        correct = [11, 6, 1]
        self.assertEqual(lengths, correct)


class IcoSphereGrowSeedTestCase(unittest.TestCase):
    def setUp(self):
        self.seed = prims.ico_seed(radius=50)
        self.seed.verts.ensure_lookup_table()

    def test_two_grow_regions(self):
        viz.add_bmesh(self.seed, "seed before grow")
        vert_a = self.seed.verts[0]
        vert_b = self.seed.verts[2500]

        Coral.grow_site(self.seed, vert_a)
        Coral.grow_site(self.seed, vert_b)
        viz.add_bmesh(self.seed, "seed after two grow sites")

    def test_three_grow_regions(self):
        viz.add_bmesh(self.seed, "seed before grow")
        vert_a = self.seed.verts[0]
        vert_b = self.seed.verts[2500]
        vert_c = self.seed.verts[2279]
        viz.add_sphere(vert_a.co, "vert_a")
        viz.add_sphere(vert_b.co, "vert_b")
        viz.add_sphere(vert_c.co, "vert_c")

        Coral.grow_site(self.seed, vert_a)
        Coral.grow_site(self.seed, vert_b)
        Coral.grow_site(self.seed, vert_c)
        viz.add_bmesh(self.seed, "seed after three grow sites")


class GrowNeighborhoodTestCase(unittest.TestCase):
    def test_on_grid(self):
        grid = bmesh.new()
        bmesh.ops.create_grid(grid, x_segments=10, y_segments=10, size=100)
        grid.verts.ensure_lookup_table()
        viz.add_bmesh(grid, "grid before grow")
        vert = grid.verts[45]

        levels = 6
        neighbors = Coral.neighbor_levels(grid, vert, levels=levels)
        grow_lengths = Coral.falloff_neighborhood_grow_lengths(
            n_levels=levels, center_grow_length=40, last_grow_length=20
        )

        Coral.grow_neighborhood(neighbors, grow_lengths)
        viz.add_bmesh(grid, "grid after grow")

    def test_on_ico_sphere(self):
        seed = prims.ico_seed(radius=100)
        seed.verts.ensure_lookup_table()
        vert = seed.verts[0]

        levels = 10
        neighbors = Coral.neighbor_levels(seed, vert, levels=levels)
        grow_lengths = Coral.falloff_neighborhood_grow_lengths(
            n_levels=levels, center_grow_length=10, last_grow_length=1
        )
        Coral.grow_neighborhood(neighbors, grow_lengths)
        viz.add_bmesh(seed, "ico after grow")


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
        # viz.add_bmesh(self.cube, "before vert displace")
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
        # viz.add_bmesh(self.cube, "before vert displace")
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

        # viz.add_bmesh(cube, "after two verts displace")


class GetNeighborsTestCase(unittest.TestCase):
    def setUp(self):
        self.seed = prims.ico_seed()
        self.seed.verts.ensure_lookup_table()

    # TODO: test what happens when levels extend beyond boundary of mesh

    def test(self):
        """get a visual that neighbors look right and no dup spheres
        """
        viz.add_bmesh(self.seed)
        vert = self.seed.verts[0]
        # viz.add_sphere(vert.co, str(0), diam=1)
        levels = 20
        neighbors = Coral.neighbor_levels(self.seed, vert, levels=levels)

        diam = 1.0
        step = (diam - 0.1) / levels
        for neighborhood in neighbors:
            for vert in neighborhood:
                # commented to make run faster
                # viz.add_sphere(vert.co, diam=diam)
                pass
            diam -= step


if __name__ == "__main__":
    unittest.main(exit=False)
