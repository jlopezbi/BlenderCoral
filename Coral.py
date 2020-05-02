import numpy as np

import bmesh
import mathutils

# import viz

LEVELS = 10
MAX_GROW = 0.07
MIN_GROW = 0.001


class Coral(object):
    def __init__(self, bme):
        self.bme = bme
        self.tree = None

    def prepare_for_interaction(self):
        self.bme.faces.ensure_lookup_table()
        self.tree = mathutils.bvhtree.BVHTree.FromBMesh(self.bme, epsilon=0.0)

    def collapse_short_edges(self, threshold_length):
        bmesh.ops.dissolve_degenerate(self.bme, dist=threshold_length, edges=self.bme.edges)

    def divide_long_edges(self, threshold_length):
        """subdivide each edge of the coral that is above the threshold length
        """
        # divide long edges
        long_edges = []
        for edge in self.bme.edges:
            if edge.calc_length() > threshold_length:
                long_edges.append(edge)
        # something werid happening that seemed like inifinte loop,
        # so trying breaking operations out into two steps

        for edge in long_edges:
            vert = edge.verts[0]
            # splits at the midpoint of the edge
            bmesh.utils.edge_split(edge, vert, 0.5)

        self._triangulate()

    def _triangulate(self):
        bmesh.ops.triangulate(self.bme, faces=self.bme.faces)

    def interact_with(self, particle):
        """check if the particle collided; if it did grow the nearest vert to the collision

        has importantside effect of growing the site that got 'fed'

        Args:
            particle
        Returns:
            boolean: True if the particle collided, false otherwise
        """
        out = particle.motion_ray_info()
        origin = out["origin"]
        vector = out["ray"]

        # particle did move
        if vector is not None:
            location, normal, face_index, distance = self.tree.ray_cast(
                origin, vector, np.linalg.norm(vector)
            )
            # particle did collide with coral
            if location is not None:
                # is this a face face_index?
                vert = self._nearest_vert(location, face_index)
                grow_site(self.bme, vert)
                return True

        return False

    def _nearest_vert(self, location, face_index):
        face = self.bme.faces[face_index]
        verts = face.verts
        return min(verts, key=lambda vert: (vert.co - location).length)


def grow_site(bme, vert):
    """this function modifies bme so that the vert and its neighbors grow
    """
    neighbors = neighbor_levels(bme, vert, levels=LEVELS)
    grow_lengths = falloff_neighborhood_grow_lengths(
        n_levels=LEVELS, center_grow_length=MAX_GROW, last_grow_length=MIN_GROW
    )
    grow_neighborhood(neighbors, grow_lengths)


def neighbor_levels(bme, vert, levels):
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

        output = bmesh.ops.region_extend(bme, geom=list(curr_geom), use_faces=0, use_face_step=True)
        verts = [ele for ele in output["geom"] if isinstance(ele, bmesh.types.BMVert)]
        new_verts = set(verts) - curr_geom
        curr_geom.update(verts)

        neighbors.append(list(new_verts))

    return neighbors


def grow_neighborhood(neighbors, grow_lengths):
    """grows verts by amount according to grow_lengths. for a vert belonging to neighborhood 1, for
    example, grows that vert by grow_lengths[1]

    NOTE: not dividing grow_lengths[i] by num_neighbors

    Modifies positions of neighbors
    Args:
        neighbors (list[list[bmesh.types.BMVert]]): list of lists of neihbbor verts
        grow_lengths (list[float]) total grow length per neighborhood
    """

    for total_grow_length, neighborhood in zip(grow_lengths, neighbors):
        # num_neighbors = len(neighborhood)
        grow_length = total_grow_length
        for vert in neighborhood:
            displace_vert(vert, grow_length)


def falloff_neighborhood_grow_lengths(n_levels, last_grow_length, center_grow_length):
    """linear falloff from total_grow_length, given to each
    """
    step_size = (center_grow_length - last_grow_length) / (n_levels - 1)
    temp_length = center_grow_length
    lengths = []
    for _ in range(n_levels):
        lengths.append(temp_length)
        temp_length = temp_length - step_size
    return lengths


def even_grow_lengths(n_levels, total_grow_length, center_grow_length):
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
