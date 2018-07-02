# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 16:29:47 2018

@author: LaVision

hz to microseconds

"""

def hztous(hz):
    return (1/hz)*10**6


if __name__ == "__main__":
    print(hztous(0.3333333333333))
