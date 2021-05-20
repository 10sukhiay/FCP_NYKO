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

def update(it, people, heat_maps, position_state, axes, colour_dict, day_length, G, number_nodes, limit, death_rate, Susceptible, Infected, Infectious, Recovered, Deceased, Room1, Room2, Room3):

    day = math.floor(it/day_length) +1

    position_state['counter'] = position_state['counter'] - 1  # counter goes down 1 each iteration

    if (it/day_length).is_integer() == True and it !=0: #checks if first iteration of any day!

        # draw node graph
        #draw_network(position_state, G, number_nodes)
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
            map.update_occupants(position_state=position_state)
            map.calculate_heat_new()
            # introduce some transmission function to infect new people
            transmission(position_state=position_state, heat=map.heat_old, node=map.node, day_length=day_length)

    Susceptible.append(len(position_state[position_state['status']==1]))
    Infected.append(len(position_state[position_state['status']==2]))
    Infectious.append(len(position_state[position_state['status']==3]))
    Recovered.append(len(position_state[position_state['status']==4]))
    Deceased.append(len(position_state[position_state['status']==5]))

    Room1.append(len(position_state[position_state["node"]==1]))
    Room2.append(len(position_state[position_state["node"]==2]))
    Room3.append(len(position_state[position_state["node"]==3]))

    for map in heat_maps:
        # clear data from old plots
        axes[0, map.node].clear()
        axes[1, map.node].clear()

        # plot positions

        sns.scatterplot(x=map.occupants['x'],
                        y=map.occupants['y'],
                        hue=map.occupants['status'],
                        palette= colour_dict,
                        ax=axes[0, map.node],
                        legend=False)
        axes[0, map.node].set_title(f'Room {map.node} Position Map (Day {day})', fontsize=8)


        # plot heat maps
        sns.heatmap(map.show_map(),
                    ax=axes[1,map.node],
                    cbar=False,
                    cmap='icefire',
                    center=0,
                    vmin =0,
                    vmax=100).invert_yaxis()
        axes[1, map.node].set_title(f'Room {map.node} Heat Map (Day {day})', fontsize=8)

        position_state = death_chance(position_state=position_state, death_rate=death_rate)
        position_state = status_change(position_state=position_state, day_length=day_length)  # check for disease progression

    # call function to record statuses (plotting infections etc...)

    # Creates the line-graph tracking the status of people in the room
    line1 = axes[0, 0].plot(Susceptible, color='green')
    line2 = axes[0, 0].plot(Infected, color="yellow")
    line3 = axes[0, 0].plot(Infectious, color="red")
    line4 = axes[0, 0].plot(Recovered, color="blue")
    line5 = axes[0, 0].plot(Deceased, color="black")
    axes[0, 0].set_title(f'Population Status (Day {day})', fontsize=8)
    axes[0, 0].set_xlabel('Time', fontsize=6)
    axes[0, 0].set_ylabel('# of People', fontsize=6)
    #axes[0, 0].set(xlabel='Number of iterations', ylabel='Number of people')

    # Creates the line-graph tracking the number of people in each room
    line1 = axes[1, 0].plot(Room1, alpha=0.5, linestyle='--', color='black')
    line2 = axes[1, 0].plot(Room2, alpha=0.5, linestyle='-', color='red')
    line3 = axes[1, 0].plot(Room3, alpha=0.5, linestyle='-', color='black')
    axes[1, 0].set_title(f'Room Tracking Plot (Day {day})', fontsize=8)
    axes[1, 0].set_xlabel('Time', fontsize=6)
    axes[1, 0].set_ylabel('# of People', fontsize=6)



