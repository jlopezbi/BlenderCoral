import importlib
import unittest

import numpy as np

import viz

importlib.reload(viz)


def test_add_polyline_one_segments():
    # viz.add_polyline(np.array([[0, 0, 0], [100, 100, 100]]), name="Single segment polyline")
    viz.add_polyline(
        [np.array([0, 0, 0]), np.array([100, 100, 100])], name="Single segment polyline"
    )


def test_add_sphere():
    viz.add_sphere(np.array((0, 0, 0)))


def test_add_box():
    lower_corner = np.array((0, 0, 0))
    upper_corner = np.array((10, 10, 10))
    viz.add_box(lower_corner, upper_corner, name="Box1")


if __name__ == "__main__":
    test_add_polyline_one_segments()
    test_add_box()
    test_add_sphere()
