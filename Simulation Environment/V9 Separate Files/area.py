#!/usr/bin/env python3
"""

area.py
Kaelan Melville
May 2021


"""

#standard imports
from matplotlib import pyplot as plt

# custom imports


class area(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r

    def draw(self):
        return plt.Circle((self.cx, self.cy), self.r, color='b', fill=False) #creates circle coords cx cy and radius r (built in function)