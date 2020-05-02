import importlib

import Coral
import nutrients
import primitives as prims
import viz
import world

importlib.reload(Coral)
importlib.reload(nutrients)
importlib.reload(world)

side = 2.0
height = 3.0
front = (-side / 2, -side / 2, 0.0)
back = (side / 2, side / 2, height)
box = world.BoxWorld(front, back)
box.show()

num_particles = 40
particle_system = nutrients.ParticleSystem(box)
particle_system.randomness_of_motion = 0.5
particle_system.trend_speed = 0.1
padding_multiplier = 2.0

particle_system.add_n_particles_at_spawn_loc(n=num_particles, radius=0.01)
# particle_system.show_particles()

coral = Coral.Coral(prims.ico_seed(radius=0.4))
long_thresh = 0.06
short_thresh = 0.001


def interact(coral, particle_system):
    coral.prepare_for_interaction()
    for particle in particle_system.particles:
        did_collide = coral.interact_with(particle)
        if did_collide == True:
            particle_system.re_spawn_particle(particle)


steps = 50
for i in range(steps):
    print("iteration: ", i)
    particle_system.move_particles()
    particle_system.re_spawn_escaped_particles()
    interact(coral, particle_system)
    coral.divide_long_edges(long_thresh)
    coral.collapse_short_edges(short_thresh)
    # box.resize_to_fit(
    #    coral.bbox_lower, coral.bbox_upper, padding=particle_system.radius * box.padding_multiplier
    # )
particle_system.show_particles(viz.add_polyline)
viz.add_bmesh(coral.bme, "coral after {} steps".format(steps))

# weed.show()
box.show()
