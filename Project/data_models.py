"""
This class contains the datamodels for different tables
"""


class Datamodel:
    def __init__(self):
        pass

    def zipcode_timeseries(self):
        return 'TestZipcodeTS', \
               dict(fields_types={'id': 'TEXT', 'zip_code': 'INT', 'county': 'TEXT', 'state': 'TEXT',
                                  'year_month': 'INT', 'median_price': 'FLOAT', 'median_rent': 'FLOAT'},
                    primary_key='id',
                    not_null_fields=['id', 'zip_code', 'county', 'state', 'year_month'])

    def great_schools(self):
        return 'TestGreatSchools', \
               dict(fields_types={'gsid': 'INT', 'zip_code': 'INT', 'state': 'TEXT', 'name': 'TEXT',
                                  'gsrating': 'FLOAT'},
                    primary_key='gsid',
                    not_null_fields=['gsid', 'zip_code', 'state', 'name'])

    def population(self):
        return 'TestPopulation', \
               dict(fields_types={'place_id': 'TEXT', 'zip_code': 'INT', 'address': 'TEXT', 'county': 'TEXT',
                                  'city': 'TEXT',
                                  'state': 'TEXT', 'closest_city': 'TEXT', 'closest_city_population': 'INT'},
                    primary_key='place_id',
                    not_null_fields=['place_id', 'state'])
