#!/usr/bin/env python3
"""

other_functions.py
Kaelan Melville, Oscar Bond
May 2021


"""

# standard imports
import numpy as np
import pandas as pd
from Heat_Mapping import RoomMap
from Person_Class import Person
from matplotlib import pyplot as plt
import random
import networkx as nx
from numpy.random import randint
import math

# custom imports


def create_edgelist(rooms):
    """Define the edge list dependant on number of rooms."""
    if rooms == 2:
        edgelist = [(1, 2)]
    elif rooms == 3:
        edgelist = [(1, 2), (1, 3), (2, 3)]
    elif rooms == 4:
        edgelist = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    elif rooms == 5:
        edgelist = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5)]
    else:
        edgelist = []

    return edgelist


def create_network(edgelist):
    """Create a networkx graph from the edgelist."""
    g = nx.Graph(edgelist)
    # nx.draw(G, with_labels=True)
    # plt.show()   # this displays the graph - turn on as required.
    return g


def network_number_nodes(g):
    """Calculate the number of nodes within the networkx graph"""
    number_nodes = g.number_of_nodes()
    return number_nodes


def create_people_array(room_size_x, room_size_y, n, number_nodes, number_infected, following_two_meter,
                        gravitate_table, using_mask, travel):
    """Set-up the array of people dependant on inputs. """
    x_position = randint(0, room_size_x+1, n)  # randomly assign x values for each person
    y_position = randint(0, room_size_y+1, n)  # randomly assign y values for each person
    start_nodes = randint(1, number_nodes+1, n)

    # SUSCEPTIBLE 1
    # INFECTED    2
    # INFECTIOUS  3
    # RECOVERED   4
    # DECEASED    5
    start_status = np.concatenate((([3]*number_infected), ([1]*(n-number_infected))))
    random.shuffle(start_status)
    # following two meter rule
    follow = math.ceil(n*following_two_meter)
    no_follow = n - follow
    two_meter = np.concatenate((([1]*follow), ([0]*no_follow)))
    random.shuffle(two_meter)
    # gravitating towards the table
    gravitate = math.ceil(n*gravitate_table)
    no_gravitate = n - gravitate
    number_gravitating = np.concatenate((([1]*gravitate), ([0]*no_gravitate)))
    random.shuffle(number_gravitating)
    # wearing a mask
    masked = math.ceil(n*using_mask)
    no_masked = n - masked
    number_masked = np.concatenate((([1]*masked), ([0]*no_masked)))
    random.shuffle(number_masked)
    # travelling round
    travelling = math.ceil(n*travel)
    no_travelling = n - travelling
    number_travelling = np.concatenate((([1]*travelling), ([0]*no_travelling)))
    random.shuffle(number_travelling)
    # infection progress counter
    counter = ([0]*n)
    # compile dataframe
    data_in = np.stack((x_position, y_position, start_nodes, start_status, two_meter, number_gravitating,
                        number_masked, number_travelling, counter), axis=1)
    position_state = pd.DataFrame(data=data_in, columns=['x', 'y', 'node', 'status', 'two_meter',
                                                         'gravitating', 'mask', 'travelling', 'counter'])
    return position_state


def people_array_room(position_state, i):
    """Create array of people dependant on node location"""
    room = position_state[position_state["node"] == i]
    return room


def possible_paths(position_state, g):
    """Creates a list of the possible nodes that people can travel to"""
    # need to be careful so that people can only travel to connected nodes.
    nodes = []
    for i in range(0, len(position_state), 1):
        possible_nodes = list(nx.single_source_shortest_path(g, source=position_state.iloc[i, 2], cutoff=1))
        nodes.append(possible_nodes)
    return nodes


def update_node_travel_prob(position_state, nodes, limit, number_nodes):
    """Update position_state dependant on limited number of people in each room"""
    if limit == 0:
        random_node_choice(position_state, nodes)
    if limit == 1:
        random_node_choice(position_state, nodes)
        while max(node_count_individuals(position_state, number_nodes)) > ((len(position_state)/number_nodes)+3):
            random_node_choice(position_state, nodes)
    return position_state


def random_node_choice(position_state, nodes):
    """Update position_state dependant on connected nodes"""
    for i in range(0, len(position_state), 1):
        if position_state.iloc[i, 7] == 1:
            position_state.iloc[i, 2] = random.choice(nodes[i])
    return position_state


def node_count_individuals(position_state, number_nodes):
    """Count the number of individual at each node"""
    node_count = []
    for n in range(1, number_nodes + 1):
        a = 0
        for i in range(0, len(position_state)):
            if position_state.iloc[i, 2] == n:
                a = a + 1
        node_count.append(a)
    return node_count


def draw_network(position_state, g, number_nodes):
    """Draw network graph"""
    node_count = node_count_individuals(position_state, number_nodes)

    for i in range(1, number_nodes+1):
        g.nodes[i]['Number'] = node_count[i-1]

    pos = nx.spring_layout(g)
    # increase size of nodes to be able to see
    node_count_size = [i * 100 for i in node_count]

    # draw the network with node size dependant on no.people
    nx.draw(g, pos, node_size=node_count_size)
    node_labels = nx.get_node_attributes(g, 'Number')
    nx.draw_networkx_labels(g, pos, labels=node_labels)
    plt.legend(['Room - Number of People in the Room'])
    plt.show()


def update_position_state(position_state, people):
    """Update position_state array with locations of people at the end of a day."""
    position_state.iloc[:, :2] = 0  # array emptied for x y only
    # this code adds values from people objects back into array
    k = 0
    for t in people:
        position_state.iloc[k, 0] = t.x
        position_state.iloc[k, 1] = t.y
        position_state.iloc[k, 2] = t.node
        position_state.iloc[k, 5] = t.gravitating
        k += 1  # iterator for picking the correct row
    # check
    # print('iteration finished and this is new position_state array:')
    # print(position_state)  # array refilled with people
    return position_state


def update_people_nodes(position_state, people):
    """Update node for people based on position_state array."""
    position_state.iloc[:, :2] = 0  # array emptied for x y only
    # this code adds values from people objects back into array
    k = 0
    for t in people:
        t.node = position_state['node'].iloc[k]
        t.x = random.randint(0, t.size_x)
        t.y = random.randint(0, t.size_y)
        k += 1  # iterator for picking the correct row
    return people


def transmission(position_state, heat, node, day_length):
    """Checks each individual for chance of infection"""

    for x in range(0, len(position_state)):
        # checks individual is in correct room and checks individual is susceptible
        if position_state.iloc[x]['node'] == node and position_state.iloc[x]['status'] == 1:

            # check the concentration is above minimum threshold (10)
            if heat[round(position_state['y'].iloc[x]), round(position_state['x'].iloc[x])] > 10:

                # if they randomly should be infected, temperature at cell greater than random value
                if heat[round(position_state.iloc[x, 0]), round(position_state.iloc[x, 1])] > (random.random()*100):
                    position_state.iloc[x, 3] = 2  # change status to infected
                    # 2 day incubation countdown +- 20%
                    position_state.iloc[x, 8] = round((1-((random.random() - 0.5) / 2.5)) * day_length * 2)
    return position_state


def status_change(position_state, day_length):
    """Checks each individual for disease progression"""

    for x in range(0, len(position_state)):
        if position_state.iloc[x, 8] == 0:  # check if status requires changing (counter reaches zero)
            if position_state.iloc[x, 3] == 2:  # infected individuals
                position_state.iloc[x, 3] = 3  # now infectious
                position_state.iloc[x, 8] = round((1-((random.random()-0.5)/2.5))*day_length*3)  # 3 day infectious period give or take 20%
            elif position_state.iloc[x, 3] == 3:  # infectious individuals
                position_state.iloc[x, 3] = 4  # now recovered
                position_state.iloc[x, 8] = -1  # set counter negative, will no longer trip if statement

    return position_state


def death_chance(position_state, death_rate):
    """Randomly changes infected and infectious individuals to deceased"""

    for x in range(0, len(position_state)):
        if position_state.iloc[x, 3] == 2 or position_state.iloc[x, 3] == 3:  # check if individual is sick
            if random.random() < death_rate:  # random chance of death
                position_state.iloc[x, 3] = 5  # individual dies

    return position_state


def check_general_inputs(number, cases, distance, table, mask, decay, days, rooms, mask_ratio):
    """Check general inputs to the code from command line."""
    if number/rooms < 5:
        raise Exception('For the number of rooms set, please enter a number of people greater than: {}'.format(rooms*5))
    if cases == 0:
        raise Exception('Please add at least one case')
    if cases > number:
        raise Exception('Number of cases must be less than: {}'.format(rooms*5))
    if distance < 0 or distance > 1:
        raise Exception('Please enter probability between 0 and 1')
    if table < 0 or table > 1:
        raise Exception('Please enter probability between 0 and 1')
    if mask < 0 or mask > 1:
        raise Exception('Please enter probability between 0 and 1')
    if mask_ratio < 0 or mask_ratio > 1:
        raise Exception('Please enter transmission rate between 0 and 1')
    if decay < 0 or decay > 0.25:
        raise Exception('Please enter aerosol decay rate between 0 and 0.25')
    if days < 1 or days > 20:
        raise Exception('Please enter number of days between 1 and 20')


def check_room_setup_inputs(size_x, size_y, table_r, table_x, table_y):
    """Check room setup inputs to the code from command line."""
    if table_x > size_x:
        raise Exception('Table must be within room. Enter value smaller than: {}'.format(size_x))
    if table_y > size_y:
        raise Exception('Table must be within room. Enter value smaller than: {}'.format(size_y))
    if table_r > size_y or table_r > size_x:
        raise Exception('Table is too large. Enter value smaller radius')


def check_network_inputs(rooms, travel, limit):
    """Check network inputs to the code from command line."""
    if rooms > 5 or rooms < 2:
        raise Exception('Number of rooms must be between 2 and 5 inclusive')
    if travel < 0 or travel > 1:
        raise Exception('Please enter probability between 0 and 1')
    if limit not in [0, 1]:
        raise Exception('Please enter 0 for limit off, 1 for limit on')