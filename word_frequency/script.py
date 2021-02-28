import re
import glob

# Print in descending order frequencies of word occurences 
def print_frequencies(frequencies, total_count):
    for w in sorted(frequencies, key=frequencies.get, reverse=True):
        freq = float(frequencies[w]) / float(total_count)
        print(w, "%.12f " % (freq))


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

    # Make keep number of occurences for each word
    frequencies = {}
    for w in words:
        if w in frequencies:
            frequencies[w] += 1
        else:
            frequencies[w] = 1
    all_frequencies.append(frequencies)
    words_counts.append(len(words))

# Go through all sets of frequencies
relative_freqs = {}
for frequencies in all_frequencies:
    # go through each word for current counts
    # & update the master count (sum of all texts)
    for key in frequencies:
        if key in relative_freqs:
            relative_freqs[key] += frequencies[key]
        else:
            relative_freqs[key] = frequencies[key]

# Print word frequencies for all texts
for i in range(len(all_frequencies)):
    print('Printing word frequencies for file -- ' + files[i])
    print_frequencies(all_frequencies[i], words_counts[i])

# Relative frequencies
print('Printing relative frequency for all texts')
total_word_count = sum(words_counts)
print_frequencies(relative_freqs, total_word_count)

