

class MissionControl:
    def __init__(self):
        pass

    def request_data(self, requests=None):
        """
        Handles requesting data from either the db or the api
        Args:
            requests: [{db_configs:db_configs, api_configs:api_configs}, ...]
                db_configs - dict(dynamodb=DynamoDb, conditions=list())
                api_configs - dict(api, api_key, **conditions)

        Returns:

        """
        data = []
        for request in requests:
            db_configs = request['db_configs']
            data_df = db_configs['dynamodb'].get_data(conditions=db_configs['conditions'])
            if len(data_df) < 1: # myan: make an API call if data does not exist in the db
                api_configs = requests['api_configs']
                api = api_configs['api'](api_configs['api_key'])



    def dispatch(self):
        pass