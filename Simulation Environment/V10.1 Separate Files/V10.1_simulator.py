#!/usr/bin/env python3
"""

simulator_NYKO.py
Oscar Bond, Kaelan Melville, Yazad Sukhia, Nathan Wooster
May 2021

This script runs simulations of an epidemic (e.g. coronavirus) for the
air borne spreading of the virus through a network.

"""
# standard imports
import argparse

# custom imports
from Heat_Mapping import RoomMap
from Person_Class import Person
from animate import animate
from other_functions import *
# from area import area


def main(*args):
    """Command line entry point.
    The file can be run from the command line thanks to the command line
    interface. This allows parameters to be changes without editing the code. e.g.:

    $ python simulator_NYKO.py               # run simulation with default settings
    $ python simulator_NYKO.py --number=10   # sets size of population to 10
    $ python simulator_NYKO.py --help        # show all command line options
    """
    #
    # Argparse has been used to handle parsing the command line arguments.
    #   https://docs.python.org/3/library/argparse.html
    #
    parser = argparse.ArgumentParser(description='Animate an epidemic')

    parser.add_argument('--number', metavar='N', type=int, default=50,
                        help='Size of population')
    parser.add_argument('--cases', metavar='C', type=int, default=1,
                        help='Number of initial infected people')
    parser.add_argument('--distance', metavar='SD', type=float, default=0.8,
                        help='Probability of following two meter social distancing')
    parser.add_argument('--table', metavar='Pt', type=float, default=0.1,
                        help='Probability of gravitating to the table')
    parser.add_argument('--mask', metavar='M', type=float, default=0.5,
                        help='Probability of wearing a mask')
    parser.add_argument('--rooms', metavar='R', type=int, default=3,
                        help='Number of rooms to simulate')
    parser.add_argument('--travel', metavar='T', type=float, default=0.5,
                        help='Proportion of people that can move between rooms')
    parser.add_argument('--size_x', metavar='X', type=int, default=14,
                        help='size of room along x axis')
    parser.add_argument('--size_y', metavar='Y', type=int, default=14,
                        help='size of room along y axis')
    parser.add_argument('--table_r', metavar='Tr', type=int, default=0.5,
                        help='radius of table')
    parser.add_argument('--table_x', metavar='Tx', type=int, default=2,
                        help='x coordinate of table')
    parser.add_argument('--table_y', metavar='Ty', type=int, default=2,
                        help='y coordinate of table')
    parser.add_argument('--days', metavar='D', type=int, default=18,
                        help='number of days simulated')
    parser.add_argument('--limit', metavar='L', type=int, default=1,
                        help='Limits on number of people in each room 1: on, 0:off')
    parser.add_argument('--decay', metavar='d', type=int, default=0.25,
                        help='The "heat" decay per iteration, represents the settling rate of particles')
    parser.add_argument('--day_length', metavar='Dl', type=int, default=24,
                        help='The number of iterations per day')
    parser.add_argument('--death_rate', metavar='Rd', type=float, default=0.0003,
                        help='Likelihood of death 0 to 1')
    parser.add_argument('--mask_ratio', metavar='Rd', type=float, default=0.5,
                        help='Ratio of particles a masked person creates in comparison to unmasked')
    args = parser.parse_args(args)

    # check user inputs with exceptions
    check_general_inputs(args.number, args.cases, args.distance, args.table, args.mask, args.decay, args.days,
                         args.rooms, args.mask_ratio)
    check_room_setup_inputs(args.size_x, args.size_y, args.table_r, args.table_x, args.table_y)
    check_network_inputs(args.rooms, args.travel, args.limit)

    # create edgelist
    edgelist = create_edgelist(args.rooms)
    # Create network
    g = create_network(edgelist)
    # Set number of nodes
    number_nodes = network_number_nodes(g)
    # Create array to track people
    position_state = create_people_array(args.size_x, args.size_y, args.number,
                                         number_nodes, args.cases, args.distance,
                                         args.table, args.mask, args.travel)
    for x in range(0, len(position_state)):  # set counter for any starting infected people
        if position_state.iloc[x]['status'] == 3:
            position_state.iloc[x]['counter'] = args.day_length*3

    # check nodes are within limits
    nodes = possible_paths(position_state, g)
    position_state = update_node_travel_prob(position_state, nodes, args.limit, number_nodes)

    # Initialise people using the position_state array (array -> person class instances)
    people = [Person(x=position_state.iloc[i, 0], y=position_state.iloc[i, 1], node=position_state.iloc[i, 2],
                     status=position_state.iloc[i, 3], two_meter=position_state.iloc[i, 4],
                     gravitating=position_state.iloc[i, 5], area_x=args.table_x,
                     area_y=args.table_y, area_r=args.table_r,
                     size_x=args.size_x, size_y=args.size_y) for i in range(len(position_state))]

    # initialise heat maps for each room
    heat_new = np.zeros((args.size_y+1, args.size_x+1))
    heat_maps = [RoomMap(heat_old=heat_new, position_state=position_state,
                         xsize=args.size_x, ysize=args.size_y,
                         node=i, decay=args.decay, mask_ratio=args.mask_ratio)
                 for i in range(1, args.rooms+1)]

    # Use Animate to show/save animations. Create Simulate function that ignores animation requirements???
    # use animate function instead of update. update is nested.
    animate(people=people,
            heat_maps=heat_maps,
            position_state=position_state,
            rooms=args.rooms, days=args.days,
            day_length=args.day_length,
            g=g,
            number_nodes=number_nodes,
            limit=args.limit,
            death_rate=args.death_rate)

    # Drawing a node graph
    draw_network(position_state, g, number_nodes)



if __name__ == "__main__":

    # Command line entry point
    import sys
    main(*sys.argv[1:])