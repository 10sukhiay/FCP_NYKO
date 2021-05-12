#!/usr/bin/env python3

# Code created 10/01/21
# Kaelan Melville
# Heat Mapping

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy.random import random, randint
import pandas as pd
import random
import seaborn as sns
import matplotlib.animation as animation





# Heat Function
# inputs:

# heat_old:  heat array of size [x, y, room_number, health_state(1 ,2, 3, 4, 5]
# position_state:  [x, y, room_number, health_state]
# xsize:  [x size of room]
# ysize [y size of room]

# outputs:
# heat_new: array output of size [xsize, ysize]
# position_state:  [x, y, room_number, health_state]

class COVID_MAP:
    def __init__(self, heat_old, position_state, xsize, ysize): 
        self.heat_old = heat_old
        self.position_state = position_state
        self.xsize = xsize
        self.ysize = ysize
    
    def map_position_states(self):
        pos_map = np.zeros((self.xsize, self.ysize))
                           
        for x in self.position_state:
            pos_map[x[0],x[1]] = x[2]
            
        return pos_map
    
    def heat_source(self): # will add heat source to map based on individuals new position
        sources = np.zeros((self.xsize,self.ysize))
        sources += self.map_position_states()
        sources[sources == 2] = 100 
        sources[sources != 100] = 0
        return sources
    
    def calculate_heat_new(self): # will calculate single step of heat dispersion
        
        heat_left = np.roll(self.heat_old, 1 , axis = 1)
        heat_right = np.roll(self.heat_old, -1 , axis = 1)
        heat_up = np.roll(self.heat_old, -1 , axis = 0)
        heat_down = np.roll(self.heat_old, 1 , axis = 0)
        
        heat_new = 0.25*(heat_left + heat_right + heat_up + heat_down) # cell heat is the average of adjacent cells
        heat_new = heat_new + self.heat_source()
        heat_new[heat_new > 100] = 100
        
        heat_new[:,0] = heat_new[:,1] # boundary conditions
        heat_new[:,-1] =  heat_new[:,-2]
        heat_new[0,:] = heat_new[1,:]
        heat_new[-1,:] = heat_new[-2,:]
        
        return heat_new
    
    def show_map(self): # creates a heatmap and position map
        # create marker for healthy individuals in heatmap
        heat_map = self.calculate_heat_new()
        pos = self.map_position_states()
        heat_map[pos == 1] = -100
        # create marker for healthy individuals in pos map
        pos_map = self.map_position_states()
        pos_map[pos_map == 1] = -2 
        
        
        #create matplot figure with subplots
        fig, axes = plt.subplots(1, 2, figsize=(15, 5)) 
        
        sns.heatmap(np.transpose(heat_map), ax=axes[0], cbar=False, cmap='icefire', center =0).invert_yaxis() #heatmap
        axes[0].set_title("Heat Map")
        
        #sns.heatmap(pos_map, ax=axes[1], cbar=False, cmap='icefire', center = 0).invert_yaxis() #position heatmap
        #axes[1].set_title("Position Map")
        sns.scatterplot(x=self.position_state[:,0], y=self.position_state[:,1], data=self.position_state, ax=axes[1], hue=self.position_state[:,2], legend=False, palette='coolwarm') #position scatterplot
        axes[1].set_title("Position Map")
        axes[1].set_xlim(0,self.xsize)
        axes[1].set_ylim(0,self.ysize)