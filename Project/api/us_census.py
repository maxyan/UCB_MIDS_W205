import pandas as pd
import requests
import us
import sys

sys.path.append('/home/myan/repos/') # TODO: change this
from UCB_MIDS_W205.Project.api_data_handler import ApiDataHandler
from UCB_MIDS_W205.Project.dynamodb_handler import DynamoDb

CENSUS_API_KEY = 'Your census API Key'


class Census:
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key else CENSUS_API_KEY
        self.response = requests.get('http://api.census.gov/data/2013/acs3?get=NAME,B01001_001E&for=county:*')

    def _county_population_json(self):
        county_name = []
        population = []
        name_abbr = us.states.mapping('name', 'abbr')
        for entry in self.response.json()[1:]:  # myan: skip the header
            try:
                county, state = str(entry[0]).replace(' County', '').replace(', ', ',').split(',')
            except:
                continue

            county_name.append(county + ', ' + name_abbr[state])
            population.append(int(entry[1]))

        result = pd.DataFrame()
        result['county'] = county_name
        result['population'] = population
        result = result.set_index('county')
        return result.to_json()

    def process(self):
        dynamodb = DynamoDb(**dict(endpoint_url="http://localhost:8000",
                                   region_name='us-east',
                                   aws_access_key_id='AKIAIG7AXLCUG7VMZFDQ',
                                   aws_secret_access_key='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'))
        dynamodb.initialize_table('County',
                                  hash_key='county',
                                  read_capacity=1000,
                                  write_capacity=1000)
        data_handler = ApiDataHandler()
        data_handler.push(dynamodb=dynamodb, list_data=[dict(data=self._county_population_json(), attribute='population')])
