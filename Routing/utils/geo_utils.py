# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 6 12:12:23 2017

@author: vijayasais
"""

import numpy as np
from pprint import pprint

""" GeoUtils module."""

class GeoUtils(object):


    def __init__(self):
        pass


    def haversine_formula(self, theta):
        return (1 - np.cos((theta))) * 0.5


    def haversine_distance(self, data_A = (), data_B = ()):

        lat1 = data_A[0]
        lat2 = data_B[0]
        long1 = data_A[1]
        long2 = data_B[1]

        radius = 6371.0  # mean radius of the earth (in KM)
        # haversine formula for determining the distance haversine function
        func = (self.haversine_formula(np.abs(np.radians(np.float(lat1)) - np.radians(np.float(lat2))))) +\
            (np.cos(np.radians(np.float(lat1))) * np.cos(np.radians(np.float(lat2))) *
                self.haversine_formula(np.abs(np.radians(np.float(long1)) - np.radians(np.float(long2)))))
        # angle from distance haversine function
        angle = 2.0 * np.arctan2(np.sqrt(func), np.sqrt(1 - func))
        # distance between the two locations
        distance = radius * angle
        return distance

    def bearing_angle(self, data_A = (), data_B = ()):
        
        lat_a = data_A[0]
        lng_a = data_A[1]
        lat_b = data_B[0]
        lng_b = data_B[1]

        lat1, lng1, lat2, lng2 = map(np.radians, [lat_a, lng_a, lat_b, lng_b])
        dLng = lng2 - lng1
        X = np.sin(dLng) * np.cos(lat2)
        Y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dLng)
        bearing_radians = np.arctan2(X, Y)
        bearing_degrees = bearing_radians*(180.0/np.pi)
        return bearing_degrees, bearing_radians


    def turning_angle(self, data_A = (), data_B = ()):

        # Here bearing is True Bearing
        # Need to analyzed a lot
        bearing1 = data_A[0]
        direction1 = data_A[1]
        bearing2 = data_B[0]
        direction2 = data_B[1]

        # if source point is pointing towards North and the destination point is pointing towards
        # any direction below formula can be used
        if direction1 == "N":
            beta = abs(bearing2 - bearing1)

        # if source point is pointing towards South
        elif direction1 == "S":
            # if destination point is pointing towards to any one of ["S","N","E","NE","SE"]
            if direction2 in ["S","N","E","NE","SE"]:
                beta = abs(bearing2 - bearing1)
            # if destination point is pointing towards to any one of ["NW","SW", "W"]
            elif direction2 in ["NW","SW", "W"]:
                beta = abs(abs(bearing2) - bearing1)

        # if source point is pointing towards West
        elif direction1 == "W":
            # if destination point is pointing towards to any one of ["W","N","E","NE","SW", "NW"]
            if direction2 in ["W","N","E","NE","SW", "NW"]:
                beta = abs(bearing2 - bearing1)
            # if destination point is pointing towards to any one of ["SE","S"]
            elif direction2 in ["SE","S"]:
                beta = 360 - (abs(bearing2 - bearing1))

        # if source point is pointing towards East
        elif direction1 == "E":
            # if destination point is pointing towards to any one of ["W","N","E","NE","NW","S","SE"]
            if direction2 in ["W","N","E","NE","NW","S","SE"]:
                beta = abs(bearing2 - bearing1)
            # if destination point is pointing towards SW
            elif direction2 == "SW":
                beta = 360 - (abs(bearing2 - bearing1))

        elif direction1 == "NE":
            if direction2 in ["W", "N", "S", "NE", "SE", "NW", "E"]:
                beta = abs(bearing2 - bearing1)
            elif direction2 == "SW":
                if abs(bearing2 + 90) <= bearing1:
                    beta = abs(bearing2 - bearing1)
                elif abs(bearing2 + 90) > bearing1: 
                    beta = 360 - (abs(bearing2 - bearing1))

        elif direction1 == "SE":
            if direction2 in ["E", "SE", "N", "S", "NE"]:
                beta = abs(bearing2 - bearing1)
            elif direction2 in ["W", "SW"]:
                beta = 360 - (abs(bearing2 - bearing1))
            elif direction2 == "NW":
                if abs(bearing2 + 180) <= bearing1:
                    beta = 360 - (abs(bearing2 - bearing1))
                elif abs(bearing2 + 180) > bearing1:
                    beta = abs(bearing2 - bearing1)

        elif direction1 == "NW":
            if direction2 in ["N","E","W", "NW", "NE", "SW"]:
                beta = abs(bearing2 - bearing1)
            elif direction2 in ["S"]:
                beta = abs(bearing2 - abs(bearing1))
            elif direction2 == "SE":
                if 180 - bearing2 >= abs(bearing1):
                    beta = abs(bearing2 - bearing1)
                elif 180 - bearing2 < abs(bearing1):
                    beta = 360 - (abs(bearing2 - bearing1))

        elif direction1 == "SW":
            if direction2 in ["SW", "W", "N", "NW"]:
                beta = abs(bearing2 - bearing1)
            elif direction2 in ["S", "E", "SE"]:
                beta = 360 - (abs(bearing2 - bearing1))
            elif direction2 == "NE":
                if 180 - bearing2 >= abs(bearing1):
                    beta = abs(bearing2 - bearing1)
                elif 180 - bearing2 < abs(bearing1):
                    beta = 360 - (abs(bearing2 - bearing1))
        return beta


    def compass(self, data_A = (), data_B = ()):
        
        bearing_degrees, bearing_radians = self.bearing_angle(data_A, data_B)

        output = {}
        output["angles"] = {}
        
        degrees = bearing_degrees if bearing_degrees > 0 else 360.0 + bearing_degrees
        radians = bearing_radians if bearing_radians > 0 else 2*np.pi + bearing_radians

        output["angles"]["degrees"] = degrees
        output["angles"]["radians"] = radians
        output["reference"] = "Clockwise from North"

        output["directions"] = {}

        if output["angles"]["degrees"] > 0.0 and output["angles"]["degrees"] < 90.0:
            output["directions"]["long"] = "North-East"
            output["directions"]["short"] = "NE"
        
        elif output["angles"]["degrees"] > 90.0 and output["angles"]["degrees"] < 180.0:
            output["directions"]["long"] = "South-East"
            output["directions"]["short"] = "SE"
        
        elif output["angles"]["degrees"] > 180.0 and output["angles"]["degrees"] < 270.0:
            output["directions"]["long"] = "South-West"
            output["directions"]["short"] = "SW"
        
        elif output["angles"]["degrees"] > 270.0 and output["angles"]["degrees"] < 360.0:
            output["directions"]["long"] = "North-West"
            output["directions"]["short"] = "NW"
        
        elif output["angles"]["degrees"] == 0.0 or output["angles"]["degrees"] == 360.0:
            output["directions"]["long"] = "North"
            output["directions"]["short"] = "N"
        
        elif output["angles"]["degrees"] == 90:
            output["directions"]["long"] = "East"
            output["directions"]["short"] = "E"
        
        elif output["angles"]["degrees"] == 180:
            output["directions"]["long"] = "South"
            output["directions"]["short"] = "S"
        
        elif output["angles"]["degrees"] == 270:
            output["directions"]["long"] = "West"
            output["directions"]["short"] = "W"
        
        return output

if __name__ == "__main__":
    geo = GeoUtils()
    output = geo.compass((18.593338, 73.735991), (18.593511, 73.735777))
    pprint (output)