# !usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:00:30 2018

@author: vijayasai
"""

import sys
sys.path.append("/home/vijay/Documents/GitHub/MyPythonFiles/GeoUtilsApp/route/")
sys.path.append("/home/vijay/Documents/GitHub/MyPythonFiles/GeoUtilsApp/utils/")
sys.path.append("/home/vijay/Documents/GitHub/MyPythonFiles/GeoUtilsApp/config/")


import pandas as pd
import googlemaps
import waymap

from pymongo import MongoClient
from polyline_route import PolylineRoute
from geo_utils import GeoUtils
from config import Configuration

config = Configuration()
gmaps = googlemaps.Client(key=config.API_KEY)
mongo_client = MongoClient(host="localhost", port=27017)

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
    output = gmaps.directions(origin=source, destination=destination, mode=mode)

    packet = {}
    packet.update(output[0])
    packet["_id"] = _id

    coll.insert(packet)

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
geo_prop = GeoUtils()

df["distance"] = df.apply(lambda x: geo_prop.haversine_distance((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"])), axis=1)
df["bearing_angle"] = df.apply(lambda x: geo_prop.compass((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"]))["angles"]["degrees"], axis=1)
df["direction"] = df.apply(lambda x:geo_prop.compass((x["latitude1"], x["longitude1"]),\
    (x["latitude"], x["longitude"]))["directions"]["long"], axis=1)
print (df.head(30))

centre_lat=df.loc[len(df)/2, "latitude"]
centre_lng=df.loc[len(df)/2, "longitude"]
wmap = waymap.WayMap(cent_lat=centre_lat, cent_lng=centre_lng, folder="../app/static/%s.png")
wmap.plot_route(df, plot_type="scatter", color="#1E90FF", popup="table-popup", data_for_table=wmap.data_for_table(df, "random"))
wmap.draw("route_map.html")
