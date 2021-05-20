#!/usr/bin/env python3
"""

Heat_Mapping.py
Kaelan Melville
May 2021


"""


import numpy as np
import pandas as pd
import random

class Room_map(object):
    def __init__(self, heat_old, position_state, xsize, ysize, node, decay):
        self.heat_old = heat_old
        self.node = node
        self.xsize = xsize+1
        self.ysize = ysize+1
        self.update_occupants(position_state)
        self.decay = decay

    def update_occupants(self, position_state):
        self.occupants = position_state[position_state["node"] == self.node]

    def map_position_states(self):
        pos_map = np.zeros((self.ysize, self.xsize))
        for row in range(0, len(self.occupants)):
            if self.occupants['mask'].iloc[row] == 1: # masked individual
                pos_map[round(self.occupants['y'].iloc[row]), round(self.occupants['x'].iloc[row])] = self.occupants['status'].iloc[row] + 0.5
            else:
                pos_map[round(self.occupants['y'].iloc[row]), round(self.occupants['x'].iloc[row])] = self.occupants['status'].iloc[row]
        return pos_map

    def heat_source(self):  # will add heat source to map based on individuals new position
        sources = np.zeros((self.ysize, self.xsize))
        boundary = np.zeros((self.ysize+2, self.xsize+2))
        sources += self.map_position_states()
        sources[sources == 3] = 100
        sources[sources == 3.5] = 50
        sources[sources < 50] = 0
        boundary[1:-1,1:-1] = sources
        sources = boundary

        return sources

    def calculate_heat_new(self):  # will calculate single step of heat dispersion
        #add zeros all around
        boundary = np.zeros((self.ysize+2, self.xsize+2))
        boundary[1:-1, 1:-1] = self.heat_old - self.decay # minus 1 is the decay
        boundary[boundary < 0] = 0

        # boundary conditions no windows
        boundary[:, 0] = boundary[:, 1]
        boundary[:, -1] = boundary[:, -2]
        boundary[0, :] = boundary[1, :]
        boundary[-1, :] = boundary[-2, :]
        #add windows
        #boundary[5:-5, 0] = 0
        #boundary[5:-5, -1] = 0

        heat = boundary
        heat_left = np.roll(heat, 1, axis=1)
        heat_right = np.roll(heat, -1, axis=1)
        heat_up = np.roll(heat, -1, axis=0)
        heat_down = np.roll(heat, 1, axis=0)

        heat_new = 0.25 * (heat_left + heat_right + heat_up + heat_down)  # cell heat is the average of adjacent cells
        heat_new[self.heat_source() == 100] = 100
        mask_1 = self.heat_source() == 50
        mask_2 = heat_new < 50
        mask_3 = np.logical_and(mask_1, mask_2)
        heat_new[mask_3] = 50
        heat_new = heat_new[1:-1, 1:-1]

        self.heat_old = heat_new

    def show_map(self):  # creates a heatmap and position map
        # create marker for healthy individuals in heatmap
        heat_map = self.heat_old
        #pos = self.map_position_states()
        #heat_map[pos == 1] = -100

        # create matplot figure with subplots

        return heat_map # heatmap