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


def even_sharing_among_levels(n_levels, total_grow_length, center_grow_length):
    """distributes (total_grow_length - center_grow_length) among the neighborhoods evenly

    n_levels is number of levels beyond the center-vert that get to grow

    Args:
        n_levels [int]: number of levels beyond center-vert that grow
        total_grow_length [float]: total grow length of center vert and n_level neighbors
        center_grow_length [float]: amount of grow length reserved for the center_vert
    Returns:
        list[float]: grow length per level, starting from 0th level (center_vert)
    """
    left_over = total_grow_length - center_grow_length
    lengths = [left_over / n_levels] * n_levels
    lengths.insert(0, center_grow_length)
    return lengths


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
