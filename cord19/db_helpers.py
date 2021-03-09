from datetime import datetime, date
from shared.date import is_valid_date_format
import traceback
import sys
import sqlite3

connection = sqlite3.connect("sqlite/metadata.db")
cursor = connection.cursor()


def load_sql_script(file_name):
    with open(file_name) as script:
        sql_as_string = script.read()
        if sql_as_string:
            print('Loaded SQL script successfully %s' % (file_name))
            return sql_as_string
    print('SQL script %s not found' % (file_name))
    return None


# Keep in memory for better performance
insert_sql_script = load_sql_script('sql/insert_metadata.sql')


def init_db():
    print('Opening DB Connection...')
    script = load_sql_script('sql/create_table.sql')
    execute_sql(script)
    print('DB initiated')


def insert_metadata_row(row):
    date = row['publish_time']
    if not date or not is_valid_date_format(date):
        date = None

    # script = load_sql_script('sql/insert_metadata.sql')
    # Use script kept in memory on init for better performance
    script = insert_sql_script
    # print('Executing SQL insert...\n%s' % (script))
    try:
        cursor.execute(
            script,
            (row['cord_uid'], row['sha'], row['source_x'], row['title'],
             row['doi'], row['pmcid'], int(row['pubmed_id']), row['license'],
             row['abstract'], date, row['authors'], row['journal'],
             row['who_covidence_id'], row['arxiv_id'], row['pdf_json_files'],
             row['pmc_json_files'], row['url'], row['s2_id']))
        connection.commit()
        # print('Command successfully executed')
    except sqlite3.Error as err:
        print_sql_err(err)
        raise Exception('SQLite error: %s' % (' '.join(err.args)))


def show_db_count():
    cursor.execute("SELECT COUNT(*) metadata")
    rows = cursor.fetchone()
    print("Total row count in metadata DB: %s" % (rows[0]))
    return rows[0]


def execute_sql(script):
    try:
        print('Executing SQL command...\n%s' % (script))
        cursor.executescript(script)
        connection.commit()
        print('Command successfully executed')
    except sqlite3.Error as err:
        print_sql_err(err)
        raise Exception('SQLite error: %s' % (' '.join(err.args)))


def close_db():
    print('Closing DB...')
    connection.close()
    print('DB closed')


def print_sql_err(er):
    print('SQLite error: %s' % (' '.join(er.args)))
    print("Exception class is: ", er.__class__)
    print('SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))
