import unittest
import bmesh
import Coral
import viz
import importlib
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
        viz.add_bmesh(self.seed)
        vert = self.seed.verts[0]
        viz.add_sphere(vert.co, str(0), diam=1)
        self.coral.neighbor_levels(vert, levels=3)

if __name__=="__main__":
    unittest.main(exit=False)
