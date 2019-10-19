import numpy as np

import bmesh
import mathutils
import viz

LEVELS = 10
MAX_GROW = 15
MIN_GROW = 1


def interact(coral, particle_system):
    coral.prepare_for_interaction()
    for particle in particle_system.particles:
        did_collide = coral.interact_with(particle)
        if did_collide == True:
            particle_system.re_spawn_particle(particle)


class Coral(object):
    def __init__(self, bme):
        self.bme = bme
        self.tree = None

    def prepare_for_interaction(self):
        self.tree = mathutils.bvhtree.BVHTree.FromBMesh(self.bme, epsilon=0.0)

    def interact_with(self, particle):
        """
        Args:
            particle_system
        """
        # NOTE: working here to make this work
        out = particle.motion_ray_info()
        origin = out["origin"]
        vector = out["ray"]

        location, normal, index, distance = self.tree.ray_cast(
            origin, vector, np.linalg.norm(vector)
        )
        return location


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
