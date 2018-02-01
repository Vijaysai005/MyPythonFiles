# !usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:00:30 2018

@author: vijayasai
"""

import googlemaps
import gmplot
import pandas as pd
import warnings
import os

gmaps = googlemaps.Client(key="AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY")

class WayMap(object):

    def __init__(self, edge_width=5, size=10, zoom=4, cent_lat=18.6233178741, cent_lng=73.7144361295):
        
        self.gmap = gmplot.GoogleMapPlotter(cent_lat, cent_lng, zoom, apikey="AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY", folder="../static/%s.png")        
        self.size = size
        self.edge_width = edge_width

    def write_csv(self, filename=None, df=None, mask=None, var=None, col="r"):
        try:
            #df = df.loc[mask].reset_index()
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

    # HTML Handling
    warnings.filterwarnings("ignore")
    def html_handling(self, df, name):
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
            #print (empty)
            data = str(empty)
            #print (data)
            string.append("\""+data[1:-1]+"\"")
        return string

    def reduced_dataframe(self, df, no_of_points=50):
        if no_of_points == "all":
            df = df
        elif len(df) <= no_of_points:
            df = df
        else:
            index_list = list(range(0, len(df), round(len(df)/no_of_points)))
            df = df.loc[index_list]
            df = df.reset_index(drop=True)
        return df

    def plot_route(self, data, plot_type="plot", color="m", marker=True, type="NoHTML", data_for="No data"):
        """
        Plot points on map
        """
        try:
            df = pd.read_csv(data)
        except Exception:
            df = data

        if type != "HTML":
            string=self.popUp(df)
        else:
            string=data_for

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


    def decode_polyline(self, point_str):
        """
        Decodes a polyline that has been encoded using Google's algorithm
        http://code.google.com/apis/maps/documentation/polylinealgorithm.html

        This is a generic method that returns a list of (latitude, longitude)
        tuples.

        :param point_str: Encoded polyline string.
        :type point_str: string
        :returns: List of 2-tuples where each tuple is (latitude, longitude)
        :rtype: list
        """

        # some coordinate offset is represented by 4 to 5 binary chunks
        coord_chunks = [[]]
        for char in point_str:

            # convert each character to decimal from ascii
            value = ord(char) - 63

            # values that have a chunk following have an extra 1 on the left
            split_after = not (value & 0x20)
            value &= 0x1F

            coord_chunks[-1].append(value)

            if split_after:
                    coord_chunks.append([])

        del coord_chunks[-1]

        coords = []

        for coord_chunk in coord_chunks:
            coord = 0

            for i, chunk in enumerate(coord_chunk):
                coord |= chunk << (i * 5)

            # there is a 1 on the right if the coord is negative
            if coord & 0x1:
                coord = ~coord  # invert
            coord >>= 1
            coord /= 100000.0

            coords.append(coord)

        # convert the 1 dimensional list to a 2 dimensional list and offsets to
        # actual values
        points = []
        prev_x = 0
        prev_y = 0
        for i in range(0, len(coords) - 1, 2):
            if coords[i] == 0 and coords[i + 1] == 0:
                continue

            prev_x += coords[i + 1]
            prev_y += coords[i]
            # a round to 6 digits ensures that the floats are the same as when
            # they were encoded
            points.append([round(prev_x, 6), round(prev_y, 6)])

        return points


    def draw_map_directions(self, direction_result, plot_type="plot", color="r", marker=True):
        """
        Draw direction results route on map
        """

        polylines = []
        for leg in direction_result[0]["legs"]:
            for step in leg["steps"]:
                polylines.append(step['polyline']['points'])

        locations = [self.decode_polyline(x) for x in polylines]
        locations = [x for y in locations for x in y]

        latitudes = [x[1] for x in locations]
        longitudes = [x[0] for x in locations]

        if plot_type == "plot":
            self.gmap.plot(latitudes, longitudes, color=color,
                      edge_width=self.edge_width, marker=marker)
        else:
            self.gmap.scatter(latitudes, longitudes, color=color,
                         size=self.size, edge_width=self.edge_width, marker=marker)


    def plot_waypoints_route(self, waypoints_csv_path, plot_type="plot", color="r", marker=False):
        """
        Plot route on map using waypoints
        """
        df = pd.read_csv(waypoints_csv_path)
        waypoints = []
        for i in range(len(df["latitude"])):
            point = []
            point.append(df["latitude"][i])
            point.append(df["longitude"][i])
            waypoints.append(point)

        while len(waypoints) > 0:
            if len(waypoints) > 23:
                wp = waypoints[0:23]
                del waypoints[0:22]
            else:
                wp = waypoints
                waypoints = []

            start = wp[0]
            finish = wp[len(wp)-1]

            del wp[len(wp)-1]
            del wp[0]

            global gmaps
            directions_result = gmaps.directions(start, finish, waypoints=wp)
            self.draw_map_directions(directions_result, plot_type, color, marker)

    def draw(self, html_file):
        self.gmap.draw(html_file)

#if __name__ == "__main__":
#
#    gplot = GoogleMap(edge_width=5)
#    gplot.plot_waypoints_route("Allrecord1410670.csv", plot_type="plot")
#    gplot.draw("./1410700A.html")
