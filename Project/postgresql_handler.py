import pandas as pd
import psycopg2


def _construct_db_field_string(fields, add_quote=False):
    if isinstance(fields, list):
        fields_string = '('
        for entry in fields:
            if add_quote:
                fields_string += ("'" + entry + "'" + ',')
            else:
                fields_string += (entry + ',')
        fields_string = fields_string[:-1] + ')'
    elif isinstance(fields, str):
        fields_string = fields
    else:
        raise TypeError('Unsupported type for input arguyment "fields".')
    return fields_string


class Postgresql:
    def __init__(self, user_name=None, password=None, host=None, port=None, db=None):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(database=self.db,
                                         user=self.user_name,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port)
        except:
            raise ValueError('Invalid Postgresql db input.')

    def _table_exists(self, table):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name='{name}')".format(
                name=table.lower()))
            return cur.fetchone()[0]
        except:
            self.conn.rollback()
            return False

    def initialize_table(self, table, schema, recreate=False):
        self.connect()
        if not self._table_exists(table):
            self.create_table(table, schema)
            return
        if recreate:
            self.drop_table(table)
            self.create_table(table, schema)

    def put(self, table, fields=None, values=None, keys=None, key_field=None,  update=False):
        """
        Puts data into the Postgresql database
        Args:
            table: str, table name, REQUIRED for both insert and update
            fields: str or list of str, REQUIRED for both insert and update
            values: str (for insert) or list of str (for update), REQUIRED for both insert and update
            keys: list of str, for update only
            key_field: str, for update only
            update: boolean, for update only

        Returns:
        Examples:
            .put('test_zipcode', keys = ['id1','id2'], values=['(value1a, value1b)', '(value2a, value2b)'], fields=['field1', 'field2'], update=True)
            .put('test_zipcode', keys = ['id1','id2'], values=['(value1a, value1b)', '(value2a, value2b)'], fields='(field1, field2)', update=True)
            .put('test_zipcode', keys = None, values='(value1a, value1b), (value2a, value2b)', fields=['field1', 'field2'], update=False)
        """
        if update:
            self._update(table, fields, keys, values, key_field)
        else:
            self._insert(table, fields, values)

    def _update(self, table, fields, keys, values, key_field='id'):
        cur = self.conn.cursor()
        fields_string = _construct_db_field_string(fields)
        for (key, value) in zip(keys, values):
            cur.execute("UPDATE {table} SET {fields}={values} WHERE {key_field}='{key}';".format(table=table,
                                                                                                 fields=fields_string,
                                                                                                 values=value,
                                                                                                 key_field=key_field,
                                                                                                 key=key))
        self.conn.commit()

    def _insert(self, table, fields, values):
        fields_string = _construct_db_field_string(fields)
        cur = self.conn.cursor()
        cur.execute("INSERT INTO {table} {fields} VALUES {values};".format(table=table,
                                                                           fields=fields_string,
                                                                           values=values))
        self.conn.commit()

    def get(self, query):
        df = pd.read_sql(query, self.conn)
        return df

    def create_table(self, table, schema):
        """
        Creates a table given table name and schema
        Args:
            table: string, name of the table
            schema: string, schema

        Returns:
        Examples:
            .create_table('test_zipcode', '(id TEXT PRIMARY KEY NOT NULL, median_price FLOAT, median_rent FLOAT)')
        """
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE {table} {schema};'''.format(table=table, schema=schema))
        self.conn.commit()

    def drop_table(self, table):
        cur = self.conn.cursor()
        cur.execute('''TRUNCATE TABLE {name};'''.format(name=table))
        cur.execute('''DROP TABLE {name};'''.format(name=table))
        self.conn.commit()
