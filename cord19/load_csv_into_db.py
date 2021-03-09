from datetime import datetime, date
from db_helpers import init_db, close_db, insert_metadata_row, show_db_count
from collections import defaultdict
from progress.bar import Bar
import csv
import os
import json
import sqlite3

try:
    init_db()
except Exception as err:
    print("Could not initialise DB: %s" % err)
    quit()

toolbar_width = 40

print('Loading CSV file')
with open('metadata.csv') as f_in:
    reader = csv.DictReader(f_in)
    bar = Bar('Processing', max=467521)  # total csv size from the changelog
    for row in reader:
        # Save row to sqlite db
        try:
            insert_metadata_row(row)
        except Exception as err:
            print('\nCould not insert row: %s' % ' '.join(err.args))
        bar.next()

bar.finish()
print('Done loading from CSV file into DB!')
show_db_count()
close_db()
