import pandas as pd

def _request_api_data(request, db_result=None):
    api_configs = request['api_configs']
    api = api_configs['api'](api_configs['api_key'])
    curr_result = api.run(db_result, **api_configs['api_args'])
    return curr_result


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
            db_result = pd.DataFrame()
            try:
                db_result = db_configs['postgres'].get(query=db_configs['query'])
            except:
                pass

            curr_result = None
            if request['api_configs']:
                curr_result = _request_api_data(request, db_result=db_result)

            total_results = db_result.append(pd.DataFrame(curr_result))
            data.append(total_results) # myan: convert everything into pandas DataFrame
        return data

    def dispatch(self):
        pass
