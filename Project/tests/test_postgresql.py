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
