from shared.db_helpers import init_db, insert_row
from datetime import datetime
from shared.folders import output_folder
from shared.file_extensions import is_rtf_file
from striprtf.striprtf import rtf_to_text
from progress.bar import Bar
import dateparser
import os
import re
import logging

logging.basicConfig(filename='logs/db_loader_log.log', level=logging.DEBUG)


def extractValue(data):
    if ':' in data:
        return data.split(':')[1].strip()
    else:
        return data.strip()


def parse_rtf_contents(text):
    docBody = False
    counter = 0
    body = ''
    document = {
        'title': None,
        'source': None,
        'date': None,
        'copyright': None,
        'length': None,
        'section': None,
        'language': 'french',
        'pubtype': 'newspaper',
        'subject': None,
        'geographic': None,
        'load_date': datetime.now().isoformat(),
        'author': None,
        'body': None
    }
    for line in text.split('\n'):
        tempLine = line.strip()
        if tempLine != '':
            counter += 1
            if counter == 1:
                document['title'] = line
                continue
            if counter == 2:
                document['source'] = line
                continue
            if counter == 3:
                try:
                    document['date'] = dateparser.parse(line).isoformat()
                except:
                    continue
                continue
            if tempLine.startswith('Copyright '):
                document['copyright'] = line
                continue
            if tempLine.startswith('Length:'):
                try:
                    # only keep number - remove non-numeric chars
                    document['length'] = int(
                        re.sub("[^0-9]", "", extractValue(line)))
                except:
                    continue
                continue
            if tempLine.startswith('Section:'):
                document['section'] = extractValue(line)
                continue
            if tempLine.startswith('Language:'):
                document['language'] = extractValue(line)
                continue
            if tempLine.startswith('Publication-Type:'):
                document['pubtype'] = extractValue(line)
                continue
            if tempLine.startswith('Subject:'):
                document['subject'] = extractValue(line)
                continue
            if tempLine.startswith('Geographic:'):
                document['geographic'] = extractValue(line)
                continue
            if tempLine.startswith('Load-Date:'):
                try:
                    document['load_date'] = dateparser.parse(line).isoformat()
                except:
                    pass
                if docBody == True:
                    docBody = False
                    document['body'] = body
                    body = ''
                continue
            if tempLine.startswith('Byline:'):
                document['byline'] = extractValue(line)
                continue
            if tempLine == 'Body':
                body = ''
                docBody = True
                continue
            if tempLine.startswith('[readmore]'):
                continue
            if tempLine == 'Classification' or tempLine == 'Graphic':
                document['body'] = body
                body = ''
                docBody = False
                continue
            if docBody:
                body += line + '\n'
                continue
            if tempLine == 'End of Document':
                break
    return document


def load_file_content(name):
    try:
        file = open(os.path.join(output_folder, name), "r")
        return rtf_to_text(file.read())
    except:
        print("File %s not found in dir %s" % (name, output_folder))
        return None


def load_files():
    print("Loading data into database...")
    files = [filename for filename in os.listdir(
        output_folder) if is_rtf_file(filename)]
    print("Found %d articles" % (len(files)))
    bar = Bar('Processing', max=len(files))  # Show progress bar
    for file in files:
        content = load_file_content(file)
        parsed_doc = parse_rtf_contents(content)
        try:
            insert_row(parsed_doc)
        except Exception as e:
            logging.error('Error inserting file %s\nError: %s' % (file, e))
        bar.next()


init_db()
load_files()
