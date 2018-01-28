# #! /virtual_envs/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 12:12:23 2017

@author: vijayasais
"""

import time
import os
import sys
sys.path.append("../utils")
sys.path.append("../vplot")
os.path.join("/home/vijay/virtual_envs/hacking/lib/python3.5/site-packages/gmplot/markers/")

from flask import Flask, render_template, request, redirect, url_for
from flask_googlemaps import Map, icons
from flask_googlemaps import GoogleMaps
import pandas as pd

from geo_utils import GeoUtils
from waymap import WayMap

wmap = WayMap()
utils = GeoUtils()

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"
GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/")
def back():
    retur

@app.route("/utilities/")
def utility():
    return render_template('utility.html')


@app.route("/maps/")
def route_maps():
    return render_template('map_input.html')

@app.route("/maps/", methods=["POST"])
def calculate_route():
    if request.method == 'POST':
        source = request.form['source'].lower()
        destination = request.form['dest'].lower()
        mode = "driving"

        command = "python ../vplot/__main__.py {} {} {}".format(source, destination, mode)
        os.system("cd templates/ && rm -rf route_map*")
        os.system(command)
        route = "{}_{}".format(source, destination)
        return redirect(url_for(".show_map", result=route))

@app.route("/maps/<result>")
def show_map(result):
    return render_template("route_map_{}.html".format(result), result=result)

@app.route('/utilities/haversine/')
def haversine_calculator():
    return render_template('haversine.html')

@app.route('/utilities/haversine/', methods = ['POST'])
def haversine_result():
    source_lat = float(request.form['source-lat'])
    source_long = float(request.form['source-long'])
    dest_lat = float(request.form['dest-lat'])
    dest_long = float(request.form['dest-long'])
    
    df = pd.DataFrame()
    df["latitude"] = [source_lat, dest_lat]
    df["longitude"] = [source_long, dest_long]
    data = wmap.html_handling(df, "random")

    if request.form['action'] == 'submit':
        result = utils.haversine_distance((source_lat, source_long), (dest_lat, dest_long))
        output = "Distance: {} km".format(round(result,3))
        return render_template('haversine.html', result=output)
    
    elif request.form['action'] == "Show on Map":
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:592px;width:1300px;margin:0;", 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.blue,
                'lat': source_lat,
                'lng': source_long,
                'infobox': data[0]
            },
            {
                'icon': icons.dots.blue,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': data[1]
            }])
        return render_template('haversine_map.html', trdmap=trdmap)


@app.route('/utilities/bearing/')
def bearing_calculator():
    return render_template('bearing.html')

@app.route('/utilities/bearing/', methods=['POST'])
def bearing_result():
    source_lat = float(request.form['source-lat'])
    source_long = float(request.form['source-long'])
    dest_lat = float(request.form['dest-lat'])
    dest_long = float(request.form['dest-long'])
    
    df = pd.DataFrame()
    df["latitude"] = [source_lat, dest_lat]
    df["longitude"] = [source_long, dest_long]
    data = wmap.html_handling(df, "random")

    if request.form['action'] == 'submit':
        result = utils.bearing_angle((source_lat, source_long), (dest_lat, dest_long))
        output = "Bearing: {} degrees. Clockwise from North".format(round(result[0],3))
        return render_template('bearing.html', result=output)
    
    elif request.form['action'] == "Show on Map":
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:592px;width:1300px;margin:0;", 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.blue,
                'lat': source_lat,
                'lng': source_long,
                'infobox': data[0]
            },
            {
                'icon': icons.dots.blue,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': data[1]
            }])
        return render_template('haversine_map.html', trdmap=trdmap)


@app.route('/utilities/')
def utility_back():
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0")