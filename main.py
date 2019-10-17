import importlib

import Coral
import nutrients
import viz
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

num_particles = 20
particle_system = nutrients.ParticleSystem(box)
particle_system.randomness_of_motion = 0.76
particle_system.trend_speed = 0.1
padding_multiplier = 2.0

particle_system.add_n_particles_at_spawn_loc(n=num_particles, radius=0.01)
# particle_system.show_particles()


""" run """
steps = 5
for i in range(steps):
    particle_system.move_particles()
    particle_system.re_spawn_escaped_particles()
    # coral.feed_off_of(particle_system)
    # box.resize_to_fit(
    #    coral.bbox_lower, coral.bbox_upper, padding=particle_system.radius * box.padding_multiplier
    # )
particle_system.show_particles(viz.add_polyline)

# weed.show()
box.show()
