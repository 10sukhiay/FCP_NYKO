#!/usr/bin/env python3
"""

Person_Class.py
Nathan Wooster
May 2021

This script contains the Person Class used in the model simulation.
It is not interacted with directly from the command line as takes
inputs from the 'people_array' that is used to interface with the
command line.

"""


import numpy as np
import pandas as pd
import random
import math

class person(object):

    """
    Creates individual people which move in specific ways.

    In the class there are numerous functions that define the movement and
    interaction of each person in a room.

    The people are x,y position dots that appear in each room.

    Each person is initialised using the data frame output from the people_array.
    A single person is created from every row when the Person class is called in
    '_simulator.py'. For example a people_array row may look like:

    Example
    =======

    x  |  y  |  node   |  status  |  two_meter  |  gravitating
    -----------------------------------------------------
    2  |  1  |    1    |    0     |      1      |       1

    Here the Person class will then create a person class instance that starts moving from
    position (2,1) in room 1. They will be non-infected. They will follow the 2meter
    social distancing rule and will move towards ('gravitate') and sit (stop) at the table.

    To implement the movement of each person, the Person Class has these key functions:

    1) make_new_step_size(): When each person is initialised it gives them a random step size
                             they take every iteration. This allows them to move. Each iteration
                             a person has 50% chance of changing step size (movement speed). Also,
                             the move() function makes sure the person does not go out of the
                             room boundaries.

    2) move():  This function contains nested functions that are called to allow it to work.
                It also contains the 'if' statements that are run each iteration and dictate
                how each person moves using the functions in the class: They key movements are:

            a)   If specified the person follows a 2meter social distancing rule. This uses functions
                 distance(), direction(), position_compared_to_object(), move_away() and
                 calc_dist_to_other_people(). If the closest person is <2m from them, they will move
                 away from that individual.

            b)   If specified the person moves towards ('gravitates to') the table and stops to 'sit' at
                 the table. The table is a user input to say where it is located and the radius size.
                 The table is designed to simulate the impact of infection if people move to congregate
                 in room. This uses the functions direction(), position_compared_to_object(),
                 move_towards(), inside() and stop(). A person moves towards the designated table area,
                 and once inside the area the person stops moving. Every iteration they then have a 50%
                 chance of leaving the table.

    The Person class outputs the updated positions to the data frame to then input to the Heat_Mapping.py.

    """

    def __init__(self, x, y, node, status, two_meter, gravitating, AREA_X, AREA_Y, AREA_R, size_x, size_y):
        # Parameters used from people_array to initialise each person instance
        self.x = x
        self.y = y
        self.node = node
        self.status = status
        self.two_meter = two_meter
        self.gravitating = gravitating

        # Calls function to create a new step size for person
        self.step_x = self.make_new_step_size()
        self.step_y = self.make_new_step_size()

        # Table area parameters
        self.AREA_X = AREA_X
        self.AREA_Y = AREA_Y
        self.AREA_R = AREA_R

        # Size of room
        self.size_x = size_x
        self.size_y = size_y

    def make_new_step_size(self, max_step=2.5):
        """Create new step size (basically movement velocity)"""

        # Creates random number for step size based off default max_step parameter
        return (np.random.random_sample() - 0.5)*max_step / 5

    def move(self, people):
        """The main move function called every iteration to move each person instance"""
        # Contains nested functions

        def distance(x1, y1, x2, y2):
            """Calculates distance between two coordinates"""

            # Uses square root squared method 2D distance
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        def inside(x1, y1, cx, cy, r):
            """Calculates distance between two coordinates"""

            #  Says if dot is inside a specific area (coord cx, cy and radius = r)
            if distance(x1, y1, cx, cy) <= r:
                return True
            else:
                return False

        def stop(self):
            """Stops person moving"""

            # Set step size to zero movement
            self.step_x = 0
            self.step_y = 0
            return

        def direction(self):
            """Outputs general movement direction of person"""

            # Output string saying what general direction the dot is moving
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
            """Outputs relative position of person compared to another person or object"""

            # Right of object
            if self.x - cx > 0:
                x_position = 1

            # Left of object
            elif self.x - cx < 0:
                x_position = -1

            # On object
            else:
                x_position = 0

            # Above object
            if self.y - cy > 0:
                y_position = 1

            # Below object
            elif self.y - cy < 0:
                y_position = -1

            # On object
            else:
                y_position = 0

            return (x_position, y_position)

        def move_towards(self, cx, cy):
            """Makes a person move towards specific coordinate"""

            # If to the right of intended location move left
            if position_compared_to_object(self, cx, cy)[0] == 1 and direction(self)[0] == 'right':
                self.step_x = -1 * self.step_x

            # If above intended location move down
            if position_compared_to_object(self, cx, cy)[1] == 1 and direction(self)[1] == 'up':
                self.step_y = -1 * self.step_y

            # If to the left of intended location move right
            if position_compared_to_object(self, cx, cy)[0] == -1 and direction(self)[0] == 'left':
                self.step_x = -1 * self.step_x

            # If below intended location move up
            if position_compared_to_object(self, cx, cy)[1] == -1 and direction(self)[1] == 'down':
                self.step_y = -1 * self.step_y
            return

        def move_away(self, cx, cy):
            """Makes a person move away from specific coordinate"""

            # If to the left of other object location move left
            if position_compared_to_object(self, cx, cy)[0] == -1 and direction(self)[0] == 'right':
                self.step_x = -1 * self.step_x

            # If below other object location move down
            if position_compared_to_object(self, cx, cy)[1] == -1 and direction(self)[1] == 'up':
                self.step_y = -1 * self.step_y

            # If to the right of other object location move right
            if position_compared_to_object(self, cx, cy)[0] == 1 and direction(self)[0] == 'left':
                self.step_x = -1 * self.step_x

            # If above other object location move up
            if position_compared_to_object(self, cx, cy)[1] == 1 and direction(self)[1] == 'down':
                self.step_y = -1 * self.step_y
            return

        def calc_dist_to_other_people(d):
            """Makes a person move away from specific coordinate"""

            # Initialise distance as large number
            dist_from_other_people = 999

            # Loop through all people
            for n in people:

                # Make sure person comparing is in the same room
                if n.node == d.node:

                    # Make sure person comparing to is not itself, d is the person, n is all the other people
                    if n != d:

                        # Calculate closest person and the distance to them
                        dist_from_person_n = distance(n.x, n.y, d.x, d.y)
                        if dist_from_person_n < dist_from_other_people:
                            dist_from_other_people = dist_from_person_n
                            closest_person = n

            return (dist_from_other_people,closest_person)

        # Actual movement now implemented each iteration using functions given above

        # %Chance the speed of person stays the same
        if np.random.random_sample() < 0.50:

            # Implement movement step
            self.x = self.x + self.step_x
            self.y = self.y + self.step_y

        else:

            # If a new step size (basically velocity) is generated
            self.velx = self.make_new_step_size()
            self.vely = self.make_new_step_size()
            self.x = self.x + self.step_x
            self.y = self.y + self.step_y

        # Make sure person cannot go outside boundary of room size grid
        if self.x >= self.size_x:
            self.x = self.size_x
            self.step_x = -1 * self.step_x
        if self.x <= 0:
            self.x = 0
            self.step_x = -1 * self.step_x
        if self.y >= self.size_y:
            self.y = self.size_y
            self.step_y = -1 * self.step_y
        if self.y <= 0:
            self.y = 0
            self.step_y = -1 * self.step_y

        # If inside table area and meant to be sat at table, stop person moving
        if inside(self.x, self.y, self.AREA_X, self.AREA_Y, self.AREA_R):
            if self.gravitating == 1:
                stop(self)

            # %Chance of leaving the table next iteration
            if np.random.random_sample() < 0.5:
                self.gravitating = 0

        # If 'gravitate' towards table specified, move towards it
        if self.gravitating == 1:
            move_towards(self, self.AREA_X, self.AREA_Y)

        # If 2meter social distancing specified implement it
        if self.two_meter == 1:
            min_dist_to_someone = calc_dist_to_other_people(self)[0]
            closest_person = calc_dist_to_other_people(self)[1]

            # If closer than 2meters to nearest person move away from them
            if min_dist_to_someone < 2:
                move_away(self, closest_person.x, closest_person.y)
