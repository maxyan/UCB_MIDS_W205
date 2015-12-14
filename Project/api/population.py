"""
This module utilizes Google Geo API to determine the closest city for any given county / city / zipcode, and
get the population for that location.
"""

from UCB_MIDS_W205.Project.api.google_geo import GoogleGeo
from UCB_MIDS_W205.Project.data_models import Datamodel
from UCB_MIDS_W205.Project.postgresql_handler import Postgresql
from haversine import haversine
import pandas as pd
import numpy as np

# myan: the zip_code should not be more than 80km (approximately) away from a major city
# which is approximately 40 minutes drive
MAX_DISTANCE_KM = 80


class Population:
    """
    This object connects to the GreatSchools.org API and retrieves information about schools and GS ratings.
    See more information on: http://www.greatschools.org/api/docs/main.page
    """

    def __init__(self,recreate=False):
        datamodel = Datamodel()
        self.table, self.table_config = datamodel.population()
        self.postgres = Postgresql(user_name='postgres',
                                   password='postgres',
                                   host='localhost',
                                   port='5432',
                                   db='TestProject')
        self.postgres.initialize_table(self.table, recreate=False, **self.table_config)
        self.googlegeo = GoogleGeo()

        # myan: only get major cities data once per request
        self.major_cities_postgres = Postgresql(user_name='postgres',
                                                password='postgres',
                                                host='localhost',
                                                port='5432',
                                                db='TestProject')
        self.major_cities = self.major_cities_postgres.get("select * from TestMajorCities")
        self.all_states = self.major_cities['state'].values
        self.all_cities = self.major_cities['city'].values
        self.all_lats = self.major_cities['lat'].values
        self.all_lngs = self.major_cities['lng'].values
        self.all_population = self.major_cities['population'].values

    def run(self, **kwargs):
        # myan: seems python has a strange way of handling memory pointers when deleting elements from lists in a loop
        # therefore create a separate list tmp_results to hold all the results from API calls first and decide what to
        # include.
        results_df = pd.DataFrame(self._closest_city_population(self._geo_info(**kwargs)))
        existing_keys = self.postgres.get("select place_id from {table};".format(table=self.table))
        addition_results = results_df.loc[np.logical_not(results_df['place_id'].isin(existing_keys['place_id'].values))]
        addition_results.drop_duplicates(subset='place_id', inplace=True)
        if len(addition_results) > 0:
            self.postgres.put_dataframe(addition_results, self.table_config['fields_types'], table=self.table)
        return results_df

    def _geo_info(self, addresses=None, fields_to_get=('place_id', 'state', 'city', 'county', 'lat', 'lng')):
        """
        Get geo info from Google API
        Args:
            addresses: list of addresses

        Returns:
            list of dict, [{field1:value1, field2:value2, ...}, {...]]

        Examples:
            p = Population()
            results = p._geo_info(address=['Houston,TX', 'Dallas, TX'])
        """

        if fields_to_get is None:
            raise ValueError('Argument fields_to_get must not be None.')
        results = []
        for entry in addresses:
            output = self.googlegeo.get(entry, fields_to_get=fields_to_get)
            output.update(address=str(entry))
            if isinstance(entry, int):
                output.update(zip_code=entry)
            results.append(output)
        return results

    def _closest_city_population(self, tmp_results):
        for entry in tmp_results:
            is_curr_state = self.all_states == entry['state']
            same_state_cities = self.all_cities[is_curr_state]
            # myan: use a simple squared distance between two points to simply get the minimum
            euc_distance = (self.all_lats[is_curr_state] - entry['lat']) ** 2 + (self.all_lngs[is_curr_state] - entry['lng']) ** 2
            closest_idx = euc_distance.argmin()
            # myan: once we locate the closest major city, we can then calculate the actual haversine distance
            haversine_distance = haversine((self.all_lats[is_curr_state][closest_idx], self.all_lngs[is_curr_state][closest_idx]),
                                           (entry['lat'], entry['lng']))
            if haversine_distance <= MAX_DISTANCE_KM:
                entry.update(closest_city=same_state_cities[closest_idx])
                entry.update(closest_city_population=self.all_population[is_curr_state][closest_idx])
            else:
                entry.update(closest_city='NULL')
                entry.update(closest_city_population='NULL')
        return tmp_results


