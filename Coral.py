import bmesh
import viz

class Coral(object):
    def __init__(self, bme):
        #what if coral was a collection of
        #polyps and edges?
        self.bme = bme
        self.bme.verts.ensure_lookup_table()

    def neighbor_levels(self, vert, levels):
        output = bmesh.ops.region_extend(self.bme, geom=[vert], use_faces=0)
        verts = [ele for ele in output['geom'] if isinstance(ele, bmesh.types.BMVert)]
        print(verts)
        for vert in verts:
            viz.add_sphere(vert.co, diam=.3)

        output = bmesh.ops.region_extend(self.bme, geom=[vert + verts], use_faces=0)
        next_verts = [ele for ele in output['geom'] if isinstance(ele, bmesh.types.BMVert)]
        for vert in next_verts:
            viz.add_sphere(vert.co, diam=.1)

class Polyp(object):
    def neighbor_levels():
        pass

# Polyp. neighbor_levels
#       . grow > upon receive nutrients
#       . ensure_space
#           (divide or merge w/ neighbor
#       .send nutrients
#hmm kiss
