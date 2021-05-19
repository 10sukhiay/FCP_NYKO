#!/usr/bin/env python3
"""

other_functions.py
Kaelan Melville
May 2021


"""

#standard imports
import numpy as np
import pandas as pd
from Heat_Mapping import Room_map
from Person_Class import person
from matplotlib import pyplot as plt
import random
import networkx as nx
from numpy.random import randint
import math

#custom imports


def create_edgelist(rooms):
    """Define the edge list dependant on number of rooms."""
    # #edgelist=[(1,2),(1,4),(2,5),(3,5),(2,3)]
    if rooms == 2:
        edgelist = [(1, 2)]
    if rooms == 3:
        edgelist = [(1, 2), (1,3), (2,3)]
    if rooms == 4:
        edgelist = [(1, 2), (1,3), (1,4), (2,3), (2,4), (3,4)]
    if rooms == 5:
        edgelist = [(1, 2), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,4), (3,5)]

    return(edgelist)

def create_network(edgelist):
    """Create a networkx graph from the edgelist."""
    G = nx.Graph(edgelist)
    #nx.draw(G, with_labels=True)
    #plt.show()   # this displays the graph - turn on as required.
    return(G)

def network_number_nodes(G):
    """Calculate the number of nodes within the networkx graph"""
    number_nodes = G.number_of_nodes()
    return(number_nodes)

def create_people_array(ROOM_SIZE_X, ROOM_SIZE_Y, N, number_nodes, number_infected, following_two_meter, gravitate_table, using_mask, travel):
    """Set-up the array of people dependant on inputs. """
    x_position = randint(0,ROOM_SIZE_X+1,N) # randomly assign x values for each person
    y_position = randint(0,ROOM_SIZE_Y+1,N) # randomly assign y values for each person
    start_nodes = randint(1, number_nodes+1, N)

    # SUSCEPTIBLE 1
    # INFECTED    2
    # INFECTIOUS  3
    # RECOVERED   4
    # DECEASED    5
    start_status = np.concatenate((([3]*number_infected), ([1]*(N-number_infected))))
    random.shuffle(start_status)
    # following two meter rule
    follow = math.ceil(N*following_two_meter)
    no_follow = math.floor(N*(1-following_two_meter))
    two_meter = np.concatenate((([1]*follow), ([0]*no_follow)))
    #gravitating towards the table
    gravitate = math.ceil(N*gravitate_table)
    no_gravitate = math.floor(N*(1-gravitate_table))
    number_gravitating = np.concatenate((([1]*gravitate), ([0]*no_gravitate)))
    #wearing a mask
    masked = math.ceil(N*using_mask)
    no_masked = math.floor(N*(1-using_mask))
    number_masked = np.concatenate((([1]*masked), ([0]*no_masked)))
    # travelling round
    travelling = math.ceil(N*travel)
    no_travelling = math.floor(N*(1-travel))
    number_travelling = np.concatenate((([1]*masked), ([0]*no_masked)))
    counter = ([0]*N)
    data_in = np.stack((x_position, y_position, start_nodes, start_status, two_meter, number_gravitating, number_masked, number_travelling, counter), axis=1)
    position_state = pd.DataFrame(data=data_in, columns=['x', 'y', 'node', 'status', 'two_meter', 'gravitating', 'mask', 'travelling', 'counter'])
    return(position_state)

def people_array_room(position_state,i):
    """Create array of people dependant on node location"""
    room = position_state[position_state["node"] == i]
    return(room)

def possible_paths(position_state, G):
    """Creates a list of the possible nodes that people can travel to"""
    # need to be careful so that people can only travel to connected nodes.
    nodes =[]
    for i in range(0, len(position_state),1):
        possible_nodes = list(nx.single_source_shortest_path(G, source=position_state.iloc[i,2], cutoff=1))
        nodes.append(possible_nodes)
    return(nodes)

def update_node_travel_prob(position_state, nodes, limit,number_nodes):
    """Update position_state dependant on limited number of people in each room"""
    if limit == 0:
        random_node_choice(position_state, nodes)
    if limit == 1:
        random_node_choice(position_state, nodes)
        while max(node_count_individuals(position_state, number_nodes))>((len(position_state)/number_nodes)+1):
            random_node_choice(position_state, nodes)
    return position_state

def random_node_choice(position_state, nodes):
    """Update position_state dependant on connected nodes"""
    for i in range(0, len(position_state), 1):
        if position_state.iloc[i, 7] == 1:
            position_state.iloc[i, 2] = random.choice(nodes[i])
    return(position_state)

def node_count_individuals(position_state, number_nodes):
    """Count the number of individual at each node"""
    node_count = []
    for n in range(1, number_nodes + 1):
        a = 0
        for i in range(0, len(position_state)):
            if position_state.iloc[i, 2] == n:
                a = a + 1
        node_count.append(a)
    return(node_count)

def draw_network(position_state, G, number_nodes):
    """Draw network graph"""
    node_count = node_count_individuals(position_state, number_nodes)

    for i in range(1, number_nodes+1):
        G.nodes[i]['Number'] =  node_count[i-1]

    pos = nx.spring_layout(G)
    # increase size of nodes to be able to see
    node_count_size = [i * 100 for i in node_count]

    # draw the network with node size dependant on no.people
    nx.draw(G, pos, node_size=(node_count_size))
    node_labels = nx.get_node_attributes(G, 'Number')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    plt.legend(['Room - Number of People in the Room'])
    plt.show()

def update_position_state(position_state,people):
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
    #print('iteration finished and this is new position_state array:')
    #print(position_state)  # array refilled with people
    return (position_state)

def update_people_nodes(position_state,people):
    """Update node for people based on position_state array."""
    position_state.iloc[:, :2] = 0  # array emptied for x y only
    # this code adds values from people objects back into array
    k = 0
    print('nodes looked')
    for t in people:
        t.node = position_state['node'].iloc[k]
        t.x = random.randint(0, t.size_x)
        t.y = random.randint(0, t.size_y)
        k += 1  # iterator for picking the correct row
    # check
    print('nodes replaced')
    #print(position_state)  # array refilled with people
    return people

def transmission(position_state, heat, node, day_length):
    for x in range(0, len(position_state)):
        if position_state.iloc[x]['node'] == node: # checks person is in correct room
            if position_state.iloc[x]['status'] == 1:# transmission only occurs on healthy individuals

                if heat[round(position_state['y'].iloc[x]), round(position_state['x'].iloc[x])] > 20:

                        if heat[round(position_state['y'].iloc[x]),round(position_state['x'].iloc[x])] > (np.random.randint(0,201))/2:

                            position_state.iloc[x]['status'] = 2 # stands for infected
<<<<<<< HEAD
                            position_state.iloc[x]['counter'] = round((1-((random.random() - 0.5) / 2.5)) * day_length * 2) # 2 day incubation period +- 20%
    return position_state

def status_change(position_state, day_length):
    for x in range(0, len(position_state)):
        if position_state.iloc[x]['counter'] == 0:  # check if status requires changing

            if position_state.iloc[x]['status'] == 2:  # infected individuals
                position_state.iloc[x]['status'] = 3  # now infectious
                position_state.iloc[x]['counter'] = round((1-((random.random()-0.5)/2.5))*day_length*3)  # 3 day infectious period give or take 20%

            elif position_state.iloc[x]['status'] == 3:  # infectious individuals
                position_state.iloc[x]['status'] = 4  # now recovered
                position_state.iloc[x]['counter'] = -1

    return position_state


def death_chance(position_state, death_rate):
    for x in range(0, len(position_state)):
        if position_state.iloc[x]['status'] == 2 or position_state.iloc[x]['status'] == 3:  # check if status requires changing
            death_roll = random.random()
            if death_roll < death_rate:
                position_state.iloc[x]['status'] = 5  # individual dies

    return position_state
=======
    return position_state

def check_general_inputs(number, cases, distance, table, mask, decay, rooms):
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
    #if decay < 0 or decay > 1:
        #raise Exception('Please enter probability between 0 and 1')

def check_room_setup_inputs(size_x, size_y, table_r, table_x, table_y):
    """Check room setup inputs to the code from command line."""
    if table_x > size_x:
        raise Exception('Table must be within room. Enter value smaller than: {}'.format(size_x))
    if table_y > size_y:
        raise Exception('Table must be within room. Enter value smaller than: {}'.format(size_y))
    if table_r > size_y or table_r > size_x:
        raise Exception('Table is too large. Enter value smaller radius')

def check_network_inputs(rooms, travel, days, limit):
    """Check network inputs to the code from command line."""
    if rooms > 5 or rooms < 2:
        raise Exception('Number of rooms must be between 2 and 5 inclusive')
    if travel < 0 or travel > 1:
        raise Exception('Please enter probability between 0 and 1')
    if limit not in [0,1]:
        raise Exception('Please enter 0 for limit off, 1 for limit on')

>>>>>>> fc53be2a416cebf3624519b20c85002b7b9f2941

