# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:06:23 2018

@author: vijayasai
"""

import os

source = "perambur"
destination = "avadi"
mode = "driving"

command = "python vplot/test.py {} {} {}".format(source, destination, mode)
os.system(command)

