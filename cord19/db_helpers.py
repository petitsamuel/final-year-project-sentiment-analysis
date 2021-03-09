import sqlite3
from datetime import datetime, date
import traceback
import sys

connection = sqlite3.connect("sqlite/metadata.db")
cursor = connection.cursor()

def init_db():
    script = load_sql_script('sql/create_table.sql')
    execute_sql(script)
    print('DB initiated')

def load_sql_script(file_name):
    with open(file_name) as script:
        sql_as_string = script.read()
        if sql_as_string:
            return sql_as_string
    return None

def execute_sql(script):
    try:
        cursor.executescript(script)
        connection.commit()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

def close_db():
    connection.close()
    print('DB closed')
