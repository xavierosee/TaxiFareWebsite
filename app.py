import streamlit as st
from datetime import datetime, date
import requests
import params


st.sidebar.markdown('# TaxiFare in NY 🗽')

pickup_date = st.sidebar.date_input(
    "When do you want to take a taxi?")

pickup_time = st.sidebar.time_input("When exactly?")

pickup = st.sidebar.text_input("Departure", 'Empire State Building')
dropoff = st.sidebar.text_input("Arrival", 'JFK Airport')

passenger_count = st.sidebar.number_input(
    "Number of passengers", min_value=1, max_value=15, step=1)


if st.sidebar.button('Get Fare'):
    pickup_datetime = f"{pickup_date} {pickup_time} UTC"

    pickup_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{pickup}.json?'
    dropoff_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{dropoff}.json?'
    mbparams = {'access_token': params.mbtoken,
                'bbox': '-74.109308,40.560583,-73.618356,40.953794',
                'limit': 2}
    pickup_latitude, pickup_longitude = requests.get(
        pickup_url, params=mbparams).json()['features'][0]['center']
    dropoff_latitude, dropoff_longitude = requests.get(
        dropoff_url, params=mbparams).json()['features'][0]['center']

    params = {
        'key': datetime.now(),
        'pickup_datetime': pickup_datetime,
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }
    url = 'https://lewagon-xavierosee-taxifareapi-tgiciww5za-ew.a.run.app/predict_fare'
    res = requests.get(url, params=params).json()
    pred = round(res['prediction'], 2)
    st.write(
        f"You're gonna pay {pred}$ 💸. Take an UBER")
