import glob
from file_reader import read_from_file

# Print in descending order frequencies of word occurences
def print_frequencies(frequencies, total_count, should_print = False):
    out_strings = []
    for w in sorted(frequencies, key=frequencies.get, reverse=True):
        freq = float(frequencies[w]) / float(total_count)
        out_strings.append("%s - %.12f" % (w, freq))
    output = "\n".join(out_strings)
    if should_print == True:
        print(output)
    return output

def write_to_file(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()
    print("Wrote to %s" % (file_name))

# Obtain list of text files in /texts dir
files = glob.glob("texts/*.txt")

all_frequencies = []
words_counts = []

for file_name in files:
    print("Processing file %s" % (file_name))
    words = read_from_file(file_name, True) # get array of words from file (True specifies using stemmer)
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
# for i in range(len(all_frequencies)):
#     print('Printing word frequencies for file -- ' + files[i])
#     print_frequencies(all_frequencies[i], words_counts[i])

# Relative frequencies
print('Printing relative frequency for all texts')
total_word_count = sum(words_counts)
output_string = print_frequencies(relative_freqs, total_word_count)

write_to_file("outputs/relative_frequencies.txt", output_string)
