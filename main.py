import importlib

import Coral
import nutrients
import world

importlib.reload(Coral)
importlib.reload(nutrients)
importlib.reload(world)

"""set up"""
side = 2.0
height = 3.0
front = (-side / 2, -side / 2, 0.0)
back = (side / 2, side / 2, height)
box = world.BoxWorld(front, back)
box.show()

num_particles = 60
particle_system = nutrients.ParticleSystem(box)
particle_system.randomness_of_motion = 0.76
particle_system.radius = 1.0
particle_system.trend_motion_magnitude = 0.01
padding_multiplier = 2.0

particle_system.add_n_particles_at_spawn_loc(n=10, radius=0.6)
particle_system.show_particles()


""" run """
steps = 1
for i in range(steps):
    particle_system.move_particles()
    particle_system.re_spawn_escaped_particles()
    # weed.collide_with(particle_system)
    # box.resize_to_fit(
    #    weed.bbox_lower, weed.bbox_upper, padding=particle_system.radius * box.padding_multiplier
    # )

# weed.show()
box.show()
