#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 00:07:30 2018
@author: Vijayasai S
"""

import pandas as pd
import numpy as np

class Train(object):

    def __init__(self, filename=None):
        self.df = pd.read_csv(filename)
        self.training_data = self.train_matrix()

    def train_matrix(self):
        return self.df.as_matrix()

    def getX(self):
        return np.matrix(self.training_data[:,0:-1])

    def gety(self):
        return np.matrix(self.training_data[:,-1]).T

    
if __name__ == "__main__":
    pass
