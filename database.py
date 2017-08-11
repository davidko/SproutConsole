#!/usr/bin/env python3

import json
import mysql.connector as sql
import os

class Database() :
    DB_NAME = "sproutlocker"
    def __init__(self):
        # See if the config file exists
        try:
            config_path = os.path.join(
                os.environ['HOME'],
                '.local',
                'etc',
                'sproutlocker_database.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
                print(config)
                self.con = sql.connect(**config)
        except Exception as e:
            raise

        self.cursor = self.con.cursor()

        try:
            self.con.database = self.DB_NAME
        except sql.Error as err:
            if err.errno == sql.errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                cnx.database = self.DB_NAME
            else:
                print(err)
                exit(1)

    def log(self, log_type, float_data=None, text_data=None):
        # Get the log_type ID
        self.cursor.execute('SELECT id FROM log_types WHERE name="{}";'.format(log_type))
        rows = self.cursor.fetchall()
        assert(len(rows) > 0)
        print(rows[0][0])
        log_type_id = rows[0][0]
        query = 'INSERT INTO log_entries( log_type '
        values = 'VALUES ( {}'.format(log_type_id)
        if float_data:
            query += ', data'
            values += ', {} '.format(float_data)
        if text_data:
            query += ', text'
            text_data = text_data.replace('\\', '\\\\')
            text_data = text_data.replace('"', '\\"')
            values += ', "{}"'.format(text_data)

        query += ') '
        values += ')'
        query += values
        print(query)
        self.cursor.execute(query)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.con.commit()
        self.con.close()


if __name__ == '__main__':
    with Database() as db:
        db.log('text', text_data="Hello. I am \"test\"")
        db.log('Ph', float_data=5.5)
        db.log('EC', float_data=1000)


