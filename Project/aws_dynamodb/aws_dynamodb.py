import decimal
import inspect
import json

import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key

AWS_ACCESS_KEY = 'Your Access Key'
AWS_SECRET_ACCESS_KEY = 'Your AWS Secret Key'


def default_aws_dynamodb_config():
    return dict(endpoint_url=None, region_name=None, aws_access_key_id=None, aws_secret_access_key=None)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def _current_filter(condition):
    expected_num_arguments = len(inspect.getargspec(condition['function'])[0]) - 1
    if expected_num_arguments != 1 and expected_num_arguments != len(condition['values']):
        raise ValueError("Wrong signature for function {function}".format(function=condition['function']))
    if expected_num_arguments < 1:
        curr_filter = condition['function']()
    elif expected_num_arguments < 2:
        curr_filter = condition['function'](condition['values'])
    elif expected_num_arguments == 2:
        curr_filter = condition['function'](condition['values'][0], condition['values'][1])
    else:
        raise ValueError("Illegal filter.")
    return curr_filter


def _conditions(conditions):
    if len(conditions) == 1:
        fe = _current_filter(conditions[0])
    else:
        for i, condition in enumerate(conditions):
            # myan: -1 to remove 'self'
            curr_filter = _current_filter(condition)

            if i < 1:
                fe = curr_filter
            else:
                fe &= curr_filter
    return fe


class DynamoDb:
    def __init__(self, **kwargs):
        """
        This is the AWS DynamoDB interaction layer for our application.
        It is required to create a new object for interaction with an individual table.
        Args:
            **kwargs: dict, dict(endpoint_url= , region_name= , aws_access_key_id=, aws_secret_access_key= )

        Returns:
            An object that interacts with Amazon DynamoDB
        """
        self.aws_config = default_aws_dynamodb_config()
        self.update_dynamodb_configs(**kwargs)
        self.dynamodb = boto3.resource('dynamodb',
                                       endpoint_url=self.aws_config['endpoint_url'],
                                       region_name=self.aws_config['region_name'],
                                       aws_access_key_id=self.aws_config['aws_access_key_id'],
                                       aws_secret_access_key=self.aws_config['aws_secret_access_key'])

        self.table_name = None
        self.hash_key = None
        self.range_key = None
        self.global_secondary_index = None
        self.global_secondary_hash_key = None
        self.global_secondary_read_capacity = None
        self.global_secondary_write_capacity = None
        self.read_capacity = None
        self.write_capacity = None

    def update_dynamodb_configs(self, **kwargs):
        self.aws_config.update(**kwargs)

    def delete_table(self, table_name=None):
        table = self.dynamodb.Table(table_name)
        try:
            table.table_status
            table.delete()
        except:
            print "Table {name} does not exist".format(name=table_name)
            return

    def initialize_table(self, table_name,
                         hash_key=None,
                         range_key=None,
                         read_capacity=10,
                         write_capacity=10,
                         global_secondary_index=None,
                         global_secondary_hash_key=None,
                         global_secondary_read_capacity=10,
                         global_secondary_write_capacity=10):
        table = self.dynamodb.Table(table_name)
        self.table_name = table_name
        try:
            # myan: if the table already exist, then get the information
            table.table_status
            for key in table.key_schema:
                if key['KeyType'] == 'HASH':
                    self.hash_key = key['AttributeName']
                elif key['KeyType'] == 'RANGE':
                    self.range_key = key['AttributeName']

            self.read_capacity = table.provisioned_throughput['ReadCapacityUnits']
            self.write_capacity = table.provisioned_throughput['WriteCapacityUnits']

            if len(table.global_secondary_indexes) > 0:
                # TODO: look into if we need to support multiple global secondary indexes?
                entry = table.global_secondary_indexes[0]
                self.global_secondary_index = entry['IndexName']
                self.global_secondary_read_capacity = entry['ProvisionedThroughput']['ReadCapacityUnits']
                self.global_secondary_write_capacity = entry['ProvisionedThroughput']['WriteCapacityUnits']
                for item in entry['KeySchema']:
                    if item['KeyType'] == 'HASH':
                        self.global_secondary_hash_key = item['AttributeName']
        except:
            # myan: if table does not exist
            self.hash_key = hash_key
            self.range_key = range_key
            self.read_capacity = read_capacity
            self.write_capacity = write_capacity

            self.global_secondary_index = global_secondary_index
            self.global_secondary_hash_key = global_secondary_hash_key
            self.global_secondary_read_capacity = global_secondary_read_capacity
            self.global_secondary_write_capacity = global_secondary_write_capacity

            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': hash_key,
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': range_key,
                        'KeyType': 'RANGE'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': hash_key,
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': range_key,
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_capacity,
                    'WriteCapacityUnits': write_capacity
                },
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': global_secondary_index,
                        'KeySchema': [
                            {
                                'AttributeName': global_secondary_hash_key,
                                'KeyType': 'HASH'
                            },
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': global_secondary_read_capacity,
                            'WriteCapacityUnits': global_secondary_write_capacity
                        }
                    }
                ],
            )
            print("Table status:", table.table_status)

    def add_data(self, json_data, attribute):
        """
        Primary entry point for adding data to the DynamoDB
        Args:
            json_data: json document of the data
            attribute: attribute to put the data to

        Returns:
            NULL
        """
        entries = json.loads(json_data, parse_float=decimal.Decimal)
        table = self.dynamodb.Table(self.table_name)
        for month in entries.keys():
            for state in entries[month].keys():
                range_key = int(month.replace('-', ''))
                try:
                    table.get_item(
                        Key={
                            self.hash_key: state,
                            self.range_key: range_key
                        }
                    )
                    table.update_item(
                        Key={
                            self.hash_key: state,
                            self.range_key: range_key
                        },
                        UpdateExpression="set {attr_name} = :r".format(attr_name=attribute),
                        ExpressionAttributeValues={
                            ':r': entries[month][state]
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                except:
                    table.put_item(
                        Item={
                            self.hash_key: state,
                            self.range_key: range_key,
                            attribute: entries[month][state]
                        }
                    )

    def get_data(self, conditions=None):
        """
        The method used for getting data from DynamoDB. Depending on the conditions being passed,
        it will either use table.query or table.scan.
        Args:
            conditions: list, a list of dictionary of {function: , values:}

        Returns:
            A dataframe containing the results

        Examples:
            dynamo_state.get_data(conditions=[dict(function=Key('state').eq, values='California')])

            dynamo_state.get_data(conditions=[dict(function=Key('year_month').eq, values=201510)])

            dynamo_state.get_data(conditions=[dict(function=Key('year_month').between, values=[201508, 201509])])

            dynamo_state.get_data(conditions=[dict(function=Attr('state').is_in, values=["California", "Alaska"])])

            dynamo_state.get_data(conditions=[dict(function=Attr('state').is_in, values=["California", "Alaska"]),
                                              dict(function=Attr('year_month').between, values=[201507, 201509])])

            dynamo_state.get_data(conditions=[dict(function=Key('state').eq, values="California"),
                                              dict(function=Attr('year_month').between, values=[201507, 201509])])

        """
        key_condition = None
        for condition in conditions:
            if self._has_hash_key_filter(condition['function']):
                key_condition = condition
                conditions.remove(key_condition)
                break

        if key_condition:
            results = self._query(key_condition=key_condition, filter_conditions=conditions)
        else:
            results = self._scan(conditions)
        return results

    def _has_hash_key_filter(self, function):
        return isinstance(function.im_self, Key) and \
               function.im_self.name in (self.hash_key, self.global_secondary_hash_key) and \
               function.im_func.func_name == 'eq'

    def _query(self, key_condition=None, filter_conditions=None):
        table = self.dynamodb.Table(self.table_name)

        arguments = dict(TableName=self.table_name,
                         Select='ALL_ATTRIBUTES',
                         KeyConditionExpression=_current_filter(key_condition))

        if key_condition['function'].im_self.name != self.hash_key:
            arguments.update(IndexName=self.global_secondary_index)

        if filter_conditions:
            arguments.update(FilterExpression=_conditions(filter_conditions))

        response = table.query(**arguments)
        return pd.DataFrame(response['Items'])

    def _scan(self, conditions=None):
        table = self.dynamodb.Table(self.table_name)
        filter_expression = _conditions(conditions)

        response = table.scan(
            Select='ALL_ATTRIBUTES',
            FilterExpression=filter_expression
        )

        return pd.DataFrame(response['Items'])
