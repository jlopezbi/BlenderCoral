import bmesh
import viz


class Coral(object):
    def __init__(self, bme):
        # what if coral was a collection of
        # polyps and edges?
        self.bme = bme
        self.bme.verts.ensure_lookup_table()

    def neighbor_levels(self, vert, levels):
        """outputs a list of lists of neighbors, ordered according to 'level' or
        distance from the input vert

        Args:
            vert (bmesh.types.BMVert)
            levels (int): number of levels to return
        Returns:
            list[list[bmesh.types.BMVert]]
        """
        curr_geom = set([vert])
        neighbors = [[vert]]
        for i in range(levels):

            output = bmesh.ops.region_extend(self.bme, geom=list(curr_geom), use_faces=0)
            verts = [ele for ele in output["geom"] if isinstance(ele, bmesh.types.BMVert)]
            new_verts = set(verts) - curr_geom
            curr_geom.update(verts)

            neighbors.append(list(new_verts))

        return neighbors


def displace_vert(vert, length):
    """moves vert along its normal by length
    """
    norm = vert.normal
    vert.co = vert.co + norm * length


# Polyp. neighbor_levels
#       . grow > upon receive nutrients
#       . ensure_space
#           (divide or merge w/ neighbor
#       .send nutrients
# hmm kiss
