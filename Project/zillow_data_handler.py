import pdb

import pandas as pd
from UCB_MIDS_W205.Project.data_models import Datamodel
from UCB_MIDS_W205.Project.postgresql_handler import Postgresql

DEFAULT_PATH = '/home/myan/Downloads/Zillow_Data'


class ZillowDataHandler:
    def __init__(self, table=None, recreate=False):
        datamodel = Datamodel()
        if table is None:
            table, table_config = datamodel.zipcode_timeseries()
        else:
            _, table_config = datamodel.zipcode_timeseries()
        self.time_series_postgres = self._initialize_postgres((table, table_config), recreate=recreate)

    def _initialize_postgres(self, (table, config), recreate=False):
        postgres = Postgresql(user_name='postgres', password='postgres', host='localhost', port='5432',
                              db='TestProject')
        postgres.initialize_table(table, recreate=recreate, **config)
        return postgres

    def get_data_from_zillow(self):
        # TODO: complete downloading data from web part
        pass

    def _drop_columns(self, data, all_columns=('RegionID', 'City', 'Metro', 'SizeRank')):
        to_drop = []
        for column in all_columns:
            if column in data.columns:
                to_drop.append(column)
        data = data.drop(to_drop, axis=1)
        return data

    def parse_and_push(self):
        latest_year_month = self.time_series_postgres.get(
            "select max(year_month) from {table};".format(table=self.time_series_postgres.table))['max'].values[0]

        prices = self._parse('/home/myan/Downloads/Zillow_Data/Zip_Zhvi_SingleFamilyResidence.csv')
        rent = self._parse('/home/myan/Downloads/Zillow_Data/Zip_MedianRentalPrice_Sfr.csv')

        self._push_price(prices, latest_year_month)
        self._update_rent(rent, latest_year_month)

    def _parse(self, path):
        data = pd.read_csv(path)
        data['key'] = data['RegionName'].astype(str) + '_' + data['CountyName'] + '_' + data['State']
        data.columns = [entry.replace('-', '') for entry in data.columns]
        data = self._drop_columns(data)
        data.drop_duplicates(subset='key', inplace=True)
        data = data.set_index('key')
        return data

    def _push_price(self, data, latest_year_month=None):
        batch_size = 500
        start_idx = 0
        while start_idx < len(data):
            end_idx = min(start_idx + batch_size, len(data))
            print 'Processing {start} to {end}'.format(start=start_idx, end=end_idx)
            curr_data = data[start_idx:end_idx]
            curr_insert_string = self._convert_into_insert_values(curr_data, latest_year_month)
            start_idx = end_idx
            self.time_series_postgres.put(self.time_series_postgres.table,
                                          fields='(id, zip_code, county, state, year_month, median_price)',
                                          values=curr_insert_string)

    def _update_rent(self, data, latest_year_month=None):
        key_strings, value_strings = self._convert_into_update_values(data, latest_year_month)
        self.time_series_postgres.put('TestZipcodeTS',
                                      keys=key_strings,
                                      values=value_strings,
                                      fields=['median_rent'],
                                      update=True,
                                      key_field='id')

    def _convert_into_insert_values(self, data, latest_year_month=None):
        insert_string = ''
        for (k, v) in data.T.to_dict().items():
            zip_code = v['RegionName']
            county = v['CountyName']
            state = v['State']
            for key in v.keys():
                if key in ('RegionName', 'CountyName', 'State'):
                    continue
                if key.isdigit() and latest_year_month is not None and int(key) <= latest_year_month:
                    continue

                insert_string += "('" + (k + '_' + key) + "', " + str(zip_code) + ", '" + county + "', '" + state + \
                                 "'," + key + ", " + self._nan_to_null(v[key]) + "),"
        return insert_string[:-1]

    def _convert_into_update_values(self, data, latest_year_month=None):
        value_strings = []
        key_strings = []
        for (k, v) in data.T.to_dict().items():
            for key in v.keys():
                if key in ('RegionName', 'CountyName', 'State'):
                    continue
                if key.isdigit() and latest_year_month is not None and int(key) <= latest_year_month:
                    continue
                value_strings.append('(' + self._nan_to_null(v[key]) + ')')
                key_strings.append((k + '_' + key))
        return key_strings, value_strings

    def _nan_to_null(self, value):
        if str(value) == 'nan':
            return 'NULL'
        return str(value)
