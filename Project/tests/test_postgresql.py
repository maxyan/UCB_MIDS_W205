import unittest

from UCB_MIDS_W205.Project.postgresql_handler import Postgresql


class TestPostgres(unittest.TestCase):
    def test_parse_list_values(self):
        pg = Postgresql()
        insert = pg.parse_values_list([{'gsId': 100, 'name': 'Max', 'zip_code': 123, 'state': 'CA', 'gsRating': 3.5},
                                       {'gsId': 101, 'name': 'Tez', 'zip_code': 123, 'state': 'CA', 'gsRating': 8.5}],
                                      {'gsId': 'INT', 'zip_code': 'INT', 'state': 'TEXT', 'name': 'TEXT', 'gsRating': 'FLOAT'},
                                      field_list=['gsId', 'name', 'gsRating'])

        assert insert == "(100, 'Max', 3.5),(101, 'Tez', 8.5)"

    def test_make_schema_string(self):
        pg = Postgresql()
        fields = {'gsid': 'INT', 'zip_code': 'INT', 'state': 'TEXT', 'name': 'TEXT', 'gsrating': 'FLOAT'}
        primary_key = 'gsid'
        not_null_fields = ['gsid', 'zip_code', 'state', 'name']
        schema_string = pg.make_schema_string(fields, primary_key=primary_key, not_null_fields=not_null_fields)
        assert schema_string == '(gsid INT PRIMARY KEY NOT NULL,zip_code INT NOT NULL,state TEXT NOT NULL,name TEXT NOT NULL,gsrating FLOAT)'
