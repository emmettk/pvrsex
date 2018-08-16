# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 13:50:56 2018

@author: LaVision

Some small PIV-related drabbles
"""
import math

def gridSize(window, overlap):
    return window*(1-overlap/100.)

def hztous(hz):
    """
    Convert frame rate in hz to microseconds between frames
    """
    return (1/hz)*10**6

def travelDistance(depth, hz):
    speed = math.sqrt(depth*9.8) #m/s
    return speed/hz



if __name__ == "__main__":
#   print(gridSize(96, 75))