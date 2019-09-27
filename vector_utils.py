import mathutils

UNIT_X = mathutils.Vector((1.0, 0.0, 0.0))
UNIT_Y = mathutils.Vector((0.0, 1.0, 0.0))
UNIT_Z = mathutils.Vector((0.0, 0.0, 1.0))


def nearly_same_vecs(vec_a, vec_b, threshold=0.001):
    """ returns True if vec_a and B are within threshold of each-other, otherwise false
    vec_a = mathutils.Vector
    vec_b = mathutils.Vector
    """
    diff = vec_a - vec_b
    if diff.length <= threshold:
        return True

    return False


def assert_nearly_same_vecs(vec_a, vec_b, threshold=0.001):
    msg = "First vec, {0}, is not within {2} of second vec: {1}".format(vec_a, vec_b, threshold)
    assert nearly_same_vecs(vec_a, vec_b, threshold), msg
