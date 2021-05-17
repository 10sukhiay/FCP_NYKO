import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import networkx as nx
import pandas as pd
import random
from numpy.random import randint
import argparse

#GLOBAL CONSTANTS
ROOM_SIZE_X = 10
ROOM_SIZE_Y = 10
AREA_X = 2 #area coordinate to gravitate towards
AREA_Y = 2
AREA_R = 0.5 #area radius

def main(*args):
    parser = argparse.ArgumentParser(description='Animate an epidemic')

    parser.add_argument('--number', metavar='N', type=int, default=10,
                        help='Use a N x N simulation grid')
    parser.add_argument('--cases', metavar='N', type=int, default=2,
                        help='Number of initial infected people')
    parser.add_argument('--distance', metavar='D', type=float, default=0.5,
                        help='Probability of following two meter social distancing')
    parser.add_argument('--table', metavar='T', type=float, default=0.1,
                        help='Probability of gravitating to the table')
    parser.add_argument('--mask', metavar='M', type=float, default=0.5,
                        help='Probability of wearing a mask')
    parser.add_argument('--rooms', metavar='R', type=int, default=2,
                        help='Number of rooms to simulate')
    args = parser.parse_args(args)

    # Define the edge list dependant on number of rooms. Could also look at connectivity such as:
    # #edgelist=[(1,2),(1,4),(2,5),(3,5),(2,3)]
    if args.rooms == 2:
        edgelist = [(1, 2)]
    if args.rooms == 3:
        edgelist = [(1, 2), (1,3), (2,3)]

    # Create network
    G = create_network(edgelist)
    # Set number of nodes
    number_nodes = network_number_nodes(G)
    # Create array to track people
    position_state = create_people_array(ROOM_SIZE_X, ROOM_SIZE_Y, args.number,
                                         number_nodes, args.cases, args.distance,
                                         args.table, args.mask)

    # Currently this is hardcoded for a set number of rooms but aim is to allow different numbers to be put in.
    room1 = people_array_room(position_state, 1)
    room2 = people_array_room(position_state, 2)
    room3 = people_array_room(position_state, 3)

    print('room1 array:')
    print(room1)

    # Initialise people using the position_state array (array -> person class instances)
    people = [person(x=position_state.iloc[i, 0], y=position_state.iloc[i, 1], node=position_state.iloc[i, 2]) for i in
              range(len(position_state))]  # creates people for each row in the array

    #update_position_state(position_state)
    print('move run finished and this is new position_state array:')
    print(position_state)  # array refilled with people

    return(people)


def create_network(edgelist):
    # Create a networkx graph from the edgelist.
    G = nx.Graph(edgelist)
    nx.draw(G, with_labels=True)
    #plt.show()   # this displays the graph - turn on as required.
    return(G)

def network_number_nodes(G):
    number_nodes = G.number_of_nodes()
    print('number of nodes is:')
    print(number_nodes)
    return(number_nodes)

def create_people_array(ROOM_SIZE_X, ROOM_SIZE_Y, N, number_nodes, number_infected, following_two_meter, gravitate_table, using_mask):
    x_position = randint(0,ROOM_SIZE_X+1,N) # randomly assign x values for each person
    y_position = randint(0,ROOM_SIZE_Y+1,N) # randomly assign y values for each person
    start_nodes = randint(1, number_nodes+1, N)
    start_status = np.concatenate((([1]*number_infected), ([0]*(N-number_infected))))
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

    data_in = np.stack((x_position, y_position, start_nodes, start_status, two_meter, number_gravitating, number_masked), axis=1)
    position_state = pd.DataFrame(data=data_in, columns=['x', 'y', 'node', 'status', 'two_meter', 'gravitating', 'mask'])
    return(position_state)

def people_array_room(position_state,i):
    room = position_state[position_state["node"] == i]
    return(room)


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
    def __init__(self, x, y, node):
        self.x = x
        self.y = y
        self.node = node
        self.step_x = self.make_new_step_size() #calls function to create a new step size for person
        self.step_y = self.make_new_step_size()

    def make_new_step_size(self, max_step=1):
        return (np.random.random_sample() - 0.5)*max_step / 5 #creates random number for step size 0 to 0.1

    def move(self):

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
        if self.x >= ROOM_SIZE_X:  # so cannot go outside boundary of 10x10 grid
            self.x = ROOM_SIZE_X
            self.step_x = -1 * self.step_x
        if self.x <= 0:  # so cannot go outside boundary of 10x10 grid
            self.x = 0
            self.step_x = -1 * self.step_x
        if self.y >= ROOM_SIZE_Y:  # so cannot go outside boundary of 10x10 grid
            self.y = ROOM_SIZE_Y
            self.step_y = -1 * self.step_y
        if self.y <= 0:  # so cannot go outside boundary of 10x10 grid
            self.y = 0
            self.step_y = -1 * self.step_y

        if inside(self.x, self.y, AREA_X, AREA_Y, AREA_R): #stop if reach table #NEED A WAY OF ACCESSING AREA CLASS if want multiple areas????
            stop(self)

        if np.random.random_sample() < 1:  # % chance to gravitate towards point 1,1
            move_towards(self, AREA_X, AREA_Y) #NEED A WAY OF ACCESSING AREA CLASS????

        if np.random.random_sample() < 0.00001: #%chance to follow 2 meter rule
            min_dist_to_someone = calc_dist_to_other_people(self)[0]
            closest_person = calc_dist_to_other_people(self)[1]
            if min_dist_to_someone < 2: #if closer than 2meters to someone
                move_away(self, closest_person.x, closest_person.y)


#this also works for 2meter rule..
        #if np.random.random_sample() < 1: #%chance to follow 2 meter rule
            #min_dist_to_someone = calc_dist_to_other_people(self)[0]
            #if min_dist_to_someone < 2:  # if closer than 2meters to someone
                #for i in range(1, 10): #creates 10 random step sizes for the person and checks if they go further from the person
                    #self.step_x = self.make_new_step_size()
                    #self.step_y = self.make_new_step_size()
                    #self.x = self.x + self.step_x #adds these steps to the current coords
                    #self.y = self.y + self.step_y
                    #if calc_dist_to_other_people(self)[0] <= min_dist_to_someone:
                        #self.x = self.x - self.step_x
                        #self.y = self.y - self.step_y

#----------------------------------------------------------------------------#
#                  Kaelan Room Heatmap classes                               #
#----------------------------------------------------------------------------#

class Room_map:
    def __init__(self, heat_new, position_state, xsize, ysize, ):
        self.heat_old = heat_new
        self.position_state = position_state
        self.xsize = xsize
        self.ysize = ysize

    def map_position_states(self):
        pos_map = np.zeros((self.xsize, self.ysize))

        for x in self.position_state:
            pos_map[x[0], x[1]] = x[2]

        return pos_map

    def heat_source(self):  # will add heat source to map based on individuals new position
        sources = np.zeros((self.xsize, self.ysize))
        sources += self.map_position_states()
        sources[sources == 2] = 100
        sources[sources != 100] = 0
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

        return heat_new

    def show_map(self):  # creates a heatmap and position map
        # create marker for healthy individuals in heatmap
        heat_map = self.calculate_heat_new()
        pos = self.map_position_states()
        heat_map[pos == 1] = -100
        # create marker for healthy individuals in pos map
        pos_map = self.map_position_states()
        pos_map[pos_map == 1] = -2

        # create matplot figure with subplots
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        sns.heatmap(np.transpose(heat_map), ax=axes[0], cbar=False, cmap='icefire', center=0).invert_yaxis()  # heatmap
        axes[0].set_title("Heat Map")

        # sns.heatmap(pos_map, ax=axes[1], cbar=False, cmap='icefire', center = 0).invert_yaxis() #position heatmap
        # axes[1].set_title("Position Map")
        sns.scatterplot(x=self.position_state[:, 0], y=self.position_state[:, 1], data=self.position_state, ax=axes[1],
                        hue=self.position_state[:, 2], legend=False, palette='coolwarm')  # position scatterplot
        axes[1].set_title("Position Map")
        axes[1].set_xlim(0, self.xsize)
        axes[1].set_ylim(0, self.ysize)

#----------------------------------------------------------------------------#
#                  End of simulation classes                                        #
#----------------------------------------------------------------------------#



#REPLACE THIS WITH YAZ CODE
# animation function.  This is called sequentially
def animate(i):
    for person in people: #goes through all people
        person.move() #does all the move function (multiple functions inside) for person
    d.set_data([person.x for person in people], #d is taken from the dots coords to plot
               [person.y for person in people])
    return d,


if __name__ == "__main__":

    # Command line entry point
    import sys
    people = main(*sys.argv[1:])
    #main(*sys.argv[1:])


    #position_state = create_people_array(ROOM_SIZE_X, ROOM_SIZE_Y, N, number_nodes, number_infected, following_two_meter)
    #print('original position_state array:')
    #print(position_state)






# Initialise areas
    area1 = area(AREA_X, AREA_Y, AREA_R)


### turn this into a function to be called from the main - called Animation
# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure() #empty figure
ax = plt.axes(xlim=(0, ROOM_SIZE_X), ylim=(0, ROOM_SIZE_Y)) #axes limit room_size
d, = ax.plot([person.x for person in people], #plot person coords x
             [person.y for person in people], 'ro') #plot person coords y

circle = area1.draw()
ax.add_artist(circle) #add circle to axes plot


# call the animator.
anim = animation.FuncAnimation(fig, animate, frames=200, interval=20) #in built function to keep updating plot to creates animation

plt.show() #shows plot


def update_position_state(position_state):
    position_state.iloc[:, :2] = 0 #array emptied for x y only
    # this code adds values from people objects back into array
    k = 0
    for t in people:
        position_state.iloc[k, 0] = t.x
        position_state.iloc[k, 1] = t.y
        position_state.iloc[k, 2] = t.node
        k +=1 # iterator for picking the correct row

    return(position_state)

