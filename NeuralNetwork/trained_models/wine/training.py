#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 00:07:30 2018
@author: Vijayasai S
"""

import sys
import pandas as pd
import numpy as np
sys.path.append("../../")

from data.wine import train_data
from network import NeuralNetwork
from normalize import batch_normalize

try:
    df = pd.read_csv('weight/weight_hidden.csv', header=None)
    whl = np.matrix(df.as_matrix())
    df = pd.read_csv('weight/weight_output.csv', header=None)
    wol = np.matrix(df.as_matrix())
    df = pd.read_csv('bias/bias_hidden.csv', header=None)
    bhl = np.matrix(df.as_matrix())
    df = pd.read_csv('bias/bias_output.csv', header=None)
    bol = np.matrix(df.as_matrix())
except OSError:
    whl = None ; bhl = None
    wol = None ; bol = None

NN = NeuralNetwork.NeuralNetwork(iterations=100000, rms_threshold=0.01, learning_rate=1.0,
                                    weight_hidden_layer=whl, weight_output_layer=wol, 
                                    bias_hidden_layer=bhl, bias_output_layer=bol)
train = train_data.Train(filename="../../data/wine/wine_data.csv")
Normalizer = batch_normalize.BatchNormalization()

train_x = train.getX()
train_y = train.gety()

Normalizer.set_data(train_x)
normalized_train_x = Normalizer.normalize()


NN.setXy(normalized_train_x, train_y)
NN.train(print_convergence=True)

df = pd.DataFrame(NN.weight_hidden_layer)
df.to_csv('weight/weight_hidden.csv', sep=',', index=False, header=False)

df = pd.DataFrame(NN.weight_output_layer)
df.to_csv('weight/weight_output.csv', sep=',', index=False, header=False)

df = pd.DataFrame(NN.bias_hidden_layer)
df.to_csv('bias/bias_hidden.csv', sep=',', index=False, header=False)

df = pd.DataFrame(NN.bias_output_layer)
df.to_csv('bias/bias_output.csv', sep=',', index=False, header=False)

print (NN.count_percentage)