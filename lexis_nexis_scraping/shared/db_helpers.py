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


def fetch_script_from_db(script_name):
    script = load_sql_script(os.path.join('sql/', script_name))
    if not script:
        print("Script %s not found" % (script_name))
        return None
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception(
            {'error': 'MySQL error when running script: %s' % (err), 'script': script_name})


def load_by_title(title):
    script = load_sql_script('sql/find_by_title.sql')
    try:
        cursor.execute(script, [(title)])
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err), 'title': title})


def remove_by_ids(ids):
    print("Loading all ids...")
    print(ids)
    script = load_sql_script('sql/remove_by_id_in.sql')
    try:
        for i in ids:
            cursor.execute(script, (i,))
        connection.commit()
        print("record(s) deleted")
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})


def load_titles_group_month():
    print("Loading all titles...")
    script = load_sql_script('sql/all_titles_group_month.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})

def articles_by_month(month, year, limit=4000):
    script = load_sql_script("sql/articles_where_month_year.sql")
    try:
        cursor.execute(script, (month, year, limit))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err), 'title': title})

def titles_by_month(month, year, limit=4000):
    script = load_sql_script("sql/titles_where_month_year.sql")
    try:
        cursor.execute(script, (month, year, limit))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err), 'title': title})  

def load_titles_group_week():
    print("Loading all titles grouped by week...")
    script = load_sql_script('sql/all_titles_group_week.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})


def load_articles_group_week():
    print("Loading all articles grouped by week...")
    script = load_sql_script('sql/all_articles_group_week.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})


def load_word_counts_weekly():
    print("Loading all articles word counts by week...")
    script = load_sql_script('sql/weekly_word_counts.sql')
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


def load_duplicates():
    print("Loading all duplicate titles...")
    script = load_sql_script('sql/select_duplicate_titles.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})


def load_sources():
    print("Loading all sources...")
    script = load_sql_script('sql/all_sources.sql')
    try:
        cursor.execute(script)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception({'error': 'MySQL error: %s' % (err)})


def load_sources_count():
    print("Loading count of all sources...")
    script = load_sql_script('sql/count_sources.sql')
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
