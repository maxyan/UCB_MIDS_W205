

class ApiDataHandler:
    def __init__(self):
        pass

    def process(self):
        pass

    def push(self, mission_control=None, dynamodb=None, list_data=None):
        if dynamodb:
            self._push_to_dynamo(dynamodb, list_data=list_data)

        if mission_control:
            self._push_to_mission_control(mission_control, list_data=list_data)

    def _push_to_mission_control(self, mission_control, list_data=None):
        pass

    def _push_to_dynamo(self, dynamodb, list_data=None):
        """
        Push data to dynamo db
        Args:
            dynamodb: obj, a dynamodb_handler object
            list_data: list, [dict(data=..., attribute=...)]

        Returns:
            NULL
        """
        for item in list_data:
            dynamodb.add_data(**item)
