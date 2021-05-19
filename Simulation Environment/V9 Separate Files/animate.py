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

def animate(people, heat_maps, position_state, rooms, days, day_length, G, number_nodes, limit):

    # colours for statuses in scatter plot
    colour_dict = dict({1: 'green',
                       2: 'yellow',
                       3: 'red',
                       4: 'blue',
                       5: 'black'})
    grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
    fig, axes = plt.subplots(2, rooms, figsize=(10, 10), sharey=True, sharex=True)
    anim = FuncAnimation(fig=fig, func=update,
                         frames=day_length*days,
                         fargs=(people, heat_maps, position_state, axes, colour_dict, day_length, G, number_nodes, limit),
                         interval=10,
                         blit=False,
                         repeat=False)


    plt.show()