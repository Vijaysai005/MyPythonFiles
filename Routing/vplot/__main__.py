# !usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:00:30 2018

@author: vijayasai
"""

import sys
sys.path.append("/home/vijay/Documents/GitLab/MyProject/Routing/route/")
sys.path.append("/home/vijay/Documents/GitLab/MyProject/Routing/utils/")
sys.path.append("/gitlab_dir/MyPythonFiles/Routing/utils")
sys.path.append("/gitlab_dir/MyPythonFiles/Routing/route")

import googlemaps
import waymap


from pymongo import MongoClient
from polyline_route import PolylineRoute
from geo_utils import GeoUtils


gmaps = googlemaps.Client(key="AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY")

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
    output = gmaps.directions(origin=source, destination=destination)

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

index = int(len(df)/2)

centre_lat = df.loc[index, "latitude"]
centre_lng = df.loc[index, "longitude"]

wmap = waymap.WayMap(zoom=6, cent_lat=centre_lat, cent_lng=centre_lng)
wmap.plot_route(df, plot_type="plot")

#reduced_df = wmap.reduced_dataframe(df, no_of_points=50)
#wmap.plot_route(reduced_df, plot_type="scatter", type="HTML", data_for=wmap.html_handling(reduced_df, "random"))

route = "{}_{}".format(source, destination)
try:
    wmap.draw("/gitlab_dir/MyPythonFiles/Routing/app/templates/route_map_{}.html".format(route))
except Exception:
    wmap.draw("/home/vijay/Documents/GitHub/MyPythonFiles/Routing/app/templates/route_map_{}.html".format(route))