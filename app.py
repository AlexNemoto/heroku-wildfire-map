from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import pandas as pd
import numpy as np
import pickle

# Instansiate Flask
app = Flask(__name__)

# Googlemap API key
# Fill '' with your api key
# api_key = ''
api_key = os.environ['SECRET_API_KEY']
GoogleMaps(app, key=api_key)


##### Prediction
def predict(data):
    model = load_model()
    vectorizer = load_vectorizer()

    vectorized_data = vectorizer.transform(data)

    predictions_proba = np.array(model.predict_proba(vectorized_data))[:, 1]
    predictions_proba = [str(int(round(i * 100))) for i in predictions_proba]

    return predictions_proba

def load_model():
    with open('static/best_model.pickle', 'rb') as f:
        model = pickle.load(f)

    return model

def load_vectorizer():
    with open('static/vectorizer.pickle', 'rb') as f:
        vectorizer = pickle.load(f)

    return vectorizer



##### Routing
@app.route('/')
def index():
    mapping_df = pd.read_csv('static/mapping_for_app.csv')
    dates = mapping_df['time'].unique()
    dates.sort()
    return render_template('index.html', dates=dates)


@app.route("/map", methods=['POST'])
def mapview():
    # Check the api key
    # If there's no api key, it renders a page without the map
    if len(api_key) == 0:
        return render_template('without_map.html')

    # Get post data
    # form is a date here
    form = request.form
    picked_date = form['date']
    
    if request.method == 'POST':

        mapping_df = pd.read_csv('static/mapping_for_app.csv')
        mapping_df = mapping_df[mapping_df['time'] == picked_date]

        # Prediction
        fire_proba = predict(mapping_df['text'])

        mapping_df['fire_proba'] = fire_proba

        # Make marker positions
        markers = []
        for _, row in mapping_df.iterrows():
            marker_dict = {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': row.latitude,
                'lng': row.longitude,
                'infobox': f'The chance of wildfires: {row.fire_proba} %'
            }

            markers.append(marker_dict)

        # creating a map in the view
        mymap = Map(
            identifier="fire-map",
            lat=36.5302909,
            lng=-120.0886181,
            markers=markers,
            style="height:500px;width:500px;margin:0;",
            zoom=6,
        )

        return render_template('map.html', mymap=mymap, date=picked_date)

    return render_template('index.html', dates=dates)

# This code is a code for running on jupyter notebook
# app.run()

if __name__ == "__main__":
    app.run(debug=True)