#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 00:07:30 2018
@author: Vijayasai S
"""

import numpy as np

class Error(object):

    def __init__(self):
        pass

    def relative_error(self, actual_value, output_value):
        return actual_value - output_value

    def absolute_error(self, actual_value, output_value):
        return abs(actual_value - output_value)

    def root_mean_square_error(self, actual_value, output_value):
        return np.sqrt(np.sum((np.array(actual_value - output_value))**2))

    def count_error(self, actual_value, output_value):
        """
        for binary class
        """
        
        binary_class = set(np.array(actual_value).ravel())
        max_value = max(binary_class) ; min_value = min(binary_class)
        count = 0
        
        for i, out in enumerate(output_value):
            if out >= 0.5:
                if actual_value[i] == max_value:
                    count +=1 
            else:
                if actual_value[i] == min_value:
                    count += 1
        return count / len(actual_value)

    def percentage_error(self, error):
        return error * 100
                
        
