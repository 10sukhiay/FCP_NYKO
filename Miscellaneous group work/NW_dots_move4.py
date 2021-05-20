import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import weakref

#global variable
room_size = 10
N = 10 #number of people

class IterArea(type): #using metaclasses?

    _areas = weakref.WeakSet()

    def __iter__(cls):
        return iter(cls._areas)

#define place people gravitate towards (circle)
class area(metaclass=IterArea):
    __metaclass__ = IterArea

    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r


    def draw(self):
        return plt.Circle((self.cx, self.cy), self.r, color='b', fill=False) #creates circle coords cx cy and radius r (built in function)

    def inside(x1, y1, cx, cy, r):
        if distance(x1, y1, cx, cy) <= r:  # defines if point is inside a specific area (coord cx, cy and radius = r)
            return True
        else:
            return False



#create moving person class
class person(object):
    def __init__(self):
        self.x = room_size * np.random.random_sample() #creates random number x coord 1 to room_size
        self.y = room_size * np.random.random_sample() #creates random number y coord 1 to room_size
        self.step_x = self.make_new_step_size() #calls function to create a new step size for person
        self.step_y = self.make_new_step_size()

    def make_new_step_size(self, max_step=1):
        return (np.random.random_sample() - 0.5)*max_step / 5 #creates random number for step size 0 to 0.1

    def move(self):

        def distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) #uses coords and calulates distance between two points

        #def inside(x1, y1, cx, cy, r):
         #   if distance(x1, y1, cx, cy) <= r:  # defines if dot is inside a specific area (coord cx, cy and radius = r)
         #       return True
         #   else:
          #      return False

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

        #for area_inst in area: #iterates through all area instances
            #if area_inst.inside(self.x, self.y, area_inst.cx, area_inst.cy, area_inst.r) == True: #stop if reach area (access area class coords and function)
                #stop(self)

        if np.random.random_sample() < 1:  # % chance to gravitate towards point 1,1
            move_towards(self, 1, 1) #NEED A WAY OF ACCESSING AREA CLASS????

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



# animation function.  This is called sequentially
def animate(i):
    for person in people: #goes through all people
        person.move() #does all the move function (multiple functions inside) for person
    d.set_data([person.x for person in people], #d is taken from the dots coords to plot
               [person.y for person in people])
    return d,


if __name__ == "__main__":

# Initialise people
    people = [person() for i in range(N)] #creates N amount of people from the object person eg person(1), person(2) ect

# Initialise areas
    area1 = area(1, 1, 0.2)
    area2 = area(5, 5, 0.2)


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure() #empty figure
ax = plt.axes(xlim=(0, room_size), ylim=(0, room_size)) #axes limit room_size
d, = ax.plot([person.x for person in people], #plot person coords x
             [person.y for person in people], 'ro') #plot person coords y

for areas in area:
    #print(areas.r)
    circle = areas.draw()
    ax.add_artist(circle) #add circle to axes plot



# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=200, interval=20) #in built function to keep updating plot to creates animation

plt.show() #shows plot