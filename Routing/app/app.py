# #! /virtual_envs/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 12:12:23 2017

@author: vijayasais
"""

import os
import sys

sys.path.append("../utils")
sys.path.append("../vplot")

from flask import Flask, render_template, request, redirect, url_for
from flask_googlemaps import Map, icons
from flask_googlemaps import GoogleMaps
import pandas as pd

from geopy.geocoders import Nominatim
geolocator = Nominatim()

from geo_utils import GeoUtils
from waymap import WayMap

#from PyQt5 import QtWidgets

wmap = WayMap()
utils = GeoUtils()

# start mongo if not started
try:
    os.system("sudo service mongod restart")
except Exception:
    pass

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY"
GoogleMaps(app, key="AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY")

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
        
        scatterness = "no"
        no_of_points = 0

        if request.form.get("scatterness"):
            scatterness = "yes"
            no_of_points = request.form["points"]

        command = "python ../vplot/__main__.py \"{}\" \"{}\" \"{}\" \"{}\" \"{}\"".format(source, destination, mode, scatterness, no_of_points)
        os.system("cd templates/ && rm -rf route_map*")
        os.system(command)
        scatter = True
        if scatterness == "no":
            scatter = False
        
        if no_of_points == "":
            no_of_points = "all"
        
        route = "source->{}_destination->{}_scatterness->{}_points->{}".format(source, destination, scatter, no_of_points)
        return redirect(url_for(".show_map", result=route))

@app.route("/maps/<result>")
def show_map(result):
    try:
        return render_template("route_map:{}.html".format(result), result=result)
    except Exception:
        return "Please try to give valid Place name"


@app.route('/utilities/haversine/')
def haversine_calculator():
    return render_template('haversine_advanced.html')

@app.route('/utilities/haversine/', methods = ['POST'])
def haversine_result():

    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314

    condition=True
    source = request.form['source']
    dest = request.form['dest']
    
    try:
        try:

            source_ = source.split(",")

            source_lat = float(source_[0])
            source_long = float(source_[1])

            dest_ = dest.split(",")

            dest_lat = float(dest_[0])
            dest_long = float(dest_[1])
            result = utils.haversine_distance((source_lat, source_long), (dest_lat, dest_long))

            df = pd.DataFrame()
            df["latitude"] = [source_lat, dest_lat]
            df["longitude"] = [source_long, dest_long]
            df["type"] = ["source", "destination"]
            df["haversine distance"] = [0, result]
            data = wmap.html_handling(df, "random")

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

            result = utils.haversine_distance((source_lat, source_long), (dest_lat, dest_long))

            df = pd.DataFrame()
            df["latitude"] = [source_lat, dest_lat]
            df["longitude"] = [source_long, dest_long]
            df["type"] = ["source", "destination"]
            df["haversine distance"] = [0, result]
            data = wmap.html_handling(df, "random")
    except Exception:
        condition=False
        pass

    if request.form['action'] == 'submit':
        try:
            output = "Distance: {} km".format(round(result,3))
        except Exception:
            return render_template('haversine_advanced.html', result="Invalid LatLng", source=source, dest=dest)
        return render_template('haversine_advanced.html', result=output, source=source, dest=dest)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.green,
                'lat': source_lat,
                'lng': source_long,
                'infobox': data[0]
            },
            {
                'icon': icons.dots.red,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': data[1]
            }])
        return render_template('haversine_map.html', trdmap=trdmap)
    else:
        return render_template('haversine_advanced.html', result="Invalid LatLng", source=source, dest=dest)


@app.route('/utilities/haversine/old/')
def old_haversine_calculator():
    return render_template('haversine.html')

@app.route('/utilities/haversine/old/', methods = ['POST'])
def old_haversine_result():
    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314
    
    condition=True
    source_lat = request.form['source-lat']
    source_long = request.form['source-long']
    dest_lat = request.form['dest-lat']
    dest_long = request.form['dest-long']
    
    try:
        source_lat = float(source_lat)
        source_long = float(source_long)
        dest_lat = float(dest_lat)
        dest_long = float(dest_long)
        
        result = utils.haversine_distance((source_lat, source_long), (dest_lat, dest_long))

        df = pd.DataFrame()
        df["latitude"] = [source_lat, dest_lat]
        df["longitude"] = [source_long, dest_long]
        df["type"] = ["source", "destination"]
        df["haversine distance"] = [0, result]
        data = wmap.html_handling(df, "random")
    except Exception:
        condition=False
        pass

    if request.form['action'] == 'submit':
        try:
            output = "Distance: {} km".format(round(result,3))
        except Exception:
            return render_template('haversine.html', result="Invalid LatLng", source_lat=source_lat, source_lng=source_long,\
                       dest_lat=dest_lat, dest_lng=dest_long)
        return render_template('haversine.html', result=output, source_lat=source_lat, source_lng=source_long,\
                       dest_lat=dest_lat, dest_lng=dest_long)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.green,
                'lat': source_lat,
                'lng': source_long,
                'infobox': data[0]
            },
            {
                'icon': icons.dots.red,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': data[1]
            }])
        return render_template('haversine_map.html', trdmap=trdmap)
    else:
        return render_template('haversine.html', result="Invalid LatLng", source_lat=source_lat, source_lng=source_long,\
                       dest_lat=dest_lat, dest_lng=dest_long)

@app.route('/utilities/bearing/')
def bearing_calculator():
    return render_template('bearing_advanced.html')

@app.route('/utilities/bearing/', methods=['POST'])
def bearing_result():

    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314

    condition=True
    source = request.form['source']
    dest = request.form['dest']

    try:
        try:
            source_ = source.split(",")

            source_lat = float(source_[0])
            source_long = float(source_[1])

            dest_ = dest.split(",")
            dest_lat = float(dest_[0])
            dest_long = float(dest_[1])

            result = utils.compass((source_lat, source_long), (dest_lat, dest_long))
            out = "Bearing: {} degrees. {}\nDirection: Pointing towards {}"\
                .format(round(result["angles"]["degrees"], 3), result["reference"], result["directions"]["long"])

            df = pd.DataFrame()
            df["latitude"] = [source_lat, dest_lat]
            df["longitude"] = [source_long, dest_long]
            df["type"] = ["source", "destination"]
            df["bearing angle"] = [0, round(result["angles"]["degrees"], 3)]
            df["direction"] = ["", result["directions"]["long"]]
            data = wmap.html_handling(df, "random")

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

            result = utils.compass((source_lat, source_long), (dest_lat, dest_long))
            out = "Bearing: {} degrees. {}\nDirection: Pointing towards {}"\
                .format(round(result["angles"]["degrees"], 3), result["reference"], result["directions"]["long"])
            
            df = pd.DataFrame()
            df["latitude"] = [source_lat, dest_lat]
            df["longitude"] = [source_long, dest_long]
            df["type"] = ["source", "destination"]
            df["bearing angle"] = [0, round(result["angles"]["degrees"], 3)]
            df["direction"] = ["", result["directions"]["long"]]
            data = wmap.html_handling(df, "random")

    except Exception:
        condition=False
        pass

    if request.form['action'] == 'submit':
        try:
            output = out
        except Exception:
            return render_template('bearing_advanced.html', result="Invalid LatLng", source=source, dest=dest)
        return render_template('bearing_advanced.html', result=output, source=source, dest=dest)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0
        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.green,
                'lat': source_lat,
                'lng': source_long,
                'infobox': data[0]
            },
            {
                'icon': icons.dots.red,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': data[1]
            }])
        return render_template('bearing_map.html', trdmap=trdmap)
    
    else:
        return render_template('bearing_advanced.html', result="Invalid LatLng", source=source, dest=dest)


@app.route('/utilities/bearing/old/')
def old_bearing_calculator():
    return render_template('bearing.html')

@app.route('/utilities/bearing/old/', methods=['POST'])
def old_bearing_result():

    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314

    condition=True
    source_lat = request.form['source-lat']
    source_long = request.form['source-long']
    dest_lat = request.form['dest-lat']
    dest_long = request.form['dest-long']

    try:
        source_lat = float(source_lat)
        source_long = float(source_long)
        dest_lat = float(dest_lat)
        dest_long = float(dest_long)

        result = utils.compass((source_lat, source_long), (dest_lat, dest_long))
        out = "Bearing: {} degrees. {}\nDirection: Pointing towards {}"\
            .format(round(result["angles"]["degrees"], 3), result["reference"], result["directions"]["long"])

        df = pd.DataFrame()
        df["latitude"] = [source_lat, dest_lat]
        df["longitude"] = [source_long, dest_long]
        df["type"] = ["source", "destination"]
        df["bearing angle"] = [0, round(result["angles"]["degrees"], 3)]
        df["direction"] = ["", result["directions"]["long"]]
        data = wmap.html_handling(df, "random")
    except Exception:
        condition=False
        pass

    if request.form['action'] == 'submit':
        try:
            output = out
        except Exception:
            return render_template('bearing.html', result="Invalid LatLng",  source_lat=source_lat, source_lng=source_long,\
                       dest_lat=dest_lat, dest_lng=dest_long)
        return render_template('bearing.html', result=output, source_lat=source_lat, source_lng=source_long,\
                       dest_lat=dest_lat, dest_lng=dest_long)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        center_lat = (source_lat + dest_lat) / 2.0
        center_lng = (source_long + dest_long) / 2.0

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.green,
                'lat': source_lat,
                'lng': source_long,
                'infobox': data[0]
            },
            {
                'icon': icons.dots.red,
                'lat': dest_lat,
                'lng': dest_long,
                'infobox': data[1]
            }])
        return render_template('bearing_map.html', trdmap=trdmap)
    
    else:
        return render_template('bearing.html', result="Invalid LatLng",  source_lat=source_lat, source_lng=source_long,\
                       dest_lat=dest_lat, dest_lng=dest_long)


@app.route('/utilities/turning/')
def turning_calculator():
    return render_template('turning.html')

@app.route('/utilities/turning/', methods=['POST'])
def turning_result():

    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314

    condition=True
    source = request.form['source']
    mid1 = request.form['mid1']
    mid2 = request.form['mid2']
    dest = request.form['dest']

    try:
        try:
            source_ = source.split(",")
            source_lat = float(source_[0])
            source_long = float(source_[1])

            mid1_ = mid1.split(",")
            mid1_lat = float(mid1_[0])
            mid1_long = float(mid1_[1])

            mid2_ = mid2.split(",")
            mid2_lat = float(mid2_[0])
            mid2_long = float(mid2_[1])

            dest_ = dest.split(",")
            dest_lat = float(dest_[0])
            dest_long = float(dest_[1])

            _from_dir = utils.compass((source_lat, source_long), (mid1_lat, mid1_long))
            _to_dir = utils.compass((mid2_lat, mid2_long), (dest_lat, dest_long))

            _from_deg, _from_rad = utils.bearing_angle((source_lat, source_long), (mid1_lat, mid1_long))
            _to_deg, _to_rad = utils.bearing_angle((mid2_lat, mid2_long), (dest_lat, dest_long))

            result = utils.turning_angle((_from_deg, _from_dir['directions']['short']),(_to_deg, _to_dir['directions']['short']))

            out = "Turning angle: {} degrees.".format(round(result, 3))

            df = pd.DataFrame()
            if mid1_lat != mid2_lat or mid1_long !=  mid1_long:
                df["latitude"] = [source_lat, mid1_lat, mid2_lat, dest_lat]
                df["longitude"] = [source_long, mid1_long, mid2_long, dest_long]
                df["type"] = ["source", "mid1", "mid2", "destination"]
                df["turning angle"] = [None, None, None, round(result, 3)]
                df["bearing angle"] = [None, _from_deg, None, _to_deg]
                df["direction"] = [None,  _from_dir['directions']['short'], None,  _to_dir['directions']['short']]
            else:
                df["latitude"] = [source_lat, mid1_lat, dest_lat]
                df["longitude"] = [source_long, mid1_long, dest_long]
                df["type"] = ["source", "mid", "destination"]
                df["turning angle"] = [None, None, round(result, 3)]
                df["bearing angle"] = [None, _from_deg, _to_deg]
                df["direction"] = [None,  _from_dir['directions']['short'], _to_dir['directions']['short']]
            data = wmap.html_handling(df, "random")

        except Exception:

            try:
                check = source.split(",")
                check = "".join(check)
                float(check)
                raise Exception
            except ValueError:
                pass

            try:
                check = mid1.split(",")
                check = "".join(check)
                float(check)
                raise Exception
            except ValueError:
                pass
            
            try:
                check = mid2.split(",")
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
            mid1_result = geolocator.geocode(mid1)
            mid2_result = geolocator.geocode(mid2)
            dest_result = geolocator.geocode(dest)

            source_lat = float(source_result.latitude)
            source_long = float(source_result.longitude)

            mid1_lat = float(mid1_result.latitude)
            mid1_long = float(mid1_result.longitude)

            mid2_lat = float(mid2_result.latitude)
            mid2_long = float(mid2_result.longitude)
            
            dest_lat = float(dest_result.latitude)
            dest_long = float(dest_result.longitude)

            _from_dir = utils.compass((source_lat, source_long), (mid1_lat, mid1_long))
            _to_dir = utils.compass((mid2_lat, mid2_long), (dest_lat, dest_long))

            _from_deg, _from_rad = utils.bearing_angle((source_lat, source_long), (mid1_lat, mid1_long))
            _to_deg, _to_rad = utils.bearing_angle((mid2_lat, mid2_long), (dest_lat, dest_long))

            result = utils.turning_angle((_from_deg, _from_dir['directions']['short']),(_to_deg, _to_dir['directions']['short']))

            out = "Turning angle: {} degrees.".format(round(result, 3))
            
            df = pd.DataFrame()
            if mid1_lat != mid2_lat or mid1_long !=  mid1_long:
                df["latitude"] = [source_lat, mid1_lat, mid2_lat, dest_lat]
                df["longitude"] = [source_long, mid1_long, mid2_long, dest_long]
                df["type"] = ["source", "mid1", "mid2", "destination"]
                df["turning angle"] = [None, None, None, round(result, 3)]
                df["bearing angle"] = [None, _from_deg, None, _to_deg]
                df["direction"] = [None,  _from_dir['directions']['short'], None,  _to_dir['directions']['short']]
            else:
                df["latitude"] = [source_lat, mid1_lat, dest_lat]
                df["longitude"] = [source_long, mid1_long, dest_long]
                df["type"] = ["source", "mid", "destination"]
                df["turning angle"] = [None, None, round(result, 3)]
                df["bearing angle"] = [None, _from_deg, _to_deg]
                df["direction"] = [None,  _from_dir['directions']['short'], _to_dir['directions']['short']]   
            data = wmap.html_handling(df, "random")


    except Exception:
        condition=False
        pass

    if request.form['action'] == 'submit':
        try:
            output = out
        except Exception:
            return render_template('turning.html', result="Invalid LatLng", source=source, mid1=mid1, mid2=mid2, dest=dest)
        return render_template('turning.html', result=output, source=source, mid1=mid1, mid2=mid2, dest=dest)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        center_lat = (source_lat + mid1_lat + mid2_lat + dest_lat) / 4.0
        center_lng = (source_long + mid1_long + mid2_long + dest_long) / 4.0
        if mid1_lat != mid2_lat or mid1_long !=  mid1_long:
            marker_list = [{
                    'icon': icons.dots.green,
                    'lat': source_lat,
                    'lng': source_long,
                    'infobox': data[0]
                },  
                {
                    'icon': icons.dots.blue,
                    'lat': mid1_lat,
                    'lng': mid1_long,
                    'infobox': data[1]
                },
                {
                    'icon': icons.dots.blue,
                    'lat': mid2_lat,
                    'lng': mid2_long,
                    'infobox': data[2]
                }, 
                {
                    'icon': icons.dots.red,
                    'lat': dest_lat,
                    'lng': dest_long,
                    'infobox': data[3]
                }]
        else:
            marker_list = [{
                    'icon': icons.dots.green,
                    'lat': source_lat,
                    'lng': source_long,
                    'infobox': data[0]
                },  
                {
                    'icon': icons.dots.blue,
                    'lat': mid1_lat,
                    'lng': mid1_long,
                    'infobox': data[1]
                },
                {
                    'icon': icons.dots.red,
                    'lat': dest_lat,
                    'lng': dest_long,
                    'infobox': data[2]
                }]

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=marker_list)
        return render_template('turning_map.html', trdmap=trdmap)
    
    else:
        return render_template('turning.html', result="Invalid LatLng", source=source, mid1=mid1, mid2=mid2, dest=dest)

@app.route('/utilities/find_lat_lng/')
def geocode():
    return render_template('geocode.html')

@app.route('/utilities/find_lat_lng/', methods=['POST'])
def geocode_result():
    
    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314

    place_name = request.form['place']
    condition=True
    try:
        result = geolocator.geocode(place_name)

        df = pd.DataFrame()
        df["latitude"] = [result.latitude]
        df["longitude"] = [result.longitude]
        df["place"] = [place_name]
        data = wmap.html_handling(df, "random")
    except Exception:
        condition=False
        pass

    if request.form['action'] == 'submit':
        try:
            output = "Latitude : {} \nLongitude: {}".format(result.latitude, result.longitude)
        except Exception:
            return render_template('geocode.html', result="Invalid place name", place_name=place_name)
        return render_template('geocode.html', result=output, place_name=place_name)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        try:
            center_lat = result.latitude
            center_lng = result.longitude
        except Exception:
            return render_template('geocode.html', result="Invalid place name", place_name=place_name)

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.green,
                'lat': center_lat,
                'lng': center_lng,
                'infobox': data[0]
            }])
        return render_template('geocode_map.html', trdmap=trdmap)
    else:
        return render_template('geocode.html', result="Invalid place name", place_name=place_name)


@app.route('/utilities/find_address/')
def reverse_geocode():
    return render_template('reverse_geocode.html')

@app.route('/utilities/find_address/', methods=['POST'])
def reverse_geocode_result():

    #app_ = QtWidgets.QApplication(sys.argv)
    #screen = app_.primaryScreen()
    #rect = screen.availableGeometry()
    height = 744
    width = 1314

    lat = request.form['lat']
    lng = request.form['lng']
    condition = True
    try:
        result = geolocator.reverse("{}, {}".format(lat, lng))
        
        df = pd.DataFrame()
        df["latitude"] = [lat]
        df["longitude"] = [lng]
        df["place"] = [result.address]
        data = wmap.html_handling(df, "random")
    except Exception:
        condition = False
        pass

    if request.form['action'] == 'submit':
        try:
            if result.address:
                output = "Address: {}".format(result.address)
            else:
                output = "Sorry, Unable to find the address"
        except Exception:
            return render_template('reverse_geocode.html', result="Invalid place name", lat=lat, lng=lng)
        return render_template('reverse_geocode.html', result=output, lat=lat, lng=lng)
    
    elif request.form['action'] == "Show on Map" and condition == True:
        
        center_lat = lat
        center_lng = lng

        trdmap = Map( identifier="trdmap", varname="trdmap", 
        style="height:{}px;width:{}px;margin:0;".format(height,width), 
        zoom=6,
        lat=center_lat, 
        lng=center_lng,
        markers=[
            {
                'icon': icons.dots.green,
                'lat': center_lat,
                'lng': center_lng,
                'infobox': data[0]
            }])
        return render_template('reverse_geocode_map.html', trdmap=trdmap)
    
    else:
        return render_template('reverse_geocode.html', result="Invalid place name", lat=lat, lng=lng)

@app.route('/utilities/turn_by_turn/')
def tbt_navigation():
    return "Coming Soon!"

@app.route('/utilities/')
def utility_back():
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0",threaded=True)
