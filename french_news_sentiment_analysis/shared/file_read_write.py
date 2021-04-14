import json
from .folders import data_folder, db_offset_file_full_path


def write_offset_to_file(value):
    print("\nWriting new offset - %d - to offset file" % (value))
    f = open(db_offset_file_full_path, "w")
    f.write("%d" % (value))
    f.close()


def read_offset_from_file():
    f = open(db_offset_file_full_path, "r")
    value = int(f.read())
    f.close()
    return value


def write_to_file(value, file):
    print("\nWriting to file - %s" % (file))
    f = open(data_folder + file, "w")
    f.write(json.dumps(value))
    print("Done!")
    f.close()

def write_raw_to_file(value, file):
    print("\nWriting raw date to file - %s" % (file))
    f = open(data_folder + file, "w")
    f.write(value)
    print("Done!")
    f.close()

def read_file(file, encoding='ISO-8859-1'):
    print("\nReading file - %s" % (file))
    try:
        f = open(data_folder + file, "r", encoding=encoding)
        content = f.read()
        f.close()
        return content
    except Exception as e:
        print(e)
        print("Error: could not load file %s%s" % (data_folder, file))
        return None
