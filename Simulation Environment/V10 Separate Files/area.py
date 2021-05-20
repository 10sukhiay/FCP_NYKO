#!/usr/bin/env python3
"""

area.py
Nathan Wooster
May 2021

This script contains the Area Class used in the model simulation.
It is used to represent a table area that people can congregate
towards and sit at.

"""


from matplotlib import pyplot as plt


class area(object):
    """ Creates an area representing a table for people to move towards if specified by a user input.
        The person moves towards the specified area if and only if 'gravitate' is 1 (ON) in their
        description.

        The class takes user inputs from the main _simulator.py, to create a circle at specific
        coordinates and a specific radius.
    """

    def __init__(self, cx, cy, r):

        # Parameters used from user input in main _simulator.py
        self.cx = cx
        self.cy = cy
        self.r = r

    def draw(self):
        """Function to be called from animator if wanting to draw the table on the axis"""

        # Draw the circle in blue
        return plt.Circle((self.cx, self.cy), self.r, color='b', fill=False) #creates circle coords cx cy and radius r (built in function)