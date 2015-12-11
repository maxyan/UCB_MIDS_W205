import pandas as pd

def _request_api_data(request):
    api_configs = request['api_configs']
    api = api_configs['api'](api_configs['api_key'])
    curr_result = api.run(**api_configs['api_args'])
    return curr_result, len(curr_result) > 0


class MissionControl:
    def __init__(self):
        pass

    def request_data(self, user_requests=None):
        """
        Handles requesting data from either the db or the api
        Args:
            user_requests: [{db_configs:db_configs, api_configs:api_configs}, ...]
                db_configs - dict(postgres=Postgresql, query=string)
                api_configs - dict(api, api_key, **conditions)

        Returns:
        Examples:
            The scripts below initializes a mission control to load time series and school infomration on a zipcode level.

            schools_pg = Postgresql(user_name='postgres', password='postgres', host='localhost', port='5432', db='TestProject')
            schools_pg.initialize_table('TestZipcode',
                                        '(id TEXT PRIMARY KEY NOT NULL, zip_code INT NOT NULL, state TEXT NOT NULL, gs_rating INT)')

            zipcode_ts_pg = Postgresql(user_name='postgres', password='postgres', host='localhost', port='5432', db='TestProject')
            zipcode_ts_pg.initialize_table('TestZipcodeTs',
                                           '(id TEXT PRIMARY KEY NOT NULL, zip_code INT NOT NULL, county TEXT NOT NULL, state TEXT NOT NULL, year_month INT NOT NULL, median_price FLOAT, median_rent FLOAT)')

            data = mission_control.request_data(user_requests=[dict(db_configs=dict(postgres=zipcode_ts_pg, query="select * from TestZipcodeTs where state = 'TX';"),
                                                                    api_configs=None
                                                                    ),
                                                               dict(db_configs=dict(postgres=schools_pg, query="select * from TestZipcode where state = 'TX';"),
                                                                    api_configs=dict(api=GreatSchools,
                                                                                     api_key='GREAT_SCHOOL_API_KEY',
                                                                                     api_args=dict(state='TX', zip_code=75228, limit=2)
                                                                                    )
                                                                    )
                                                               ]
                                                )
        """
        data = []
        for request in user_requests:
            db_configs = request['db_configs']
            try:
                # TODO: ideally, what the API should do is to load data from db, and also from api, and update db using
                # the new infomration obtained by the API
                curr_result = db_configs['postgres'].get(query=db_configs['query'])
                if len(curr_result) < 1:
                    curr_result = _request_api_data(request)
            except:
                if request['api_configs']:
                    curr_result = _request_api_data(request)
                else:
                    curr_result = None

            data.append(pd.DataFrame(curr_result)) # myan: convert everything into pandas DataFrame
        return data

    def dispatch(self):
        pass
