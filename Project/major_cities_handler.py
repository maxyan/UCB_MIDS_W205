"""
This is the static data handler. The aim of the functions here is that they only need to be called once.
"""
from time import sleep

import numpy as np
import pandas as pd
import requests

from UCB_MIDS_W205.Project.api.google_geo import GoogleGeo
from UCB_MIDS_W205.Project.postgresql_handler import Postgresql


def push_major_cities():
    all_cities = requests.get('http://api.census.gov/data/2013/acs3?get=NAME,B01001_001E&for=place:*')
    major_cities, _ = _parse_city_population(all_cities.json())
    major_cities = major_cities.loc[major_cities.population >= 100000]  # myan: major city should have more than 100000
    major_cities = _get_city_info(major_cities)

    postgres = Postgresql(user_name='postgres', password='postgres', host='localhost', port='5432', db='TestProject')
    field_types = {'place_id': 'TEXT', 'city': 'TEXT', 'state': 'TEXT', 'population': 'INT',
                   'lat': 'FLOAT', 'lng': 'FLOAT'}
    postgres.initialize_table('TestMajorCities',
                              fields_types=field_types,
                              primary_key='place_id',
                              not_null_fields=['place_id', 'city', 'state'],
                              recreate=False)
    postgres.put_dataframe(major_cities, field_types)


def _get_city_info(major_cities):
    place_ids = []
    lats = []
    lngs = []
    states = []

    # base_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='
    progress = 0.0
    google_geo = GoogleGeo()
    for i, city in enumerate(major_cities.city.values):
        sleep(0.5)
        output = dict(place_id=None, state=None, lat=None, lng=None)
        try:
            # response = requests.get(base_url + '{string}'.format(string=city))
            # output = _parse_google_geo_response(response.json())
            output = google_geo.get(city, fields_to_get=('place_id', 'lat', 'lng', 'state'))
            if float(i) / len(major_cities) - progress >= 0.1:
                print "Processed {pct}%".format(pct=str(float(i) / len(major_cities) * 100))
                progress = float(i) / len(major_cities)
        except:
            pass

        place_ids.append(output['place_id'])
        states.append(output['state'])
        lats.append(output['lat'])
        lngs.append(output['lng'])

    major_cities['place_id'] = place_ids
    major_cities['state'] = states
    major_cities['lat'] = lats
    major_cities['lng'] = lngs
    major_cities.drop_duplicates(subset='place_id', inplace=True)
    major_cities = major_cities.loc[np.logical_not(major_cities.place_id.isnull())]
    return major_cities


def _parse_city_population(data):
    city_full_name = []
    population = []
    failed = []
    for entry in data[1:]:  # myan: skip the header
        try:
            name = entry[0]
            value = int(entry[1])
            city_full_name.append(name)
            population.append(value)
        except:
            failed.append(entry)

    result = pd.DataFrame()
    result['city'] = city_full_name
    result['population'] = population
    return result, failed

