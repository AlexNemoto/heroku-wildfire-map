from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os

# Instansiate Flask
app = Flask(__name__)

# Googlemap API key
# Fill '' with your api key
api_key = os.environ['SECRET_API_KEY']
GoogleMaps(app, key=api_key)

@app.route('/')
def index():
    dates = [1, 2, 3]
    return render_template('index.html', dates=dates)


@app.route("/map", methods=['POST'])
def mapview():
    # Check the api key
    # If there's no api key, it renders a page without the map
    if len(api_key) == 0:
        return render_template('without_map.html')

    form = request.form
    if request.method == 'POST':
        # creating a map in the view
        mymap = Map(
            identifier="view-side",
            lat=-25.3636,
            lng=134.2117,
            markers=[
                {
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    'lat': -25.3636,
                    'lng': 134.2117,
                    'infobox': "<b>Hello World</b>"
                }
            ],
            style="height:500px;width:500px;margin:0;",
            region='AUS',
            zoom=3,
        )
        '''sndmap = Map(
            identifier="sndmap",
            lat=37.4419,
            lng=-122.1419,
            markers=[
              {
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                 'lat': 37.4419,
                 'lng': -122.1419,
                 'infobox': "<b>Hello World</b>"
              },
              {
                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 37.4300,
                 'lng': -122.1400,
                 'infobox': "<b>Hello World from other place</b>"
              }
            ]
        )'''

        return render_template('map.html', mymap=mymap)

    return render_template('index.html', dates=dates)

# This code is a code for running on jupyter notebook
# app.run()

if __name__ == "__main__":
    app.run(debug=True)