import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

#CREATE STARTING CONDITIONS
iter=100
pop_size = 10 # total number of individuals
xsize = 50  # number of cell or pixels in the xaxis
ysize = 50  # number of cells or pixels in the yaxis
infheat=100
susheat=-100
heat = np.zeros((xsize,ysize)) # heat map array, currently all cold

xpos = np.random.randint(0,xsize-1, size=(pop_size,1))  # random x coordinates in column vector
ypos = np.random.randint(0,ysize-1, size=(pop_size,1))  # random y coordinates in column vector
map_pos=np.column_stack((xpos,ypos))
random_states = [1, 2]  # 1 means healthy, 2 means infectious
weights = [96, 4] # lists the states and weightings (has no bearing on real weights)
state = np.transpose([np.array(random.choices(random_states, weights=weights, k=pop_size))]) #randomly picks state using weighting probability, convert to column vector
if np.any(np.where(state == 2)) == False: # checks if we have 0 infected individuals
    state[np.random.randint(0,pop_size)] = 2 # adds 1 infected at random
pos_st = np.column_stack((xpos, ypos, state))

re_pos_st=np.array([],dtype=int)
for z in range(0,len(pos_st)):
    if pos_st[z,2]==2:
        re_pos_st=np.append(re_pos_st,infheat)
    if pos_st[z,2]==1:
        re_pos_st=np.append(re_pos_st,susheat)
pos_st=np.column_stack((pos_st,re_pos_st))


class COVID_MAP:
    #Creates covid map objects
    def __init__(self, pos_st,heat_old,xsize,ysize):
        self.pos_st = pos_st
        self.heat_old=heat_old
        self.xsize= xsize
        self.ysize= ysize
    def map_position_states(self):
        pos_map1 = np.zeros((self.xsize, self.ysize))

        for x in self.pos_st:
            pos_map1[x[0], x[1]] = x[2]

        return pos_map1

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
        heat_new = heat_new+self.heat_source()
        heat_new[heat_new > 100] = 100

        heat_new[:, 0] = heat_new[:, 1]  # boundary conditions
        heat_new[:, -1] = heat_new[:, -2]
        heat_new[0, :] = heat_new[1, :]
        heat_new[-1, :] = heat_new[-2, :]

        return heat_new
    
    def show_map(self):  # creates a heatmap and position map
        # create marker for healthy individuals in heatmap
        heat_map = self.calculate_heat_new()

        # create matplot figure with subplots
        fig,axes = plt.subplots(1, 2, figsize=(15, 5))

        sns.heatmap(np.transpose(heat_map), ax=axes[0], cbar=False, cmap='icefire', center=0).invert_yaxis() # heatmap
        axes[0].set_title("Heat Map")

def find_inf(pos_st):
    old_inf=np.array([],dtype=int)
    for t in range(0,pop_size-1):
        if pos_st[t,2]==2:
            new=np.array(map_pos[t])
            old_inf=np.append(old_inf,new,axis=0)
    sv= np.reshape(old_inf,(-1,2),order='C')
    return sv

def find_sus(pos_st):
    old_sus=np.array([],dtype=int)
    for r in range(0,pop_size-1):
        if pos_st[r,2]==1:
            new1=map_pos[r]
            old_sus=np.append(old_sus,new1,axis=0)
    sv1= np.reshape(old_sus,(-1,2),order='C')
    return sv1
#CREATE MAP INSTANCE
map1 = COVID_MAP(pos_st,heat,xsize, ysize)

for i in range(0,iter-1):
    heat = map1.calculate_heat_new()
    #if (i / 2).is_integer():  # only move every other iteration
        #Move(position_state)
    inf=np.count_nonzero(pos_st[:, 2] == 2)
    d=[]
    d.append(inf)

map1.show_map()
plt.show()

print("Total Infected: ", np.count_nonzero(pos_st[:, 2] == 2))
print("Total Population: ", pop_size)
print("Iterations: ", iter)

