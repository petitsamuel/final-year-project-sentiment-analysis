from shared.file_extensions import ends_in_zip, is_index_file, is_rtf_file
from shared.folders import download_folder, output_folder
from shared.files import remove_index_files, remove_duplicates
from shared.db_loader import load_files
import os
import zipfile
import re


def unzip_all():
    print("Grabbing Zip Files")
    zip_files = [filename for filename in os.listdir(
        download_folder) if ends_in_zip(filename)]

    count = 1
    total = len(zip_files)
    for file in zip_files:
        print("Extracting file %d out of %d" % (count, total))
        count += 1
        with zipfile.ZipFile(os.path.join(download_folder, file), "r") as zip_ref:
            zip_ref.extractall(output_folder)
    print("Finished!")


unzip_all()
remove_index_files()
remove_duplicates()
load_files()
