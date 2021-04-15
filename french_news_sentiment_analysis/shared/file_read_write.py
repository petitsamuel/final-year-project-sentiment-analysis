from .folders import data_folder, db_offset_file_full_path
import json
import csv
import os


def write_dict_array_to_csv(dict_data, csv_file):
    print("\nWriting CSV file - %s" % (csv_file))
    f = open(os.path.join(data_folder, csv_file), "w")
    writer = csv.writer(f)
    # Write CSV Header
    writer.writerow(dict_data[0].keys())
    # Write CSV Content
    for d in dict_data:
        writer.writerow(d.values())
    f.close()


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
