from datetime import datetime, date
import traceback
import sys
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/home/sam/dev/fyp/lexis_nexis_scraping/.env")

host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')

if host == None or user == None or password == None or database == None:
    print("MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD and MYSQL_DATABASE must be set in the .env file")
    exit(1)
try:
    connection = mysql.connector.connect(host=host,
                                         user=user,
                                         password=password,
                                         database=database)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
    exit(1)
finally:
    cursor = connection.cursor()


def load_sql_script(file_name):
    with open(file_name) as script:
        sql_as_string = script.read()
        if sql_as_string:
            print('Loaded SQL script successfully %s' % (file_name))
            return sql_as_string
    print('SQL script %s not found' % (file_name))
    return None


def init_db():
    script = load_sql_script('sql/create_table.sql')
    execute_sql(script)
    print('DB initiated')

def load_titles_group_month():
    print("Loading all titles...")
    script = load_sql_script('sql/all_titles_group_month.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})

def load_articles_group_month():
    print("Loading all titles...")
    script = load_sql_script('sql/all_articles_group_month.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})
    

def load_titles():
    print("Loading all titles...")
    script = load_sql_script('sql/all_titles.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})

def load_full_articles():
    print("Loading all articles bodies...")
    script = load_sql_script('sql/all_bodies.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})


# Keep in memory for better performance
insert_sql_script = load_sql_script('sql/insert_row.sql')


def insert_row(row):
    script = insert_sql_script
    # print('Executing SQL insert...\n%s' % (script))
    try:
        cursor.execute(
            script,
            (row['title'], row['source'],
             datetime.fromisoformat(row['date']), row['copyright'],
             row['length'], row['section'],
             row['language'], row['pubtype'],
             row['subject'], row['geographic'],
             datetime.fromisoformat(row['load_date']), row['author'],
             row['body'], row['filename']))
        connection.commit()
        # print('Command successfully executed')
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err), 'doc': row})


def execute_sql(script):
    try:
        print('Executing SQL command...\n%s' % (script))
        cursor.execute(script)
        connection.commit()
        print('Command successfully executed')
    except mysql.connector.Error as err:
        print_sql_err(err)
        raise Exception('SQLite error: %s' % (' '.join(err.args)))


def close_db():
    print('Closing DB...')
    connection.close()
    print('DB closed')


def print_sql_err(er):
    print('MySQL error: %s' % (' '.join(er.args)))
    print("Exception class is: ", er.__class__)
    print('MySQL traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))
