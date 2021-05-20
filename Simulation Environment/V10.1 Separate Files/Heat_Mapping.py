#!/usr/bin/env python3
"""

Heat_Mapping.py
Kaelan Melville
May 2021

This script contains the RoomMap class used in the model simulation.
It is not interacted with directly from the command line as takes
inputs from the 'people_array' that is used to interface with the
command line.

"""


import numpy as np
import pandas as pd
import random


class RoomMap(object):

    """
    Creates arrays with numerical temperatures for each room.

    In the class there are numerous functions for updating the room temperatures and identifying individuals
    as point sources for distributing heat.

    Each cell corresponds to a discrete x and y coordinate.

    Each room map is initialised using an array of zeros of dimensions xsize and ysize as passed by the _simulator
    script:

     0 | 0 | 0 | 0 | 0 | 0
    -----------------------
     0 | 0 | 0 | 0 | 0 | 0
    -----------------------
     0 | 0 | 0 | 0 | 0 | 0
    -----------------------
     0 | 0 | 0 | 0 | 0 | 0
    -----------------------
     0 | 0 | 0 | 0 | 0 | 0

    From here the RoomMap class will update the array based on the location of individuals passed by simulator script
    in the position_state variable.

    To implement this dynamic heat array the class has four built-in functions:

    1) update_occupants():  When each instance of RoomMap is initialised it is given a unique 'node' number. This
                            function uses a mask on the position_state dataframe where the 'node' matches, returning
                            a subsection of this dataframe called occupants.

    2) map_position_states():   This function places individuals in the occupants dataframe onto an array of zeros by
                                using the 'x' and 'y' values as an index. The value at these indices is dependent on the
                                'status' all non-zero value representing an occupied cell.

                                Example:
                                     0 | 1 | 0 | 0 | 0 | 0
                                    -----------------------
                                     0 | 0 | 0 | 1 | 0 | 0
                                    -----------------------
                                     0 | 0 | 0 | 0 | 0 | 0
                                    -----------------------
                                     0 | 3 | 0 | 0 | 2 | 0
                                    -----------------------
                                     0 | 0 | 0 | 4 | 0 | 0

    3) heat_source():   This function takes the

    4) calculate_heat_new():
    The Person class outputs the updated positions to the data frame to then input to the Heat_Mapping.py.

    """

    def __init__(self, heat_old, position_state, xsize, ysize, node, decay, mask_ratio):
        self.heat_old = heat_old
        self.node = node
        self.xsize = xsize+1
        self.ysize = ysize+1
        self.occupants = self.update_occupants(position_state)
        self.decay = decay
        self.mask_ratio = mask_ratio*100

    def update_occupants(self, position_state):
        self.occupants = position_state[position_state["node"] == self.node]
        return self.occupants

    def map_position_states(self):
        pos_map = np.zeros((self.ysize, self.xsize))
        for row in range(0, len(self.occupants)):
            if self.occupants['mask'].iloc[row] == 1:  # masked individual
                pos_map[round(self.occupants['y'].iloc[row]), round(self.occupants['x'].iloc[row])] = self.occupants['status'].iloc[row] + 0.5
            else:
                pos_map[round(self.occupants['y'].iloc[row]), round(self.occupants['x'].iloc[row])] = self.occupants['status'].iloc[row]
        return pos_map

    def heat_source(self):  # will add heat source to map based on individuals new position
        sources = np.zeros((self.ysize, self.xsize))
        boundary = np.zeros((self.ysize+2, self.xsize+2))
        sources += self.map_position_states()
        sources[sources == 3] = 100
        sources[sources == 3.5] = self.mask_ratio
        sources[sources < self.mask_ratio] = 0
        boundary[1:-1, 1:-1] = sources
        sources = boundary

        return sources

    def calculate_heat_new(self):  # will calculate single step of heat dispersion
        # add zeros all around
        boundary = np.zeros((self.ysize+2, self.xsize+2))
        boundary[1:-1, 1:-1] = self.heat_old - self.decay  # minus 1 is the decay
        boundary[boundary < 0] = 0

        # boundary conditions no windows
        boundary[:, 0] = boundary[:, 1]
        boundary[:, -1] = boundary[:, -2]
        boundary[0, :] = boundary[1, :]
        boundary[-1, :] = boundary[-2, :]
        # add windows
        # boundary[5:-5, 0] = 0
        # boundary[5:-5, -1] = 0

        heat = boundary
        heat_left = np.roll(heat, 1, axis=1)
        heat_right = np.roll(heat, -1, axis=1)
        heat_up = np.roll(heat, -1, axis=0)
        heat_down = np.roll(heat, 1, axis=0)

        heat_new = 0.25 * (heat_left + heat_right + heat_up + heat_down)  # cell heat is the average of adjacent cells
        heat_new[self.heat_source() == 100] = 100
        mask_1 = self.heat_source() == self.mask_ratio
        mask_2 = heat_new < self.mask_ratio
        mask_3 = np.logical_and(mask_1, mask_2)
        heat_new[mask_3] = self.mask_ratio
        heat_new = heat_new[1:-1, 1:-1]

        self.heat_old = heat_new