#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:44:30 2018

@author: vijayasai
"""

""" Import module."""
import os
import sys
sys.path.append("../utils")
sys.path.append("../vplot")
sys.path.append("../config")

import pandas as pd
from flask_googlemaps import Map, icons
from flask_googlemaps import GoogleMaps
from flask import Flask, render_template, request, redirect, url_for

from waymap import WayMap
from geo_utils import GeoUtils
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from configuration import Configuration

""" Creating instances."""
wmap = WayMap()
utils = GeoUtils()
geolocator = Nominatim()
config = Configuration()

""" Starting mongo if its not started."""
try:
    os.system("sudo service mongod restart")
except Exception:
    pass

mongo_client = MongoClient(host=config.MONGO_HOST, port=config.MONGO_PORT)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['GOOGLEMAPS_KEY'] = config.API_KEY
GoogleMaps(app, key=config.API_KEY)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/utilities/")
def utilities():
    return "hi"
    

@app.route("/maps/")
def maps():
    return render_template("map-input.html")


@app.route("/about/")
def about():
    return "hi"

@app.route("/")
def back():
    return 
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(sys.argv[1]), threaded=True)


