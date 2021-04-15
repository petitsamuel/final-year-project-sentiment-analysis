from shared.db_loader import load_files, load_files
from shared.folders import loaded_batches_full_path, output_folder, tmp_folder, current_batch_full_path
from shared.duplicates_helpers import remove_index_files
from shared.file_extensions import is_rtf_file
import os
import glob
import zipfile


# Load the data downloaded from the LexisNexis scraper into the database.
# This script loads files from the output directory (where downloaded files are indexed).
# One by one it will unzip the files, remove index files (non articles), parse them
# then finally load them into a database.
# This script keeps track of which files were loaded previously and
# which one is currently being loaded. If killed and re-launched it will resume work where it left off.
# Note: Currently MySQL commits after every instert. This could be changed to only commit once
# per batch & would accelerate this script by a ton.

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


# Print paths but only contain the batch ID and filename.
def format_path_str(s):
    return s.replace(output_folder, '')


# Unzip file at provided path into output dir.
def unzip(path):
    print("Unzipping file %s" % (path))
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(tmp_folder)


# Remove all files from output dir.
def clean_output_dir():
    print("Cleaning Tmp folder")
    index_files = [filename for filename in os.listdir(tmp_folder)]
    for file in index_files:
        os.remove(os.path.join(tmp_folder, file))
    print("Removed %d files" % (len(index_files)))


# If a batch is currently being loaded and there are
# RTF files in the output dir. Finish loading them.
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
    # Finish an interrupted batch if required
    check_was_interrupted()
    # Get list of files to unzip
    zips = list_zip_files()
    for z in zips:
        # Only load file into DB if it was not previously loaded
        loaded_files = load_batches_txt_file()
        if z in loaded_files:
            print("File %s already loaded - skipping" % (format_path_str(z)))
            continue

        # Unzip file, clean dir and load into database
        print("Loading file %s" % (format_path_str(z)))
        unzip(z)
        remove_index_files(tmp_folder)
        write_current_batch(z)
        load_files(tmp_folder)
        # Keep track of loaded files in txt file.
        write_batch_id_to_loaded_files(z)
        clear_current_batch_id()
        clean_output_dir()
    print("Loaded all zip files!")


import_to_db()
