import importlib
import unittest

import bmesh
import Coral
import viz

importlib.reload(Coral)


def ico_seed():
    bme = bmesh.new()
    bmesh.ops.create_icosphere(bme, subdivisions=5, diameter=10)
    return bme


class blah(unittest.TestCase):
    def setUp(self):
        self.seed = ico_seed()
        self.coral = Coral.Coral(bme=self.seed)

    def test(self):
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
