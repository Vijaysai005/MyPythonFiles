#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 00:07:30 2018
@author: Vijayasai S
"""

import sys
sys.path.append("../../")

from data.wine import train_data
from network import NeuralNetwork

NN = NeuralNetwork.NeuralNetwork(rms_threshold=0.0001, learning_rate=0.1, iterations=10)
train = train_data.Train(filename="../../data/wine/wine_data.csv")

train_x = train.getX()
train_y = train.gety()

NN.setXy(train_x, train_y)
NN.train()

print (NN.multi_weight_matrix)
print (NN.gradient_norm)
