# !usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Jan 4 01:00:30 2018

@author: vijayasai
"""

import os, sys, warnings
sys.path.append(
    "/home/vijay_sai005/gitlab_dir/MyPythonFiles/GeoUtilsApp/config/")

import googlemaps, gmplot
import pandas as pd
from configuration import Configuration

config = Configuration()
gmaps = googlemaps.Client(key=config.API_KEY)

""" WayMap Module."""
class WayMap(object):

    def __init__(self, edge_width=5, size=10, zoom=4, cent_lat=18.623317, cent_lng=73.714436, folder = "../static/%s.png"):
        
        self.gmap = gmplot.GoogleMapPlotter(cent_lat, cent_lng, zoom, apikey=config.API_KEY, folder=folder)        
        self.size = size
        self.edge_width = edge_width

    def write_csv(self, filename=None, df=None, mask=None, var=None, col="r"):
        try:
            if (not mask is None) and var != None:
                df.loc[mask, var] = col
                df = df[df["color"] == col]
                df.reset_index(inplace=True)
                df.drop(["index"], axis=1, inplace=True)
            if filename != None:
                df.to_csv(filename, index=False)
        except Exception:
            raise Exception("No Data")
        return df

    warnings.filterwarnings("ignore")
    def data_for_table(self, df, name):
        df_trans = df.T
        data = []
        for index in range(len(df.index)):
            x = pd.DataFrame(df_trans[index])
            x.to_html("{}_{}.html".format(name, index), index=True, header=False)
            with open("{}_{}.html".format(name, index), 'r') as myfile:
                html_data = "'+'".join(myfile.read().splitlines())
                new = "\'{}\'".format(html_data)
            myfile.close()
            os.remove("{}_{}.html".format(name, index))
            data.append(new)
        return data

    def popUp(self, df):
        headers = df.columns.values.tolist()
        string = []
        for i in range(len(df[headers[0]])):
            empty = []
            for header in headers:
                empty.append(header+": "+str(df[header][i]))
            data = str(empty)
            string.append("\""+data[1:-1]+"\"")
        return string

    def reduced_dataframe(self, df, no_of_points=50, default_str="all"):
        if no_of_points == default_str:
            df = df
        elif len(df) <= no_of_points:
            df = df
        else:
            index_list = list(range(0, len(df), round(len(df)/no_of_points)))
            df = df.loc[index_list]
            df = df.reset_index(drop=True)
        return df

    def plot_route(self, data, plot_type="plot", color="m", marker=True, popup="none", data_for_table="No data"):
        """
        Plot points on map
        """
        try:
            df = pd.read_csv(data)
        except Exception:
            df = data
        
        string = "No Data"
        if popup == "table-popup":
            string = data_for_table
        elif popup == "normal-popup":
            string = self.popUp(df)

        if plot_type == "plot":

            try:
                self.gmap.plot(df["latitude"].values.tolist(),
                      df["longitude"].values.tolist(), color=color,
                      edge_width=self.edge_width, marker=marker, string=string)
            except Exception:
                try:
                    self.gmap.plot(df["poi_lat"].values.tolist(),
                          df["poi_lng"].values.tolist(), color=color,
                          edge_width=self.edge_width, marker=marker, string=string)
                except:
                    self.gmap.plot(df["lat"].values.tolist(),
                          df["lng"].values.tolist(), color=color,
                          edge_width=self.edge_width, marker=marker, string=string)

        else:
            try:
                self.gmap.scatter(df["latitude"].values.tolist(),
                         df["longitude"].values.tolist(), color=color,
                         size=self.size, edge_width=self.edge_width, marker=marker,string=string)
            except Exception:
                try:
                    self.gmap.scatter(df["poi_lat"].values.tolist(),
                             df["poi_lng"].values.tolist(), color=color,
                             size=self.size, edge_width=self.edge_width, marker=marker,string=string)
                except:
                    self.gmap.scatter(df["lat"].values.tolist(),
                             df["lng"].values.tolist(), color=color,
                             size=self.size, edge_width=self.edge_width, marker=marker,string=string)


    def plot_route_coord(self, x, y, plot_type="plot", color="b", marker=True):
        """
        Plot points on map
        """

        if plot_type == "plot":
            self.gmap.plot(x, y, color=color,
                      edge_width=self.edge_width, marker=marker)
        else:
            self.gmap.scatter(x, y, color=color,
                         size=self.size, edge_width=self.edge_width, marker=marker)


    def draw(self, html_file):
        self.gmap.draw(html_file)

