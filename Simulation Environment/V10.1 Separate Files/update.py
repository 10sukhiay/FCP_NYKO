#!/usr/bin/env python3
"""

update.py
Kaelan Melville, Yazad Sukhia
May 2021


"""

# standard imports
import numpy as np
import pandas as pd
import seaborn as sns
import math

# custom imports
from Heat_Mapping import RoomMap
from Person_Class import Person
from other_functions import *


def update(it, people, heat_maps, position_state, axes, colour_dict, day_length, g, number_nodes, limit, death_rate,
           susceptible, infected, infectious, recovered, deceased, room1, room2, room3):
    """" """

    day = math.floor(it/day_length) + 1

    position_state['counter'] = position_state['counter'] - 1  # counter goes down 1 each iteration

    if (it/day_length).is_integer() is True and it != 0:  # checks if first iteration of any day!

        # draw node graph
        # draw_network(position_state, g, number_nodes)
        # change nodes of individuals
        nodes = possible_paths(position_state, g)
        position_state = update_node_travel_prob(position_state, nodes, limit, number_nodes)
        people = update_people_nodes(position_state, people)
        # clear heat maps
        for m in heat_maps:
            m.heat_old[:, :] = 0

    # move each person
    for p in people:
        p.move(people=people)
    position_state = update_position_state(position_state, people)

    # update heat maps
    for x in range(2):
        for m in heat_maps:
            m.update_occupants(position_state=position_state)
            m.calculate_heat_new()
            # introduce some transmission function to infect new people
            transmission(position_state=position_state, heat=m.heat_old, node=m.node, day_length=day_length)

    # data fed into the animation lists
    susceptible.append(len(position_state[position_state['status'] == 1]))
    infected.append(len(position_state[position_state['status'] == 2]))
    infectious.append(len(position_state[position_state['status'] == 3]))
    recovered.append(len(position_state[position_state['status'] == 4]))
    deceased.append(len(position_state[position_state['status'] == 5]))

    room1.append(len(position_state[position_state["node"] == 1]))
    room2.append(len(position_state[position_state["node"] == 2]))
    room3.append(len(position_state[position_state["node"] == 3]))

    for m in heat_maps:
        # clear data from old plots
        axes[0, m.node].clear()
        axes[1, m.node].clear()

        # plot positions
        sns.scatterplot(x=m.occupants['x'],
                        y=m.occupants['y'],
                        hue=m.occupants['status'],
                        palette=colour_dict,
                        ax=axes[0, m.node],
                        legend=False)
        axes[0, m.node].set_title(f'Room {m.node} Position Map (Day {day})', fontsize=8)
        axes[0, m.node].set_xlim(0, m.xsize)
        axes[0, m.node].set_ylim(0, m.ysize)
        axes[0, m.node].set_xlabel('x')
        axes[0, m.node].set_ylabel('y')

        # plot heat maps
        sns.heatmap(m.heat_old,
                    ax=axes[1, m.node],
                    cbar=False,
                    cmap='icefire',
                    center=0,
                    vmin=0,
                    vmax=100).invert_yaxis()
        axes[1, m.node].set_title(f'Room {m.node} Heat Map (Day {day})', fontsize=8)
        axes[1, m.node].set_xlabel('x')
        axes[1, m.node].set_ylabel('y')

        # CHECK FOR DEATHS
        position_state = death_chance(position_state=position_state, death_rate=death_rate)
        # check for disease progression
        position_state = status_change(position_state=position_state, day_length=day_length)

    # call function to record statuses (plotting infections etc...)

    # Creates the line-graph tracking the status of people across all rooms
    axes[0, 0].plot(susceptible, color='green')
    axes[0, 0].plot(infected, color="yellow")
    axes[0, 0].plot(infectious, color="red")
    axes[0, 0].plot(recovered, color="blue")
    axes[0, 0].plot(deceased, color="black")

    axes[0, 0].set_title(f'Population Status (Day {day})', fontsize=8)
    axes[0, 0].set_xlabel('Time', fontsize=6)
    axes[0, 0].set_ylabel('Number of People', fontsize=6)
    axes[0, 0].legend(labels=['Susceptible', 'Infected', 'Infectious', 'Recovered', 'Deceased'], loc='upper center',
                      bbox_to_anchor=(0.5, 1.3), ncol=3, fontsize=6)

    # Creates the line-graph tracking the number of people in each room
    axes[1, 0].plot(room1, alpha=0.5, linestyle='--', color='black')
    axes[1, 0].plot(room2, alpha=0.5, linestyle='-', color='red')
    axes[1, 0].plot(room3, alpha=0.5, linestyle='--', color='blue')

    axes[1, 0].set_title(f'Room Tracking Plot (Day {day})', fontsize=8)
    axes[1, 0].set_xlabel('Time', fontsize=6)
    axes[1, 0].set_ylabel('Number of People', fontsize=6)
    axes[1, 0].legend(labels=['Room1', 'Room2(Hub)', 'Room3'], loc='lower center', bbox_to_anchor=(0.5, -0.3),
                      ncol=3, fontsize=6)
    axes[1, 0].set_ylim(0, round(0.6*len(position_state)))