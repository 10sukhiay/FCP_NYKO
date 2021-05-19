#!/usr/bin/env python3
"""

update.py
Kaelan Melville
May 2021


"""

#standard imports
import numpy as np
import pandas as pd
import seaborn as sns
import math

# custom imports
from Heat_Mapping import Room_map
from Person_Class import person
from other_functions import *
import update

def update(it, people, heat_maps, position_state, axes, colour_dict, day_length, G, number_nodes, limit):

    day = math.floor(it/day_length) +1


    if (it/day_length).is_integer() == True and it !=0: #checks if first iteration of any day!

        # draw node graph
        draw_network(position_state, G, number_nodes)
        # change nodes of individuals
        nodes = possible_paths(position_state, G)
        position_state = update_node_travel_prob(position_state, nodes, limit, number_nodes)
        people = update_people_nodes(position_state, people)
        # clear heat maps
        for map in heat_maps:
            map.heat_old[:, :] = 0


    # move each person
    for i in people:
        i.move(people=people)
    position_state = update_position_state(position_state, people)

    # update heat maps
    for x in range(2):
        for map in heat_maps:
            map.update_occupants(position_state)
            map.calculate_heat_new()
            # introduce some transmission function to infect new people
            transmission(position_state, map.heat_old, map.node)

    for map in heat_maps:
        # clear data from old plots
        axes[0, map.node - 1].clear()
        axes[1, map.node - 1].clear()

        # plot positions

        sns.scatterplot(x=map.occupants['x'],
                        y=map.occupants['y'],
                        hue=map.occupants['status'],
                        palette= colour_dict,
                        ax=axes[0, map.node - 1],
                        legend=False)
        axes[0, map.node - 1].set_title(f'Room {map.node} Position Map (Day {day})', fontsize=8)


        # plot heat maps
        sns.heatmap(map.show_map(),
                    ax=axes[1,map.node-1],
                    cbar=False,
                    cmap='icefire',
                    center=0,
                    vmin =0,
                    vmax=100).invert_yaxis()
        axes[1, map.node-1].set_title(f'Room {map.node} Heat Map (Day {day})', fontsize=8)

    # call function to record statuses (plotting infections etc...)


