import re
import glob

# Obtain list of text files in /texts dir
files = glob.glob("texts/*.txt")

all_frequencies = []
words_counts = []

for file_name in files:
    # read current file contents
    file = open(file_name, "r")
    contents = file.read()
    # Remove all special characters using regex (& put to lowercase)
    contents = re.sub('[^A-Za-z0-9\s]+', '', contents).lower()
    # Split string into array of words (removes white spaces by default)
    words = contents.split()

    frequencies = {}
    for w in words:
        if w in frequencies:
            frequencies[w] += 1
        else:
            frequencies[w] = 1
    all_frequencies.append(frequencies)
    words_counts.append(len(words))

relative_freqs = {}
for frequencies in all_frequencies:
    for key in frequencies:
        if key in relative_freqs:
            relative_freqs[key] += frequencies[key]
        else:
            relative_freqs[key] = frequencies[key]
for w in sorted(relative_freqs, key=relative_freqs.get, reverse=False):
    print(w, relative_freqs[w])

total_word_count = sum(words_counts)
print(total_word_count)