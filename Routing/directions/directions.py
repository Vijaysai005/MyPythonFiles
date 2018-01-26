# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:16:23 2018

@author: vijayasai
"""
from compass import Compass

class Directions(object):

    def __init__(self):
        pass

    def 

if __name__ == "__main__":
    comp = Compass()
    data = [
            (13.086878, 80.108567), 
            (13.086704, 80.108540), 
            (13.086552, 80.108583), 
            (13.086477, 80.108546), 
            (13.086412, 80.108807)
            ]
    for i in range(len(data)-1):
        comp.GeoData(data[i], data[i+1])
        comp.solve()
        print comp.output
