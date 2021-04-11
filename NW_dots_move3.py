import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math

#global variable
room_size = 10
N = 10 #number of people

#define place people gravitate towards
class area(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r

    def draw(self):
        return plt.Circle((self.cx, self.cy), self.r, color='b', fill=False) #creates circle coords cx cy and radius r (built in function)

#create moving person class
class person(object):
    def __init__(self):
        self.x = room_size * np.random.random_sample() #creates random number x coord 1 to room_size
        self.y = room_size * np.random.random_sample() #creates random number y coord 1 to room_size
        self.step_x = self.make_new_step_size() #calls function to create a new step size for person
        self.step_y = self.make_new_step_size()

    def make_new_step_size(self):
        return (np.random.random_sample() - 0.5) / 5 #creates random number for step size 0 to 0.1

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
            if self.step_x == 0 and self.step_y == 0:
                x_direction = 'stationary'
                y_direction = 'stationary'

            return (x_direction, y_direction)


        def move_towards(self, cx, cy,):
            if self.x - cx > 0 and direction(self)[0] == 'right':
                self.step_x = -1 * self.step_x
            if self.y - cy > 0 and direction(self)[0] == 'up':
                self.step_y = -1 * self.step_y
            if self.x - cx < 0 and direction(self)[1] == 'left':
                self.step_x = -1 * self.step_x
            if self.y - cy < 0 and direction(self)[1] == 'down':
                self.step_y = -1 * self.step_y


        if np.random.random_sample() < 0.50:  # % chance the speed of person stays the same (constant step added to coord)
            self.x = self.x + self.step_x  # this is how the dot moves at constant rate (constant added to dot position)
            self.y = self.y + self.step_y
            # certain % chance person changes step size
        else:
            self.velx = self.make_new_step_size() # % chance a new velocity is generated
            self.vely = self.make_new_step_size()
            self.x = self.x + self.step_x   # the coord is updated with that new constant (different amount than before so dot looks like it sped up/slowed down)
            self.y = self.y + self.step_y
        if self.x >= room_size:  # so cannot go outside boundary of 10x10 grid
            self.x = room_size
            self.step_x = -1 * self.step_x
        if self.x <= 0:  # so cannot go outside boundary of 10x10 grid
            self.x = 0
            self.step_x = -1 * self.step_x
        if self.y >= room_size:  # so cannot go outside boundary of 10x10 grid
            self.y = room_size
            self.step_y = -1 * self.step_y
        if self.y <= 0:  # so cannot go outside boundary of 10x10 grid
            self.y = 0
            self.step_y = -1 * self.step_y

        if inside(self.x, self.y, 1, 1, 0.2): #NEED A WAY OF ACCESSING AREA CLASS????
            stop(self)

        if np.random.random_sample() < 1:  # % chance
            move_towards(self, 1, 1,) #NEED A WAY OF ACCESSING AREA CLASS????



# Initialise people
people = [person() for i in range(N)] #creates N amount of people from the object person eg person(1), person(2) ect

# Initialise areas
area1 = area(1, 1, 0.2)


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure() #empty figure
ax = plt.axes(xlim=(0, room_size), ylim=(0, room_size)) #axes limit room_size
d, = ax.plot([person.x for person in people], #plot person coords x
             [person.y for person in people], 'ro') #plot person coords y

circle = area1.draw()
ax.add_artist(circle) #add circle to axes plot


# animation function.  This is called sequentially
def animate(i):
    for person in people: #goes through all people
        person.move() #does all the move function (multiple functions inside) for person
    d.set_data([person.x for person in people], #d is taken from the dots coords to plot
               [person.y for person in people])
    return d,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=200, interval=20) #in built function to keep updating plot to creates animation

plt.show() #shows plot