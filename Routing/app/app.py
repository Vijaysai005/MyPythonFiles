# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 12:12:23 2017

@author: vijayasais
"""

import sys
sys.path.append("../utils")

from flask import Flask, render_template, request
from flask_googlemaps import Map, icons
from flask_googlemaps import GoogleMaps

from geo_utils import GeoUtils
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

@app.route('/utilities/haversine/')
def haversine_calculator():
    return render_template('haversine.html')

@app.route('/utilities/haversine/', methods = ['POST'])
def haversine_result():
    source_lat = float(request.form['source-lat'])
    source_long = float(request.form['source-long'])
    dest_lat = float(request.form['dest-lat'])
    dest_long = float(request.form['dest-long'])
    
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
                'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
            },
            {
                'icon': icons.dots.blue,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
            }])
        return render_template('map.html', trdmap=trdmap)


@app.route('/utilities/')
def utility_back():
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0")