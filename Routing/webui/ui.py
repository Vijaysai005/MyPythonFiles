from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

app = Flask(__name__, template_folder="templates")
app._static_folder = "../static/"
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")

@app.route('/utilities')
def utilities():
    return render_template('haversine_calculator.html')

@app.route('/utilities/haversine')
def haversine_calculator():
    return "hi"
@app.route('/utilities/bearing')
def bearing_calculator():
    return "hi"
@app.route('/utilities/turning')
def turning_calculator():
    return "hi"

@app.route('/utilities', methods=['POST'])
def haversine_post():
    text = request.form['text']
    process = text.upper()
    return process

@app.route('/map/')
def mapview():
    trdmap = Map( identifier="trdmap", varname="trdmap", style="height:475px;width:1300px;margin:0;", lat=37.4419, lng=-122.1419,
    markers=[
        {
            'icon': icons.dots.blue,
            'lat': 37.4300,
            'lng': -122.1400,
            'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
        }])
    return render_template('map.html',trdmap=trdmap)

@app.route("/")
def root():
    return render_template('new_layout.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)