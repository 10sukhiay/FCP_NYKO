#!/usr/bin/env python3
"""

animate.py
Kaelan Melville
May 2021


"""

#standard imports
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt

#custom imports
from update import update

def animate(people, heat_maps, position_state, rooms, days, day_length, G, number_nodes, limit, death_rate):

    # colours for statuses in scatter plot
    colour_dict = dict({1: 'green',
                       2: 'yellow',
                       3: 'red',
                       4: 'blue',
                       5: 'black'})
    grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
    fig, axes = plt.subplots(2, rooms+1, figsize=(5*(rooms+1), 10), sharey=False, sharex=False)

    Susceptible = []
    Infected = []
    Infectious = []
    Recovered = []
    Deceased = []

    Room1 = []
    Room2 = []
    Room3 = []

    anim = FuncAnimation(fig=fig, func=update,
                         frames=day_length*days,
                         fargs=(people, heat_maps, position_state, axes, colour_dict, day_length, G, number_nodes, limit, death_rate, Susceptible, Infected, Infectious, Recovered, Deceased, Room1, Room2, Room3),
                         interval=50,
                         blit=False,
                         repeat=False)
    f = r"./animation.mp4"
    writervideo = animation.FFMpegWriter(fps=60)
    anim.save(f, writer=writervideo)

    plt.show()