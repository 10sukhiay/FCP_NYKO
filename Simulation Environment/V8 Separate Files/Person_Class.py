#!/usr/bin/env python3
"""

Person_Class.py
Nathan Wooster
May 2021


"""


import numpy as np
import pandas as pd
import random
import math

class person(object):
    def __init__(self, x, y, node, status, two_meter, gravitating, AREA_X, AREA_Y, AREA_R, size_x, size_y):
        self.x = x
        self.y = y
        self.node = node
        self.status = status
        self.two_meter = two_meter
        self.gravitating = gravitating
        self.step_x = self.make_new_step_size() #calls function to create a new step size for person
        self.step_y = self.make_new_step_size()
        self.AREA_X = AREA_X
        self.AREA_Y = AREA_Y
        self.AREA_R = AREA_R
        self.size_x = size_x
        self.size_y = size_y

    def make_new_step_size(self, max_step=10):
        return (np.random.random_sample() - 0.5)*max_step / 5 #creates random number for step size 0 to 0.1

    def move(self, people):

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
                if n.node == d.node:
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
        if self.x >= self.size_x:  # so cannot go outside boundary of 10x10 grid
            self.x = self.size_x
            self.step_x = -1 * self.step_x
        if self.x <= 0:  # so cannot go outside boundary of 10x10 grid
            self.x = 0
            self.step_x = -1 * self.step_x
        if self.y >= self.size_y:  # so cannot go outside boundary of 10x10 grid
            self.y = self.size_y
            self.step_y = -1 * self.step_y
        if self.y <= 0:  # so cannot go outside boundary of 10x10 grid
            self.y = 0
            self.step_y = -1 * self.step_y

        if inside(self.x, self.y, self.AREA_X, self.AREA_Y, self.AREA_R): #if at table area
            if self.gravitating == 1: #if meant to be at table stay there
                stop(self)
            if np.random.random_sample() < 0.5: #have a %chance of leaving the table
                self.gravitating = 0

        if self.gravitating == 1:   # if gravitate on
            move_towards(self, self.AREA_X, self.AREA_Y)

        if self.two_meter == 1: #follow 2 meter rule
            min_dist_to_someone = calc_dist_to_other_people(self)[0]
            closest_person = calc_dist_to_other_people(self)[1]
            if min_dist_to_someone < 2: #if closer than 2meters to someone
                move_away(self, closest_person.x, closest_person.y)
