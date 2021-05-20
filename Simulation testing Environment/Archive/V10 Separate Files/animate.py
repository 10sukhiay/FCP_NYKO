#!/usr/bin/env python3
"""

animate.py
Kaelan Melville
May 2021


"""

#standard imports
import numpy as np
import pandas as pd
from matplotlib import animation
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

    font = {'family': 'DejaVu Sans',
            'weight': 'normal',
            'size': 6}

    plt.rc('font', **font)

    fig, axes = plt.subplots(2, rooms+1, figsize=(3.5*(rooms+1), 7), sharey=False, sharex=False)

    Susceptible = []
    Infected = []
    Infectious = []
    Recovered = []
    Deceased = []

    Room1 = []
    Room2 = []
    Room3 = []
    Room4 = []
    Room5 = []

    anim = FuncAnimation(fig=fig, func=update,
                         frames=day_length*days,
                         fargs=(people, heat_maps, position_state, axes, colour_dict, day_length, G, number_nodes, limit, death_rate, Susceptible, Infected, Infectious, Recovered, Deceased, Room1, Room2, Room3),
                         interval=50,
                         blit=False,
                         repeat=False)


    plt.show()