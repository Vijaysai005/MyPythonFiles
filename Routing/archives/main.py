#! /usr/bin/env python

from pymongo import MongoClient
import pandas as pd

import numpy as np
from compass import Directions

client = MongoClient("localhost", 27017)
db = client.maximus_db

rides = db.rides
ride_members = db.ride_members
devices = db.devices

rides_data = rides.find({}, {"route": 0, "tbt_route": 0}).sort([('date_started', -1)]).limit(1)

rides_data = list(list(rides_data))
ride_members = ride_members.find({"ride_id": rides_data[0]["_id"]})
#ride_members = list(list(ride_members))


global out
out = Directions()
def direc(lat1, lng1, lat2, lng2, mode="angle", type="degrees"):
    global out
    out.GeoData((lat1, lng1), (lat2, lng2))
    output = out.solve()
    if mode == "angle" and type == "radians":
        return output["angles"]["radians"]
    if mode == "angle" and type == "degrees":
        return output["angles"]["degrees"]
    if mode == "direction" and type == "long":
        return output["directions"]["long"]
    if mode == "direction" and type == "short":
        return output["directions"]["short"]


achievement_objects = {}
for rm in ride_members:
    device_id = db.devices.find_one({"_id": rm["ride_device_id"]})
    ptr = db.device_data.find(
        {"unit_id": int(device_id["serial_number"]), "ignition_status": 1, "packettimestamp":{"$gte":rides_data[0]["date_started"], "$lte":rides_data[0]["date_finished"]}, 'gps_validity':1, 'ground_speed':{'$gte': 10}},{'_id': 0, 'unit_id': 1, 'packettimestamp': 1, 'latitude': 1,'longitude': 1}).sort([("packettimestamp", 1)])


    data = list(list(ptr))
    df = pd.DataFrame(data)


    df = pd.concat((df, df[["latitude", "longitude"]].shift(periods=-1).rename(columns=\
                {"latitude":"lat1", "longitude":"lng1"})), axis=1)
    df = df.reset_index(drop=True)
    df = df.fillna(0)
    df["bearing_angle"] = df.apply(lambda x: direc(x["latitude"], x["longitude"], x["lat1"], x["lng1"], mode="angle", type="degrees"), axis=1)
    df["heading"] = df.apply(lambda x: direc(x["latitude"], x["longitude"], x["lat1"], x["lng1"], mode="direction", type="long"), axis=1)
    #print (df)
