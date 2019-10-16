import unittest

import numpy as np

import nutrients
import vector_utils as vu


class ParticleTestCase(unittest.TestCase):
    def test_motion_ray_info(self):
        particle = nutrients.Particle(position=np.array((0, 0, 5)), radius=None)
        out = particle.motion_ray_info(threshold=0.1)
        self.assertEqual(out["origin"], None)
        self.assertEqual(out["ray"], None)

        particle.position = np.array((0, 0, 10))

        out = particle.motion_ray_info(threshold=0.1)
        vu.assert_nearly_same_vecs(out["origin"], np.array((0, 0, 5)))
        vu.assert_nearly_same_vecs(out["ray"], np.array((0, 0, 5)))


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=3)
