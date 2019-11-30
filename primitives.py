import bmesh


def cube(side=10):
    bme = bmesh.new()
    bmesh.ops.create_cube(bme, size=side)
    return bme


def ico_seed(radius=10):
    bme = bmesh.new()
    # incorrect variable name 'diameter'
    bmesh.ops.create_icosphere(bme, subdivisions=5, diameter=radius)
    return bme
