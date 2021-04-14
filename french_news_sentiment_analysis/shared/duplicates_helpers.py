from .db_helpers import load_duplicates, load_by_title, remove_by_ids
from .file_extensions import is_index_file, is_rtf_file
from .folders import output_folder
from difflib import SequenceMatcher, get_close_matches
from striprtf.striprtf import rtf_to_text
from operator import itemgetter
import os
import re


# Returns the ratio of similarity between 2 strings
def compute_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# From 2 provided file names, return the similarity ratio of their contents.
def check_file_contents(a, b):
    file_a = open(os.path.join(output_folder, a), "r")
    file_b = open(os.path.join(output_folder, b), "r")
    return compute_similarity(rtf_to_text(file_a.read()),
                              rtf_to_text(file_b.read()))


# Remove non-articles (index) files from the output folder.
def remove_index_files(folder=output_folder):
    print("\nRemoving index files (non articles)")
    index_files = [
        filename for filename in os.listdir(folder) if is_index_file(filename)
    ]
    for file in index_files:
        os.remove(os.path.join(folder, file))

    print("Removed %d index files" % (len(index_files)))
    print("Finished!")


def to_file_dict(filename):
    return {
        'filename': filename,  # Keep for potentially removing
        # Use regex to remove (<any_text>) from file names
        'cleaned_name': re.sub(r'\(\S+\)', '', filename).lower()
    }


# Note: THIS DID NOT END UP BEING USED AS DUPLICATES WERE KEPT!!
# (more details in my disseration)
# Method to remove duplicate RTF articles from the output directory.
# Works by checking if titles match some threashold then removes an article
# if it matches another one up to some threshold.
# Runs in N^2 time complexity (worst case) - in practise it runs faster:
# n*(n-1)/2 (remains O(n^2))
def remove_duplicates():
    print("Listing all RTF files in output dir...")
    files = [
        to_file_dict(filename) for filename in os.listdir(output_folder)
        if is_rtf_file(filename)
    ]
    # sort files by cleaned name order
    original_len = len(files)
    sorted_files = sorted(files, key=itemgetter('cleaned_name'))
    files.clear()

    for i in range(len(sorted_files) - 1):
        for j in range(i + 1, len(sorted_files)):
            title_similarity = compute_similarity(
                sorted_files[i]['cleaned_name'],
                sorted_files[j]['cleaned_name'])
            if title_similarity >= 0.8:
                content_match = check_file_contents(
                    sorted_files[i]['filename'], sorted_files[j]['filename'])
                if content_match >= 0.8:
                    os.remove(
                        os.path.join(output_folder,
                                     sorted_files[i]['filename']))
                    print(
                        "Removed %s - title matching %.2f - content matching %.2f"
                        % (sorted_files[i]['filename'], title_similarity,
                           content_match))
                    break
    new_len = len([
        to_file_dict(filename) for filename in os.listdir(output_folder)
        if is_rtf_file(filename)
    ])
    print(
        "\nFinished removing duplicated - total amount of files: %d, number of removed files: %d"
        % (new_len, (original_len - new_len)))


# Note: THIS DID NOT END UP BEING USED AS DUPLICATES WERE KEPT!!
# (more details in my disseration)
# Method to remove duplicate articles from MySQL DB.
# Works by identifying articles within the MySQL DB which have the same title
# Then a similarity check is performed, if 2 articles match over 90% one of the articles
# is removed from the database
# Algorithm complexity is n^2 in the worst case but performs much better in practise
# (all_duplicates reduces in size over iterations)
def remove_db_duplicates():
    duplicates = load_duplicates()
    for _, title in duplicates:
        all_duplicates = load_by_title(title)
        if len(all_duplicates) >= 100:
            print("Skipping duplicate checking - over 100 articles have the same title")
            continue
        print("Loaded %d potential duplicates" % (len(all_duplicates)))
        to_remove = []
        while len(all_duplicates) > 1:
            i_id, i_body = all_duplicates.pop(0)
            tmp_to_remove = []
            for j_id, j_body in all_duplicates:
                if compute_similarity(i_body, j_body) >= 0.90:
                    tmp_to_remove.append(j_id)
            to_remove = to_remove + tmp_to_remove

            # Remove ids in tmp_to_remove from all_duplicates
            # these will be removed so we don't need to consider them anymore
            all_duplicates = [(x, y)
                              for x, y in all_duplicates if not x in tmp_to_remove]
        if len(to_remove):
            remove_by_ids(to_remove)
