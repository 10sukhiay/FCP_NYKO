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
#standard imports
import argparse

# custom imports
from Heat_Mapping import Room_map
from Person_Class import person
from animate import animate
from other_functions import *
from area import area

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

    parser.add_argument('--number', metavar='N', type=int, default=17,
                        help='Size of population')
    parser.add_argument('--cases', metavar='N', type=int, default=1,
                        help='Number of initial infected people')
    parser.add_argument('--distance', metavar='D', type=float, default=1,
                        help='Probability of following two meter social distancing')
    parser.add_argument('--table', metavar='T', type=float, default=0.1,
                        help='Probability of gravitating to the table')
    parser.add_argument('--mask', metavar='M', type=float, default=0.5,
                        help='Probability of wearing a mask')
    parser.add_argument('--rooms', metavar='R', type=int, default=3,
                        help='Number of rooms to simulate')
    parser.add_argument('--travel', metavar='T', type=float, default=1,
                        help='Proportion of people that move between rooms')
    parser.add_argument('--size_x', metavar='R', type=int, default=8,
                        help='size of room along x axis')
    parser.add_argument('--size_y', metavar='R', type=int, default=10,
                        help='size of room along y axis')
    parser.add_argument('--table_r', metavar='R', type=int, default=0.5,
                        help='radius of table')
    parser.add_argument('--table_x', metavar='R', type=int, default=2,
                        help='x coordinate of table')
    parser.add_argument('--table_y', metavar='R', type=int, default=2,
                        help='y coordinate of table')
    parser.add_argument('--days', metavar='R', type=int, default=2,
                        help='number of days simulated')
    parser.add_argument('--limit', metavar='L', type=int, default=0,
                        help='Limits on number of people in each room - 1: on, 0:off')
    parser.add_argument('--decay', metavar='L', type=int, default=1,
                        help='The "heat" decay per iteration, represents the settling rate of particles')
    args = parser.parse_args(args)

    check_general_inputs(args.number, args.cases, args.distance, args.table, args.mask, args.decay, args.rooms)

    #check_room_setup_inputs(args.size_x, args.size_y, args.table_r, args.table_x, args.table_y)

    #check_network_inputs(args.rooms, args.travel, args.days, args.limit)

    #create edgelist
    edgelist = create_edgelist(args.rooms)
    # Create network
    G = create_network(edgelist)
    # Set number of nodes
    number_nodes = network_number_nodes(G)
    # Create array to track people
    position_state = create_people_array(args.size_x, args.size_y, args.number,
                                         number_nodes, args.cases, args.distance,
                                         args.table, args.mask, args.travel)
    # check nodes are within limits
    nodes = possible_paths(position_state, G)
    position_state = update_node_travel_prob(position_state, nodes, args.limit, number_nodes)

    # Initialise people using the position_state array (array -> person class instances)
    people = [person(x=position_state.iloc[i, 0], y=position_state.iloc[i, 1], node=position_state.iloc[i, 2], status=position_state.iloc[i, 3], two_meter=position_state.iloc[i, 4], gravitating=position_state.iloc[i, 5], AREA_X=args.table_x, AREA_Y=args.table_y, AREA_R=args.table_r, size_x=args.size_x, size_y=args.size_y) for i in range(len(position_state))]

    # Initialise areas
    area1 = area(args.table_x, args.table_y, args.table_r)
    circle = area1.draw()

    #initialise heat maps for each room
    heat_new = np.zeros((args.size_y+1, args.size_x+1))
    heat_maps = [Room_map(heat_old=heat_new, position_state=position_state,
                          xsize=args.size_x, ysize=args.size_y,
                          node=i, decay=args.decay)
                 for i in range(1,args.rooms+1)]



    # loop for multiple days
    for day in range(args.days):
    # Use Animate to show/save animations. Create Simulate function that ignores animation requirements???
        #use animate function instead of update. update is nested!!!

        animate(people=people, heat_maps=heat_maps, position_state=position_state, rooms=args.rooms)

        # Drawing a node graph
        draw_network(position_state, G, number_nodes)

        # Update the position state for new nodes.
        nodes = possible_paths(position_state, G)

        position_state = update_node_travel_prob(position_state, nodes, args.limit, number_nodes)
        people = [person(x=position_state.iloc[i, 0], y=position_state.iloc[i, 1], node=position_state.iloc[i, 2], status=position_state.iloc[i, 3], two_meter=position_state.iloc[i, 4], gravitating=position_state.iloc[i, 5], AREA_X=args.table_x, AREA_Y=args.table_y, AREA_R=args.table_r, size_x=args.size_x, size_y=args.size_y) for i in range(len(position_state))]

        print(position_state)
        # Draw updated node graph after simulation
        #draw_network(position_state, G, number_nodes)



if __name__ == "__main__":

    # Command line entry point
    import sys
    main(*sys.argv[1:])
















