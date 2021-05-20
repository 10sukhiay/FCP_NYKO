#!/usr/bin/env python3
"""

animate.py
Kaelan Melville, Yazad Sukhia
May 2021

This script contains the animate function used in the model simulation.
It is not interacted with directly from the command line. It is called by the simulator
and calls the update function to move the simulation forward a certain number of iterations.
This function produces an animation alongside the simulation performed.

"""

# standard imports
import numpy as np
import pandas as pd
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt

# custom imports
from update import update


def animate(people, heat_maps, position_state, rooms, days, day_length, g, number_nodes, limit, death_rate):
    """" set up animation for heat map, scatter graphs and line graphs of the simulation"""

    # colours for statuses in scatter plot
    colour_dict = dict({1: 'green',
                       2: 'yellow',
                       3: 'red',
                       4: 'blue',
                       5: 'black'})

    # set plot fonts
    font = {'family': 'DejaVu Sans',
            'weight': 'normal',
            'size': 6}
    plt.rc('font', **font)

    # initialise plot with subplots for each room
    fig, axes = plt.subplots(2, rooms+1, figsize=(3.5*(rooms+1), 7))

    # ----------------------------------------------------------------------------- #
    # initialising empty lists for updated animation information to append to       #
    # ----------------------------------------------------------------------------- #

    # Population status tracking
    susceptible = []
    infected = []
    infectious = []
    recovered = []
    deceased = []

    # Room population tracking
    room1 = []
    room2 = []
    room3 = []

    # ----------------------------------------------------------------------------- #
    # FuncAnimation function taking in all necessary arguments                      #
    # ----------------------------------------------------------------------------- #
    anim = FuncAnimation(fig=fig, func=update,
                         frames=day_length*days,
                         fargs=(people, heat_maps, position_state, axes, colour_dict, day_length, g, number_nodes,
                                limit, death_rate,
                                susceptible, infected, infectious, recovered, deceased,
                                room1, room2, room3),
                         interval=50,
                         blit=False,
                         repeat=False)

    plt.show()