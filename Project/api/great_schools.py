from xml.etree import ElementTree

import requests

from UCB_MIDS_W205.Project.postgresql_handler import Postgresql

GREAT_SCHOOL_API_KEY = "Your Key"


class GreatSchools:
    """
    This object connects to the GreatSchools.org API and retrieves information about schools and GS ratings.
    See more information on: http://www.greatschools.org/api/docs/main.page
    """

    def __init__(self, key=None):
        self.api_key = key
        self.postgres = Postgresql(user_name='postgres',
                                   password='postgres',
                                   host='localhost',
                                   port='5432',
                                   db='TestProject')
        # TODO: find a better and more generic way to parse the schema?
        self.schema = '(gsid INT PRIMARY KEY NOT NULL, zip_code INT NOT NULL, state TEXT NOT NULL, name TEXT NOT NULL, gsrating FLOAT)'
        self.fields = {'gsid': 'INT', 'zip_code': 'INT', 'state': 'TEXT', 'name': 'TEXT', 'gsrating': 'FLOAT'}
        self.primary_key = 'gsid'
        self.not_null_fields = ['gsid', 'zip_code', 'state', 'name']
        self.table = 'TestGreatSchools'

    def set_api_key(self, key=None):
        self.api_key = key

    def run(self, db_result=None, **kwargs):
        # myan: seems python has a strange way of handling memory pointers when deleting elements from lists in a loop
        # therefore create a separate list tmp_results to hold all the results from API calls first and decide what to
        # include.
        tmp_results = self._nearby_schools(**kwargs)
        results = []
        for entry in tmp_results:
            if len(db_result) < 1 or entry['gsid'] not in db_result['gsid'].values:
                results.append(entry)
        self._push(results)
        return results

    def _push(self, data, batch_size=500):
        self.postgres.initialize_table(self.table, self.schema)
        fields_list = list(self.fields.keys())
        fields_to_push = self.postgres.construct_db_field_string(fields_list)
        start_idx = 0
        while start_idx < len(data):
            end_idx = min(len(data), start_idx + batch_size)
            values_to_insert = self.postgres.parse_values_list(data, self.fields, fields_list)
            start_idx = end_idx
            self.postgres.put(self.table, fields=fields_to_push, values=values_to_insert)

    def _nearby_schools(self, state=None, zip_code=None, radius=5, limit=10):
        """
        Gets a list of schools for a specified physical location (i.e. state + zip_code), within a certain radius
        Args:
            state:
            zip_code:
            radius:
            limit:

        Returns:
            list, [dict(gsId=int, name=string, gsRating=float), dict(...), ...]

        Examples:
            gs = GreatSchools(key='Your GS Key')
            results = gs._nearby_schools(state='TX', zip_code=75228, limit=2)
            # [{'gsId': '1769', 'gsRating': '3', 'name': 'Bryan Adams High School'}, {'gsId': '7566', 'name': 'White Rock Montessori School'}]
        """
        self._check_key()
        url = "http://api.greatschools.org/schools/nearby?key={key}&state={state}&radius={radius}&zip={zip_code}&limit={limit}".format(
            key=self.api_key,
            state=state,
            zip_code=zip_code,
            radius=radius,
            limit=limit)

        results = self._run(url,
                            key_string='school',
                            result_fields=[(int, 'gsId'), (None, 'name'), (float, 'gsRating')],
                            zip_code=zip_code,
                            state=state)
        return results

    def _run(self, url, key_string="school", result_fields=None, zip_code=None, state=None):
        """
        Generic method to extract data from API calls
        Args:
            url: string, the API call url to retrieve data
            key_string: string, the parent field in the XML file
            result_fields: list, [(func, field), ...] where func can be int, float etc.

        Returns:
            list, [dict(field_1=value_1, field_2=value2, ...), dict(...)]
        """
        nearby = requests.get(url)
        results = []
        for school in ElementTree.fromstring(nearby.content).findall(key_string):
            curr_result = dict(zip_code=zip_code, state=state)
            try:
                for (func, field) in result_fields:
                    if func is None:
                        curr_result[field.lower()] = school.find(field).text
                    else:
                        curr_result[field.lower()] = func(school.find(field).text)
            except:
                pass
            if curr_result:
                results.append(curr_result)
        return results

    def _check_key(self):
        if self.api_key is None:
            raise ValueError("Use .set_api_key() method to set Great School API Keys first.")
