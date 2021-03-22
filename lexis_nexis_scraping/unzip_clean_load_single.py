from shared.folders import download_folder, output_folder
from shared.variable_loader import read_offset_from_file, write_offset_to_file
from shared.files import remove_index_files, remove_duplicates
from pathlib import Path
from shared.db_loader import load_files
import os
import zipfile


def clean_output_dir():
    print("\nRemoving files from output folder")
    index_files = [filename for filename in os.listdir(output_folder)]
    for file in index_files:
        os.remove(os.path.join(output_folder, file))
    print("Removed %d files" % (len(index_files)))


def unzip(path):
    print("Unzipping file %s" % (path))
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(output_folder)
    print("Done!")


def get_files_in_creation_order():
    sorted_files = sorted(Path(download_folder).iterdir(),
                          key=os.path.getmtime)
    return [f for f in sorted_files if f.name.lower().endswith('.zip')]


def script():
    paths = get_files_in_creation_order()
    offset = read_offset_from_file()

    if offset >= len(paths):
        print("No more files to load! Offset: %d - file len: %d")
        exit()
    print("File offset set to %d" % (offset))
    clean_output_dir()
    unzip(paths[offset])
    remove_index_files()
    remove_duplicates()
    load_files()
    write_offset_to_file(offset + 1)


while True:
    script()
