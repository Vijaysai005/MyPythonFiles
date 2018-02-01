# !usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:00:30 2018

@author: vijayasai
"""

import sys
sys.path.append("/home/vijay/Documents/GitHub/MyPythonFiles/Routing/route/")
sys.path.append("/home/vijay/Documents/GitHub/MyPythonFiles/Routing/utils/")
sys.path.append("/home/vijay_sai005/gitlab_dir/MyPythonFiles/Routing/utils")
sys.path.append("/home/vijay_sai005/gitlab_dir/MyPythonFiles/Routing/route")

import googlemaps
import waymap

import pandas as pd
from pymongo import MongoClient
from polyline_route import PolylineRoute
from geo_utils import GeoUtils


gmaps = googlemaps.Client(key="AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY")
mongo_client = MongoClient(host="localhost", port=27017)
utils = GeoUtils()

source = sys.argv[1]
destination = sys.argv[2]
mode = sys.argv[3]

db_name = "tbt_data"
coll_name = "google_routes"

db = mongo_client[db_name]
coll = db[coll_name]

_id = "{}_{}_{}".format(source.lower(), destination.lower(), mode)

if not coll.find_one({"_id":_id}):
    print ("Hi I am calling google API")
    try:
        output = gmaps.directions(origin=source, destination=destination)

        packet = {}
        packet.update(output[0])
        packet["_id"] = _id

        coll.insert(packet)
    except IndexError:
        sys.exit()

packet = coll.find_one({"_id": _id})
direction_legs = packet["legs"]

PR = PolylineRoute()
lat, lng = PR.polyline_route(direction_legs)

df = pd.DataFrame()
df["latitude"], df["longitude"] = lat, lng
df = pd.concat((df, df[["latitude", "longitude"]].shift().\
    rename(columns={"latitude":"latitude1", "longitude":"longitude1"})),axis=1)
df.loc[0, "latitude1"] = df.loc[0, "latitude"]
df.loc[0, "longitude1"] = df.loc[0, "longitude"] 

df["current_distance"] = df.apply(lambda x: utils.haversine_distance((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"])), axis=1)
df["total_distance"] = df["current_distance"].cumsum()

df["absolute_bearing"] = df.apply(lambda x: utils.compass((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"]))["angles"]["degrees"], axis=1)
df["true_bearing"] = df.apply(lambda x: utils.bearing_angle((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"]))[0], axis=1)

df["direction"] = df.apply(lambda x:utils.compass((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"]))["directions"]["short"], axis=1)

df = pd.concat((df, df[["true_bearing", "direction"]].shift().\
    rename(columns={"true_bearing":"true_bearing1", "direction":"direction1"})),axis=1)
df.loc[0, "true_bearing1"] = df.loc[0, "true_bearing"]
df.loc[0, "direction1"] = df.loc[0, "direction"] 

df["turning_angle"] = df.apply(lambda x:utils.turning_angle((x["true_bearing1"],x["direction1"]),\
    (x["true_bearing"],x["direction"])), axis=1)

df = df.drop(columns=["latitude1", "longitude1", "true_bearing1", "direction1"])
index = int(len(df)/2)

centre_lat = df.loc[index, "latitude"]
centre_lng = df.loc[index, "longitude"]

wmap = waymap.WayMap(zoom=6, cent_lat=centre_lat, cent_lng=centre_lng)

scatterness = False
no_of_points = 0
if sys.argv[4] == "yes":
    scatterness = True
    if sys.argv[5] != "":
        no_of_points = int(sys.argv[5])
    else:
        no_of_points = "all"

    reduced_df = wmap.reduced_dataframe(df, no_of_points=no_of_points)
    wmap.plot_route(reduced_df, plot_type="scatter", color="#1E90FF", type="HTML", data_for=wmap.html_handling(reduced_df, "random"))

wmap.plot_route(df, plot_type="plot", type="HTML", data_for=wmap.html_handling(df, "random"))

route = "source->{}_destination->{}_scatterness->{}_points->{}".format(source, destination, scatterness, no_of_points)
try:
    wmap.draw("/home/vijay_sai005/gitlab_dir/MyPythonFiles/Routing/app/templates/route_map:{}.html".format(route))
except Exception:
    wmap.draw("/home/vijay/Documents/GitHub/MyPythonFiles/Routing/app/templates/route_map:{}.html".format(route))