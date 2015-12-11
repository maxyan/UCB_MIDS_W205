import requests
from xml.etree import ElementTree

GREAT_SCHOOL_API_KEY = "Your Key"


class GreatSchools:
    """
    This objects connects to the GreatSchools.org API and retrieves information about schools and GS ratings.
    See more information on: http://www.greatschools.org/api/docs/main.page
    """

    def __init__(self, key=None):
        self.api_key = key

    def set_api_key(self, key=None):
        self.api_key = key

    def run(self, **kwargs):
        return self._nearby_schools(**kwargs)

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
            results = gs.nearby_schools(state='TX', zip_code=75228, limit=2)
            # [{'gsId': '1769', 'gsRating': '3', 'name': 'Bryan Adams High School'}, {'gsId': '7566', 'name': 'White Rock Montessori School'}]
        """
        self._check_key()
        url = "http://api.greatschools.org/schools/nearby?key={key}&state={state}&radius={radius}&zip={zip_code}&limit={limit}".format(
            key=self.api_key,
            state=state,
            zip_code=zip_code,
            radius=radius,
            limit=limit)

        results = self._run(url, 'school', [(int(), 'gsId'), (None, 'name'), (float(), 'gsRating')])
        return results

    def _run(self, url, key_string="school", result_fields=None):
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
            curr_result = dict()
            try:
                for (func, field) in result_fields:
                    if func:
                        curr_result[field] = func(school.find(field).text)
                    else:
                        curr_result[field] = school.find(field).text
            except:
                pass
            if curr_result:
                results.append(curr_result)
        return results

    def _check_key(self):
        if self.api_key is None:
            raise ValueError("Use .set_api_key() method to set Great School API Keys first.")
