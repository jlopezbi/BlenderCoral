import unittest
import bmesh
import Coral
import viz

def ico_seed():
    bme = bmesh.new()
    bmesh.ops.create_icosphere(bme, subdivisions=5, diameter=10)
    return bme

class blah(unittest.TestCase):
    def setUp(self):
        self.seed = ico_seed()
        self.coral = Coral.coral(bme=self.seed)

    def test(self):
        viz.add_bmesh(self.seed)
        self.coral.neighbor_levels(vert, levels=3)

if __name__=="__main__":
    unittest.main(exit=False)
