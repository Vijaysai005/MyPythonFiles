#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 17:52:04 2017
@author: Vijayasai S
"""

import sys
sys.path.append("../")

from error.error import Error

import numpy as np
import bigfloat as bf

class NeuralNetwork(Error):
    """
    Master class for neural network
    """
    def __init__(self, learning_rate=0.1, iterations=1000,
                 hidden_layer_neurons=100, output_layer_neurons=1, weight_hidden_layer=None,
                 weight_output_layer=None, bias_hidden_layer=None, bias_output_layer=None, 
                 gradient_threshold=5, rms_threshold=0.01):
        Error.__init__(self)
        self.X = None
        self.y = None

        self.learning_rate = learning_rate
        self.iterations = iterations
        self.hidden_layer_neurons = hidden_layer_neurons
        self.output_layer_neurons = output_layer_neurons
        self.input_layer_neurons = None

        if weight_hidden_layer is None and self.input_layer_neurons is not None:
            self.weight_hidden_layer = np.random.uniform(size=(self.input_layer_neurons, self.hidden_layer_neurons))
        else:
            self.weight_hidden_layer = weight_hidden_layer

        if bias_hidden_layer is None:
            self.bias_hidden_layer = np.random.uniform(size=(1,self.hidden_layer_neurons))
        else:
            self.bias_hidden_layer = bias_hidden_layer

        if weight_output_layer is None:
            self.weight_output_layer = np.random.uniform(size=(self.hidden_layer_neurons, self.output_layer_neurons))
        else:
            self.weight_output_layer = weight_output_layer

        if bias_output_layer is None:
            self.bias_output_layer = np.random.uniform(size=(1, self.output_layer_neurons))
        else:
            self.bias_output_layer = bias_output_layer

        self.output = None
        self.hidden_layer_activations = None
        self.gradient_threshold = gradient_threshold
        self.Error = None
        self.rms_threshold = rms_threshold
        self.rms_error = None
        self.gradient_norm = []
        self.multi_weight_matrix = None
        self.weight_multiclass = []
        self.min_gradient_norm = None
        self.min_weight_matrix = None


    def sigmoid(self, x):
        """
        Sigmoid function : Returns value between 0 to 1 
        for given value of x
        """
        return 1. / (1. + np.exp(-x))


    def derivative_sigmoid(self, x):
        """
        Returns derivative value of the 
        sigmoid funcion
        Note : x is a sigmoid function
        """
        return np.multiply(x, (1-x))


    def setXy(self, X, y):
        """
        Set the X and y value to the class variable.
        Return None
        Note: X (input features) should be a vector or matrix (numpy)
        y (output) should be a vector (numpy)
        """
        self.X = X
        self.y = y
        self.input_layer_neurons = self.X.shape[1]

        if self.weight_hidden_layer is None and self.input_layer_neurons is not None:
            self.weight_hidden_layer = np.random.uniform(size=(self.input_layer_neurons, self.hidden_layer_neurons))
        

    def forward_propagation(self):
        """
        Forward propagation for NN (NeuralNetwork). It is used in binary classification problem.
        Returns None. It works based on class variable.
        """
        hidden_layer_input = np.dot(self.X, self.weight_hidden_layer) + self.bias_hidden_layer
        self.hidden_layer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(self.hidden_layer_activations, self.weight_output_layer) + self.bias_output_layer
        self.output = self.sigmoid(output_layer_input)
        

    def backward_propagation(self):
        """
        Backward propagation for NN (NeuralNetwork). It is used in binary classification problem.
        Returns None. It works based on class variable.
        """
        self.error = self.relative_error(self.y, self.output)
        self.rms_error = self.root_mean_square_error(self.y, self.output)
        self.count_matched = self.count_error(self.y, self.output)
        self.count_percentage = self.percentage_error(self.count_matched)
        
        slope_output_layer = self.derivative_sigmoid(self.output)
        slope_hidden_layer = self.derivative_sigmoid(self.hidden_layer_activations)
        
        d_output = np.multiply(self.error, slope_output_layer)

        Error_at_hidden_layer = np.dot(d_output, self.weight_output_layer.T)
        d_hidden_layer = np.multiply(Error_at_hidden_layer, slope_hidden_layer)

        self.weight_output_layer = self.weight_output_layer + np.dot(self.hidden_layer_activations.T,d_output) * self.learning_rate
        self.weight_hidden_layer = self.weight_hidden_layer + np.dot(self.X.T, d_hidden_layer) * self.learning_rate

        self.bias_hidden_layer = self.bias_hidden_layer + np.sum(d_hidden_layer, axis=0) * self.learning_rate
        self.bias_output_layer = self.bias_output_layer + np.sum(d_output, axis=0) * self.learning_rate
        

    def train(self, w_matrix=None, print_convergence=False):
        """
        NN Training method for given input features and output vector.
        """
        classes = len(set(np.array(self.y).ravel()))
        if classes <= 2:
            for n in range(self.iterations):
                self.forward_propagation()
                self.backward_propagation()
                if print_convergence:
                    print (self.rms_error, n)
                    
                if self.rms_error is not None:
                    if self.rms_error <= self.rms_threshold:
                        print ("Converged in {} steps".format(n+1))
                        break
                    if n == self.iterations - 1:
                        print ("Warning, did not converge")
        else:
            self.multiclass(w_matrix)
        

    @classmethod
    def _predict(self, X, w_matrix=None, model="lgd", batch=100):
        """
        predict class method to determine the output for the given
        test data based on the class variables
        """
        if len(set(np.array(self.y).ravel())) <= 2:
            hidden_layer_input = np.dot(X, self.weight_hidden_layer) + self.bias_hidden_layer
            hidden_layer_activations = self.sigmoid(hidden_layer_input)
            output_layer_input = np.dot(hidden_layer_activations, self.weight_output_layer) + self.bias_output_layer
            output = self.sigmoid(output_layer_input)
            
            res = np.empty_like(output)
            for i,out in enumerate(output):
                if out >= 0.5:
                    res[i] = 1
                else:
                    res[i] = 0
            return res
        else:
            weight_matrix = self.multiclass(w_matrix=w_matrix, optimizer=model, batch=batch)
            output = np.zeros((X.shape[0], 1))
            for i in range(X.shape[0]):
                output[i] = np.argmax(weight_matrix.dot(X[i,:].T))
            return output


    @staticmethod
    def predict(X, whl=None, bhl=None, wol=None, bol=None, mwm=None, multiclass=False):
        """
        predict static method to determine the output for the given
        test data based on the method variables
        """
        if not multiclass:
            hidden_layer_input = np.dot(X, whl) + bhl
            hidden_layer_activations = self.sigmoid(hidden_layer_input)
            output_layer_input = np.dot(hidden_layer_activations, wol) + bol
            output = self.sigmoid(output_layer_input)

            res = np.empty_like(output)
            for i, out in enumerate(output):
                if out >= 0.5:
                    res[i] = 1
                else:
                    res[i] = 0
            return res
        else:
            output = np.zeros((X.shape[0], 1))
            for i in range(X.shape[0]):
                output[i] = np.argmax(mwm.dot(X[i, :].T))
            return output


    def bigfloat_exp(self, values):
        """
        Returns list of bigfloat exponential value
        for given list of values
        """
        return [bf.exp(value) for value in values]


    def multiclass(self, w_matrix=None, optimizer="lgd", batch=100):
        """
        Trainer method for multiclassification problem.
        args:
        1. w_matrix: weight matrix for the classification if there is 
        2. optimizer: as for now there are two optimizer model
            a. lgd : linear gradient descent
            b. sgd : stochastic gradient descent
                 b.1. batch : No. of data should be taken randomly for 
                                training.
        """
        classes = len(set(np.array(self.y).ravel()))
        if w_matrix is None:
            weight_multiclass = np.zeros((classes, self.X.shape[1]))
        else:
            weight_multiclass = np.array(w_matrix)

        for n in range(self.iterations):
            gradient_matrix = np.zeros((classes,self.X.shape[1]))

            # for stochastic gradient descent
            if optimizer is "sgd":
                random = np.random.permutation(len(self.X))
                self.X = self.X[random[0:batch],:]

            for index in range(self.X.shape[0]):
                x = np.array(self.X[index,:]).ravel()
                y = np.array(self.y[index]).ravel()
                hypo = weight_multiclass.dot(x)

                if max(hypo) <= 10000:
                    exponential_value = np.exp(np.float128(hypo))
                else:
                    exponential_value = self.bias_output_layer(hypo)

                prob = exponential_value[int(y)] / np.sum(exponential_value)
                gradient_matrix[int(y),:] += x * (1-prob)

            weight_multiclass += (1.0/self.X.shape[0]) * gradient_matrix
            self.weight_multiclass.append(weight_multiclass)
            gradient_norm = np.linalg.norm(gradient_matrix)
            self.gradient_norm.append(gradient_norm)
            print (gradient_norm, n)

            if gradient_norm < self.gradient_threshold:
                print ("Converged in {} steps".format(n+1))
                self.min_gradient_norm = min(self.gradient_norm)
                self.min_weight_matrix = self.weight_multiclass[np.argmin(self.gradient_norm)]
                self.multi_weight_matrix = weight_multiclass
                return self.min_weight_matrix

            if n == self.iterations - 1:
                print ("Warning, did not converge")
                self.min_gradient_norm = min(self.gradient_norm)
                self.min_weight_matrix = self.weight_multiclass[np.argmin(self.gradient_norm)]
                self.multi_weight_matrix = weight_multiclass
                return self.min_weight_matrix


#if __name__ == "__main__":
#
#    #train_X = np.matrix([[1,0,-1],[1,2,0],[-1,-2,2],[-3,-2,10],[30,0,1]])
#    #train_y = np.matrix([[0],[1],[0],[1],[2]])
#    filename = "skin_diseases/cleaned_skin_diseases.csv"
#    data = np.loadtxt(filename, delimiter=",")
#    X = data[:,0:-1]
#    y = data[:, -1].reshape((-1, 1))
#    test_data = 1
#    train_X = np.matrix(X[0:-test_data, :])
#    train_y = y[0:-test_data] - 1
#    test_X = np.matrix(X[-100:, :])
#    test_y = y[-100:] - 1
#    t = 70000
#    NN = NeuralNetwork(hidden_layer_neurons=5, iterations=50000, gradient_threshold=0.1, rms_threshold=0.001, learning_rate=1e-5)
#
#    NN.setXy(train_X, train_y)
#    NN.fit()
#    #test_X = np.matrix([[1, 0, -1],[30,0,1]])
#    import pandas as pd
#    try:
#        df1 = pd.read_csv('skin_diseases/weight_matrix.csv', header=None)
#        w_matrix = np.matrix(df1.as_matrix())
#    except OSError:
#        w_matrix = None
#    predicted_y = NN.predict(test_X, w_matrix=w_matrix)
#
#    df = pd.DataFrame(NN.multi_weight_matrix)
#    df.to_csv('skin_diseases/weight_matrix.csv',delimiter=',', index=False, header=False)
#
#    accuracy = predicted_y - test_y == 0
#    count = 0
#    for i in range(len(predicted_y)):
#        if predicted_y[i] - test_y[i] == 0:
#            count += 1
#    accuracy = count / len(test_y)
#    print (accuracy)
#
#    import matplotlib.pyplot as plt
#    plt.plot(range(len(NN.gradient_norm)), NN.gradient_norm)
#    plt.show()
#    #x_min, x_max = train_X[:, 1].min() - 0.5, train_X[:, 1].max() + 0.5
#    #y_min, y_max = train_X[:, 2].min() - 0.5, train_X[:, 2].max() + 0.5
#    #h = 0.2 # step size in the mesh
#    #xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#    #plt.figure()
#    #plt.pcolormesh(train, yy, Z, cmap=cmap_light)
#    #plt.plot(X[0:N_c-1, 1], X[0:N_c-1, 2], 'ro', X[N_c:2*N_c-1, 1], X[N_c:2*N_c-1,
#    #2], 'bo', X[2*N_c:, 1], X[2*N_c:, 2], 'go')
#    #plt.axis([np.min(X[:, 1])-0.5, np.max(X[:, 1])+0.5, np.min(X[:, 2])-0.5, np.max(X[:, 2])+0.5])
#    #plt.show()
#    #import pandas as pd
#    #df = pd.read_csv(filename)
#    #df = df[df["55"] != "?"]
#    #df.to_csv("skin_diseases/cleaned_skin_diseases.csv", index=False)











