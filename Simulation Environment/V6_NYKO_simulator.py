#!/usr/bin/env python3
"""

XXXXXX.py
Nathan Wooster, Kaelan Melville, Oscar Bond, Yazad Sukhia
May 2021

This script runs simulations of an epidemic (e.g. coronavirus) for the
air borne spreading of the virus through a network, taking.
The script can be used to:

    1. XXXXX

This is all done using the same simulation code which can also be imported
from this file and used in other ways.

The command line interface to the script makes it possible to run different
simulations without needing to edit the code e.g.:

    $ python simulator.py               # run simulation with default settings
    $ python simulator.py --number=10   # sets size of population to 10
    $ python simulator.py --help        # show all command line options

"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import networkx as nx
import pandas as pd
import random
from numpy.random import randint
import argparse
import seaborn as sns
from matplotlib.animation import FuncAnimation

def main(*args):
    """Command line entry point.
    ## Currently these are just examples, to be finalised at the end of the code #######
            $ python simulator.py                        # show animation on screen
            $ python simulator.py --file=video.mp4       # save animation to video
            $ python simulator.py --plot                 # show plot on screen

            """
    #
    # Argparse has been used to handle parsing the command line arguments.
    #   https://docs.python.org/3/library/argparse.html
    #
    parser = argparse.ArgumentParser(description='Animate an epidemic')

    parser.add_argument('--number', metavar='N', type=int, default=20,
                        help='Size of population')
    parser.add_argument('--cases', metavar='N', type=int, default=2,
                        help='Number of initial infected people')
    parser.add_argument('--distance', metavar='D', type=float, default=1,
                        help='Probability of following two meter social distancing')
    parser.add_argument('--table', metavar='T', type=float, default=0.1,
                        help='Probability of gravitating to the table')
    parser.add_argument('--mask', metavar='M', type=float, default=0.5,
                        help='Probability of wearing a mask')
    parser.add_argument('--rooms', metavar='R', type=int, default=2,
                        help='Number of rooms to simulate')
    parser.add_argument('--travel', metavar='T', type=float, default=0.5,
                        help='Proportion of people that move between rooms')
    parser.add_argument('--size_x', metavar='R', type=int, default=20,
                        help='size of room along x axis')
    parser.add_argument('--size_y', metavar='R', type=int, default=15,
                        help='size of room along y axis')
    parser.add_argument('--table_r', metavar='R', type=int, default=0.5,
                        help='radius of table')
    parser.add_argument('--table_x', metavar='R', type=int, default=2,
                        help='x coordinate of table')
    parser.add_argument('--table_y', metavar='R', type=int, default=2,
                        help='y coordinate of table')
    parser.add_argument('--days', metavar='R', type=int, default=5,
                        help='number of days simulated')
    parser.add_argument('--limit', metavar='L', type=int, default=1,
                        help='Limits on number of people in each room - 1: on, 0:off')
    args = parser.parse_args(args)

    edgelist = create_edgelist(args.rooms)

    # Create network
    G = create_network(edgelist)
    # Set number of nodes
    number_nodes = network_number_nodes(G)
    # Create array to track people
    position_state = create_people_array(args.size_x, args.size_y, args.number,
                                         number_nodes, args.cases, args.distance,
                                         args.table, args.mask, args.travel)
    print(position_state)

    # check nodes are within limits
    nodes = possible_paths(position_state, G)
    position_state = update_node_travel_prob(position_state, nodes, args.limit, number_nodes)


    # Currently this is hardcoded for a set number of rooms but aim is to allow different numbers to be put in.
    room1 = people_array_room(position_state, 1)
    room2 = people_array_room(position_state, 2)
    room3 = people_array_room(position_state, 3)

    # Initialise people using the position_state array (array -> person class instances)
    people = [person(x=position_state.iloc[i, 0], y=position_state.iloc[i, 1], node=position_state.iloc[i, 2], status=position_state.iloc[i, 3], two_meter=position_state.iloc[i, 4], gravitating=position_state.iloc[i, 5], AREA_X=args.table_x, AREA_Y=args.table_y, AREA_R=args.table_r, size_x=args.size_x, size_y=args.size_y) for i in range(len(position_state))]

    # Initialise areas
    area1 = area(args.table_x, args.table_y, args.table_r)
    circle = area1.draw()

    #initialise heat maps for each room
    heat_new = np.zeros((args.size_y+1, args.size_x+1))
    heat_maps = [Room_map(heat_old=heat_new, occupants=position_state, xsize=args.size_x, ysize=args.size_y, node=i) for i in range(1,args.rooms+1)]
    for map in heat_maps:
        map.position_state = position_state
        map.heat_new = map.calculate_heat_new()




    #simulate(it = 0, people=people, heat_maps=heat_maps, position_state=position_state, rooms=args.rooms)


    #use animate function instead of simulate. Simulate is nested!!!
    animate(people=people, heat_maps=heat_maps, position_state=position_state, rooms=args.rooms)

    # Drawing a node graph
    #draw_network(position_state, G, number_nodes)

    # Update the position state for new nodes.
    #nodes = possible_paths(position_state, G)

    position_state = update_node_travel_prob(position_state, nodes, args.limit, number_nodes)

    # Draw updated node graph after simulation
    #draw_network(position_state, G, number_nodes)


def create_edgelist(rooms):
    """Define the edge list dependant on number of rooms."""
    # #edgelist=[(1,2),(1,4),(2,5),(3,5),(2,3)]
    if rooms == 2:
        edgelist = [(1, 2)]
    if rooms == 3:
        edgelist = [(1, 2), (1,3), (2,3)]
    if rooms == 5:
        edgelist = [(1, 2), (1, 4), (2, 5), (3, 5), (2, 3)]

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
    follow = round(N*following_two_meter)
    no_follow = round(N*(1-following_two_meter))
    two_meter = np.concatenate((([1]*follow), ([0]*no_follow)))
    #gravitating towards the table
    gravitate = round(N*gravitate_table)
    no_gravitate = round(N*(1-gravitate_table))
    number_gravitating = np.concatenate((([1]*gravitate), ([0]*no_gravitate)))
    #wearing a mask
    masked = round(N*using_mask)
    no_masked = round(N*(1-using_mask))
    number_masked = np.concatenate((([1]*masked), ([0]*no_masked)))
    # travelling round
    travelling = round(N*travel)
    no_travelling = round(N*(1-travel))
    number_travelling = np.concatenate((([1]*masked), ([0]*no_masked)))
    data_in = np.stack((x_position, y_position, start_nodes, start_status, two_meter, number_gravitating, number_masked, number_travelling), axis=1)
    position_state = pd.DataFrame(data=data_in, columns=['x', 'y', 'node', 'status', 'two_meter', 'gravitating', 'mask', 'travelling'])
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

def transmission(position_state, heat):
    for x in range(0, len(position_state)):

        if position_state.iloc[x]['status'] == 1:# transmission only occurs on healthy individuals

            if heat[round(position_state['y'].iloc[x]), round(position_state['x'].iloc[x])] > 20:

                    if heat[round(position_state['y'].iloc[x]),round(position_state['x'].iloc[x])] > np.random.randint(0,101):

                        position_state.iloc[x]['status'] = 2 # stands for infected
    return position_state

#----------------------------------------------------------------------------#
#                  Simulation classes                                        #
#----------------------------------------------------------------------------#

#--------------------------NATHAN CLASSES-----------#

#define place people gravitate towards (circle)
class area(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r

    def draw(self):
        return plt.Circle((self.cx, self.cy), self.r, color='b', fill=False) #creates circle coords cx cy and radius r (built in function)

#create moving person class with original x, y and node inputs
class person(object):
    def __init__(self, x, y, node, status, two_meter, gravitating, AREA_X, AREA_Y, AREA_R, size_x, size_y):
        self.x = x
        self.y = y
        self.node = node
        self.status = status
        self.two_meter = two_meter
        self.gravitating = gravitating
        self.step_x = self.make_new_step_size() #calls function to create a new step size for person
        self.step_y = self.make_new_step_size()
        self.AREA_X = AREA_X
        self.AREA_Y = AREA_Y
        self.AREA_R = AREA_R
        self.size_x = size_x
        self.size_y = size_y

    def make_new_step_size(self, max_step=10):
        return (np.random.random_sample() - 0.5)*max_step / 5 #creates random number for step size 0 to 0.1

    def move(self, people):

        def distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) #uses coords and calulates distance between two points

        def inside(x1, y1, cx, cy, r):
            if distance(x1, y1, cx, cy) <= r:  # defines if dot is inside a specific area (coord cx, cy and radius = r)
                return True
            else:
                return False

        def stop(self):
            self.step_x = 0
            self.step_y = 0
            return

        def direction(self):

            if self.step_x > 0:
                x_direction = 'right'
            if self.step_x < 0:
                x_direction = 'left'
            if self.step_y > 0:
                y_direction = 'up'
            if self.step_y < 0:
                y_direction = 'down'
            if self.step_x == 0:
                x_direction = 'stationary'
            if self.step_y == 0:
                y_direction = 'stationary'

            return (x_direction, y_direction)

        def position_compared_to_object(self, cx, cy):
            if self.x - cx > 0:
                x_position = 1 #'right of circle'
            elif self.x - cx < 0:
                x_position = -1 #'left of circle'
            else:
                x_position = 0 #'on circle'

            if self.y - cy > 0:
                y_position = 1 #'above circle'
            elif self.y - cy < 0:
                y_position = -1 #'below circle'
            else:
                y_position = 0 #'on circle'

            return (x_position, y_position)


        def move_towards(self, cx, cy):
            if position_compared_to_object(self, cx, cy)[0] == 1 and direction(self)[0] == 'right':
                self.step_x = -1 * self.step_x
            if position_compared_to_object(self, cx, cy)[1] == 1 and direction(self)[1] == 'up':
                self.step_y = -1 * self.step_y
            if position_compared_to_object(self, cx, cy)[0] == -1 and direction(self)[0] == 'left':
                self.step_x = -1 * self.step_x
            if position_compared_to_object(self, cx, cy)[1] == -1 and direction(self)[1] == 'down':
                self.step_y = -1 * self.step_y
            return

        def move_away(self, cx, cy):
            if position_compared_to_object(self, cx, cy)[0] == -1 and direction(self)[0] == 'right':
                self.step_x = -1 * self.step_x
            if position_compared_to_object(self, cx, cy)[1] == -1 and direction(self)[1] == 'up':
                self.step_y = -1 * self.step_y
            if position_compared_to_object(self, cx, cy)[0] == 1 and direction(self)[0] == 'left':
                self.step_x = -1 * self.step_x
            if position_compared_to_object(self, cx, cy)[1] == 1 and direction(self)[1] == 'down':
                self.step_y = -1 * self.step_y
            return

        def calc_dist_to_other_people(d): #d is the person, n is all the other people
            dist_from_other_people = 999
            for n in people:
                if n.node == d.node:
                    if n != d: #make sure not doing same person in calc
                        dist_from_person_n = distance(n.x, n.y, d.x, d.y)
                        if dist_from_person_n < dist_from_other_people:
                            dist_from_other_people = dist_from_person_n
                            closest_person = n
            return (dist_from_other_people,closest_person)

        #actual movement now stated using functions given above
        if np.random.random_sample() < 0.50:  # % chance the speed of person stays the same (constant step added to coord)
            self.x = self.x + self.step_x  # this is how the dot moves at constant rate (constant added to dot position)
            self.y = self.y + self.step_y
            # certain % chance person changes step size
        else:
            self.velx = self.make_new_step_size() # % chance a new velocity is generated
            self.vely = self.make_new_step_size()
            self.x = self.x + self.step_x   # the coord is updated with that new constant (different amount than before so dot looks like it sped up/slowed down)
            self.y = self.y + self.step_y
        if self.x >= self.size_x:  # so cannot go outside boundary of 10x10 grid
            self.x = self.size_x
            self.step_x = -1 * self.step_x
        if self.x <= 0:  # so cannot go outside boundary of 10x10 grid
            self.x = 0
            self.step_x = -1 * self.step_x
        if self.y >= self.size_y:  # so cannot go outside boundary of 10x10 grid
            self.y = self.size_y
            self.step_y = -1 * self.step_y
        if self.y <= 0:  # so cannot go outside boundary of 10x10 grid
            self.y = 0
            self.step_y = -1 * self.step_y

        if inside(self.x, self.y, self.AREA_X, self.AREA_Y, self.AREA_R): #if at table area
            if self.gravitating == 1: #if meant to be at table stay there
                stop(self)
            if np.random.random_sample() < 0.5: #have a %chance of leaving the table
                self.gravitating = 0

        if self.gravitating == 1:   # if gravitate on
            move_towards(self, self.AREA_X, self.AREA_Y)

        if self.two_meter == 1: #follow 2 meter rule
            min_dist_to_someone = calc_dist_to_other_people(self)[0]
            closest_person = calc_dist_to_other_people(self)[1]
            if min_dist_to_someone < 2: #if closer than 2meters to someone
                move_away(self, closest_person.x, closest_person.y)


#----------------------------------------------------------------------------#
#                  Kaelan Room Heatmap classes                               #
#----------------------------------------------------------------------------#

class Room_map(object):
    def __init__(self, heat_old, occupants, xsize, ysize, node):
        self.heat_old = heat_old
        self.node = node
        self.occupants = occupants[occupants['node'] == self.node]
        self.xsize = xsize+1
        self.ysize = ysize+1

    def map_position_states(self):
        pos_map = np.zeros((self.ysize, self.xsize))
        for row in range(0, len(self.occupants)):
            pos_map[round(self.occupants['y'].iloc[row]), round(self.occupants['x'].iloc[row])] = self.occupants['status'].iloc[row]
        return pos_map

    def heat_source(self):  # will add heat source to map based on individuals new position
        sources = np.zeros((self.ysize, self.xsize))
        sources += self.map_position_states()
        sources[sources == 3] = 100
        sources[sources == 3.5] = 50
        sources[sources < 50] = 0
        return sources

    def calculate_heat_new(self):  # will calculate single step of heat dispersion

        heat_left = np.roll(self.heat_old, 1, axis=1)
        heat_right = np.roll(self.heat_old, -1, axis=1)
        heat_up = np.roll(self.heat_old, -1, axis=0)
        heat_down = np.roll(self.heat_old, 1, axis=0)

        heat_new = 0.25 * (heat_left + heat_right + heat_up + heat_down)  # cell heat is the average of adjacent cells
        heat_new = heat_new + self.heat_source()
        heat_new[heat_new > 100] = 100

        heat_new[:, 0] = heat_new[:, 1]  # boundary conditions
        heat_new[:, -1] = heat_new[:, -2]
        heat_new[0, :] = heat_new[1, :]
        heat_new[-1, :] = heat_new[-2, :]

        self.heat_old = heat_new

    def show_map(self):  # creates a heatmap and position map
        # create marker for healthy individuals in heatmap
        heat_map = self.heat_old
        #pos = self.map_position_states()
        #heat_map[pos == 1] = -100

        # create matplot figure with subplots

        return heat_map # heatmap
#----------------------------------------------------------------------------#
#                  End of simulation classes                                        #
#----------------------------------------------------------------------------#



#REPLACE THIS WITH YAZ CODE
# animation function.  This is called sequentially
def animate(people, heat_maps, position_state, rooms):

    grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
    fig, axes = plt.subplots(1, rooms, figsize=(15, 5))
    anim = FuncAnimation(fig=fig, func=simulate,
                         frames=100,
                         fargs=(people, heat_maps, position_state, axes),
                         interval=50,
                         blit=False,
                         repeat=False)
    plt.show()

def update_position_state(position_state,people):
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

# placeholder simulate function
def simulate(it, people, heat_maps, position_state, axes):

    # move each person
    for i in people:
        i.move(people=people)
    position_state = update_position_state(position_state, people)


    # update heat maps
    for map in heat_maps:
        map.occupants = position_state
        map.calculate_heat_new()

        # introduce some transmission function to infect new people
        transmission(map.occupants, map.heat_old)

    for map in heat_maps:
        sns.heatmap(map.show_map(),
                    ax=axes[map.node-1],
                    cbar=False,
                    cmap='icefire',
                    center=0,
                    vmin =0,
                    vmax=100,
                    )
        axes[map.node-1].set_title(f'Room {map.node} Heat Map')

if __name__ == "__main__":

    # Command line entry point
    import sys
    main(*sys.argv[1:])
















