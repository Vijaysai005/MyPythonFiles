#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 00:07:30 2018
@author: Vijayasai S
"""

import numpy as np
class BatchNormalization(object):

    def __init__(self, epsilon=0.01):
        self.X = None
        self.epsilon = epsilon

    def set_data(self, X):
        self.X = X

    def normalize(self):
        mean = self.X.mean(0)
        variance = self.X.var(0)
        
        normalized_matrix = (self.X - mean) / np.sqrt(variance + self.epsilon)
        return normalized_matrix

        


