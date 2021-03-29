from shared.db_loader import load_files, load_files
from shared.folders import loaded_batches_full_path, output_folder, tmp_folder, current_batch_full_path
from shared.files import remove_index_files
from pathlib import Path
from shared.file_extensions import is_rtf_file
import os
import glob
import zipfile


def load_batches_txt_file():
    f = open(loaded_batches_full_path, "r")
    value = f.read()
    f.close()
    return value


def write_batch_id_to_loaded_files(batch_id):
    print("Writting batch %s to list of loaded batches" % (batch_id))
    with open(loaded_batches_full_path, "a") as batches_file:
        batches_file.write("%s\n" % (batch_id))


def write_current_batch(batch_id):
    print("Writing current batch to file")
    with open(current_batch_full_path, "w") as batch_file:
        batch_file.write("%s" % (batch_id))


def read_current_batch():
    f = open(current_batch_full_path, "r")
    value = f.read()
    f.close()
    return value


def clear_current_batch_id():
    print("Clearing current batch id from file")
    with open(current_batch_full_path, "w") as batch_file:
        batch_file.write("")


def list_zip_files():
    return glob.glob(os.path.join(output_folder, '*/*.zip'))


def format_path_str(s):
    return s.replace(output_folder, '')


def unzip(path):
    print("Unzipping file %s" % (path))
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(tmp_folder)


def clean_output_dir():
    print("Cleaning Tmp folder")
    index_files = [filename for filename in os.listdir(tmp_folder)]
    for file in index_files:
        os.remove(os.path.join(tmp_folder, file))
    print("Removed %d files" % (len(index_files)))


def check_was_interrupted():
    print("Checking if a batch was interrupted")
    loaded_files = load_batches_txt_file()
    current_batch = read_current_batch()
    tmp_dir_files = [
        filename for filename in os.listdir(tmp_folder)
        if is_rtf_file(filename)
    ]
    if current_batch and current_batch not in loaded_files and len(
            tmp_dir_files) > 0:
        # Finish loading interrupted batch
        print("Finishing loading interrupted batch %s" %
              (format_path_str(current_batch)))
        load_files(tmp_folder)
        write_batch_id_to_loaded_files(current_batch)

    clear_current_batch_id()
    clean_output_dir()


def import_to_db():
    check_was_interrupted()
    zips = list_zip_files()
    for z in zips:
        loaded_files = load_batches_txt_file()
        if z in loaded_files:
            print("File %s already loaded - skipping" % (format_path_str(z)))
            continue

        print("Loading file %s" % (format_path_str(z)))
        unzip(z)
        remove_index_files(tmp_folder)
        write_current_batch(z)
        load_files(tmp_folder)
        write_batch_id_to_loaded_files(z)
        clear_current_batch_id()
        clean_output_dir()
    print("Loaded all zip files!")


import_to_db()
