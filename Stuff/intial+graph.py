import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation
import math

#CREATE STARTING CONDITIONS
iter=100
pop_size = 10 # total number of individuals
xsize = 50  # number of cell or pixels in the xaxis
ysize = 50  # number of cells or pixels in the yaxis
heat = np.zeros((xsize,ysize)) # heat map array, currently all cold
infheat=100
susheat=-100
boundary = np.zeros((xsize,ysize)) # boundary array, will have values where there are boundaries, values can dictate behaviour

#CREATE INITIAL SET OF VALUES
x_pos = np.random.randint(1,xsize-2, size=(pop_size,1))  # random x coordinates in column vector
y_pos = np.random.randint(1,ysize-2, size=(pop_size,1))  # random y coordinates in column vector
state = np.zeros((pop_size,1))
map_pos=np.column_stack((x_pos,y_pos))
random_states = [1, 2]  # 1 means healthy, 2 means infectious
weights = [96, 4] # lists the states and weightings (has no bearing on real weights)
state = np.transpose([np.array(random.choices(random_states, weights=weights, k=pop_size))]) #randomly picks state using weighting probability, convert to column vector
if np.any(np.where(state == 2)) == False: # checks if we have 0 infected individuals
    state[np.random.randint(0,pop_size)] = 2 # adds 1 infected at random
position_state = np.column_stack((x_pos, y_pos, state)) # horizontal stack into 1 array

#######
#re_position_state=np.array([],dtype=int)
#for z in range(0,len(position_state)-1):
    #if position_state[z,2]==2:
       #re_position_state=np.append(re_position_state,infheat)
    #if position_state[z,2]==1:
        #re_position_state=np.append(re_position_state,susheat)
    #position_state=np.column_stack((position_state,re_position_state))

#HEAT MAPPING CLASS AND FUNCTIONS
# create covid map object
class COVID_MAP:
    def __init__(self, heat_old, position_state, boundaries, xsize, ysize):
        self.heat_old = heat_old
        self.position_state = position_state
        self.boundaries = boundaries
        self.xsize = xsize
        self.ysize = ysize

    def map_position_states(self):
        pos_map1 = np.zeros((self.xsize, self.ysize))

        for x in self.position_state:
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
        fig, axs = plt.subplots(2, 2,figsize=(15,8))



        sns.heatmap(np.transpose(heat_map), ax=axs[0,0], cbar=False, cmap='icefire', center=0).invert_yaxis()  # heatmap
        axs[0,0].set_title("Heat Map")
        axs[0,0].set_xlim(0, self.xsize)
        axs[0,0].set_ylim(0, self.ysize)
        axs[0,1].set_title("Position Map")
        axs[0,1].set_xlim(0, self.xsize)
        axs[0,1].set_ylim(0, self.ysize)
        sns.scatterplot(x=self.position_state[:, 0], y=self.position_state[:, 1], data=self.position_state, ax=axs[0,1],
                        hue=self.position_state[:, 2], legend=False, palette='coolwarm')  # position scatterplot
        axs[1,0].plot(iter_array,inf_count)
        axs[1,0].set_title('Infected per iteration')
        axs[1,0].set(xlabel='number of iterations', ylabel='population')
        axs[1,0].set_xlim(0,iter)
        axs[1,0].set_ylim(0,pop_size)

#POSITION AND MOVEMENT
def Move(position_state):
    movement = np.random.randint(-1, 2, size=(
    pop_size, 2))  # creates a random array of -1 to 1 to add to the current positions
    coords = position_state[:, 0:2] + movement
    coords[coords < 1] = 1  # prevent movement below x and y axis
    coords[coords[:, 0] > (xsize - 2)] = (xsize - 2)  # prevent movement beyond x axis
    coords[coords[:, 1] > (ysize - 2)] = (ysize - 2)  # prevent movement beyond y axis
    position_state[:, 0:2] = coords
    return position_state

def Move2(position_state):
    movement = np.random.randint(-3, 3, size=(
    pop_size, 2))  # creates a random array of -1 to 1 to add to the current positions
    coords = position_state[:, 0:2] + movement
    coords[coords < 1] = 1  # prevent movement below x and y axis
    coords[coords[:, 0] > (xsize - 2)] = (xsize - 2)  # prevent movement beyond x axis
    coords[coords[:, 1] > (ysize - 2)] = (ysize - 2)  # prevent movement beyond y axis
    position_state[:, 0:2] = coords
    return position_state

def Move3(position_state):
    movement = np.random.randint(-2, 1, size=(
    pop_size, 2))  # creates a random array of -1 to 1 to add to the current positions
    coords = position_state[:, 0:2] + movement
    coords[coords < 1] = 1  # prevent movement below x and y axis
    coords[coords[:, 0] > (xsize - 2)] = (xsize - 2)  # prevent movement beyond x axis
    coords[coords[:, 1] > (ysize - 2)] = (ysize - 2)  # prevent movement beyond y axis
    position_state[:, 0:2] = coords
    return position_state

#TRANSMITION FUNCTION
def Transmission(position_state, heat):
    for x in range(len(position_state)):
            if heat[position_state[x,0],position_state[x,1]] > 20 and heat[position_state[x,0],position_state[x,1]] > np.random.randint(0,101):
                position_state[x,2] = 2 # stands for infected
    return position_state

########
def find_inf(position_state):
    old_inf=np.array([],dtype=int)
    for t in range(0,pop_size-1):
        if position_state[t,2]==2:
            new=np.array(map_pos[t])
            old_inf=np.append(old_inf,new,axis=0)
    sv= np.reshape(old_inf,(-1,2),order='C')
    return sv

##########
def find_sus(position_state):
    old_sus=np.array([],dtype=int)
    for r in range(0,pop_size-1):
        if position_state[r,2]==1:
            new1=map_pos[r]
            old_sus=np.append(old_sus,new1,axis=0)
    sv1= np.reshape(old_sus,(-1,2),order='C')
    return sv1


#CREATE MAP INSTANCE
#CREATE MAP INSTANCE
map1 = COVID_MAP(heat, position_state, boundary, xsize, ysize)

#ITERATE MAP 1 INSTANCE
i = 0   # total iteration counter
n = 0  # throwaway iterator
inf_count=np.array([],dtype=int)
iter_array=np.array([],dtype=int)
while n < 100:

    Transmission(position_state, heat)
    heat = map1.calculate_heat_new()

    if (n / 2).is_integer():  # only move every other iteration
        Move(position_state)
    
    new2=np.array([np.count_nonzero(position_state[:, 2] == 2)])
    inf_count=np.append(inf_count,new2,axis=0)
    new3=np.array([i])
    iter_array=np.append(iter_array,new3,axis=0)

    map1 = COVID_MAP(heat, position_state, boundary, xsize, ysize)

    i += 1
    n += 1

map1.show_map()


#plt.plot(i,np.count_nonzero(position_state[:, 2] == 2))
#plt.title('position map')
plt.show()


print("Total Infected: ", np.count_nonzero(position_state[:, 2] == 2))
print("Total Population: ", pop_size)
print("Iterations: ", i)