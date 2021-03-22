from .folders import output_folder
from .file_extensions import is_index_file, is_rtf_file
from difflib import SequenceMatcher, get_close_matches
from striprtf.striprtf import rtf_to_text
from operator import itemgetter
import os
import re


def remove_index_files():
    print("\nRemoving index files (non articles)")
    index_files = [filename for filename in os.listdir(
        output_folder) if is_index_file(filename)]
    for file in index_files:
        os.remove(os.path.join(output_folder, file))

    print("Removed %d index files" % (len(index_files)))
    print("Finished!")


def compute_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check_file_contents(a, b):
    file_a = open(os.path.join(output_folder, a), "r")
    file_b = open(os.path.join(output_folder, b), "r")
    return compute_similarity(rtf_to_text(file_a.read()), rtf_to_text(file_b.read()))


def to_file_dict(filename):
    return {
        'filename': filename,  # Keep for potentially removing
        # Use regex to remove (<any_text>) from file names
        'cleaned_name': re.sub(r'\(\S+\)', '', filename).lower()
    }


def remove_duplicates():
    print("Listing all RTF files in output dir...")
    files = [to_file_dict(filename) for filename in os.listdir(
        output_folder) if is_rtf_file(filename)]
    # sort files by cleaned name order
    original_len = len(files)
    sorted_files = sorted(files, key=itemgetter('cleaned_name'))
    files.clear()

    for i in range(len(sorted_files) - 1):
        for j in range(i + 1, len(sorted_files)):
            title_similarity = compute_similarity(
                sorted_files[i]['cleaned_name'], sorted_files[j]['cleaned_name'])
            if title_similarity >= 0.8:
                content_match = check_file_contents(
                    sorted_files[i]['filename'], sorted_files[j]['filename'])
                if content_match >= 0.8:
                    os.remove(os.path.join(output_folder,
                              sorted_files[i]['filename']))
                    print("Removed %s - title matching %.2f - content matching %.2f" %
                          (sorted_files[i]['filename'], title_similarity, content_match))
                    break
    new_len = len([to_file_dict(filename) for filename in os.listdir(
        output_folder) if is_rtf_file(filename)])
    print("\nFinished removing duplicated - total amount of files: %d, number of removed files: %d" %
          (new_len, (original_len - new_len)))
