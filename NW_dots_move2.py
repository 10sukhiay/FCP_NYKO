import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math

# Initializing number of dots
N = 10

# Creating dot class
class dot(object): #creates a dot object with the following functions applied to it
    def __init__(self):
        self.x = 10 * np.random.random_sample() #creates random number x coord 1to10
        self.y = 10 * np.random.random_sample() #creates random number y coord 1to10
        self.velx = self.generate_new_vel() #defines x velocity by calling fcuntion
        self.vely = self.generate_new_vel() # (not actually a velocity, is just a number to take away from the coord so moves the dot)

    def generate_new_vel(self):
        return (np.random.random_sample() - 0.5) / 5 #creates random number for velocity 0 to 0.1

    def move(self):
        def distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) #uses coords and calulates distance between two points

        def inside(x1, y1):
            if distance(x1, y1, 5, 5) <= 1: #defines if dot is inside a specific centre circle (coord 5,5 and r = 1)
                return True
            else:
                return False

        def calc_dist(d): #if dot n is inside the circle and is not the same as the dot d (dot focusing on), then
                            #return the distance between these two dots, otherwise return 0 (only called if dot d is inside circle)
            ret = 0
            for n in dots:
                if inside(n.x, n.y) and n != d:
                    ret = ret + distance(n.x, n.y, d.x, d.y)
            return ret

        # if dot is inside the circle it tries to maximize the distances to
        # other dots inside circle
        if inside(self.x, self.y): #if dot d inside circle is true
            dist = calc_dist(self) #dist is distance dot d is from dot n (both inside circle)
            for i in range(1, 10): #creates 10 random velocities for the dot d and checks if they comply
                self.velx = self.generate_new_vel()
                self.vely = self.generate_new_vel()
                self.x = self.x + self.velx #adds these velocities to the current coords (how the velocities work in this script)
                self.y = self.y + self.vely #(SO NOT ACTUAL VELOCITIES)
                if calc_dist(self) <= dist or not inside(self.x, self.y): #takes away the velocities from the coords if it went outside the circle or closer to the dot n
                    self.x = self.x - self.velx
                    self.y = self.y - self.vely
        else: #if dot d not inside circle
            if np.random.random_sample() < 0.95: #95% chance the speed of dot stays the same (constant vel added to coord)
                self.x = self.x + self.velx   #this is how velocity works on this script (is actaully a constant added to the coord)
                self.y = self.y + self.vely
            else:
                self.velx = self.generate_new_vel() #5% chance a new velocity is generated
                self.vely = self.generate_new_vel()
                self.x = self.x + self.velx #the coord is updated with that new constant (different amount than before so dot looks like it sped up/slowed down)
                self.y = self.y + self.vely
            if self.x >= 10: #so cannot go outside boundary of 10x10 grid
                self.x = 10
                self.velx = -1 * self.velx
            if self.x <= 0: #so cannot go outside boundary of 10x10 grid
                self.x = 0
                self.velx = -1 * self.velx
            if self.y >= 10: #so cannot go outside boundary of 10x10 grid
                self.y = 10
                self.vely = -1 * self.vely
            if self.y <= 0: #so cannot go outside boundary of 10x10 grid
                self.y = 0
                self.vely = -1 * self.vely



# Initializing dots
dots = [dot() for i in range(N)] #creates N amount of dots from the object dot

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure() #empty figure
ax = plt.axes(xlim=(0, 10), ylim=(0, 10)) #axes limit 10x10
d, = ax.plot([dot.x for dot in dots], #plot dot coords x
             [dot.y for dot in dots], 'ro') #plot dot coords y
circle = plt.Circle((5, 5), 1, color='b', fill=False) #creates circle coords 5,5 and radius 10 (in built function)
ax.add_artist(circle) #add circle to axes plot


# animation function.  This is called sequentially
def animate(i):
    for dot in dots: #goes through all dots
        dot.move() #does all the move function (multiple functions inside) for dot
    d.set_data([dot.x for dot in dots], #d is taken from the dots coords to plot
               [dot.y for dot in dots])
    return d,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=200, interval=20) #in built function to keep updating plot to creates animation

plt.show() #shows plot