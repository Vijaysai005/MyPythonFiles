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

import gmplot
import pandas as pd
from flask_googlemaps import Map, icons
from flask_googlemaps import GoogleMaps
from flask import Flask, render_template, request, redirect, url_for

from waymap import WayMap
from geo_utils import GeoUtils
from chatbot import ChatBox
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from configuration import Configuration

""" Creating instances."""
utils = GeoUtils()
geolocator = Nominatim()
config = Configuration()
ai_response = ChatBox()

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

@app.route("/about/")
def about():
    return "hi"

@app.route("/")
def back():
    return 

@app.route("/login/")    
def log_in():
    return render_template("login.html")

@app.route("/hearty/")
def chat_some():
    return render_template("hearty.html")

@app.route("/hearty/", methods=["POST"])
def chat_resp():
    if request.method == "POST":
        if request.form['action'] == 'Submit':
            query = request.form['you']
            answer = ai_response.get_output(query)
            return render_template('hearty.html', you=query, hearty=answer)
        
@app.route("/hearty/training/")
def chat_train():
    return render_template("hearty_training.html")

@app.route("/hearty/training/", methods=['POST'])
def chat_train_resp():
    if request.method == "POST":
        if request.form['action'] == 'Train Me':
            query = request.form['query']
            response = request.form['response']
            try:
                ai_response.do_train(query, response)
                result="Thanks for training me"
            except Exception:
                result = "Invalid query or response"

            return render_template("hearty_training.html", result=result)

@app.route("/maps/")
def maps():
    return render_template("map_input.html")
    
@app.route("/maps/", methods=["POST"])
def calculate_route():
    if request.method == 'POST':
        source = request.form['source'].lower()
        destination = request.form['dest'].lower()
        mode = config.ROUTE_MODE

        scatterness = config.DATA_SCATTERNESS
        no_of_points = config.DATA_POINTS
        pop_status = config.POP_STATUS

        if request.form.get("scatterness"):
            scatterness = "yes"
            no_of_points = request.form["points"]

        command = "python ../vplot/__main__.py \"{}\" \"{}\" \"{}\" \"{}\" \"{}\" \"{}\"".format(
            source, destination, mode, scatterness, no_of_points, pop_status) 
        os.system("cd templates/ && rm -rf route_map*")
        os.system(command)

        scatter = False if scatterness == "no" else True 

        try:
            int(no_of_points)
        except ValueError:
            no_of_points = "all"

        route = "source->{}_destination->{}_scatterness->{}_points->{}".format(
            source, destination, scatter, no_of_points)
        return redirect(url_for(".show_map", result=route))


@app.route("/maps/<result>")
def show_map(result):
    try:
        return render_template("route_map:{}.html".format(result), result=result)
    except Exception:
        return "Please try to give valid Place name"


@app.route('/haversine/')
def haversine_calculator():
    return render_template('haversine.html')


@app.route('/haversine/', methods=['POST'])
def haversine_result():

    condition = True
    source = request.form['source']
    dest = request.form['dest']
    wmap = WayMap(zoom=6, folder="../../static/images/%s.png")
    try:
        try:

            source_ = source.split(",")

            source_lat = float(source_[0])
            source_long = float(source_[1])

            dest_ = dest.split(",")

            dest_lat = float(dest_[0])
            dest_long = float(dest_[1])
            result = utils.haversine_distance(
                (source_lat, source_long), (dest_lat, dest_long))

            df = pd.DataFrame()
            df["latitude"] = [source_lat, dest_lat]
            df["longitude"] = [source_long, dest_long]
            df["type"] = ["source", "destination"]
            df["haversine distance"] = [0, result]
            data = wmap.data_for_table(df, "random")

        except Exception:

            try:
                check = source.split(",")
                check = "".join(check)
                float(check)
                raise Exception
            except ValueError:
                pass

            try:
                check = dest.split(",")
                check = "".join(check)
                float(check)
                raise Exception
            except ValueError:
                pass

            source_result = geolocator.geocode(source)
            dest_result = geolocator.geocode(dest)

            source_lat = float(source_result.latitude)
            source_long = float(source_result.longitude)
            dest_lat = float(dest_result.latitude)
            dest_long = float(dest_result.longitude)

            result = utils.haversine_distance(
                (source_lat, source_long), (dest_lat, dest_long))

            df = pd.DataFrame()
            df["latitude"] = [source_lat, dest_lat]
            df["longitude"] = [source_long, dest_long]
            df["type"] = ["source", "destination"]
            df["haversine distance"] = [0, result]
            data = wmap.data_for_table(df, "random")
    except Exception:
        condition = False
        pass

    if request.form['action'] == 'Submit':
        
        try:
            output = "Distance: {} km".format(round(result, 3))
        except Exception:
            return render_template('haversine.html', result="Invalid LatLng", source=source, dest=dest)
        return render_template('haversine.html', result=output, source=source, dest=dest)

    elif request.form['action'] == "Show on Map" and condition == True:
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0
        
        os.system("cd templates/ && rm -rf haversine_map*")
        wmap.plot_route(df, plot_type="plot", popup="table-popup", data_for_table=data)
        #wmap.plot_route(df, plot_type="scatter",
        #                popup="table-popup", color="#1E90FF", marker=True, data_for_table=data)
        wmap.draw("templates/haversine_map_{}_{}.html".format(source, dest))

        return render_template('haversine_map_{}_{}.html'.format(source,dest))
    else:
        return render_template('haversine.html', result="Invalid LatLng", source=source, dest=dest)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(sys.argv[1]), threaded=True)


