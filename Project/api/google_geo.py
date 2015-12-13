import requests


class GoogleGeo:
    def __init__(self):
        self.base_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='

    def _get(self, address):
        response = requests.get(self.base_url + '{string}'.format(string=address))
        return response

    def get(self, address, fields_to_get=('place_id', 'lat', 'lng', 'county', 'state')):
        response = self._get(address)
        output = self._parse_google_geo_response(response.json(), fields_to_get=fields_to_get)
        return output

    def _parse_google_geo_response(self, response_json, fields_to_get=None):
        """
        Retrieves location information from Google Location API
        Args:
            response_json: dict, response from Google
            fields_to_get: set, (field1, field2, ...)

        Returns:
            dict, containing the required fields

        Examples:
            _parse_google_geo_response(json, ('place_id', 'lat', 'lng', 'state'))
        """
        if response_json['status'] != 'OK':
            return None, None, None, None
        results = response_json['results'][0]

        output = dict(state=None, city=None, county=None)
        if 'place_id' in fields_to_get:
            output.update(place_id=results['place_id'])

        if 'lat' in fields_to_get:
            output.update(lat=results['geometry']['location']['lat'])

        if 'lng' in fields_to_get:
            output.update(lng=results['geometry']['location']['lng'])

        for entry in results['address_components']:
            if 'state' in fields_to_get and output['state'] is None:
                if entry['types'][0] == 'administrative_area_level_1':
                    output.update(state=entry['short_name'])

            if 'city' in fields_to_get and output['city'] is None:
                if entry['types'][0] == 'locality':
                    output.update(city=entry['long_name'])

            if 'county' in fields_to_get and output['county'] is None:
                if entry['types'][0] == 'administrative_area_level_2':
                    output.update(county=entry['long_name'])

        return output
